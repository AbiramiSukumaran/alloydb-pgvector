from main import hello_http

import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def entrypoint():
    return hello_http(request)


class GCFRequest:
    def __init__(self, data):
        self.data = data

    def get_json(self):
        return json.loads(json.dumps(self.data))


# Example usage
trialRunObject = GCFRequest(
    {
        "search": "A new Natural Language Processing related Machine Learning Model",
        "log_level": "NO_DEBUG",
    }
)

print("Route / ==> Load data via Langchain")

if __name__ == "__main__":
    app.run(debug=False)
