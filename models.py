from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# Venue model
class Venue(db.Model):
    __tablename__ = 'Venue'
    # I complete missing fields as in placeholder data
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String, nullable=False)
    city: str = db.Column(db.String(120), nullable=False)
    state: str = db.Column(db.String(120), nullable=False)
    phone: str = db.Column(db.String(120), nullable=True)
    image_link: str = db.Column(db.String(500), nullable=True)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    address: str = db.Column(db.String(120), nullable=False)
    website: str = db.Column(db.String(120), nullable=True)
    facebook_link: str = db.Column(db.String(120), nullable=True)
    seeking_talent: bool = db.Column(db.Boolean, nullable=False)
    seeking_description: str = db.Column(db.String(500), nullable=True)

# Artist Model
class Artist(db.Model):
    __tablename__ = 'Artist'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String, nullable=False)
    city: str = db.Column(db.String(120), nullable=False)
    state: str = db.Column(db.String(120), nullable=False)
    phone: str = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    address: str = db.Column(db.String(120), nullable=False)
    image_link: str = db.Column(db.String(500), nullable=True)
    facebook_link: str = db.Column(db.String(120), nullable=True)
    website: str = db.Column(db.String(120), nullable=True)
    seeking_venue: bool = db.Column(db.Boolean, nullable=False)
    seeking_description: str = db.Column(db.String(500), nullable=True)

# I create Show Model
class Show(db.Model):
    __tablename__ = 'Show'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time: datetime = db.Column(db.DateTime)

    # I create ForeignKey for to link between tables
    # foreign key constraint, referring to the primary key of the Artist tabel
    artist_key: int = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    # foreign key constraint, referring to the primary key of the Venu tabel
    venue_key: int = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)

    # Join the Relationships with backref and using the relationship.cascade option
    # configure a mapped relationship between show model and artist model.
    artist = db.relationship('Artist', backref=db.backref('shows', cascade='all, delete'))
    # configure a mapped relationship between show model and venu model.
    venue = db.relationship('Venue', backref=db.backref('shows', cascade='all, delete'))

