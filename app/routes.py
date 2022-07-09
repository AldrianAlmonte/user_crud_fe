from urllib import response
from flask import (
    Flask,
    render_template
)
import requests

BACKEND_URL = "http://127.0.0.1:5000"

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/about")
def about():
    out = {
        "up": False
    }
    ping_url = "%s/%s" % (BACKEND_URL, "ping")
    up = requests.get(ping_url)
    if up.status_code == 200:
        out["up"] = True
        version_url = "%s/%s" % (BACKEND_URL, "version")
        version_response = requests.get(version_url)
        version_json = version_response.json()
        out["version"] = version_json.get("version")
    return render_template("about.html", content=out)


@app.get("/users")
def view_users():
    user_url = "%s/%s" % (BACKEND_URL, "users")
    response = requests.get(user_url)
    if response.status_code == 200:
        response_json = response.json()  # incoming data is a Python Dictionary
        user_list = response_json.get("users")
        return render_template("user_list.html", users=user_list)
    else:
        return render_template("error.html")


@app.get("users/new")
def create_user():
    return render_template("new_user.html")


@app.get("/users/create")
def create_user():
    create_url = "%s/%s" % (BACKEND_URL, "users")
    response = requests.post(create_url)
    if response.status_code == 204:
        return render_template("create.html")
    else:
        return render_template("error.html")


@app.get("/users/<int:pk>")
def delete_user(pk):
    delete_url = "%s/%s" % (BACKEND_URL, f"users/{pk}")
    response = requests.delete(delete_url)
    if response.status_code == 204:
        return render_template("delete.html", userID=pk)
    else:
        return render_template("error.html")


@app.get("/users/update/<int:pk>")
def update_user(pk):
    update_url = "%s/%s" % (BACKEND_URL, f"users/{pk}")
    response = requests.put(update_url)
    if response.status_code == 204:
        return render_template("update.html", userID=pk)
    else:
        return render_template("error.html")
