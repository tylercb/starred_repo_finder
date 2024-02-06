import click
from .starred_repo_finder import get_repos_starred_by_same_users, print_results
from .__version__ import __version__


@click.command()
@click.version_option(version=__version__, prog_name="starred_repo_finder")
@click.argument("repo_name")
@click.option(
    "--limit",
    "-l",
    default=100,
    help="The maximum number of results to return (default: 100)",
    type=int,
)
@click.option(
    "--order",
    "-o",
    default="stargazers",
    help="Column to order by (default: stargazers). Options: stargazers, forkers, ratio",
    type=click.Choice(["stargazers", "forkers", "ratio"], case_sensitive=False),
)
@click.option(
    "--stargazers",
    "-s",
    default=None,
    help="Minimum number of stargazers to include (default: None)",
    type=int,
)
@click.option(
    "--forkers",
    "-f",
    default=None,
    help="Minimum number of forkers to include (default: None)",
    type=int,
)
@click.option(
    "--ratio",
    "-r",
    default=None,
    help="Minimum ratio of stargazers to forkers to include (default: None)",
    type=float,
)
@click.option(
    "--format",
    "-fmt",
    default="table",
    help="Output format (default: table). Options: table, csv, json, markdown",
    type=click.Choice(["table", "csv", "json", "markdown"], case_sensitive=False),
)
def cli(repo_name, limit, order, stargazers, forkers, ratio, format):
    """
    Parse command line arguments
    """
    results, _ = get_repos_starred_by_same_users(
        repo_name,
        limit,
        order,
        stargazers,
        forkers,
        ratio,
        format,
    )
    print_results(results, format)


if __name__ == "__main__":
    cli()
