# learn_graphene

https://github.com/graphql-python/graphene

1. Use example on the above Github page:
2. Try Flask-GraphQL integration: https://github.com/graphql-python/flask-graphql
3. Go through query examples https://docs.graphene-python.org/en/latest/quickstart/
    1. setup flask runner for starwars example
    2. play with custom ObjectType, Enums, Interfaces on GraphQL viewer
    3. Mutations:
4. Adiadne: Schema-first GraphQL

### Examples

* https://analytics.iotexscan.io/
* Deploy Flask project to production: https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/
* Chat App: https://nordicapis.com/create-a-chat-app-api-using-python-and-graphql/

## Error Handling

The query below has a missing argument "todoId":
```graphql
query {
    todo {
        success
        errors
        todo {
            id
            description
            completed
            dueDate
        }
    }
}
```
Since it is a bad request, the error thrown in production and debug mode is as follows:
```json
{
  "error": {
    "errors": [
      {
        "locations": [
          {
            "column": 3,
            "line": 13
          }
        ],
        "message": "Field 'todo' argument 'todoId' of type 'ID!' is required, but it was not provided.",
        "path": null
      }
    ]
  }
}
```
The query below is an intended query to throw an exception:
```graphql
query {
    todoError(todoId: 1) {
        success
        errors
        todo {
            id
            description
            completed
            dueDate
        }
    }
}
```
The error thrown in debug mode is as follows:
```json
{
  "data": null,
  "errors": [
    {
      "extensions": {
        "exception": {
          "context": {
            "info": "GraphQLResolv...7feb480e8820>)",
            "obj": "None",
            "todo_id": "'1'"
          },
          "stacktrace": [
            "Traceback (most recent call last):",
            "  File \"/Users/wuhan/Documents/GitHub/graphql/graphql_server_python_101/venv/lib/python3.9/site-packages/graphql/execution/execute.py\", line 617, in resolve_field",
            "    result = resolve_fn(source, info, **args)",
            "  File \"/Users/wuhan/Documents/GitHub/graphql/graphql_server_python_101/venv/lib/python3.9/site-packages/ariadne/utils.py\", line 75, in wrapper",
            "    return func(*args, **convert_to_snake_case(kwargs))",
            "  File \"/Users/wuhan/Documents/GitHub/graphql/graphql_server_python_101/api/queries.py\", line 50, in resolve_todo",
            "    raise Exception('Intended error')",
            "Exception: Intended error"
          ]
        }
      },
      "locations": [
        {
          "column": 3,
          "line": 2
        }
      ],
      "message": "Intended error",
      "path": [
        "todoError"
      ]
    }
  ]
}
```
The error thrown in production mode is as follows. Compared to the one in debug mode, "extensions" field is missing:
```json
{
  "data": null,
  "errors": [
    {
      "locations": [
        {
          "column": 3,
          "line": 2
        }
      ],
      "message": "Intended error",
      "path": [
        "todoError"
      ]
    }
  ]
}
```