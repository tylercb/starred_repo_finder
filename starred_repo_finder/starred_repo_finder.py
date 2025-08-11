#!/usr/bin/env python3

import requests
import json
from rich.console import Console
from rich.table import Table

console = Console()


def build_query(repo_name, limit, order_by, min_stargazers, min_forkers, min_ratio):
    """
    Build a SQL query to send to the ClickHouse server for the GitHub data based on the provided parameters.

    :param repo_name: The full name of the GitHub repository, in the format '<owner>/<repo>'.
    :param limit: The maximum number of results to return.
    :param order_by: The column to order the results by.
    :param min_stargazers: The minimum number of stargazers a repository must have to be included in the results.
    :param min_forkers: The minimum number of forkers a repository must have to be included in the results.
    :param min_ratio: The minimum ratio of stargazers to forkers a repository must have to be included in the results.
    :return: The SQL query as a string.
    """
    # Add HAVING clauses to the query if min_stargazers or min_forkers or min_ratio is provided
    having_clause = "HAVING 1=1"
    if min_stargazers:
        having_clause += f" AND stargazers >= {min_stargazers}"
    if min_forkers:
        having_clause += f" AND forkers >= {min_forkers}"
    if min_ratio:
        having_clause += f" AND ratio >= {min_ratio}"

    return f"""
    WITH source AS (
      SELECT actor_login AS stargazer
      FROM github_events
      WHERE repo_name = '{repo_name}' AND event_type = 'WatchEvent'
      GROUP BY 1
    )

    SELECT
      e.repo_name,
      count(DISTINCT(if(event_type = 'WatchEvent', e.actor_login, null))) as stargazers,
      count(DISTINCT(if(event_type = 'ForkEvent', e.actor_login, null))) as forkers,
      round(if(forkers = 0, null, stargazers / forkers), 2) AS ratio
    FROM github_events e
    JOIN source s ON e.actor_login = s.stargazer
    WHERE e.event_type IN ('ForkEvent', 'WatchEvent')
    GROUP BY e.repo_name
    {having_clause}
    ORDER BY {order_by} DESC
    LIMIT {limit}
    """


def make_request(query, url, params):
    """
    Make a request to the ClickHouse server.
    """
    try:
        return requests.post(url, params=params, data=query, timeout=10)
    except requests.exceptions.RequestException as err:
        console.print(f"Request failed: {err}", style="bold red")
        raise err


def process_response(response):
    """
    Process the response from the request to the ClickHouse server.
    """
    if response.status_code != 200:
        console.print(
            f"Request failed with status code {response.status_code}: {response.content.decode()}",
            style="bold red",
        )
        return []

    lines = response.content.decode().split("\n")
    return [line.split("\t") for line in lines if line]


def normalize_row(row):
    """
    Normalize a row from the results.
    """
    if isinstance(row, dict):
        repo_name = row.get("repo_name")
        stargazers = row.get("stargazers", 0)
        forkers = row.get("forkers", 0)
        ratio = row.get("ratio")
    elif isinstance(row, (list, tuple)) and len(row) >= 4:
        repo_name, stargazers, forkers, ratio = row[:4]
    else:
        raise ValueError("Invalid row format.")

    return {
        "repo_name": repo_name,
        "github_url": f"https://github.com/{repo_name}",
        "stargazers": int(stargazers),
        "forkers": int(forkers),
        "ratio": None if ratio in [None, "\\N"] else float(ratio),
    }



def convert_and_format_results(results, output_format):
    """
    Converts and formats results list.
    """
    # Using list comprehension
    converted_results = [normalize_row(row) for row in results]

    if output_format == "csv":
        
        lines = [",".join([str(row[key]) for key in ["repo_name", "github_url", "stargazers", "forkers", "ratio"]]) for row in converted_results]
        output = "repo_name,github_url,stargazers,forkers,ratio\n" + "\n".join(lines)
    elif output_format == "json":
        output = json.dumps(converted_results, indent=4)
    elif output_format == "markdown":
        # Generate Markdown table format more
        md_lines = [f'| [{row["repo_name"]}]({row["github_url"]}) | {row["stargazers"]} | {row["forkers"]} | {row.get("ratio", "N/A")} |' for row in converted_results]
        output = "| Project | Stargazers | Forkers | Ratio |\n|---|---|---|---|\n" + "\n".join(md_lines)
    elif output_format == "table":
        from rich.table import Table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Project")
        table.add_column("Stargazers")
        table.add_column("Forkers")
        table.add_column("Ratio")

        for row in converted_results:
            stargazers, forkers = "{:,}".format(row["stargazers"]), "{:,}".format(row["forkers"])
            ratio = row["ratio"] if row["ratio"] is not None else "N/A"
            table.add_row(f'[link={row["github_url"]}] {row["repo_name"]} [/link]', stargazers, forkers, str(ratio))
        output = table
    else:
        output = str(converted_results)

    return converted_results, output


def print_results(results, output_format):
    """
    Print the results to the console in the specified format.
    """
    if not results:
        console.print("No results found", style="bold red")
        return

    results, output = convert_and_format_results(results, output_format)

    # Don't use rich for csv, json, or markdown output
    if output_format in ["csv", "json", "markdown"]:
        print(output)
    else:
        console.print(output)

    return results


def get_repos_starred_by_same_users(
    repo_name,
    limit=100,
    order_by="stargazers",
    stargazers=None,
    forkers=None,
    ratio=None,
    output_format="table",
):
    """
    Run the script and get repos starred by the same users.
    """
    query = build_query(repo_name, limit, order_by, stargazers, forkers, ratio)

    # Make the request
    params = {"user": "explorer"}
    url = "https://play.clickhouse.com/"
    try:
        response = make_request(query, url, params)
    except requests.exceptions.RequestException as err:
        console.print(f"Failed to make a request: {err}", style="bold red")
        return

    # Ensure the response is not None and has a 200 status code
    if not response or response.status_code != 200:
        console.print("No response or bad response from server.", style="bold red")
        return

    # Process the response
    results = process_response(response)
    return convert_and_format_results(results, output_format)
