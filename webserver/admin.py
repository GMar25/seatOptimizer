from flask import Blueprint, render_template

admin_blueprint = Blueprint(
    "admin",
    __name__,
    static_folder="static",
    template_folder="static/templates",
)


@admin_blueprint.route("/")
def home():
    return render_template("admin_home.html")
