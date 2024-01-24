# GPTmyPR

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/167ca4e9157343d6b632bfed3e663c87)](https://app.codacy.com/gh/waclawthedev/GPTmyPR/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

GPTmyPR is a Python command-line tool that uses OpenAI's GPT to change your code according to comments in the GitHub
pull request.

## Installation

```bash
pip install gptmypr
```

## Configuration

A configuration file will be created during the first run. You'll need a GitHub token and an OpenAI API key to use
GPTmyPR.

### How to generate a GitHub Token:

*   Visit https://github.com/settings/tokens.
*   Select 'Personal access tokens', then 'Fine-grained tokens'.
*   Click 'Generate new token'.
*   Specify 'Repository access' for the desired repository.
*   Choose 'Access: Read-only' for 'Contents' and 'Access: Read and write' for 'Pull requests'.

### How to generate an OpenAI API Key:

*   Go to https://platform.openai.com/api-keys.
*   Click 'Create new secret key'.

## Author's opinion about model choice

Updated: **1/23/2024**. It is recommended to check the official page for the latest
information: https://platform.openai.com/docs/models/ and https://openai.com/pricing.

| Model              | Price          | Speed     | Quality for gptmypr | Note                                                                                      | Token limit (the higher the number, the larger the file you can process). Remember, you pay for every token used per request. |
|--------------------|----------------|-----------|---------------------|-------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| gpt-4-1106-preview | Moderate       | Medium    | Optimal             | Good choice for most tasks; also has recent knowledge base.                               | 128,000 tokens                                                                                                                |
| gpt-4              | Expensive      | Slow      | The best            | Slow, but the most intelligent.                                                           | 8,192 tokens                                                                                                                  |
| gpt-3.5-turbo-1106 | Cheap          | Fast      | Below average       | Fast, but not always accurate with results.                                               | 16,385 tokens                                                                                                                 |
| gpt-3.5-turbo      | Very cheap     | Very fast | Below average       | The cheapest and fastest way to work with small source files and process simple comments. | 4,096 tokens                                                                                                                  |

## Changing Configuration Later

Edit the configuration file usually located at `~/.gptmypr.conf.json`:

```json
{
  "openai_apikey": "YOUR_OPENAI_API_KEY",
  "github_token": "YOUR_GITHUB_TOKEN",
  "openai_model": "OPENAI_MODEL_NAME",
  "reaction_to_mark_comment_as_read": "REACTION_NAME"
}
```

To modify the configuration at any time, replace `YOUR_OPENAI_API_KEY`, `YOUR_GITHUB_TOKEN`, `OPENAI_MODEL_NAME`,
and `REACTION_NAME` with your respective OpenAI API Key, GitHub token, preferred OpenAI model name, and the reaction to
mark comments as read (+1, -1, laugh, confused, heart, hooray, rocket, or eyes).

## Usage

Execute the tool from the command line within your git repository:

```bash
gptmypr [--config CONFIG_PATH] [--verbose] [--pr PR_NUMBER]
```

### Arguments

*   `--pr`: The pull request number (mandatory). While on the PR page, look at the URL. The integer at the end is the PR
  number.
*   `--config`: The path to the configuration file (optional, default value is `~/.gptmypr.conf.json`).
*   `--verbose`: Enables verbose output (optional).

## Limitations

*   The code improvements will be performed by using only the file related to the comment. It means that GPT will not
  account for the entire project when processing the comment - only its file.
*   Only comments attached to a line of code will be processed.
*   The file size that can be processed by the model is limited by the model's context window. Also, models with a larger
  window may cost more.
*   Not every result can be accurate. Use the tool to make refactoring easier, but check everything before committing :)

## Expenses

The script will send the entire source code file, along with comments and instructions, to the OpenAI API. The response
will contain the full version of the improved source code. The larger or more files you process, the higher your bill
will be from OpenAI. The script will display the count of prompt and response tokens used during the OpenAI API calls
upon completion to help you understand the expenses. You can make estimations based on the prices listed
here: https://openai.com/pricing. Additionally, don't forget to review the usage stats
here: https://platform.openai.com/usage or/and set usage limits here: https://platform.openai.com/account/limits.

## Privacy

As previously mentioned, source code that you are planning to change using gptmypr will be sent to the OpenAI API for
processing. Ensure that the code owners allow such actions.

## License

This software and its source code are released under the MIT License and are provided "AS IS". The author is not liable 
for any outcomes, damages or expenses, including those from software bugs, third-party libraries used in the project, 
or the use of paid OpenAI APIs, among others.

## Contributing

Your pull requests are welcome. For significant changes, please open an issue first to discuss your proposed changes.

## Support

Should you encounter any issues, kindly open an issue on the project's GitHub repository.
