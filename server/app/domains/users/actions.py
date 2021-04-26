
from server.app.domains.users.models import User
from server.Utils.constants import USER_TABLE
from uuid import uuid4
from server.app.domains.users.validate import UserValidator
from server.database.db_access import \
    get as get_db,\
    get_by_id as get_by_id_db,\
    update as update_db,\
    insert as insert_db,\
    delete as delete_db


def create(data: dict):
    UserValidator(create=True, json=data)
    user = User()
    user.id = str(uuid4())
    user.name = data.get('name')
    user.email = data.get('email')
    insert_db(USER_TABLE, user.serialize())
    return user


def get() -> list:
    user_line = get_db(USER_TABLE)[1:]
    users_list = []
    for line in user_line:
        user = line.strip().split(',')
        user_model = User()
        user_model.id = user[0]
        user_model.name = user[1]
        user_model.email = user[2]
        users_list.append(user_model)

    return users_list


def get_by_id(id) -> User:
    UserValidator(get=True, id=id)
    user = get_by_id_db(USER_TABLE, id)
    user_model = User()
    if user:
        user = user.strip().split(',')
        user_model.id = user[0]
        user_model.name = user[1]
        user_model.email = user[2]
        return user_model


def update(id, data) -> User:
    UserValidator(data)
    user = get_by_id(id)
    user.name = data.get('name') if data.get('name') else user.name
    user.email = data.get('email') if data.get('email') else user.email
    update_db(USER_TABLE, id, user.serialize())
    return user


def delete(id) -> User:
    UserValidator(id=id)
    user = get_by_id_db(USER_TABLE, id)
    delete_db(USER_TABLE, id)
    user_model = User()
    if user:
        user = user.strip().split(',')
        user_model.id = user[0]
        user_model.name = user[1]
        user_model.email = user[2]
        return user_model
