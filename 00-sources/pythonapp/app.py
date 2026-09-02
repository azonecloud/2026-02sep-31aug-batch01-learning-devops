from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Docker + Kubernetes! for V5.0.....Release by Kumarans , DevOps Engg...2Sep2026"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)