import json
import os
import argparse

from github.PullRequest import PullRequest
from github.PullRequestComment import PullRequestComment
from gptmypr.logging import std_console, err_console

try:
    from git import Repo
except (Exception, ImportError):
    err_console.print(
        "Git is not accessible. Make sure git installed and added to PATH environment variable."
    )
    exit(1)


def is_comment_read(
    comment: PullRequestComment, current_user: str, read_reaction: str
) -> bool:
    return any(
        reaction.user.login == current_user and reaction.content == read_reaction
        for reaction in comment.get_reactions()
    )


def get_repository_name() -> str:
    repo = Repo(os.getcwd())
    remotes = list(repo.remotes)
    if len(remotes) == 0:
        raise Exception("Git repo does not have remotes.")
    return "/".join(remotes[0].url.replace(".git", "").split("/")[-2:])


def update_local_file(file_path: str, content: str):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def has_uncommitted_changes(file_path) -> bool:
    repo = Repo(os.getcwd())
    diffs = repo.index.diff(None)
    return any(diff.a_path == file_path for diff in diffs)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Improve the GitHub PR using OpenAI GPT"
    )
    parser.add_argument(
        "--pr",
        type=int,
        required=True,
        help="PR number (.../pull/{number} in address line)",
    )
    parser.add_argument(
        "--config", type=str, required=False, help="JSON config file path"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        required=False,
        help="Enable verbose output, displaying each step's details as they are executed",
    )
    return parser.parse_args()


def get_comments_for_files(pr: PullRequest) -> dict:
    comments_for_files = {}
    for comment in pr.get_review_comments():
        file = comment.path
        if file not in comments_for_files:
            comments_for_files[file] = []
        comments_for_files[file].append(comment)
    return comments_for_files


def get_comments_ids(comments: [PullRequestComment]) -> [int]:
    return json.dumps(list(map(lambda x: x.id, comments)))


def get_only_unprocessed_comments(
    comments: [PullRequestComment],
    current_username: str,
    reaction_to_mark_comment_as_read: str,
) -> [PullRequestComment]:
    not_processed_comments = []
    for c in comments:
        if is_comment_read(c, current_username, reaction_to_mark_comment_as_read):
            std_console.log(f"Comment {c.id} for {c.path} has already been processed")
            continue
        else:
            not_processed_comments.append(c)
    return not_processed_comments
