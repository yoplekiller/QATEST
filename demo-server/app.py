from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to Kurly Clone QA!</h1>"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "Logged IN"
    return "<form method='post'><input name='user'><input type='submit'></form>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)