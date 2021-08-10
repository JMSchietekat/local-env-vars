import unittest
import os
import json

from src.local_env_vars.env import EnvironmentManager, EnvironmentException

class TestClassWithNoEnvFile(unittest.TestCase):
    """
    Initialise class with no prior .env file.
    """

    def setUp(self):
        try:
            os.remove(".env")
        except FileNotFoundError:
            pass

        self.assertRaises(EnvironmentException, lambda: EnvironmentManager(
            "sql_server_address", "sql_username", "sql_password"))

    def tearDown(self):
        os.remove(".env")

    def test_env_file_created(self):
        self.assertEqual(os.path.exists(".env"), True)

    def test_new_env_file_containes_specified_keys(self):
        dictionary = EnvironmentManager.json_file_to_dictionary(".env")

        self.assertDictEqual(
            dictionary, {"sql_server_address": "", "sql_username": "", "sql_password": ""})


class TestClassWithPopulatedEnvFile(unittest.TestCase):
    """
    Initialise class with correct pre exisiting .env file.
    """

    def setUp(self):
        EnvironmentManager.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})
        self.envManager = EnvironmentManager("sql_username", "sql_password")

    def tearDown(self):
        os.remove(self.envManager._env_file)

    def test_class_dictionary_equals_env_file_content(self):
        self.assertDictEqual(self.envManager.dictionary, {
                             "sql_username": "un", "sql_password": "pwd"})


class TestClassWithUnpopulatedEnvFile(unittest.TestCase):
    """
    Initialise class with pre exisiting .env file that has an empty value.
    """

    def test_that_exception_is_thrown(self):
        EnvironmentManager.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": ""})

        self.assertRaises(EnvironmentException, lambda: EnvironmentManager(
            "sql_username", "sql_password"))

        os.remove(".env")

class TestClassWithAddedKeysOnInit(unittest.TestCase):
    """
    Initialise class with more keys than in .env file.
    """

    def setUp(self):
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

    def tearDown(self):
        os.remove(".env")

    def test_env_file_contains_added_key(self):
        readline = ""
        with open(".env", "r") as filereader:
            readline = filereader.read()

        self.assertEqual(
            readline, '{"username": "my_username", "password": "my_password", "ssh_key": ""}')


class TestClassWithRemovedKeysOnInit(unittest.TestCase):
    """
    Initialise class with less keys than in .env file.
    """

    def setUp(self):
        EnvironmentManager.dictionary_to_json_file(
            ".env",
            {
                "username": "my_username",
                "password": "my_password"
            }
        )

        self.assertRaises(EnvironmentException,
                          lambda: EnvironmentManager("username"))

    def tearDown(self):
        os.remove(".env")

    def test_env_file_contains_does_not_contain_removed_key(self):
        readline = ""
        with open(".env", "r") as filereader:
            readline = filereader.read()

        self.assertEqual(readline, '{"username": "my_username"}')


class TestClassWithNoInputArgs(unittest.TestCase):
    """
    Initialise class with no input arguments
    """

    def test_empty_initialisation_to_throw_assertion_error(self):
        self.assertRaises(AssertionError, lambda: EnvironmentManager())


if __name__ == "__main__":
    unittest.main()
