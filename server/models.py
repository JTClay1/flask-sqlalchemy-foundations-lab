# server/models.py

# SQLAlchemy ORM import
from flask_sqlalchemy import SQLAlchemy

# Optional metadata object (can be used for advanced configurations)
from sqlalchemy import MetaData


# Create metadata object
metadata = MetaData()

# Initialize SQLAlchemy instance with metadata
db = SQLAlchemy(metadata=metadata)


# -------------------------------------------------------
# Earthquake Model
# -------------------------------------------------------

class Earthquake(db.Model):
    """
    Represents a single earthquake record in the database.

    Columns:
        id         - Primary key
        magnitude  - Earthquake magnitude (float)
        location   - Location description (string)
        year       - Year event occurred (integer)
    """

    # Explicit table name
    __tablename__ = "earthquakes"

    # Primary key column
    id = db.Column(db.Integer, primary_key=True)

    # Earthquake magnitude
    magnitude = db.Column(db.Float)

    # Geographic location of event
    location = db.Column(db.String)

    # Year the earthquake occurred
    year = db.Column(db.Integer)

    def __repr__(self):
        """
        Developer-friendly string representation.
        Useful in Flask shell and debugging.
        """
        return f"<Earthquake {self.id}, {self.magnitude}, {self.location}, {self.year}>"
