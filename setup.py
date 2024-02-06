from setuptools import setup, find_packages

setup(
    name="starred_repo_finder",
    version="1.4.0",
    description="A simple command line tool to find and explore GitHub repositories through stargazers for a given repository.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tylercb/starred_repo_finder",
    author="Tyler Hanway",
    author_email="hanway.tyler@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
        "rich",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points="""
        [console_scripts]
        starred_repo_finder=starred_repo_finder.cli:cli
    """,
)
