import json
import os

from argparse import Namespace

from git import InvalidGitRepositoryError
from github.PullRequest import PullRequest
from github.Repository import Repository
from openai import OpenAI, AuthenticationError
from github import Auth
from rich.prompt import Prompt
from gptmypr.logging import err_console, std_console
from .completions_parameters import TOOLS, TOOL_CHOICE, create_messages
from .config import Config
from .utils import (
    get_repository_name,
    update_local_file,
    get_only_unprocessed_comments,
    has_uncommitted_changes,
    parse_args,
    get_comments_for_files,
    get_comments_ids,
)
from github import (
    Github,
    BadCredentialsException,
    UnknownObjectException,
    GithubException,
)


def process_comments_for_files(
    gpt_client: OpenAI,
    config: Config,
    args: Namespace,
    repo: Repository,
    pr: PullRequest,
    current_username: str,
    comments_for_files: dict,
) -> (int, int):
    prompt_tokens_n = 0
    answer_tokens_n = 0

    for file_path, comments in comments_for_files.items():
        comments_ids = get_comments_ids(comments)
        if has_uncommitted_changes(file_path):
            allow_rewrite = Prompt.ask(
                f"PR comments {comments_ids} require changes to {file_path}, which has uncommitted changes. "
                f"The file will be REWRITTEN, and uncommitted changes in {file_path} will be LOST. Continue?",
                choices=["yes", "no"],
                default="no",
            )
            if allow_rewrite.lower() != "yes":
                std_console.print(
                    f"Comments {comments_ids} have been skipped. Proceeding to the next comment..."
                )
                continue

        not_processed_comments = get_only_unprocessed_comments(
            comments, current_username, config.reaction_to_mark_comment_as_read
        )

        if len(not_processed_comments) == 0:
            continue

        not_processed_comments_ids = get_comments_ids(not_processed_comments)

        if args.verbose:
            std_console.log(
                f"Processing the comments {not_processed_comments_ids} for {file_path}"
            )

        try:
            pr_file_content = repo.get_contents(
                file_path, ref=pr.head.sha
            ).decoded_content.decode("utf-8")
        except GithubException as e:
            raise Exception(f"Can't fetch {file_path} from GitHub: {e}.")

        gpt_messages = create_messages(pr_file_content, not_processed_comments)

        completion = gpt_client.chat.completions.create(
            model=config.openai_model,
            tools=TOOLS,
            tool_choice=TOOL_CHOICE,
            messages=gpt_messages,
        )

        if (
            len(completion.choices) == 0
            or len(completion.choices[0].message.tool_calls) == 0
        ):
            raise Exception(
                "An unexpected error occurred: Received an empty completion from the OpenAI API. Just run gptmypr again."
            )

        improved_file_content = json.loads(
            completion.choices[0].message.tool_calls[0].function.arguments
        ).get("updated_source_code")

        if improved_file_content is None or improved_file_content == "":
            raise Exception(
                "An unexpected error occurred: The generated source code is empty. Please try running the command again."
            )

        for c in not_processed_comments:
            try:
                c.create_reaction(reaction_type=config.reaction_to_mark_comment_as_read)
            except GithubException as e:
                raise Exception(
                    f"Can't mark comment {c.id} as read by reaction '{config.reaction_to_mark_comment_as_read}': {e}"
                )

        update_local_file(os.getcwd() + os.sep + file_path, improved_file_content)

        prompt_tokens_n += completion.usage.prompt_tokens
        answer_tokens_n += completion.usage.completion_tokens

    return prompt_tokens_n, answer_tokens_n


def run(args: Namespace, config: Config) -> (int, int):
    gpt_client = OpenAI(api_key=config.openai_apikey)
    github_client = Github(auth=Auth.Token(config.github_token))
    current_username = github_client.get_user().login

    repo_name = get_repository_name()

    try:
        repo = github_client.get_repo(repo_name)
    except UnknownObjectException as e:
        raise Exception(
            f"Repo {repo_name} not found on GitHub: {e}. Change github_token in config"
        )

    try:
        pr = repo.get_pull(args.pr)
    except UnknownObjectException as e:
        raise Exception(
            f"Pull request {args.pr} not found for {repo_name}: {e}. Choose correct PR number for --pr parameter."
        )

    if args.verbose:
        std_console.log(f'PR "{pr.title}" has {pr.get_comments().totalCount} comments')

    comments_for_files = get_comments_for_files(pr)
    prompt_tokens_n, answer_tokens_n = process_comments_for_files(
        gpt_client, config, args, repo, pr, current_username, comments_for_files
    )

    github_client.close()
    return prompt_tokens_n, answer_tokens_n


def main():
    args = parse_args()
    config = Config(
        path=os.path.expanduser(f"~{os.sep}.gptmypr.conf.json")
        if not args.config
        else os.path.expanduser(args.config)
    )
    try:
        prompt_tokens_n, answer_tokens_n = run(args, config)
        std_console.print(
            f"Operation completed successfully. OpenAI GPT tokens usage - Input: {prompt_tokens_n}, Output: {answer_tokens_n}."
        )
    except BadCredentialsException as e:
        err_console.print(
            f"GitHub credentials issue: {e}. Change github_token in config"
        )
    except AuthenticationError as e:
        err_console.print(
            f"OpenAI credentials issue: {e}. Change openai_apikey in config"
        )
    except InvalidGitRepositoryError as e:
        err_console.print(
            f"Git repository issue: {e}. Make sure that repo was initialized."
        )
    except Exception as e:
        err_console.print(f"{e.__class__.__name__}: {e}")


if __name__ == "__main__":
    main()
