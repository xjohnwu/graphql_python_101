import os.path

import uvicorn
from ariadne import make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers
from ariadne.asgi import GraphQL
from chat.mutations import mutation
from chat.queries import query
from chat.subscriptions import subscription

type_defs = load_schema_from_path(os.path.join(os.path.dirname(__file__), "chat/schema.graphql"))

schema = make_executable_schema(type_defs, query, mutation, subscription, snake_case_fallback_resolvers)
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
