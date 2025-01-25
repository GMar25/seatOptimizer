from flask import Blueprint, render_template

user_blueprint = Blueprint(
    "user",
    __name__,
    static_folder="static",
    template_folder="static/templates",
)


@user_blueprint.route("/")
def home():
    return render_template("user_home.html")
