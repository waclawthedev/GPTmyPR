from setuptools import setup, find_packages

setup(
    name="gptmypr",
    version="0.1.0",
    author="waclawthedev",
    author_email="waclawthedev@gmail.com",
    url="https://github.com/waclawthedev/GPTmyPR",
    description="CLI tool to improve the PR after code review using OpenAI GPT",
    long_description="CLI tool to improve the PR after code review using OpenAI GPT",
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    entry_points={"console_scripts": ["gptmypr = gptmypr.gptmypr:main"]},
    keywords="gptmypr",
    install_requires=["rich==13.7.0", "openai==1.9.0", "PyGithub==2.1.1", "GitPython==3.1.41"],
    zip_safe=False,
)
