from flask import render_template, request

from app import app, db
from app.models import Actor, Movie


@app.route('/')
def index():
    return render_template('index.html', actors=None, movies=None)


@app.route('/', methods=['POST'])
def index_post():
    query = request.form['query'].lower()
    actors = Actor.query.filter(Actor.simple_name.like(f'%{query}%')).all()
    movies = Movie.query.filter(Movie.simple_name.like(f'%{query}%')).all()
    return render_template('index.html', query=query, actors=actors, movies=movies)


@app.route('/actor/<int:actor_id>')
def get_actor(actor_id):
    return render_template('actor.html', actor=Actor.query.get(actor_id))


@app.route('/movie/<int:movie_id>')
def get_movie(movie_id):
    return render_template('movie.html', movie=Movie.query.get(movie_id))
