from bs4 import BeautifulSoup
import requests
from app import db, app
from app.models import Movie, Actor

BASE_URL = 'https://www.csfd.cz'
MOVIES_URL = BASE_URL + '/zebricky/nejlepsi-filmy/?show=complete'


def get_content(url):
    result = requests.get(url)
    return result.content


def href_to_simple_name(url):
    phase1 = url.split('/')[2]
    phase2 = phase1.split('-')
    return ''.join(phase2[1:])


def get_movie_actors(movie_url):
    actors = []
    data = BeautifulSoup(get_content(movie_url), 'lxml')
    actors_span = data.find_all('span', {'data-truncate': '340'})[0]
    for actor_data in actors_span.find_all('a'):
        actor = {
            'name': actor_data.text,
            'simple_name': href_to_simple_name(actor_data['href']),
            'link': BASE_URL + actor_data['href'],
            'csfd_id': int(actor_data['href'][8:].split('-')[0])
        }
        actor['id_link'] = f'{BASE_URL}/tvurce/{actor["csfd_id"]}'
        actors.append(actor)
    return actors


def get_movies():
    data = BeautifulSoup(get_content(MOVIES_URL), 'lxml')
    movies = []
    for movie_data in data.find_all('td', {'class': 'film'}):
        app.logger.info(f'Processing movie {movie_data.a.text}')
        movie = {
            'name': movie_data.a.text,
            'simple_name': href_to_simple_name(movie_data.a['href']),
            'link': BASE_URL + movie_data.a['href'],
            'csfd_id': int(movie_data['id'][6:])
        }
        movie['id_link'] = f'{BASE_URL}/film/{movie["csfd_id"]}'
        movie['actors'] = get_movie_actors(movie['id_link'])
        movies.append(movie)
    return movies


def extract_actors(movies):
    actors = {}
    for movie in movies:
        for actor in movie['actors']:
            actors[actor['csfd_id']] = actor
    return actors


def create_actors(actors):
    for csfd_id, actor in actors.items():
        a = Actor(
            name=actor['name'],
            simple_name=actor['simple_name'],
            csfd_id=actor['csfd_id'],
        )
        db.session.add(a)
        actor['db_entry'] = a
    db.session.commit()


def create_movies(movies, actors):
    for movie in movies:
        acts = []
        for actor in movie['actors']:
            acts.append(actors[actor['csfd_id']]['db_entry'])
        m = Movie(
            name=movie['name'],
            simple_name=movie['simple_name'],
            csfd_id=movie['csfd_id'],
            actors=acts
        )
        db.session.add(m)
    db.session.commit()


def main():
    movies = get_movies()
    actors = extract_actors(movies)

    create_actors(actors)
    create_movies(movies, actors)


if __name__ == "__main__":
    main()
