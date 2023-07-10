# Starred Repo Finder

A simple command line tool to find and explore GitHub repositories through stargazers for a given repository.

Create a new virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install requirements:

```bash
pip install -e .
```

Run tests:

```bash
pytest
```

Command line usage:

```bash
usage: starred_repo_finder [-h] [-l LIMIT] [-o {stargazers,forkers,ratio}] [-s STARGAZERS] [-f FORKERS] [-r RATIO] repo_name

positional arguments:
  repo_name             The repository name like`<owner>/<repo>`

options:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        The maximum number of results to return (default: 100)
  -o {stargazers,forkers,ratio}, --order {stargazers,forkers,ratio}
                        Column to order by (default: stargazers). Options: stargazers, forkers, ratio
  -s STARGAZERS, --stargazers STARGAZERS
                        Minimum number of stargazers to include (default: None)
  -f FORKERS, --forkers FORKERS
                        Minimum number of forkers to include (default: None)
  -r RATIO, --ratio RATIO
                        Minimum ratio of stargazers to forkers to include (default: None)
```

## Examples

Find the top 10 GitHub repositories with the most shared stargazers to `facebook/react`, with a minimum of 10,000 stargazers, 1,000 forkers, and a ratio of 10 stargazers to forkers:

```bash
$ starred_repo_finder --limit=10 --order=ratio --stargazers=10000 --forkers=1000 --ratio=10 facebook/react
```

| Project | Stargazers | Forkers | Ratio |
|---|---|---|---|
| denoland/deno | 23362 | 1016 | 22.994 |
| typicode/json-server | 22319 | 1013 | 22.033 |
| GoogleChrome/puppeteer | 21945 | 1057 | 20.762 |
| nestjs/nest | 20487 | 1077 | 19.022 |
| flutter/flutter | 34695 | 1838 | 18.876 |
| jlevy/the-art-of-command-line | 22344 | 1221 | 18.3 |
| rust-lang/rust | 21320 | 1178 | 18.098 |
| 996icu/996.ICU | 21113 | 1173 | 17.999 |
| thedaviddias/Front-End-Checklist | 18298 | 1024 | 17.869 |
| danistefanovic/build-your-own-x | 20732 | 1209 | 17.148 |

```bash

```

```csv

```