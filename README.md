# Starred Repo Finder

A simple command line tool to find and explore GitHub repositories through stargazers for a given repository.

## Installation

```bash
pip install starred-repo-finder
```

## Build

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

## Usage

Command line usage:

```bash
usage: starred_repo_finder [-h] [-l LIMIT] [-o {stargazers,forkers,ratio}] [-s STARGAZERS] [-f FORKERS] [-r RATIO]
                           [-fmt {table,csv,json,markdown}]
                           repo_name

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
  -fmt {table,csv,json,markdown}, --format {table,csv,json,markdown}
                        Output format (default: table). Options: table, csv, json, markdown
```

## Examples

#### Find the top 10 GitHub repositories with the most shared stargazers to `facebook/react`, with a minimum of 10,000 stargazers, 1,000 forkers, and a ratio of at least 10 stargazers to forkers:

```bash
$ starred_repo_finder --limit=10 --order=ratio --stargazers=10000 --forkers=1000 --ratio=10 --format=markdown facebook/react
```

| Project | Stargazers | Forkers | Ratio |
|---|---|---|---|
| [denoland/deno](https://github.com/denoland/deno) | 23363 | 1016 | 23.0 |
| [typicode/json-server](https://github.com/typicode/json-server) | 22322 | 1013 | 22.04 |
| [GoogleChrome/puppeteer](https://github.com/GoogleChrome/puppeteer) | 21945 | 1057 | 20.76 |
| [nestjs/nest](https://github.com/nestjs/nest) | 20489 | 1077 | 19.02 |
| [flutter/flutter](https://github.com/flutter/flutter) | 34695 | 1838 | 18.88 |
| [jlevy/the-art-of-command-line](https://github.com/jlevy/the-art-of-command-line) | 22344 | 1221 | 18.3 |
| [rust-lang/rust](https://github.com/rust-lang/rust) | 21320 | 1178 | 18.1 |
| [996icu/996.ICU](https://github.com/996icu/996.ICU) | 21113 | 1173 | 18.0 |
| [thedaviddias/Front-End-Checklist](https://github.com/thedaviddias/Front-End-Checklist) | 18298 | 1024 | 17.87 |
| [danistefanovic/build-your-own-x](https://github.com/danistefanovic/build-your-own-x) | 20732 | 1209 | 17.15 |

#### Find the top 10 GitHub repositories with the most shared stargazers to `pulumi/templates` in the default CLI [rich table](https://rich.readthedocs.io/en/stable/tables.html) format:

```bash
$ starred_repo_finder --limit=10 pulumi/templates

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━┓
┃ Project                           ┃ Stargazers ┃ Forkers ┃ Ratio ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━┩
│  pulumi/templates                 │ 63         │ 6       │ 10.5  │
│  pulumi/pulumi                    │ 40         │ 4       │ 10.0  │
│  pulumi/examples                  │ 34         │ 5       │ 6.8   │
│  kubernetes/kubernetes            │ 28         │ 6       │ 4.67  │
│  localstack/localstack            │ 25         │ 3       │ 8.33  │
│  ansible/ansible                  │ 24         │ 3       │ 8.0   │
│  hashicorp/terraform              │ 23         │ 4       │ 5.75  │
│  mingrammer/diagrams              │ 23         │ 0       │ N/A   │
│  kamranahmedse/developer-roadmap  │ 22         │ 3       │ 7.33  │
│  GoogleCloudPlatform/terraformer  │ 21         │ 2       │ 10.5  │
└───────────────────────────────────┴────────────┴─────────┴───────┘
```

#### Find the top 25 GitHub repositories with the most shared stargazers to `theOehrly/Fast-F1`, with a minimum of 5 forkers ordered by ratio in markdown format:

```bash
$ starred_repo_finder --limit=25 --order=ratio --forkers=5 --format=markdown theOehrly/Fast-F1
```

| Project | Stargazers | Forkers | Ratio |
|---|---|---|---|
| [kamranahmedse/developer-roadmap](https://github.com/kamranahmedse/developer-roadmap) | 186 | 5 | 37.2 |
| [public-apis/public-apis](https://github.com/public-apis/public-apis) | 220 | 8 | 27.5 |
| [theOehrly/Fast-F1](https://github.com/theOehrly/Fast-F1) | 1633 | 72 | 22.68 |
| [huggingface/transformers](https://github.com/huggingface/transformers) | 128 | 6 | 21.33 |
| [sindresorhus/awesome](https://github.com/sindresorhus/awesome) | 189 | 9 | 21.0 |
| [danistefanovic/build-your-own-x](https://github.com/danistefanovic/build-your-own-x) | 164 | 8 | 20.5 |
| [airbnb/javascript](https://github.com/airbnb/javascript) | 93 | 5 | 18.6 |
| [tiangolo/fastapi](https://github.com/tiangolo/fastapi) | 128 | 7 | 18.29 |
| [trimstray/the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge) | 107 | 6 | 17.83 |
| [microsoft/PowerToys](https://github.com/microsoft/PowerToys) | 141 | 8 | 17.62 |
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | 175 | 10 | 17.5 |
| [Genymobile/scrcpy](https://github.com/Genymobile/scrcpy) | 85 | 5 | 17.0 |
| [openai/gym](https://github.com/openai/gym) | 85 | 5 | 17.0 |
| [twitter/the-algorithm](https://github.com/twitter/the-algorithm) | 118 | 7 | 16.86 |
| [3b1b/manim](https://github.com/3b1b/manim) | 134 | 8 | 16.75 |
| [pi-hole/pi-hole](https://github.com/pi-hole/pi-hole) | 98 | 6 | 16.33 |
| [CorentinJ/Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning) | 79 | 5 | 15.8 |
| [supabase/supabase](https://github.com/supabase/supabase) | 110 | 7 | 15.71 |
| [sherlock-project/sherlock](https://github.com/sherlock-project/sherlock) | 93 | 6 | 15.5 |
| [vinta/awesome-python](https://github.com/vinta/awesome-python) | 170 | 11 | 15.45 |
| [strapi/strapi](https://github.com/strapi/strapi) | 77 | 5 | 15.4 |
| [microsoft/Web-Dev-For-Beginners](https://github.com/microsoft/Web-Dev-For-Beginners) | 92 | 6 | 15.33 |
| [NationalSecurityAgency/ghidra](https://github.com/NationalSecurityAgency/ghidra) | 76 | 5 | 15.2 |
| [florinpop17/app-ideas](https://github.com/florinpop17/app-ideas) | 75 | 5 | 15.0 |

#### Write the top 100 GitHub repositories with the most shared stargazers to `sveltejs/svelte` to a CSV file:

```bash
$ starred_repo_finder --limit=100 --format=csv sveltejs/svelte > examples/sveltejs-svelte.csv
```

See [examples/sveltejs-svelte.csv](examples/sveltejs-svelte.csv) for the output.

#### Write the top 50 GitHub repositories with the most shared stargazers to `duckdb/duckdb` to a JSON file:

```bash
$ starred_repo_finder --limit=50 --format=json duckdb/duckdb > examples/duckdb-duckdb.json
```

See [examples/duckdb/duckdb.json](examples/duckdb-duckdb.json) for the output.

#### Write the top 50 GitHub repositories with the most shared stargazers to `Ionaru/easy-markdown-editor` to a markdown file:

```bash
$ starred_repo_finder --limit=50 --format=markdown Ionaru/easy-markdown-editor > examples/ionaru-easy-markdown-editor.md
```

See [examples/ionaru-easy-markdown-editor.md](examples/ionaru-easy-markdown-editor.md) for the output.
