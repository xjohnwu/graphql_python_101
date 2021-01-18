import datetime

from graphene import ObjectType, String, Schema, Date, DateTime, Time, Field


class Person(ObjectType):
    first_name = String()
    last_name = String()
    full_name = String()

    def resolve_full_name(parent, info):
        return f"{parent.first_name} {parent.last_name}"


def get_human(name):
    parts = name.split(' ')
    return Person(first_name=parts[0], last_name=parts[1])


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    test = String()
    goodbye = String()
    one_week_from = Date(required=True, date_input=Date(required=True))
    one_hour_from = DateTime(required=True, datetime_input=DateTime(required=True))
    one_minute_from = Time(required=True, time_input=Time(required=True))

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_test(root, info):
        return 'Testing...'

    def resolve_goodbye(root, info):
        return 'See ya!'

    def resolve_one_week_from(root, info, date_input):
        """
{ oneWeekFrom(dateInput:"2020-10-10") }
        :param info:
        :param date_input:
        :return:
        """
        assert type(date_input) == datetime.date
        return date_input + datetime.timedelta(weeks=1)

    def resolve_one_hour_from(root, info, datetime_input):
        """
{ oneHourFrom(datetimeInput:"2006-01-02T15:04:05") }
        :param info:
        :param datetime_input:
        :return:
        """
        assert type(datetime_input) == datetime.datetime
        return datetime_input + datetime.timedelta(hours=1)

    def resolve_one_minute_from(root, info, time_input):
        """
{ oneHourFrom(timeInput: "15:04:05") }
        :param info:
        :param time_input:
        :return:
        """
        assert type(time_input) == datetime.time
        tmp_time_input = datetime.datetime.combine(datetime.date(1, 1, 1), time_input)
        return (tmp_time_input + datetime.timedelta(minutes=1)).time()

    me = Field(Person)

    def resolve_me(parent, info):
        # returns an object that represents a Person
        return get_human(name="Luke Skywalker")


if __name__ == '__main__':
    from flask import Flask
    from flask_graphql import GraphQLView

    app = Flask(__name__)

    schema = Schema(query=Query)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    ))
    app.run()
