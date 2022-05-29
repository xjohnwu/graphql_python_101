import os.path

from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers

from .mutations import mutation
from .queries import query

type_schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'schema'))
type_defs = load_schema_from_path("api/schema")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)
