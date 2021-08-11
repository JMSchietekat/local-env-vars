import unittest
import os
import json

from src.local_env_vars.env import LocalEnvVars, LocalEnvVarsException


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

        LocalEnvVars.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})
        self.envManager = LocalEnvVars("sql_username", "sql_password")

        self.assertTrue(os.path.exists(".gitignore"))

    def test_append_to_empty_ignore_file_when_env_not_ignored(self):
        with open(".gitignore", 'a'):
            os.utime(".gitignore", None)

        LocalEnvVars.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})
        self.envManager = LocalEnvVars("sql_username", "sql_password")

        found = False

        with open(".gitignore") as filereader:
            if '.env' in filereader.read():
                found = True

        self.assertTrue(found)

    def test_append_to_non_empty_ignore_file_when_env_not_ignored(self):
        with open(".gitignore", 'w') as filewriter:
            filewriter.write('*bak')

        LocalEnvVars.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})
        self.envManager = LocalEnvVars("sql_username", "sql_password")

        found = 0

        with open(".gitignore") as filereader:
            if '.env' in filereader.read():
                found += 1

        self.assertEqual(found, 1)

    def test_append_to_non_empty_ignore_file_when_env_already_ignored(self):
        with open(".gitignore", 'w') as filewriter:
            filewriter.write('.env')

        LocalEnvVars.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})
        self.envManager = LocalEnvVars("sql_username", "sql_password")

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

        self.assertRaises(LocalEnvVarsException, lambda: LocalEnvVars(
            "sql_server_address", "sql_username", "sql_password"))

        dictionary = LocalEnvVars.json_file_to_dictionary(".env")

        self.assertDictEqual(
            dictionary, {"sql_server_address": "", "sql_username": "", "sql_password": ""})

    def test_persist_env_file_when_exact_keys_are_used(self):
        LocalEnvVars.dictionary_to_json_file(
            ".env", {
                "username": "my_username",
                "password": "my_password"
            }
        )
        self.lev = LocalEnvVars("username", "password")

        self.assertDictEqual(self.lev.vars, {
            "username": "my_username",
            "password": "my_password"
        }
        )

    def test_exception_is_thrown_with_unpopulated_values(self):
        LocalEnvVars.dictionary_to_json_file(
            ".env",
            {
                "username": "my_username",
                "password": ""
            }
        )

        self.assertRaises(LocalEnvVarsException, lambda: LocalEnvVars(
            "username", "password"))

    def test_added_keys_on_init_to_be_added_to_env_file(self):
        LocalEnvVars.dictionary_to_json_file(
            ".env",
            {
                "username": "my_username",
                "password": "my_password"
            }
        )

        self.assertRaises(LocalEnvVarsException,
                          lambda: LocalEnvVars(
                              "username", "password", "ssh_key")
                          )

        readline = ""
        with open(".env", "r") as filereader:
            readline = filereader.read()

        self.assertEqual(
            readline, '{"username": "my_username", "password": "my_password", "ssh_key": ""}')

    def test_removed_keys_on_init_to_be_removed_from_env_file(self):
        LocalEnvVars.dictionary_to_json_file(
            ".env",
            {
                "username": "my_username",
                "password": "my_password"
            }
        )

        self.assertRaises(LocalEnvVarsException,
                          lambda: LocalEnvVars("username"))

        readline = ""

        with open(".env", "r") as filereader:
            readline = filereader.read()

        self.assertEqual(readline, '{"username": "my_username"}')

    def test_empty_initialisation_to_throw_assertion_error(self):
        self.assertRaises(AssertionError, lambda: LocalEnvVars())

class TestStaticArgsToEmptyDictionary(unittest.TestCase):
    """
    Should create a dictionary with empty values and keys equal to the list provided.
    """

    def test_input_args_and_compare_with_expected_dictionary(self):

        dictionary = LocalEnvVars.args_to_empty_dictionary(
            "args", "to", "test")

        self.assertDictEqual(dictionary, {"args": "", "to": "", "test": ""})


class TestStaticCreateFile(unittest.TestCase):
    """
    Should create file.
    """

    def setUp(self):
        self.filename = "create_file_test.txt"
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass

    def tearDown(self):
        os.remove(self.filename)

    def test_create_file_when_it_already_existed(self):
        LocalEnvVars.create_file(self.filename)
        self.assertRaises(
            AssertionError, lambda: LocalEnvVars.create_file(self.filename))


