from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gptmypr",
    version="0.1.0",
    author="waclawthedev",
    author_email="waclawthedev@gmail.com",
    url="https://github.com/waclawthedev/GPTmyPR",
    description="CLI tool that uses OpenAI's GPT to change your code according to comments in the GitHub pull request",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    entry_points={"console_scripts": ["gptmypr = gptmypr.gptmypr:main"]},
    keywords=[
        "gptmypr",
        "pull request",
        "code review",
        "refactoring",
        "code quality",
        "ChatGPT",
        "GPT",
        "OpenAI",
        "GitHub",
    ],
    install_requires=[
        "rich==13.7.0",
        "openai==1.9.0",
        "PyGithub==2.1.1",
        "GitPython==3.1.41",
    ],
    zip_safe=False,
)
