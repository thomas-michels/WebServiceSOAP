
from server.app.domains.groups.models import Groups
from server.Utils.constants import GROUP_TABLE
from uuid import uuid4
from server.app.domains.groups.validate import GroupsValidator
from server.app.domains.users.actions import get_by_id as get_id_user
from server.database.db_access import \
    get as get_db,\
    get_by_id as get_by_id_db,\
    update as update_db,\
    insert as insert_db,\
    delete as delete_db


def create(data: dict):
    GroupsValidator(create=True, json=data)
    group = Groups()
    group.id = str(uuid4())
    group.name = data.get('name')
    insert_db(GROUP_TABLE, group.serialize())
    return group


def get() -> list:
    group_line = get_db(GROUP_TABLE)[1:]
    groups_list = []
    for line in group_line:
        group = line.strip().split(',$')
        group_model = Groups()
        group_model.id = group[0]
        group_model.name = group[1]
        for line in group[2:]:
            group_model.members.append(line)
        groups_list.append(group_model)

    return groups_list


def get_by_id(id) -> Groups:
    GroupsValidator(get=True, id=id)
    group = get_by_id_db(GROUP_TABLE, id)
    group_model = Groups()
    if group:
        group = group.strip().split(',$')
        group_model.id = group[0]
        group_model.name = group[1]
        group_model.members = group[2:]
        return group_model


def update(id, data) -> Groups:
    GroupsValidator(data)
    group = get_by_id(id)
    group.name = data.get('name') if data.get('name') else group.name
    update_db(GROUP_TABLE, id, group.serialize())
    return group


def delete(id) -> Groups:
    GroupsValidator(id=id)
    group = get_by_id_db(GROUP_TABLE, id)
    delete_db(GROUP_TABLE, id)
    group_model = Groups()
    if group:
        group = group.strip().split(',$')
        group_model.id = group[0]
        group_model.name = group[1]
        group_model.members = group[2:]
        return group_model


def add_member(id_group, id_user):
    group = get_by_id(id_group)
    group.members.append(get_id_user(id_user))
    return group
