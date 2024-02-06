# Starred Repo Finder

A simple command line tool to find and explore GitHub repositories through stargazers for a given repository.

Features:

- Find all repositories that are starred by the stargazers of a given repository
- Filter results by minimum number of stargazers, forkers, and ratio of stargazers to forkers
- Order results by stargazers, forkers, and ratio of stargazers to forkers
- Output results in table, CSV, JSON, and markdown formats
- Uses the [GitHub Events Dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/github-events) and [ClickHouse](https://clickhouse.com) to query the data

## Installation

```bash
pip install starred-repo-finder --upgrade
```

## Usage

Command line usage:

```bash
$ starred_repo_finder --help
usage: starred_repo_finder [-h] [-l LIMIT]
                           [-o {stargazers,forkers,ratio}]
                           [-s STARGAZERS] [-f FORKERS] [-r RATIO]
                           [-fmt {table,csv,json,markdown}]
                           repo_name

positional arguments:
  repo_name             The repository name like`<owner>/<repo>`

options:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        The maximum number of results to return
                        (default: 100)
  -o {stargazers,forkers,ratio}, --order {stargazers,forkers,ratio}
                        Column to order by (default: stargazers).
                        Options: stargazers, forkers, ratio
  -s STARGAZERS, --stargazers STARGAZERS
                        Minimum number of stargazers to include
                        (default: None)
  -f FORKERS, --forkers FORKERS
                        Minimum number of forkers to include
                        (default: None)
  -r RATIO, --ratio RATIO
                        Minimum ratio of stargazers to forkers to
                        include (default: None)
  -fmt {table,csv,json,markdown}, --format {table,csv,json,markdown}
                        Output format (default: table). Options:
                        table, csv, json, markdown
```

Flask app usage:
  
```bash
pip install starred-repo-finder --upgrade
```

Once the package is installed, import and use the `get_repos_starred_by_same_users()` function in your Flask app like this:

```python
from flask import Flask, jsonify, request
from starred_repo_finder import get_repos_starred_by_same_users

app = Flask(__name__)

@app.route('/starred_repo', methods=['GET', 'POST'])
def find_starred_repo():
    # check the request method
    if request.method == "POST":
        params = request.json
    else:
        params = request.args

    # repo_name is required
    repo_name = params.get("repo_name")
    if repo_name is None:
        return (
            jsonify({"error": "repo_name parameter is required"}),
            400,
        )

    # get the optional parameters or use the default values
    limit = int(params.get("limit", 10))
    order = params.get("order", "stargazers")

    # call the function from your package
    results, _ = get_repos_starred_by_same_users(repo_name, limit, order)

    # process the results as needed, here for instance we're sending them as JSON
    return jsonify(results)
```

Jupyter Notebook usage:

```python
%pip install starred-repo-finder --upgrade
```

Once the package is installed, import and use the `get_repos_starred_by_same_users()` function in your Jupyter Notebook like this:

```python
# Import necessary packages
from starred_repo_finder import get_repos_starred_by_same_users

# Define parameters
repo_name = 'vinta/awesome-python'
limit = 10
order = 'stargazers'

# Call the function
results, _ = get_repos_starred_by_same_users(repo_name, limit, order)

# Display the results
print(results)
```

## Build & Test

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

## Examples

#### Find the top 100 shared GitHub repositories by stars for stargazers of the `Elderjs/elderjs` repo:

```bash
$ starred_repo_finder Elderjs/elderjs
```

![Screenshot](https://github.com/tylercb/starred_repo_finder/raw/main/screenshot.png)

#### Find the top 10 shared GitHub repositories by stars for stargazers of the `facebook/react` repo, from repos with a minimum of 10,000 stargazers, 1,000 forkers, and a ratio of at least 10 stargazers to each forkers:

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

#### Find the top 10 shared GitHub repositories by stars for stargazers of the `pulumi/templates` repo, using the default CLI [rich table](https://rich.readthedocs.io/en/stable/tables.html) output format:

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

#### Find the top 25 shared GitHub repositories by stars for stargazers of the `theOehrly/Fast-F1` repo, from repos with a minimum of 5 forkers ordered by ratio in markdown format:

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

#### Write the top 100 shared GitHub repositories by stars for stargazers of the `sveltejs/svelte` repo to a CSV file:

```bash
$ starred_repo_finder --limit=100 --format=csv sveltejs/svelte > examples/sveltejs-svelte.csv
```

See [examples/sveltejs-svelte.csv](https://github.com/tylercb/starred_repo_finder/blob/main/examples/sveltejs-svelte.csv) for the output.

#### Write the top 50 shared GitHub repositories by stars for stargazers of the `duckdb/duckdb` repo to a JSON file:

```bash
$ starred_repo_finder --limit=50 --format=json duckdb/duckdb > examples/duckdb-duckdb.json
```

See [examples/duckdb-duckdb.json](https://github.com/tylercb/starred_repo_finder/blob/main/examples/duckdb-duckdb.json) for the output.

#### Write the top 50 shared GitHub repositories by stars for stargazers of the `Ionaru/easy-markdown-editor` repo to a markdown file:

```bash
$ starred_repo_finder --limit=50 --format=markdown Ionaru/easy-markdown-editor > examples/ionaru-easy-markdown-editor.md
```

See [examples/ionaru-easy-markdown-editor.md](https://github.com/tylercb/starred_repo_finder/blob/main/examples/ionaru-easy-markdown-editor.md) for the output.

## Tools

Bump the version:

```bash
bumpversion minor
```

## Acknowledgements

This would not be possible without the following:

- [ClickHouse Playground](https://clickhouse.com/docs/en/getting-started/playground)
- [ClickHouse Query](https://play.clickhouse.com/play)
- [GitHub Events Dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/github-events)

## Contributing

Contributions are welcome! Negative feedback is also welcome, but please be constructive. If you have a feature request, please open an issue first to discuss it. If you want to contribute code, please open an issue first to discuss it. If you want to contribute documentation, please open an issue first to discuss it. If you want to contribute an example, please open an issue first to discuss it. If you want to contribute a bug fix, please open an issue first to discuss it. If you want to contribute a test, please open an issue first to discuss it. If you want to contribute anything else, please open an issue first to discuss it. If you want to contribute a donation, please open an issue first to discuss it.

## License

[MIT](LICENSE)
