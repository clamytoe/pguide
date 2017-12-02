import imdb
import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from re import sub

Show = namedtuple('Show', ['id', 'movieID', 'title', 'url'])
Show.__new__.__defaults__ = (None, None, None, None)


def initialize_connection():
    ia = imdb.IMDb()
    return ia


def search_for_title(session, search_term):
    s_result = session.search_movie(search_term)
    shows = {}

    for count, result in enumerate(s_result):
        show_id = count
        movie_id = result.movieID
        title = result['long imdb canonical title']
        url = f'http://www.imdb.com/title/tt{movie_id}/parentalguide'
        shows[count] = Show(show_id, movie_id, title, url)
    return shows


def display_shows(shows):
    another = False
    while True:
        if another:
            again = input('Would you like to review a different one? [y/n]')
            if not again.lower().startswith('y'):
                print('Ok')
                break

        for n in range(len(shows)):
            print(f'[{n}] {shows[n].title}')

        choice = int(input('Which one would you like to review? '))
        another = True

        if choice in shows.keys():
            print(f'Retrieving additional information for "{shows[choice].title}"')
            plot = get_plot(shows[choice].url)
            if plot:
                print('[PLOT]')
                print(f' {plot}')
            # print(shows[choice].url)
            scrape_movie(shows[choice].url)
        else:
            print(f'{choice} is not a valid choice!')
            break


def scrape_movie(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html5lib')
    soup_sections = soup.find('section', {'class': 'article listo content-advisories-index'})
    soup_certificates = soup_sections.find('section', {'id': 'certificates'})
    soup_nudity = soup_sections.find('section', {'id': 'advisory-nudity'})
    # soup_violence = soup_sections.find('section', {'id': 'advisory-violence'})
    soup_profanity = soup_sections.find('section', {'id': 'advisory-profanity'})
    # soup_alcohol = soup_sections.find('section', {'id': 'advisory-alcohol'})
    # soup_frightening = soup_sections.find('section', {'id': 'advisory-frightening'})

    ratings = parse_certificates(soup_certificates)
    if ratings:
        print('[RATINGS]')
        for rating in ratings:
            print(f' {rating}', end=' ')

    nudity, nudity_comments = parse_nudity(soup_nudity)
    if nudity or nudity_comments:
        print('\n[NUDITY]')
        print(f' {nudity}')
        for n_comment in nudity_comments:
            print(f'  * {n_comment}')

    profanity, profanity_comments = parse_profanity(soup_profanity)
    if profanity and profanity_comments:
        print('[PROFANITY]')
        print(f' {profanity}')
        for p_comment in profanity_comments:
            print(f'  * {p_comment}')


def get_plot(url):
    url = url.rsplit('/', 1)[0]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html5lib')
    plot_tag = soup.find('div', {'class': 'summary_text'})
    return plot_tag.string.strip()


def cleanup_comments(comments):
    clean_comments = []
    if comments:
        for comment in comments:
            cleaned_up = sub(r'\n\n {8}\n {8}\n {12}\n {16}\n {16}\n {12}\nEdit', '', comment)
            clean_comments.append(cleaned_up)
    return clean_comments


def parse_certificates(soup):
    rating_tags = soup.find_all('a')[1:]
    rating_codes = [code.string for code in rating_tags]
    mpaa = []

    if rating_codes:
        for rating in rating_codes:
            if rating.startswith('United States'):
                mpaa.append(rating)
    return mpaa


def parse_nudity(soup):
    nudity_tags = soup.find_all('a', {'class': 'advisory-severity-vote__message'})
    nudity_scale = [code.string for code in nudity_tags]
    nudity = nudity_scale[0] if nudity_scale else None

    comment_tags = soup.find_all('li', {'class': 'ipl-zebra-list__item'})
    comment_list = [comment.text.strip() for comment in comment_tags]
    comments = cleanup_comments(comment_list)

    return nudity, comments


def parse_profanity(soup):
    # print(soup)
    profanity_tags = soup.find_all('a', {'class': 'interesting-count-text severity-vote-prompt'})
    profanity_scale = [code.string for code in profanity_tags]
    profanity = profanity_scale[0] if profanity_scale else None

    comment_tags = soup.find_all('li', {'class': 'ipl-zebra-list__item'})
    comment_list = [comment.text.strip() for comment in comment_tags]
    comments = cleanup_comments(comment_list)

    return profanity, comments


def main():
    session = initialize_connection()
    search_term = input("What movie/show would you like me to look up for you? ")
    print(f'Please wait while I search for "{search_term}"...')
    shows = search_for_title(session, search_term)
    print(f'Found {len(shows)} matches.')
    display_shows(shows)


if __name__ == '__main__':
    main()