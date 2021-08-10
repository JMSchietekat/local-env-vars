import os.path
import json


class EnvironmentManager():

    def __init__(self, *argv):
        assert len(argv) > 0, "Supply at least 1 argument."

        self._filename = '.env'
        self._gitignore = ".gitignore"

        if(not EnvironmentManager.file_exists(self._gitignore)):
            with open(self._gitignore, "w") as filewriter:
                filewriter.write(self._filename)
        else:
            ignore_found = [False]
            with open(self._gitignore, "r") as filereader:
                ignore_found = [line for line in filereader.readlines(
                ) if line == self._filename + '\n']

            if(not ignore_found):
                with open(self._gitignore, "a") as filewriter:
                    filewriter.write(self._filename + '\n')

        if(not EnvironmentManager.file_exists(self._filename)):
            self.create_file(self._filename)
            EnvironmentManager.dictionary_to_json_file(
                self._filename, self.args_to_empty_dictionary(*argv))
            raise EnvironmentException(
                "New .env file created with keys. Add their values and try again.")

        self.dictionary = EnvironmentManager.json_file_to_dictionary(
            self._filename)

        if(not EnvironmentManager.dict_has_equal_keys(EnvironmentManager.args_to_empty_dictionary(*argv), self.dictionary)):
            self.dictionary = EnvironmentManager.merge_dictionary_with_keys(
                self.dictionary, *argv)
            EnvironmentManager.dictionary_to_json_file(
                self._filename, self.dictionary)
            raise EnvironmentException(
                "Environment keys differ. Keys will be added/removed. Add the values and try again.")

        if(not EnvironmentManager.dict_has_values(self.dictionary)):
            raise EnvironmentException(
                "Environment keys are set up. Some values are missing, please add them and try again.")

    @staticmethod
    def args_to_empty_dictionary(*argv):
        dictionary = {}
        for arg in argv:
            dictionary[arg] = ""

        return dictionary

    @staticmethod
    def create_file(filename):
        assert not os.path.exists(filename), "File already exists."

        filewriter = open(filename, "w+")
        filewriter.close()

    @staticmethod
    def dict_has_equal_keys(dict1={}, dict2={}):
        return set(dict1.keys()) == set(dict2.keys())

    @staticmethod
    def dict_has_values(dict1={}):
        assert len(dict1) > 0, "Dictionary must contain at least one value."

        for key, value in dict1.items():
            if (not value):
                return False

        return True

    @staticmethod
    def dictionary_to_json_file(filename, dictionary={}):
        with open(filename, 'w') as filewriter:
            json.dump(dictionary, filewriter)

    @staticmethod
    def file_exists(filename):
        return os.path.exists(filename)

    @staticmethod
    def json_file_to_dictionary(filename):
        dictionary = {}

        with open(filename, 'r') as filereader:
            dictionary = json.load(filereader)

        return dictionary

    @staticmethod
    def merge_dictionary_with_keys(dict1={}, *argv):
        dictionary = {}
        for arg in argv:
            if arg in dict1:
                dictionary[arg] = dict1[arg]
            else:
                dictionary[arg] = ""

        return dictionary


class EnvironmentException(Exception):
    """
    Exception raised for an environment setup issue.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
