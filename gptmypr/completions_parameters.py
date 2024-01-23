import json

from github.PullRequestComment import PullRequestComment
from openai.types.chat import ChatCompletionToolParam

TOOLS = [
    ChatCompletionToolParam(
        type="function",
        function={
            "name": "send_back_updated_source_code",
            "parameters": {
                "type": "object",
                "properties": {
                    "updated_source_code": {
                        "type": "string",
                        "description": "updated source code after implementing edits according to comments",
                    }
                },
                "required": ["updated_source_code"],
            },
        },
    )
]

TOOL_CHOICE = {
    "type": "function",
    "function": {"name": "send_back_updated_source_code"},
}

SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are improving source code in GitHub pull request. "
    "The prompt contains comments in JSON array format and source code. "
    "You need to change source code according to comments and "
    "pass updated source code to function send_back_updated_source_code.",
}


def create_messages(file_content: str, comments: [PullRequestComment]):
    prepared_comments = list(
        map(
            lambda c: {
                "diff_hunk": c.diff_hunk,
                "comment": c.body,
            },
            comments,
        )
    )

    content = (
        f"Change the source code according to comments in pull request: {json.dumps(prepared_comments)}\n\n"
        f"The latest version of source code from pull request:\n{file_content}"
    )

    return [
        SYSTEM_MESSAGE,
        {"role": "user", "content": content},
    ]
