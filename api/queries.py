from ariadne import convert_kwargs_to_snake_case, ObjectType
from .models import Todo

query = ObjectType("Query")


@query.field('todos')
def resolve_todos(obj, info):
    """

    :param obj: obj is a value returned by a parent resolver, which in this case will be the root resolver
    :param info: info contains any context information that the GraphQL server provided the resolver during execution
    :return:
    """
    try:
        todos = [todo.to_dict() for todo in Todo.query.all()]
        payload = {
            "success": True,
            "todos": todos
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@query.field('todo')
@convert_kwargs_to_snake_case
def resolve_todo(obj, info, todo_id):
    todo = Todo.query.get(todo_id)
    if todo is not None:
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    else:
        payload = {
            "success": False,
            "errors": [f"Todo item matching id {todo_id} not found"]
        }

    return payload


@query.field('todoError')
@convert_kwargs_to_snake_case
def resolve_todo(obj, info, todo_id):
    raise Exception('Intended error')
