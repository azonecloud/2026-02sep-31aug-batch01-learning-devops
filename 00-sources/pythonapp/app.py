from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Docker + Kubernetes! for V8.0.....Release by Kumarans , DevOps Engg...3Sep2026 for Batch2"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)