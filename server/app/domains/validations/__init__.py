from datetime import date

from server.app.exceptions import UnprocessableException, NotFoundException
from server.database.db_access import get_by_id
from typing import Dict, List, final, Any
import string


class Validator:

    _errors: List[str] = list()

    def __init__(self):
        self._all_error_messages: List[str] = list()

        self.errors = list()

        self._punctuations: final = list(string.punctuation)
        self._uppercase: final = list(string.ascii_uppercase)
        self._lowercase: final = list(string.ascii_lowercase)
        self._letters: final = list(string.ascii_letters)
        self._numbers: final = list(string.digits)
        self._seat: final = r""" àèìòùáéíóúýâêîôûãõäëïöüÿçÀÈÌÒÙÁÉÍÓÚÝÂÊÎÔÛÃÕÄËÏÖÜŸÇ"""

    @property
    def errors(self) -> List[str]:
        return self._errors

    @errors.setter
    def errors(self, value: List) -> None:
        if not isinstance(value, list):
            self._errors = list()
        else:
            self._errors = value

    @property
    def all_error_messages(self) -> List[str]:
        return self._all_error_messages

    @all_error_messages.setter
    def all_error_messages(self, error_message: List or str) -> None:
        """
        Add or clear error messages to the private list '_all_error_messages'.
        """
        if isinstance(error_message, list):
            self._all_error_messages.clear()
        if isinstance(error_message, str):
            self._all_error_messages.append(error_message)

    def _shows_all_invalid_data_messages(self) -> None:
        """
        Checks if there are messages, if any,
        returns an unprocessable exception with all messages.
        """
        if self.all_error_messages:
            raise UnprocessableException(self.all_error_messages)

    def _check_for_null_fields(self, data: Dict, allowed_column: List = []) -> None:
        """
        Method that checks for null values
        in the dictionary and whether they can contain nulls,
        returns an 'unprocessable exception' with all null and disallowed columns.
        """
        for column in data:
            if data.get(column) is None or column not in allowed_column:
                self.errors.append(f"{column} column contains error: null field found!")
        if self.errors:
            raise UnprocessableException(self._errors)

    @staticmethod
    def _check_the_id_in_database(table, id: str) -> None:
        """
        Method that takes an identification string and
        checks whether it exists in the database as real data,
        returns an error message if it is invalid.
        """
        if not get_by_id(table, id):
            new_msg = f"ID column not found in database."
            raise NotFoundException(msg=new_msg)

    def _contains_uppercase_letters(self, argument: str) -> bool:
        """
        Method that receives a string and
        verify that it does not contain uppercase letters,
        returns a boolean and an error message if it is invalid.
        """
        has: bool = False
        try:
            for character in argument:
                if character in self._uppercase:
                    self.errors.append(f"contains uppercase letters. Found: {character}")
                    has = True
                    break
        finally:
            return has

    def _contains_lowercase_letters(self, argument: str) -> bool:
        """
        Method that receives a string and
        verify that it does not contain lowercase letters,
        returns a boolean and an error message if it is invalid.
        """
        has: bool = False
        try:
            for character in argument:
                if character in self._lowercase:
                    self.errors.append(f"contains lowercase letters. Found: {character}")
                    has = True
                    break
        finally:
            return has

    def _contains_letters(self, argument: str) -> bool:
        """
        Method that receives a string and
        verify that it does not contain letters,
        returns a boolean and an error message if it is invalid.
        """
        has: bool = False
        try:
            for character in argument:
                if character in self._letters:
                    self.errors.append(f"contains letters. Found: {character}")
                    has = True
                    break
        finally:
            return has

    def _contains_numbers(self, argument: str) -> bool:
        """
        Method that receives a string and
        verify that it does not contain numbers,
        returns a boolean and an error message if it is invalid.
        """
        has: bool = False
        try:
            for character in argument:
                if character in self._numbers:
                    self.errors.append(f"contains numbers. Found: {character}")
                    has = True
                    break
        finally:
            return has

    def _contains_special_characters(self, argument: str, symbols_released: str = '') -> bool:
        """
        Method that takes a string and
        checks that it does not contain special characters,
        returns a boolean and an error message if it is invalid.
        """
        has: bool = False
        try:
            for character in argument:
                if character not in self._letters \
                        and character not in self._numbers \
                        and character not in symbols_released:
                    self.errors.append(f"contains special characters. Found: {character}")
                    has = True
                    break
        finally:
            return has

    def _date_is_valid(self, value: str) -> bool:
        """
        Method that receives the value str e
        checks if the year, month and day are valid values,
        creates an error message if it is invalid
        returns index error if not in the American standard and returns a boolean.
        """
        maximum_year = date.today().year
        minimum_year = maximum_year - 150
        try:
            date_list = value.split('-')
            year = date_list[0]
            month = date_list[1]
            day = date_list[2]
            if minimum_year > int(year) or int(year) > maximum_year:
                self.errors.append(f"contains a year outside the "
                                   f"{minimum_year} to {maximum_year} range")
                return False
            if 1 > int(month) or int(month) > 12:
                self.errors.append(f"contains a month outside the 1 to 12 range")
                return False
            if 1 > int(day) or int(day) > 31:
                self.errors.append(f"contains a day outside the 1 to 31 range")
                return False
        except IndexError:
            raise UnprocessableException(f'date format is not on US keyboard or invalid')
        return True

    def _value_is_string(self, value: Any) -> bool:
        """
        Method that receives any value and
        check if it is of type string,
        creates an error message if it is invalid and returns a boolean.
        """
        if not isinstance(value, str):
            self.errors.append("must be of string type")
            return False
        return True

    def _type_is_valid(self, argument: str) -> bool:
        """
        Method that receive a string and
        verify if is either 'residential' or 'commercial'
        returns a boolean and and error message if the argument is invalid
        """
        result: bool = True
        try:
            if argument != "residential" and argument != 'commercial':
                self.errors.append(f"wrong syntax! Expected: 'residential' or 'commercial'. Actual: {argument}")
                result = False
        finally:
            return result
