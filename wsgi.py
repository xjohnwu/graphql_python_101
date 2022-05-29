import logging

from api import app
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify, redirect

from api.mutations import resolve_create_todo, resolve_mark_done, resolve_delete_todo, resolve_update_due_date
from api.queries import resolve_todos, resolve_todo

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(filename)s:%(funcName)s %(levelname)-7s %(message)s")

query = ObjectType("Query")

query.set_field("todos", resolve_todos)
query.set_field("todo", resolve_todo)

mutation = ObjectType("Mutation")
mutation.set_field("createTodo", resolve_create_todo)
mutation.set_field("markDone", resolve_mark_done)
mutation.set_field("deleteTodo", resolve_delete_todo)
mutation.set_field("updateDueDate", resolve_update_due_date)

type_defs = load_schema_from_path("api/schema")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


@app.route("/")
def index():
    return redirect('/graphql')


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    logging.info(data)

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    app.run(port=31111, debug=True)
