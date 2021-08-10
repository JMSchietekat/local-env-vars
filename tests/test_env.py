import unittest
import os
import json

from src.local_env_vars.env import EnvironmentManager, EnvironmentException

class TestStaticArgsToEmptyDictionary(unittest.TestCase):
    """
    Should create a dictionary with empty values and keys equal to the list provided.
    """

    def test_input_args_and_compare_with_expected_dictionary(self):

        dictionary = EnvironmentManager.args_to_empty_dictionary(
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
            print("File did't exist, safe to continue.")

    def tearDown(self):
        os.remove(self.filename)

    def test_create_file_when_it_already_existed(self):
        EnvironmentManager.create_file(self.filename)
        self.assertRaises(
            AssertionError, lambda: EnvironmentManager.create_file(self.filename))


class TestStaticDictHasEqualKeys(unittest.TestCase):
    """
    Should compare the keys (not their values) of two dictionaries and report equality.
    """

    def test_dictionaries_with_non_equal_keys_to_be_false(self):
        dict1 = {"args": "", "to": "", "test": ""}
        dict2 = {"args": "value1", "to": "value2", "tes": "value3"}

        self.assertFalse(EnvironmentManager.dict_has_equal_keys(dict1, dict2))

    def test_dictionaries_with_a_subset_of_equal_keys_to_be_false(self):
        dict1 = {"args": "", "to": "", "test": ""}
        dict2 = {"args": "value1", "to": "value2",
                 "test": "value3", "with": ""}

        self.assertFalse(EnvironmentManager.dict_has_equal_keys(dict1, dict2))

    def test_dictionaries_with_equal_keys_to_be_true(self):
        dict1 = {"args": "", "to": "", "test": ""}
        dict2 = {"args": "value1", "to": "value2", "test": "value3"}

        self.assertTrue(EnvironmentManager.dict_has_equal_keys(dict1, dict2))

    def test_dictionaries_with_equal_keys_in_different_order_to_be_true(self):
        dict1 = {"args": "", "to": "", "test": ""}
        dict2 = {"to": "value2", "args": "value1", "test": "value3"}

        self.assertTrue(EnvironmentManager.dict_has_equal_keys(dict1, dict2))

    def test_empty_dictionary(self):
        dict1 = {}
        dict2 = {}

        self.assertTrue(EnvironmentManager.dict_has_equal_keys(dict1, dict2))


class TestStaticDictHasValues(unittest.TestCase):
    """
    Check that a dictionary has no empty values.
    """

    def test_with_values_to_be_true(self):
        dictionary = {"args": "1", "to": "2", "test": "3"}
        self.assertTrue(EnvironmentManager.dict_has_values(dictionary))

    def test_with_omitted_values_to_be_false(self):
        dictionary = {"args": "1", "to": "2", "test": ""}
        self.assertFalse(EnvironmentManager.dict_has_values(dictionary))

    def test_with_zero_items_should_throw_error(self):
        dictionary = {}
        self.assertRaises(
            AssertionError, lambda: EnvironmentManager.dict_has_values(dictionary))


class TestStaticDictionaryToJsonFile(unittest.TestCase):
    """
    Write dictionary to file in json format.
    """

    def test_provided_dictionary_is_writen_to_file(self):
        dictionary = {"args": "", "to": "", "test": ""}
        filename = ".env"
        readline = ""

        EnvironmentManager.dictionary_to_json_file(filename, dictionary)

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

        self.assertTrue(EnvironmentManager.file_exists(self.filename))

        os.remove(self.filename)

    def test_when_file_does_not_exists(self):
        self.assertFalse(EnvironmentManager.file_exists(self.filename))


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

        self.assertDictEqual(EnvironmentManager.json_file_to_dictionary(
            self.filename), {"one": "1", "two": "22", "three": ""})

    def test_with_invalid_json(self):
        with open(self.filename, 'w') as filewriter:
            filewriter.write('{"one":"1","two":"22", "three":""')

        self.assertRaises(
            Exception, lambda: EnvironmentManager.json_file_to_dictionary(self.filename))


class TestStaticMergeDictionaryWithKeys(unittest.TestCase):
    """
    Given a list of keys and a pre-populated dictionary, merge the keys and return a new dictionary, retaining existing values.
    """

    def test_new_key_added(self):
        keys = ["one", "two", "three"]
        key_vals = {"one": "1", "two": "22"}

        output = EnvironmentManager.merge_dictionary_with_keys(key_vals, *keys)

        self.assertDictEqual(output, {"one": "1", "two": "22", "three": ""})

    def test_key_removed(self):
        keys = ["one"]
        key_vals = {"one": "1", "two": "22"}

        output = EnvironmentManager.merge_dictionary_with_keys(key_vals, *keys)

        self.assertDictEqual(output, {"one": "1"})

    def test_new_key_added_and_then_removed(self):
        keys = ["one", "two", "three"]
        key_vals = {"one": "1", "two": "22"}

        output = EnvironmentManager.merge_dictionary_with_keys(key_vals, *keys)

        self.assertDictEqual(output, {"one": "1", "two": "22", "three": ""})

        keys2 = ["one", "three"]

        output = EnvironmentManager.merge_dictionary_with_keys(output, *keys2)

        self.assertDictEqual(output, {"one": "1", "three": ""})


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
        os.remove(self.envManager._filename)

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
            ".env", {"sql_username": "un", "sql_password": "pwd"})

        self.assertRaises(EnvironmentException, lambda: EnvironmentManager(
            "sql_username", "sql_password", "sql_address"))

    def tearDown(self):
        os.remove(".env")

    def test_env_file_contains_added_key(self):
        readline = ""
        with open(".env", "r") as filereader:
            readline = filereader.read()

        self.assertEqual(
            readline, '{"sql_username": "un", "sql_password": "pwd", "sql_address": ""}')


class TestClassWithRemovedKeysOnInit(unittest.TestCase):
    """
    Initialise class with less keys than in .env file.
    """

    def setUp(self):
        EnvironmentManager.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})

        self.assertRaises(EnvironmentException,
                          lambda: EnvironmentManager("sql_username"))

    def tearDown(self):
        os.remove(".env")

    def test_env_file_contains_does_not_contain_removed_key(self):
        readline = ""
        with open(".env", "r") as filereader:
            readline = filereader.read()

        self.assertEqual(readline, '{"sql_username": "un"}')


class TestClassWithNoInputArgs(unittest.TestCase):
    """
    Initialise class with no input arguments
    """

    def test_empty_initialisation_to_throw_assertion_error(self):
        self.assertRaises(AssertionError, lambda: EnvironmentManager())


class TestClassToAddIgnore(unittest.TestCase):
    """
    Initialise class with working setup. Ensure .gitignore file is created if it does not exists.
    """

    def setUp(self):
        self._gitignore = ".gitignore"
        try:
            os.remove(self._gitignore)
        except Exception:
            pass

    def tearDown(self):
        os.remove(".env")
        os.remove(self._gitignore)

    def test_create_ignore_if_it_does_not_exists_and_ignore_env_file(self):
        EnvironmentManager.dictionary_to_json_file(
            ".env", {"sql_username": "un", "sql_password": "pwd"})
        self.envManager = EnvironmentManager("sql_username", "sql_password")

        self.assertTrue(os.path.exists(self._gitignore))


if __name__ == "__main__":
    unittest.main()
