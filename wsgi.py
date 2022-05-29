import logging

from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify, redirect

from api import app, schema

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(filename)s:%(funcName)s %(levelname)-7s %(message)s")


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
