import unittest
import pguide


def test_asdict():
    t_show = pguide.Show(1, '0451279', 'Wonder Woman', 'http://www.imdb.com/title/tt0451279')
    t_dict = t_show._asdict()
    expected = {'show_id': 1,
                'movie_id': '0451279',
                'title': 'Wonder Woman',
                'url': 'http://www.imdb.com/title/tt0451279'}
    assert t_dict == expected


def test_initialize_connection():
    session = pguide.initialize_connection()
    assert type(session) == pguide.imdb.parser.http.IMDbHTTPAccessSystem


