import unittest


class TestImports(unittest.TestCase):
    def test_module_imports(self):
        """
        Test if the main modules can be imported without raising a ModuleNotFoundError.
        """
        try:
            from starred_repo_finder.cli import cli
            from starred_repo_finder.starred_repo_finder import (
                get_repos_starred_by_same_users,
                print_results,
            )
        except ModuleNotFoundError as e:
            self.fail(f"Failed to import modules: {e}")


if __name__ == "__main__":
    unittest.main()
