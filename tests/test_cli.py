import unittest
from unittest.mock import patch
from click.testing import CliRunner
from starred_repo_finder.cli import cli


class TestCLI(unittest.TestCase):
    @patch("starred_repo_finder.cli.get_repos_starred_by_same_users")
    def test_cli(self, mock_run):
        runner = CliRunner()

        # setup
        repo_name = "test_repo"
        limit = 50
        order = "stargazers"
        format = "table"
        mock_run.return_value = (
            [["test_repo", "100", "20", "5"]],
            "table",
        )

        # action
        result = runner.invoke(
            cli,
            [repo_name, "--limit", str(limit), "--order", order, "--format", format],
        )

        # assert
        self.assertEqual(result.exit_code, 0)
        mock_run.assert_called_once_with(
            repo_name, limit, order, None, None, None, format
        )


if __name__ == "__main__":
    unittest.main()
