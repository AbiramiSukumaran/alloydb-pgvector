from main import hello_http

import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def entrypoint():
    return hello_http(request)


print("Route / ==> Load data via Langchain")

if __name__ == "__main__":
    app.run(debug=False)
