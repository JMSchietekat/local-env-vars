import unittest
import os
import json

from src.local_env_vars.env import EnvironmentManager, EnvironmentException


class TestIntegration(unittest.TestCase):

    def setUp(self):
        try:
            os.rename('.gitignore', '.gitignore.bak')
        except Exception:
            pass

    def tearDown(self):
        try:
            os.remove(".env")
            os.remove(".gitignore")
            os.rename('.gitignore.bak', '.gitignore')
        except Exception:
            pass

    def test_create_ignore_file_if_it_does_not_exist(self):
        try:
            os.remove(".gitignore")
        except Exception:
            pass

        EnvironmentManager.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})
        self.envManager = EnvironmentManager("sql_username", "sql_password")

        self.assertTrue(os.path.exists(".gitignore"))

    def test_append_to_empty_ignore_file_when_env_not_ignored(self):
        with open(".gitignore", 'a'):
            os.utime(".gitignore", None)

        EnvironmentManager.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})
        self.envManager = EnvironmentManager("sql_username", "sql_password")

        found = False

        with open(".gitignore") as filereader:
            if '.env' in filereader.read():
                found = True

        self.assertTrue(found)

    def test_append_to_non_empty_ignore_file_when_env_not_ignored(self):
        with open(".gitignore", 'w') as filewriter:
            filewriter.write('*bak')

        EnvironmentManager.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})
        self.envManager = EnvironmentManager("sql_username", "sql_password")

        found = 0

        with open(".gitignore") as filereader:
            if '.env' in filereader.read():
                found += 1

        self.assertEqual(found, 1)

    def test_append_to_non_empty_ignore_file_when_env_already_ignored(self):
        with open(".gitignore", 'w') as filewriter:
            filewriter.write('.env')

        EnvironmentManager.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})
        self.envManager = EnvironmentManager("sql_username", "sql_password")

        found = 0

        with open(".gitignore") as filereader:
            if '.env' in filereader.read():
                found += 1

        self.assertEqual(found, 1)

    def test_create_env_file_with_no_prior(self):
        try:
            os.remove(".env")
        except FileNotFoundError:
            pass

        self.assertRaises(EnvironmentException, lambda: EnvironmentManager(
            "sql_server_address", "sql_username", "sql_password"))

        dictionary = EnvironmentManager.json_file_to_dictionary(".env")

        self.assertDictEqual(
            dictionary, {"sql_server_address": "", "sql_username": "", "sql_password": ""})

    def test_persist_env_file_when_exact_keys_are_used(self):
        EnvironmentManager.dictionary_to_json_file(
            ".env", {
                "username": "my_username",
                "password": "my_password"
            }
        )
        self.envManager = EnvironmentManager("username", "password")

        self.assertDictEqual(self.envManager.dictionary, {
            "username": "my_username",
            "password": "my_password"
        }
        )

    def test_exception_is_thrown_with_unpopulated_values(self):
        EnvironmentManager.dictionary_to_json_file(
            ".env",
            {
                "username": "my_username",
                "password": ""
            }
        )

        self.assertRaises(EnvironmentException, lambda: EnvironmentManager(
            "username", "password"))

    def test_added_keys_on_init_to_be_added_to_env_file(self):
        EnvironmentManager.dictionary_to_json_file(
            ".env",
            {
                "username": "my_username",
                "password": "my_password"
            }
        )

        self.assertRaises(EnvironmentException,
                          lambda: EnvironmentManager(
                              "username", "password", "ssh_key")
                          )

        readline = ""
        with open(".env", "r") as filereader:
            readline = filereader.read()

        self.assertEqual(
            readline, '{"username": "my_username", "password": "my_password", "ssh_key": ""}')

    def test_removed_keys_on_init_to_be_removed_from_env_file(self):
        EnvironmentManager.dictionary_to_json_file(
            ".env",
            {
                "username": "my_username",
                "password": "my_password"
            }
        )

        self.assertRaises(EnvironmentException,
                          lambda: EnvironmentManager("username"))

        readline = ""

        with open(".env", "r") as filereader:
            readline = filereader.read()

        self.assertEqual(readline, '{"username": "my_username"}')

    def test_empty_initialisation_to_throw_assertion_error(self):
        self.assertRaises(AssertionError, lambda: EnvironmentManager())


if __name__ == "__main__":
    unittest.main()
