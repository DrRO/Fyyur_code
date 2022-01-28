# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
from logging import Formatter, FileHandler

import babel
import babel.dates
import dateutil.parser
# group methods from the same module
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct
# added
from models import (db, Venue, Artist, Show)
from forms import ShowForm, VenueForm, ArtistForm
from datetime import datetime
from flask_wtf import Form
from flask_wtf.csrf import CSRFProtect

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
# I install flask-migrate
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db.init_app(app)
Migrate(app, db)

# Done TODO: connect to a local postgresql database
# I config project with my postgres Database
# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
# As reviwer suggestion, I create a models.py and copy all your models to that file then use an import statement


#  Done TODO: implement any missing fields, as a database migration using Flask-Migrate


# Done TODO: implement any missing fields, as a database migration using Flask-Migrate

# Done TODO: implement any missing fields, as a database migration using Flask-Migrate

# Done TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
        #  I add locale='en' to work with windows
        return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # Done TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    places = Venue.query.distinct(Venue.city, Venue.state).all()
    locals = []
    venues = Venue.query.all()

    for place in places:
        locals.append({
        'city': place.city,
        'state': place.state,
        'venues': [{
            'id': venue.id,
            'name': venue.name,
        } for venue in venues if
            venue.city == place.city and venue.state == place.state]
    })
    return render_template('pages/venues.html', areas=locals)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # Done TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term', '')
    # Find all name matches
    venues = Venue.query.filter(Venue.name.ilike("%" + search_term + "%")).all()

    response = {
        "count": len(venues),
        "data": []
    }

    for venue in venues:
        response["data"].append({
            'id': venue.id,
            'name': venue.name,
        })

    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=search_term
    )



