import graphene
from promise import Promise
from promise.dataloader import DataLoader


class User(graphene.ObjectType):
    name = graphene.String()
    age = graphene.Int()


users = {
    "1": "Han",
    "2": "Ran"
}


def get_user(id):
    return users[id]


class UserLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        return Promise.resolve([get_user(id=key) for key in keys])
