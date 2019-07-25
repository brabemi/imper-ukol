from app import db

movie_to_actor = db.Table(
    'movie_to_actor',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True, index=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True, index=True)
)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Text)
    simple_name = db.Column(db.Text)
    csfd_id = db.Column(db.Integer, unique=True)
    actors = db.relationship(
        'Actor',
        secondary=movie_to_actor,
        back_populates='movies'
    )


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Text)
    simple_name = db.Column(db.Text)
    csfd_id = db.Column(db.Integer, unique=True)
    movies = db.relationship(
        'Movie',
        secondary=movie_to_actor,
        back_populates='actors'
    )
