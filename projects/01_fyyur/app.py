# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from flask import (
    Flask, render_template, request, Response, flash, redirect, url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy import func
from datetime import datetime
import sys
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database (done)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

venue_genre = db.Table('Venue_Genre',
                       db.Column('venue_id', db.Integer,
                                 db.ForeignKey('Venue.id'), primary_key=True),
                       db.Column('genre_id', db.Integer,
                                 db.ForeignKey('Genre.id'), primary_key=True)
                       )
artist_genre = db.Table('Artist_Genre',
                        db.Column('artist_id', db.Integer,
                                  db.ForeignKey('Artist.id'), primary_key=True),
                        db.Column('genre_id', db.Integer,
                                  db.ForeignKey('Genre.id'), primary_key=True)
                        )


class Show(db.Model):  # using association object pattern
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'Venue.id'), nullable=False, primary_key=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False,  primary_key=False)
    datetime = db.Column('datetime', db.String, nullable=False)
    venues = db.relationship(
        'Venue', backref='artists', lazy=True,
    )
    artists = db.relationship(
        'Artist', backref='venues', lazy=True,
    )


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    # genre is multivalued attribute
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    official_website = db.Column(db.String)
    facebook_link = db.Column(db.String(120))
    seek = db.Column(db.String)
    image_link = db.Column(db.String(500))

    genres = db.relationship(
        'Genre', secondary=venue_genre,
        backref=db.backref('venues', lazy=True, cascade='all, delete')
    )

    def __repr__(self):
        return f"<Venue id={self.id}, name={self.name}>"

    # TODO: implement any missing fields,
    # as a database migration using Flask-Migrate (done)


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f"{self.name}"


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    # genre is a multivalued attribute
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    official_website = db.Column(db.String)
    facebook_link = db.Column(db.String(120))
    seek = db.Column(db.String)
    image_link = db.Column(db.String(500))

    genres = db.relationship(
        'Genre', secondary=artist_genre,
        backref=db.backref('artists', lazy=True)
    )

    def __repr__(self):
        return f"<Artist id={self.id}, name={self.name}>"

    # TODO: implement any missing fields, as
    # a database migration using Flask-Migrate (done)

# TODO Implement Show and Artist models, and complete all model relationships
# and properties, as a database migration. (done)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@ app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@ app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    # num_shows should be aggregated based on number of
    # upcoming shows per venue. (done)

    data = []
    areas = db.session.query(Venue.city, Venue.state, func.count(
        Venue.id)).group_by(Venue.city).group_by(Venue.state).all()
    for area in areas:
        print(area.city)
        area_dict = {}
        area_dict['city'] = area.city
        area_dict['state'] = area.state
        area_dict['venues'] = []
        venues = db.session.query(Venue.id, Venue.name).filter(
            Venue.city == area.city).filter(Venue.state == area.state).all()
        print(venues)
        for venue in venues:
            venue_dict = {}
            venue_dict['id'] = venue.id
            venue_dict['name'] = venue.name.title()
            area_dict['venues'].append(venue_dict)
        data.append(area_dict)

    return render_template('pages/venues.html', areas=data)


@ app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure
    # it is case-insensitive. seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square
    # Live Music & Coffee" (done)

    pattern = request.form.get('search_term', '')
    data = db.session.query(Venue.id, Venue.name).filter(
        Venue.name.ilike('%'+pattern+'%')).all()

    response = {}
    response['count'] = len(data)
    venues = []
    for venue in data:
        venue_dect = {}
        venue_dect['id'] = venue.id
        venue_dect['name'] = venue.name.title()
        venues.append(venue_dect)
    response['data'] = venues

    return render_template('pages/search_venues.html', results=response,
                           search_term=pattern)


