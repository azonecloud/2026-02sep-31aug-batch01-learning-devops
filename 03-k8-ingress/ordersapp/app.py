from flask import Flask

app = Flask(__name__)

@app.route("/orders")
def home():
    return "Hello from Orders App!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)