@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # Done TODO: replace with real venue data from the venues table, using venue_id

    venue = Venue.query.filter_by(id=venue_id).first_or_404()

    past_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
        Show.venue_key == venue_id,
        Show.artist_key == Artist.id,
        Show.start_time < datetime.now()
    ).all()
    upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
        Show.venue_key == venue_id,
        Show.artist_key == Artist.id,
        Show.start_time > datetime.now()
    ).all()

    data = {
        'id': venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": [{
            'artist_id': artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in past_shows],
        "upcoming_shows": [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in upcoming_shows],

        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # Done TODO: insert form data as a new Venue record in the db, instead

    form = VenueForm(request.form)
    error = False
    try:

        #  insertion  of data as a new venu
        # Done TODO: modify data to be the data object returned from db insertion

        new_venue_data = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            facebook_link=form.facebook_link.data,
            genres=form.genres.data,
            image_link=form.image_link.data,
            website=form.website.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data)

        db.session.add(new_venue_data)
        db.session.commit()
    except:
        error = True
        db.session.rollback()

        # Done TODO: on unsuccessful db insert, flash an error instead.
    finally:
        db.session.close()
        if error:
            from numpy.random.tests import data
            flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
        else:
            # on successful db insert, flash success
            flash('Venue ' + form.name.data + ' was successfully listed!')

    return render_template("pages/home.html")


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # Done TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        # get venue id then delete it then update db
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()

    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # Done TODO: replace with real data returned from querying the database
    # I get id and name of artist and put it in array
    artist_info = []
    artists_query = db.session.query(Artist).all()
    for artist in artists_query:
        artist_info.append(
            {"id": artist.id, "name": artist.name}
        )
    # data = [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    # }, {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    # }, {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    # }]
    return render_template('pages/artists.html', artists=artists_query)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # Done TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_result = request.form.get('search_term', '')
    search_form = request.form['search_term']
    # Find all name matches
    search_artist = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_form))).all()
    response = {
        "count": len(search_artist),
        "data": []
    }
    for artist in search_artist:
        response["data"].append({
            "id": artist.id,
            "name": artist.name,
            # "num_upcoming_shows": artist.upcoming_shows_count
        })

    return render_template('pages/search_artists.html', results=response,
                           search_term=search_result)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # Done TODO: replace with real venue data from the venues table, using venue_id
    artist = Venue.query.filter_by(id=artist_id).first_or_404()

    past_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
        Show.venue_key == Venue.id,
        Show.artist_key == artist_id,
        Show.start_time < datetime.now()
    ).all()
    upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
        Show.venue_key == Venue.id,
        Show.artist_key == artist_id,
        Show.start_time > datetime.now()
    ).all()


    data = {
        'id': artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "address": artist.address,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_talent": artist.seeking_talent,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": [{
            'venu_id': venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for venue, show in past_shows],
        "upcoming_shows": [{
            'venu_id': venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for venue, show in upcoming_shows],

        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }

    return render_template("pages/show_artist.html", artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist_json = {}
    artist = Artist.query.filter(Artist.id == artist_id).all()
    artist_json = {
        "id": artist.id,
        "name": artist.name,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "genres": ','.join(artist.genres),
        "image_link": artist.image_link,
        "facebook_link": artist.facebook_link,
        "website": artist.website,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description

    }

    form = ArtistForm(data=artist_json)
    return render_template('forms/edit_artist.html', form=form, artist=artist_json)
    # Done  TODO: populate form with fields from artist with ID <artist_id>


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # Done TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    new_artists_data = Artist.query.filter(Artist.id == artist_id)

    # add new artists data
    new_artists_data.name = request.form.get("name")
    new_artists_data.city = request.form.get("city")
    new_artists_data.state = request.form.get("state")
    new_artists_data.phone = request.form.get("phone")
    new_artists_data.facebook_link = request.form.get("facebook_link")
    new_artists_data.website = request.form.get("website")
    new_artists_data.genres = request.form.get("genres")
    new_artists_data.image_link = request.form.getlist("image_link")
    new_artists_data.seeking_venue = request.form.getlist("seeking_venue")
    new_artists_data.seeking_description = request.form.getlist("seeking_description")

    db.session.add(new_artists_data)
    # save new data to database
    db.session.commit()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venu_json = {}
    venu_data = Venue.query.filter(Venue.id == venue_id).all()
    venu_json = {
        "id": venu_data.id,
        "name": venu_data.name,
        "city": venu_data.city,
        "state": venu_data.state,
        "phone": venu_data.phone,
        "image_link": venu_data.image_link,
        "genres": ','.join(venu_data.genres),
        "website": venu_data.website,
        "facebook_link": venu_data.facebook_link,
        "seeking_venue": venu_data.seeking_venue,
        "seeking_description": venu_data.seeking_description

    }
    # adding data into form
    form = VenueForm(data=venu_json)

    # Done TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venu_json)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # Done TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    new_venu_data = Venue.query.filter(Venue.id == venue_id)

    # add new  data
    new_venu_data.name = request.form.get("name")
    new_venu_data.city = request.form.get("city")
    new_venu_data.state = request.form.get("state")
    new_venu_data.phone = request.form.get("phone")
    new_venu_data.facebook_link = request.form.get("facebook_link")
    new_venu_data.website = request.form.get("website")
    new_venu_data.genres = request.form.get("genres")
    new_venu_data.image_link = request.form.getlist("image_link")
    new_venu_data.seeking_venue = request.form.getlist("seeking_venue")
    new_venu_data.seeking_description = request.form.getlist("seeking_description")

    db.session.add(new_venu_data)
    # save new data to database
    db.session.commit()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # Done TODO: insert form data as a new Venue record in the db, instead
    # Done TODO: modify data to be the data object returned from db insertion

    form = ArtistForm(request.form)
    error = False
    try:

        #  insertion  of data as a new artist data
        new_artist_data = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            facebook_link=form.facebook_link.data,
            genres=form.genres.data,
            image_link=form.image_link.data,
            website=form.website.data,
            seeking_venue=form.seeking_venue.data,
            seeking_description=form.seeking_description.data)

        db.session.add(new_artist_data)
        db.session.commit()
    except:
        error = True
        db.session.rollback()


    finally:
        db.session.close()
        if error:
            from numpy.random.tests import data
            flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
        else:
            # on successful db insert, flash success
            flash('Artist ' + form.name.data + ' was successfully listed!')

    # Done TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # Done TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows_list = db.session.query(Show).all()
    shows_In_future = []

    for show in shows_list:
        artist = Artist.query.filter_by(id=show.artist_key).first_or_404()
        venue = Venue.query.filter_by(id=show.venue_key).first_or_404()

        start_datetime = show.start_time.strftime("%d/%m/%Y%H:%M:%S")

        if datetime.strptime(start_datetime, "%d/%m/%Y%H:%M:%S") > datetime.now():
            shows_In_future.append(
                {
                    "id": show.id,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
                    "venue_id": venue.id,
                    "venue_name": venue.name,
                    "artist_id": artist.id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link
                }
            )

    return render_template('pages/shows.html', shows=shows_In_future)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # Done TODO: insert form data as a new Show record in the db, instead

    form = ShowForm(request.form)
    error = False
    try:

        #  create new show data

        new_show_data = Show(
            artist_key =form.artist_id.data,
            venue_key =form.venue_id.data,
            start_time =form.start_time.data)

        db.session.add(new_show_data)
        db.session.commit()
    except:
        error = True
        db.session.rollback()


    finally:
        db.session.close()
        if error:
            from numpy.random.tests import data
            flash('An error occurred. Show could not be listed.')
        else:
            # on successful db insert, flash success
            flash('Show was successfully listed!')

    # Done TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