@ app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    error = False
    try: 
        data = db.session.query(Venue).get(venue_id)
        seeking_talent = False
        if data.seek:
            seeking_talent = True
        shows = db.session.query(Show).filter(Show.venue_id == data.id).all()
        # image_link = show_result.artists.image_link
        past_shows = []
        upcoming_shows = []
        current_time = format_datetime(str(datetime.now()), format='full')
        for show in shows:
            if current_time >= show.datetime:
                past_shows.append(show)
            else:
                upcoming_shows.append(show)
    except:
        error = True
        print(sys.exc_info())
    finally:
        if error:
            flash('venue is no longer present.')
            return redirect(url_for('index'))
        else:
            return render_template(
                'pages/show_venue.html', venue=data,
                seeking_talent=seeking_talent,
                past_shows=past_shows,
                past_shows_count=len(past_shows),
                upcoming_shows=upcoming_shows,
                upcoming_shows_count=len(upcoming_shows)
            )


@ app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@ app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db (done), instead
    # TODO: modify data to be the data object returned from db insertion(done)
    error = False
    modify = False
    try:

        name = request.form['name'].title()
        city = request.form['city'].title()
        state = request.form['state']
        address = request.form['address'].title()
        phone = request.form['phone']
        facebook_link = request.form['facebook_link']
        official_website = request.form['official_website']
        image_link = request.form['image_link']
        seek = request.form['seek']
        genre_names_list = request.form.getlist('genres')

        genre_list = []
        for genre_name in genre_names_list:
            genre = db.session.query(Genre)\
                    .filter(Genre.name == genre_name).first()
            if genre:
                genre_list.append(genre)
            else:
                genre_list.append(Genre(name=genre_name))
        venue = db.session.query(Venue).filter(Venue.name.ilike(name)).first()
        if venue:
            modify = True
            venue.city = city
            venue.state = state
            venue.address = address
            venue.phone = phone
            venue.genres = genre_list
            venue.facebook_link = facebook_link
            venue.official_website = official_website
            venue.image_link = image_link
            venue.seek = seek
        else:

            venue = Venue(
                name=name, city=city, state=state, address=address,
                phone=phone, genres=genre_list, facebook_link=facebook_link,
                official_website=official_website, image_link=image_link,
                seek=seek
            )

            db.session.add(venue)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        if modify:
            flash('An error occurred. Venue ' + request.form['name'] +
                  ' could not be modified.')
        else:
            flash('An error occurred. Venue ' + request.form['name'] +
                  ' could not be listed.')
    else:
        if modify:
            flash('Venue ' + request.form['name'] +
                  ' was successfully modified!')
        else:
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')

    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.(done)
    # e.g., flash('An error occurred. Venue ' + data.name + ' coul
    # not be listed.') see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@ app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session
    # commit could fail. (done)
    error = False
    try:
        venue = db.session.query(Venue).get(venue_id)
        for show in venue.artists:
            db.session.delete(show)
        db.session.delete(venue)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page,
    # have it so that clicking that button delete it from the db then redirect
    # the user to the homepage(done)
    if error:
        flash('venue not found.')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------


