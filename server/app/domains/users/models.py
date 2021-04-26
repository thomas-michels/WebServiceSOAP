
class User:
    id = 0
    name = ""
    email = ""

    def serialize(self):
        return f'{self.id},${self.name},${self.email}'

    def serialize_normal(self):
        return f'{self.id},{self.name},{self.email}'
