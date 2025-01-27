from flask import Blueprint, render_template, request, jsonify  # Add request here
from .genetic import initialize, get_next_generation

plane, curr_gen, change, prev = initialize()
score = -1

def formater():
    if curr_gen == None:
        return []

    global change
    global prev
    global score
    vals = []

    r_sum = 0
    r_max = -1
    r_genome = None
    for genome in curr_gen:
        if (r_max < genome.score):
            r_max = genome.score
            r_genome = genome
        r_sum += genome.score
    score = round(r_max, 2)

    r_sum /= len(curr_gen)
    if change == -1:
        change = 1
    else:
        change = abs(prev - r_sum)

    prev = r_sum

    for i in range(len(r_genome.arr)):
        if (i % plane.cols == 0):
            vals.append([])

        elem = r_genome.arr[i]
        if elem == None :
            vals[-1].append(-2)
            
        elif not elem.is_movable():
            vals[-1].append(-1)

        else:
            vals[-1].append(elem.score)

    return vals

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
    seat_data = formater()  # Get seat status data
    return render_template("seat_details.html", seat_data=seat_data, score=score)  # Render the correct template

@user_blueprint.route('/get_seat_data')
def get_seat_data():
    global curr_gen, change, prev
    curr_gen = get_next_generation(plane, curr_gen, change) 
    return jsonify((formater(), score))