@ app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = db.session.query(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@ app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure
    # it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and 
    # "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    pattern = request.form.get('search_term', '')
    data = db.session.query(Artist.id, Artist.name).filter(
        Artist.name.ilike('%'+pattern+'%')).all()
    response = {}
    response['count'] = len(data)
    response['data'] = data
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@ app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data = db.session.query(Artist).get(artist_id)
    if not data:
        return redirect(url_for('index'))
    seeking_venue = False
    if data.seek:
        seeking_venue = True
    shows = db.session.query(Show).filter(Show.artist_id == data.id).all()
    # image_link = show_result.artists.image_link
    past_shows = []
    upcoming_shows = []
    current_time = format_datetime(str(datetime.now()), format='full')
    for show in shows:
        if current_time >= show.datetime:
            past_shows.append(show)
        else:
            upcoming_shows.append(show)

    return render_template('pages/show_artist.html', artist=data,
                           seeking_venue=seeking_venue,
                           past_shows=past_shows,
                           past_shows_count=len(past_shows),
                           upcoming_shows=upcoming_shows,
                           upcoming_shows_count=len(upcoming_shows)
                           )

#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = db.session.query(Artist).get(artist_id)
    if artist:
        return render_template('forms/edit_artist.html', form=form,
                               artist_name=artist.name,
                               artist_id=artist.id)
    else:
        flash('artist id is not found.')
        return redirect(url_for('index'))
    # TODO: populate form with fields from artist with ID <artist_id> (done)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes (done)
    error = False
    artist = db.session.query(Artist).get(artist_id)
    try:
        artist.name = request.form['name'].title()
        artist.city = request.form['city'].title()
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        genre_names_list = request.form.getlist('genres')
        genre_list = []
        for genre_name in genre_names_list:
            genre = db.session.query(Genre)\
                    .filter(Genre.name == genre_name).first()
            if genre:
                genre_list.append(genre)
            else:
                genre_list.append(Genre(name=genre_name))
        artist.genres = genre_list
        artist.facebook_link = request.form['facebook_link']
        artist.official_website = request.form['official_website']
        artist.image_link = request.form['image_link']
        artist.seek = request.form['seek']
        db.session.add(artist)
        db.session.commit()
    except Exception:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        print()
        db.session.close()
    if error:
        flash('the artist could not be edited.')
        return redirect(url_for('index'))
    else:
        flash('the artist has been edited successfully!')
        return redirect(url_for('show_artist', artist_id=artist_id))


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes (done)
    venue = db.session.query(Venue).get(venue_id)
    if venue:
        return render_template('forms/edit_venue.html', form=form, venue=venue)
    else:
        flash('venue id is not found.')
        return redirect(url_for('index'))

    # TODO: populate form with values from venue with ID <venue_id> (done)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes (done)

    error = False
    venue = db.session.query(Venue).get(venue_id)
    try:
        venue.name = request.form['name'].title()
        venue.city = request.form['city'].title()
        venue.address = request.form['address']
        venue.state = request.form['state']
        venue.phone = request.form['phone']
        genre_names_list = request.form.getlist('genres')
        genre_list = []
        for genre_name in genre_names_list:
            genre = db.session.query(Genre)\
                    .filter(Genre.name == genre_name).first()
            if genre:
                genre_list.append(genre)
            else:
                genre_list.append(Genre(name=genre_name))
        venue.genres = genre_list
        venue.facebook_link = request.form['facebook_link']
        venue.official_website = request.form['official_website']
        venue.image_link = request.form['image_link']
        venue.seek = request.form['seek']
        db.session.add(venue)
        db.session.commit()
    except Exception:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('the venue could not be edited.')
        return redirect(url_for('index'))
    else:
        flash('the venue has been edited successfully!')
        return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    found = True
    try:
        artist = db.session.query(Artist).filter(Artist.name.ilike(
            request.form['name'])).first()
        if not artist:
            found = False
            artist = Artist()
        artist.name = request.form['name'].title()
        artist.city = request.form['city'].title()
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        genre_names_list = request.form.getlist('genres')
        genre_list = []
        for genre_name in genre_names_list:
            genre = db.session.query(Genre)\
                    .filter(Genre.name == genre_name).first()
            if genre:
                genre_list.append(genre)
            else:
                genre_list.append(Genre(name=genre_name))
        artist.genres = genre_list
        artist.facebook_link = request.form['facebook_link']
        artist.official_website = request.form['official_website']
        artist.image_link = request.form['image_link']
        artist.seek = request.form['seek']
        if not found:
            db.session.add(artist)
        db.session.commit()
    except Exception:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' + artist.name
              + ' could not be listed')
        return redirect(url_for('index'))
    else:
        if not found:
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
        else:
            flash('Artist ' + request.form['name'] + ' was successfully modified!')
        return render_template('pages/home.html')

    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could
    # not be listed.') (done)


#  Shows
#  ----------------------------------------------------------------

@ app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.(done)
    # num_shows should be aggregated based on number of upcoming
    # shows per venue.

    data = db.session.query(Show).join(Venue).join(Artist).all()

    return render_template('pages/shows.html', shows=data)


@ app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show
    # listing form TODO: insert form data as a new Show record
    # in the db, instead (done)
    error = False

    try:
        db.session.add(Show(
            artists=db.session.query(Artist).get(request.form['artist_id']),
            venues=db.session.query(Venue).get(request.form['venue_id']),
            datetime=format_datetime(request.form['start_time'], format='full')
        ))
        db.session.commit()
    except Exception:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('Show could not be listed.')
        return render_template('pages/home.html')
    else:
        flash('Show was successfully listed!')
        return render_template('pages/home.html')

    # on successful db insert, flash success

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')(done)
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