class TestStaticDictHasEqualKeys(unittest.TestCase):
    """
    Should compare the keys (not their values) of two dictionaries and report equality.
    """

    def test_dictionaries_with_non_equal_keys_to_be_false(self):
        dict1 = {"args": "", "to": "", "test": ""}
        dict2 = {"args": "value1", "to": "value2", "tes": "value3"}

        self.assertFalse(LocalEnvVars.dict_has_equal_keys(dict1, dict2))

    def test_dictionaries_with_a_subset_of_equal_keys_to_be_false(self):
        dict1 = {"args": "", "to": "", "test": ""}
        dict2 = {"args": "value1", "to": "value2",
                 "test": "value3", "with": ""}

        self.assertFalse(LocalEnvVars.dict_has_equal_keys(dict1, dict2))

    def test_dictionaries_with_equal_keys_to_be_true(self):
        dict1 = {"args": "", "to": "", "test": ""}
        dict2 = {"args": "value1", "to": "value2", "test": "value3"}

        self.assertTrue(LocalEnvVars.dict_has_equal_keys(dict1, dict2))

    def test_dictionaries_with_equal_keys_in_different_order_to_be_true(self):
        dict1 = {"args": "", "to": "", "test": ""}
        dict2 = {"to": "value2", "args": "value1", "test": "value3"}

        self.assertTrue(LocalEnvVars.dict_has_equal_keys(dict1, dict2))

    def test_empty_dictionary(self):
        dict1 = {}
        dict2 = {}

        self.assertTrue(LocalEnvVars.dict_has_equal_keys(dict1, dict2))


class TestStaticDictHasValues(unittest.TestCase):
    """
    Check that a dictionary has no empty values.
    """

    def test_with_values_to_be_true(self):
        dictionary = {"args": "1", "to": "2", "test": "3"}
        self.assertTrue(LocalEnvVars.dict_has_values(dictionary))

    def test_with_omitted_values_to_be_false(self):
        dictionary = {"args": "1", "to": "2", "test": ""}
        self.assertFalse(LocalEnvVars.dict_has_values(dictionary))

    def test_with_zero_items_should_throw_error(self):
        dictionary = {}
        self.assertRaises(
            AssertionError, lambda: LocalEnvVars.dict_has_values(dictionary))


class TestStaticDictionaryToJsonFile(unittest.TestCase):
    """
    Write dictionary to file in json format.
    """

    def test_provided_dictionary_is_writen_to_file(self):
        dictionary = {"args": "", "to": "", "test": ""}
        filename = ".env"
        readline = ""

        LocalEnvVars.dictionary_to_json_file(filename, dictionary)

        with open(filename, "r") as filereader:
            readline = filereader.read()

        self.assertEqual(readline, '{"args": "", "to": "", "test": ""}')

        os.remove(filename)


class TestStaticFileExists(unittest.TestCase):
    """
    Cofirm that a file exists or not.
    """

    def setUp(self):
        self.filename = "test.txt"

    def test_when_file_exists(self):
        filewriter = open(self.filename, "w+")
        filewriter.close()

        self.assertTrue(LocalEnvVars.file_exists(self.filename))

        os.remove(self.filename)

    def test_when_file_does_not_exists(self):
        self.assertFalse(LocalEnvVars.file_exists(self.filename))


class TestStaticJsonFileToDictionary(unittest.TestCase):
    """
    Import and parse json and return a dictionary.
    """

    def setUp(self):
        self.filename = "json_test_file.json"

    def tearDown(self):
        os.remove(self.filename)

    def test_with_valid_json(self):
        with open(self.filename, 'w') as filewriter:
            json.dump({"one": "1", "two": "22", "three": ""}, filewriter)

        self.assertDictEqual(LocalEnvVars.json_file_to_dictionary(
            self.filename), {"one": "1", "two": "22", "three": ""})

    def test_with_invalid_json(self):
        with open(self.filename, 'w') as filewriter:
            filewriter.write('{"one":"1","two":"22", "three":""')

        self.assertRaises(
            Exception, lambda: LocalEnvVars.json_file_to_dictionary(self.filename))


class TestStaticMergeDictionaryWithKeys(unittest.TestCase):
    """
    Given a list of keys and a pre-populated dictionary, merge the keys and return a new dictionary, retaining existing values.
    """

    def test_new_key_added(self):
        keys = ["one", "two", "three"]
        key_vals = {"one": "1", "two": "22"}

        output = LocalEnvVars.merge_dictionary_with_keys(key_vals, *keys)

        self.assertDictEqual(output, {"one": "1", "two": "22", "three": ""})

    def test_key_removed(self):
        keys = ["one"]
        key_vals = {"one": "1", "two": "22"}

        output = LocalEnvVars.merge_dictionary_with_keys(key_vals, *keys)

        self.assertDictEqual(output, {"one": "1"})

    def test_new_key_added_and_then_removed(self):
        keys = ["one", "two", "three"]
        key_vals = {"one": "1", "two": "22"}

        output = LocalEnvVars.merge_dictionary_with_keys(key_vals, *keys)

        self.assertDictEqual(output, {"one": "1", "two": "22", "three": ""})

        keys2 = ["one", "three"]

        output = LocalEnvVars.merge_dictionary_with_keys(output, *keys2)

        self.assertDictEqual(output, {"one": "1", "three": ""})


if __name__ == "__main__":
    unittest.main()
