from flask import Flask

app = Flask(__name__)


@app.route("/health")
def health_check():
    return "OK", 200


if __name__ == "__main__":
    app.run(port=8000)
