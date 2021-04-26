from typing import Dict, List, Any

from server.Utils.constants import USER_TABLE
from server.app.domains.validations import Validator


class UserValidator(Validator):
    """
    JSON data validator customized to the User model.
    """

    def __init__(self, json: Dict or None = None, create: bool = False, get = False, **kwargs):
        super().__init__()

        if get:
            if kwargs.get('id'):
                self._check_the_id_in_database(USER_TABLE, kwargs.get('id'))
        if create:
            allowed_column: List[str] = ['name', 'email']
            self._check_for_null_fields(json, allowed_column)
        if json:
            if json.get('email'):
                self._check_the_email(json.get('email'))
            if json.get('name'):
                self._check_the_name(json.get('name'))

            self._shows_all_invalid_data_messages()

    def _check_the_email(self, value: Any) -> None:
        self._value_is_string(value)
        self._contains_special_characters(argument=str(value), symbols_released=r'@._')
        if self.errors:
            self.all_error_messages = f"Email column contains errors: {self.__str__()}"
        self.errors.clear()

    def _check_the_name(self, value: Any) -> None:
        self._value_is_string(value)
        if self.errors:
            self.all_error_messages = f"Name column contains errors: {self.__str__()}"
        self.errors.clear()
