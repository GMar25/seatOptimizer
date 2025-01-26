from flask import Blueprint, render_template, request  # Add request here

user_blueprint = Blueprint(
    "user",
    __name__,
    static_folder="static",
    template_folder="static/templates",
)

# Routes for the sequence
@user_blueprint.route("/")
def home():
    return render_template("user_home.html")

@user_blueprint.route("/flight-details")
def flight_details():
    return render_template("flight_details.html")

@user_blueprint.route("/trip-summary")
def trip_summary():
    return render_template("trip_summary.html")

@user_blueprint.route("/passenger-detail")
def passenger_detail():
    num_passengers = int(request.args.get("numPassengers", 1))  # Now request is defined
    return render_template("passenger_detail.html", num_passengers=num_passengers)

@user_blueprint.route("/seat-details")
def seat_details():
    return render_template("seat_details.html")
