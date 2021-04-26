
class Groups:
    id = 0
    name = ""
    members = []

    def serialize(self):
        return f'[{self.id},${self.name},${self.members}]'

    def serialize_normal(self):
        return f'[{self.id},{self.name},{self.members}]'
