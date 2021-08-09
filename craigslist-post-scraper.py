from bs4 import BeautifulSoup, Tag
import requests
from typing import Tuple


def create_url()-> str:
    """
    Takes value from dict to appened to base url 
    in order to make a complete url for craigslist
    """
    search_options_dict = {
        1: 'sss',
        2: 'ccc',
        3: 'rrr',
        4: 'jjj',
        5: 'eee',
        6: 'hhh',
        7: 'ggg',
        8: 'bbb'
    }

    base_url = 'https://paris.craigslist.org/search/'
    search_integer = int(input("please enter the digit" + 
    " that matches your search\n [1] For Sale [2] Community [3] CV [4] Use" +
    " [5] Events [6] Real Estate [7] Odd Jobs [8] Services\n"))
    search_ext = search_options_dict[search_integer]
    return base_url + search_ext + '?'
    

def make_soup(url: str)-> object:
    """
    Creates Soup to be used for parsing
    """
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')
    

def get_posts(soup: object)-> list[str]:
    """
    Gets div elements with class of 'result-info' which are individual posts
    """
    return soup.find_all("div", class_="result-info")

def get_post_title_and_url(post: object)-> tuple[str, str]:
    """
    Retrieves the title and href link for a post
    """
    post_title = post.a.get_text()
    post_url = post.a['href']
    return (post_title, post_url)

def get_desired_tuples(
    keywords: list[str], posts: list[Tuple[str,str]])-> list[Tuple[str,str]]:
    """
    Creates new list of tuples for posts that only match keywords entered in.
    'posts' is a list of tuples with the first index being a string of the 
    title of a post and the second index being a string of the url
    """
    return [
        get_full_info(post[1]) for post in posts for k in keywords if 
        k in post[0]
        ]
    
def get_full_info(href: str)-> dict[str:list[str,str,str,str]]:
    """
    For every href passed in, a new soup is made, and all relevant 
    information is stored
    """
    soup = make_soup(href)
    posted_on = soup.time['datetime']
    body = soup.find("section", id="postingbody")
    post_body = clean_post_body(body.get_text())
    post_title = soup.find("span", id="titletextonly").get_text()
    post_attrgroup = get_attrgroup(soup)
    return {
        post_title: [
            posted_on, post_attrgroup[0], post_attrgroup[1], post_body
            ]
        }

def get_attrgroup(soup: object)-> tuple[str,str]:
    """ 
    remove linebreaks from soup, get attrgroup, 
    clean it, assign compensation and contract type
    """
    for linebreak in soup.find_all('br'):
        linebreak.extract()
    attrgroup = soup.find("p", class_="attrgroup")
    cleaned_attrgroup = [
        att.get_text().split(':')[1].strip(' ').replace('.', 'N/A') 
        for att in attrgroup if isinstance(att, Tag) 
        and  ':' in att.get_text()]

    compensation, contract_type = cleaned_attrgroup
    return (compensation, contract_type)

def clean_post_body(body: str)-> str:
    """
    simply cleans body of post
    """
    return body.replace('\n', ' ').strip('  ')

########## magic happens

url = create_url()

keywords = [
    keyword.lower() for keyword in input(
        "Enter the keywords you want to search for"+
        ", separated by commas:\n").split(',')]

soup = make_soup(url)
posts = get_posts(soup)
post_tuples = list(map(get_post_title_and_url, posts))
desired_posts = get_desired_tuples(keywords, post_tuples)

print(f"found {len(desired_posts)} matches from: {','.join(keywords)}")

with open('results_from_CL.txt', 'w') as file:
    for d in desired_posts:
        for key, value in d.items():
            file.write(
                f"TITLE : {key}\nDATE : {value[0]}\nCOMPENSATION : " +
                f"'{value[1]}'\nCONTRACT TYPE : {value[2]}\nDESCRIPTION : " +
                f"{value[3]}\n\n")

