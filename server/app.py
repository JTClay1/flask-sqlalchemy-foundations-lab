# server/app.py
#!/usr/bin/env python3

# Core Flask imports
from flask import Flask, make_response

# Database migration support
from flask_migrate import Migrate

# Import database instance and model
from models import db, Earthquake


# -------------------------------------------------------
# Application Configuration
# -------------------------------------------------------

app = Flask(__name__)

# Configure SQLite database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Disable modification tracking (saves memory)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Disable compact JSON formatting (better readability in responses)
app.json.compact = False

# Initialize migration system and bind database to app
migrate = Migrate(app, db)
db.init_app(app)


# -------------------------------------------------------
# Root Route
# -------------------------------------------------------

@app.route('/')
def index():
    """
    Simple health-check endpoint.
    Confirms the API is running.
    """
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


# -------------------------------------------------------
# Route: Get Earthquake by ID
# -------------------------------------------------------

@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    """
    Retrieve a single earthquake record by its primary key ID.

    Returns:
        200 + earthquake JSON if found
        404 + error message JSON if not found
    """

    # Query database for earthquake with matching ID
    quake = Earthquake.query.filter_by(id=id).first()

    # If no record exists, return 404 error response
    if quake is None:
        return make_response({"message": f"Earthquake {id} not found."}, 404)

    # Return earthquake data in JSON format
    return make_response(
        {
            "id": quake.id,
            "magnitude": quake.magnitude,
            "location": quake.location,
            "year": quake.year
        },
        200
    )


# -------------------------------------------------------
# Route: Get Earthquakes by Minimum Magnitude
# -------------------------------------------------------

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    """
    Retrieve all earthquakes with magnitude >= provided value.

    Returns:
        200 + JSON containing:
            - count (number of matching records)
            - quakes (list of earthquake objects)
    """

    # Query database for earthquakes meeting magnitude threshold
    # Order by ID ascending to ensure predictable output order
    quakes = (
        Earthquake.query
        .filter(Earthquake.magnitude >= magnitude)
        .order_by(Earthquake.id.asc())
        .all()
    )

    # Convert SQLAlchemy objects into serializable dictionaries
    quakes_list = [
        {
            "id": q.id,
            "magnitude": q.magnitude,
            "location": q.location,
            "year": q.year
        }
        for q in quakes
    ]

    # Return count and list of matching earthquakes
    return make_response(
        {
            "count": len(quakes_list),
            "quakes": quakes_list
        },
        200
    )


# Run development server if executed directly
if __name__ == '__main__':
    app.run(port=5555, debug=True)
