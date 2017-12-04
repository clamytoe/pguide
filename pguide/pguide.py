import imdb
import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from re import sub

Show = namedtuple('Show', ['show_id', 'movie_id', 'title', 'url'])
Show.__new__.__defaults__ = (None, None, None, None)


def initialize_connection():
    """
    Initializes the connection with IMDb.
    :return: An imdb.parser.http.IMDbHTTPAccessSystem object
    """
    session = imdb.IMDb()
    return session


def search_for_title(session, search_term):
    """
    Given an imdb session object, will search the site for the given search term.
    :param session: imdb session object
    :param search_term: String for the movie/show/game to search for
    :return: A dictionary with Show() namedtuple objects for each match
    """
    s_result = session.search_movie(search_term)
    shows = {}

    # made the keys of the namedtuple a digit for ease of selecting the correct one later
    for count, result in enumerate(s_result):
        show_id = count
        movie_id = result.movieID
        title = result['long imdb canonical title']
        url = f'http://www.imdb.com/title/tt{movie_id}/parentalguide'
        shows[count] = Show(show_id, movie_id, title, url)
    return shows


def display_shows(shows):
    """
    Given a dictionary of show objects, displays them and gives you a choice of which one to get further details for.
    :param shows: Dictionary of the Show() namedtuples
    :return: None
    """
    another = False

    # put this portion into an infinite loop to allow for reviewing other listed media
    while True:
        # display a different question on the second or more pass
        if another:
            again = input('Would you like to review a different one? [y/n]')
            # if user replies with anything starting with a y, run it gain; otherwise break out fo the loop
            if not again.lower().startswith('y'):
                print('Ok')
                break

        # list all of the shows that were found
        for n in range(len(shows)):
            print(f'[{n}] {shows[n].title}')

        choice = int(input('Which one would you like to review? '))
        another = True # after first pass, set this flag

        if choice in shows.keys():
            print(f'Retrieving additional information for {shows[choice].title}')
            # the plot is not on the same page as the other information so requires its own scrape
            plot = get_plot(shows[choice].url)

            # if the plot was found, display it, otherwise skip past it
            if plot:
                print('[PLOT]')
                print(f' {plot}')

            # scrape the actual content that we need
            scrape_movie(shows[choice].url)
        else:
            print(f'{choice} is not a valid choice!')
            break


def display_ratings(ratings):
    """
    Displays the ratings that were scraped.
    :param ratings: List of MPAA ratings
    :return: None
    """
    # only attempt to display the ratings if any were found
    if ratings:
        print('[RATINGS]')

        for rating in ratings:
            print(f' {rating}', end=' ')
        # needed to get printing back to normal
        print()


def display_section(title, category, category_comments):
    """
    Displays the given section in the proper format.
    :param title: String name of the section that we are displaying
    :param category: String or List for the section category
    :param category_comments: List of comments that were found for the given category
    :return:
    """
    # only attempt to print these if either of them were found
    if category or category_comments:
        print(f'[{title.upper()}]')
        print(f' {category}')

        for comment in category_comments:
            print(f'  * {comment}')


def scrape_movie(url):
    """
    Scraping handler

    Initiates scraping of the different sections required by the script.
    :param url: String with the URL of the media to scrape
    :return: None
    """
    soup = get_soup(url)

    # scrape all of the sections
    soup_sections = soup.find('section', {'class': 'article listo content-advisories-index'})

    # scrape for the specific sections required
    soup_certificates = soup_sections.find('section', {'id': 'certificates'})
    soup_nudity = soup_sections.find('section', {'id': 'advisory-nudity'})
    soup_profanity = soup_sections.find('section', {'id': 'advisory-profanity'})

    # further scrape the sections above
    ratings = parse_certificates(soup_certificates)
    nudity, nudity_comments = parse_section(soup_nudity)
    profanity, profanity_comments = parse_section(soup_profanity)

    # here is where we actually format and show the results
    display_ratings(ratings)
    display_section('nudity', nudity, nudity_comments)
    display_section('profanity', profanity, profanity_comments)


def get_plot(url):
    """
    Scrapes the plot from the provided URL.
    :param url: String with the URL to the main page of the media
    :return: String contents of the plot or default message
    """
    soup = get_soup(url.rsplit('/', 1)[0])

    # scrape the plot section
    plot_tag = soup.find('div', {'class': 'summary_text'})

    # fixes bug were no plot is found
    try:
        return plot_tag.string.strip()
    except AttributeError:
        return 'The plot was not available.'


def cleanup_comments(comments):
    """
    Cleans up the given comments.
    :param comments: List containing all the comments for a specific section
    :return: List with the comments cleanup up
    """
    clean_comments = []

    if comments:
        for comment in comments:
            cleaned_up = sub(r'\n\n {8}\n {8}\n {12}\n {16}\n {16}\n {12}\nEdit', '', comment)
            clean_comments.append(cleaned_up)

    return clean_comments


def parse_certificates(soup):
    """
    Parses the certificates specific to the United States.
    :param soup: Beautiful soup object for the certificates section
    :return: List of the ratings that were found
    """
    # removes the first item because it does not needed
    rating_tags = soup.find_all('a')[1:]
    rating_codes = [code.string for code in rating_tags]
    mpaa = []

    if rating_codes:
        for rating in rating_codes:
            # sorry international folks, only interested in the US ratings
            if rating.startswith('United States'):
                mpaa.append(rating)
    return mpaa


def parse_section(soup):
    """
    Parses the given section.
    :param soup: Beautifulsoup object for the section to process
    :return: Tuple containinf the String of section if one was found or else None and a List of cleaned up comments
    """
    section_tag = soup.find_all('a', {'class': 'advisory-severity-vote__message'})
    section_scale = [code.string for code in section_tag]
    section = section_scale[0] if section_scale else None

    section_comment_tags = soup.find_all('li', {'class': 'ipl-zebra-list__item'})
    section_comment_list = [comment.text.strip() for comment in section_comment_tags]
    comments = cleanup_comments(section_comment_list)

    return section, comments


def get_soup(url):
    # standard scraping setup
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html5lib')

    return soup


def main():
    """
    Main entry point for the script
    :return: None
    """
    search_term = input("What would you like me to look up for you? ")
    print(f'Please wait while I search for "{search_term}"...')
    # initial connection is slow, so moved here to improve perceived performance
    shows = search_for_title(initialize_connection(), search_term)
    print(f'Found {len(shows)} matches.')
    display_shows(shows)


if __name__ == '__main__':
    """
    Runs the script if it is ran from the command line and not if loaded as a module.
    """
    main()
