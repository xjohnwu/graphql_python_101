from datetime import datetime

from ariadne import convert_kwargs_to_snake_case, ObjectType

from .app import db
from .models import Todo

mutation = ObjectType("Mutation")


@mutation.field('createTodo')
@convert_kwargs_to_snake_case
def resolve_create_todo(obj, info, description, due_date):
    try:
        due_date = datetime.strptime(due_date, '%d-%m-%Y').date()
        todo = Todo(
            description=description, due_date=due_date
        )
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }

    return payload


@mutation.field('markDone')
@convert_kwargs_to_snake_case
def resolve_mark_done(obj, info, todo_id):
    try:
        todo = Todo.query.get(todo_id)
        todo.completed = True
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} was not found"]
        }

    return payload


@mutation.field('deleteTodo')
@convert_kwargs_to_snake_case
def resolve_delete_todo(obj, info, todo_id):
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        payload = {"success": True}

    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} not found"]
        }

    return payload


@mutation.field('updateDueDate')
@convert_kwargs_to_snake_case
def resolve_update_due_date(obj, info, todo_id, new_date):
    try:
        todo = Todo.query.get(todo_id)
        if todo:
            todo.due_date = datetime.strptime(new_date, '%d-%m-%Y').date()
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": ["Incorrect date format provided. Date should be in "
                       "the format dd-mm-yyyy"]
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} not found"]
        }
    return payload
