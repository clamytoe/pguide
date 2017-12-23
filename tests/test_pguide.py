from pguide import pguide

session = pguide.initialize_connection()


def test_asdict():
    t_show1 = pguide.Show()
    t_dict1 = t_show1._asdict()
    expected1 = {'show_id': None,
                 'movie_id': None,
                 'title': None,
                 'url': None}
    t_show2 = pguide.Show(1, '0451279', 'Wonder Woman', 'http://www.imdb.com/title/tt0451279')
    t_dict2 = t_show2._asdict()
    expected2 = {'show_id': 1,
                 'movie_id': '0451279',
                 'title': 'Wonder Woman',
                 'url': 'http://www.imdb.com/title/tt0451279'}
    assert t_dict1 == expected1
    assert t_dict2 == expected2


def test_initialize_connection():
    assert type(session) == pguide.imdb.parser.http.IMDbHTTPAccessSystem


def test_search_for_title():
    search_term = 'Wonder Woman'
    t_shows = pguide.search_for_title(session, search_term)
    assert len(t_shows) == 20
    assert t_shows[0].show_id == 0
    assert t_shows[0].movie_id == '0451279'
    assert t_shows[0].title == 'Wonder Woman (2017)'
    assert t_shows[0].url == 'http://www.imdb.com/title/tt0451279/parentalguide'


def test_get_plot():
    t_plot1 = pguide.get_plot('http://www.imdb.com/title/tt0451279/')
    t_plot2 = pguide.get_plot('http://www.imdb.com/')
    assert t_plot1 == 'Diana, princess of the Amazons, trained to be an unconquerable warrior. Raised on a sheltered ' \
                      'island paradise, when a pilot crashes on their shores and tells of a massive conflict raging ' \
                      'in the outside world, Diana leaves her home, convinced she can stop the threat. Fighting ' \
                      'alongside man in a war to end all wars, Diana will discover her full powers and her true ' \
                      'destiny.'
    assert t_plot2 == 'The plot was not available.'
