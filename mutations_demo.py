import graphene


class Person(graphene.ObjectType):
    name = graphene.String()
    age = graphene.Int()


class PersonInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    age = graphene.Int(required=True)


class CreatePerson(graphene.Mutation):
    class Arguments:
        person_data = PersonInput(required=True)

    ok = graphene.Boolean()
    person = graphene.Field(lambda: Person)

    def mutate(root, info, person_data):
        person = Person(
            name=person_data.name,
            age=person_data.age
        )
        ok = True
        return CreatePerson(person=person, ok=ok)


class MyMutations(graphene.ObjectType):
    create_person = CreatePerson.Field()


# We must define a query for our schema
class Query(graphene.ObjectType):
    person = graphene.Field(Person)


if __name__ == '__main__':
    from flask import Flask
    from flask_graphql import GraphQLView

    app = Flask(__name__)

    schema = graphene.Schema(query=Query, mutation=MyMutations)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    ))
    app.run()
