from flask import Blueprint, render_template
import genetic

admin_blueprint = Blueprint(
    "admin",
    __name__,
    static_folder="static",
    template_folder="static/templates",
)


@admin_blueprint.route("/")
def home():
    return render_template("admin_home.html")

def formater():
    vals = []

    original = genetic.output()
    for elem in original.arr:
        vals.append(elem.score)

    return vals

@admin_blueprint.route("/")
def seat_selection():
    seat_data = formater()  # Get seat status data
    return render_template("seat_details.html", seat_data=seat_data)  # Render the correct template