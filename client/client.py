from zeep import Client

client = Client('http://localhost:8000/?wsdl')

print(client.service.get_user())
print(client.service.get_by_id_user('e6009e95-e0a2-4b0d-978f-42f795234f56'))
print(client.service.create_user('grupo teste', 'asdad'))
print(client.service.update_user('e6009e95-e0a2-4b0d-978f-42f795234f56', 'asda'))
print(client.service.delete_user('e6009e95-e0a2-4b0d-978f-42f795234f56'))

print(client.service.get_groups())
print(client.service.get_by_id_groups('15557725-86d2-4347-bb84-55a9413f523d'))
print(client.service.create_groups('grupo teste'))
print(client.service.update_groups('59c5fb1f-5c5b-4304-ac88-37a2ff041a9c', 'asda'))
print(client.service.delete_groups('59c5fb1f-5c5b-4304-ac88-37a2ff041a9c'))
