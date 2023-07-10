#!/usr/bin/env python3

import requests
import argparse
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


def convert_and_format_results(results, output_format):
    """
    Converts and formats results list.
    """
    converted_results = []
    for row in results:
        repo_name = row[0]
        github_url = f"https://github.com/{repo_name}"
        stargazers = int(row[1])
        forkers = int(row[2])
        ratio = float(row[3]) if row[3] != "\\N" else None
        converted_results.append(
            {
                "repo_name": repo_name,
                "github_url": github_url,
                "stargazers": stargazers,
                "forkers": forkers,
                "ratio": ratio,
            }
        )

    if output_format == "csv":
        output = "repo_name,github_url,stargazers,forkers,ratio\n"
        for row in converted_results:
            output += f'{row["repo_name"]},{row["github_url"]},{row["stargazers"]},{row["forkers"]},{row["ratio"]}\n'
    elif output_format == "json":
        output = json.dumps(converted_results, indent=4)
    elif output_format == "markdown":
        output = "| Project | Stargazers | Forkers | Ratio |\n|---|---|---|---|\n"
        for row in converted_results:
            output += f'| [{row["repo_name"]}]({row["github_url"]}) | {row["stargazers"]} | {row["forkers"]} | {row["ratio"]} |\n'
    elif output_format == "table":
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Project")
        table.add_column("Stargazers")
        table.add_column("Forkers")
        table.add_column("Ratio")

        for row in converted_results:
            stargazers = "{:,}".format(row["stargazers"])
            forkers = "{:,}".format(row["forkers"])
            ratio = row["ratio"] if row["ratio"] is not None else "N/A"
            table.add_row(
                f'[link={row["github_url"]}] {row["repo_name"]} [/link]',
                stargazers,
                forkers,
                str(ratio),
            )
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


def run(
    repo_name,
    limit=100,
    order_by="stargazers",
    stargazers=None,
    forkers=None,
    ratio=None,
    output_format="table",
):
    """
    Run the script.
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

    # Print the results
    print_results(results, output_format)


def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_name", help="The repository name like`<owner>/<repo>`")
    parser.add_argument(
        "-l",
        "--limit",
        help="The maximum number of results to return (default: 100)",
        default=100,
        type=int,
    )
    parser.add_argument(
        "-o",
        "--order",
        help="Column to order by (default: stargazers). Options: stargazers, forkers, ratio",
        default="stargazers",
        choices=["stargazers", "forkers", "ratio"],
    )
    parser.add_argument(
        "-s",
        "--stargazers",
        help="Minimum number of stargazers to include (default: None)",
        type=int,
        default=None,
    )
    parser.add_argument(
        "-f",
        "--forkers",
        help="Minimum number of forkers to include (default: None)",
        type=int,
        default=None,
    )
    parser.add_argument(
        "-r",
        "--ratio",
        help="Minimum ratio of stargazers to forkers to include (default: None)",
        type=float,
        default=None,
    )
    parser.add_argument(
        "-fmt",
        "--format",
        help="Output format (default: table). Options: table, csv, json, markdown",
        default="table",
        choices=["table", "csv", "json", "markdown"],
    )
    args = parser.parse_args()

    # Run the script
    run(
        args.repo_name,
        args.limit,
        args.order,
        args.stargazers,
        args.forkers,
        args.ratio,
        args.format,
    )


if __name__ == "__main__":
    main()
