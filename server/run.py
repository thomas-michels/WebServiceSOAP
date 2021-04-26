from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from server.app.domains.users.actions import get as user_get,\
    get_by_id as user_get_id,\
    create as user_create,\
    update as user_update,\
    delete as user_delete

from server.app.domains.groups.actions import get as groups_get,\
    get_by_id as groups_get_id,\
    create as groups_create,\
    update as groups_update,\
    delete as groups_delete, \
    add_member


class User(ServiceBase):
    @rpc(_returns=Iterable(Unicode))
    def get_user(ctx):
        users_list = user_get()
        for user in users_list:
            yield u'users: %s' % user.serialize()

    @rpc(Unicode, _returns=Iterable(Unicode))
    def get_by_id_user(ctx, id):
        user = user_get_id(id)
        yield u'user: %s' % user.serialize()

    @rpc(Unicode, Unicode, _returns=Iterable(Unicode))
    def create_user(ctx, name, email):
        user = user_create({'name': name, 'email': email})
        yield u'user: %s' % user.serialize()

    @rpc(Unicode, Unicode, Unicode, _returns=Iterable(Unicode))
    def update_user(ctx, id, name=None, email=None):
        user = user_update(id, {'name': name, 'email': email})
        yield u'user: %s' % user.serialize()

    @rpc(Unicode, _returns=Iterable(Unicode))
    def delete_user(ctx, id):
        user = user_delete(id)
        yield u'user: %s' % user.serialize()


class Groups(ServiceBase):

    @rpc(_returns=Iterable(Unicode))
    def get_groups(ctx):
        groups_list = groups_get()
        for groups in groups_list:
            yield u'groups: %s' % groups.serialize_normal()

    @rpc(Unicode, _returns=Iterable(Unicode))
    def get_by_id_groups(ctx, id):
        groups = groups_get_id(id)
        yield u'groups: %s' % groups.serialize_normal()

    @rpc(Unicode, _returns=Iterable(Unicode))
    def create_groups(ctx, name):
        groups = groups_create({'name': name})
        yield u'groups: %s' % groups.serialize_normal()

    @rpc(Unicode, Unicode, _returns=Iterable(Unicode))
    def update_groups(ctx, id, name=None):
        groups = groups_update(id, {'name': name})
        yield u'groups: %s' % groups.serialize_normal()

    @rpc(Unicode, _returns=Iterable(Unicode))
    def delete_groups(ctx, id):
        groups = groups_delete(id)
        yield u'groups: %s' % groups.serialize_normal()

    @rpc(Unicode, Unicode, _returns=Iterable(Unicode))
    def add_member(ctx, id_group, id_user):
        groups = add_member(id_group, id_user)
        yield u'groups: %s' % groups.serialize_normal()


application = Application([User, Groups], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()
