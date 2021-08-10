import unittest
import os
import json

from src.local_env_vars.env import EnvironmentManager, EnvironmentException


class TestClassToAddIgnoreFile(unittest.TestCase):
    """
    Initialise class with working setup. Ensure .gitignore file is created if it does not exists.
    """

    def setUp(self):
        try:
            os.rename('.gitignore', '.gitignore.bak')
        except Exception:
            pass

        self._gitignore = ".gitignore"
        
        try:
            os.remove(self._gitignore)
        except Exception:
            pass

    def tearDown(self):
        os.remove(".env")
        os.remove(self._gitignore)

        try:
            os.rename('.gitignore.bak', '.gitignore')
        except Exception:
            pass

    def test_create_ignore_if_it_does_not_exists_and_ignore_env_file(self):
        EnvironmentManager.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})
        self.envManager = EnvironmentManager("sql_username", "sql_password")

        self.assertTrue(os.path.exists(self._gitignore))


if __name__ == "__main__":
    unittest.main()
