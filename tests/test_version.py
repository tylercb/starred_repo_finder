import unittest
from click.testing import CliRunner
from starred_repo_finder.cli import cli
from starred_repo_finder.__version__ import __version__


class TestCLIVersion(unittest.TestCase):
    def test_version_output(self):
        """Test if `--version` option returns the current version."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        expected_output = f"starred_repo_finder, version {__version__}\n"

        self.assertEqual(result.exit_code, 0)
        self.assertIn(expected_output, result.output)


if __name__ == "__main__":
    unittest.main()
