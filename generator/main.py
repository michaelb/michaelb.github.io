import bs4
import sys
from bs4 import BeautifulSoup
import ruamel.yaml
from pathlib import Path
from pprint import pprint
import requests
import json
import sys


def get_configurable(soup, name):
    return soup.find(configurable=lambda x: x == name)


def get_location(soup, name):
    return soup.find(location=lambda x: x == name)


def add_main_page_text(soup, page):
    b = get_configurable(soup, "title")
    b.string = page['title']
    b = get_configurable(soup, "welcome")
    b.string = page['welcome']
    b = get_configurable(soup, "bottom_left_message")
    b.string = page['bottom_left_message']
    if page['file_location'] == "index.html":
        b = get_configurable(soup, "bottom_author_name")
        b.string = page['bottom_author_name']
        a = get_location(soup, 'author_icon')
        a.attrs['src'] = page['avatar']
    else:
        a = get_location(soup, 'credits')
        a.string = ""


def fill_lead_card(soup, lead_card_config):
    with open("template/lead_card.html", 'r') as f:
        lead_card_soup = BeautifulSoup(f, 'html.parser')
    a = get_configurable(lead_card_soup, "lead_card_title")
    a.string = lead_card_config['title']
    a = get_configurable(lead_card_soup, "lead_card_welcome_bold_message")
    a.string = lead_card_config['bold_message']
    a = get_configurable(lead_card_soup, 'lead_card_message')
    a.string = lead_card_config['message']
    a = get_location(lead_card_soup, 'avatar')
    a.attrs['src'] = lead_card_config['avatar']
    a.attrs['data-tippy-content'] = lead_card_config['author_name']
    a = get_location(lead_card_soup, 'linkto')
    a.attrs['href'] = lead_card_config['links_to']

    a = get_location(lead_card_soup, 'cover')
    a.attrs['src'] = lead_card_config['cover']

    if 'repo' in lead_card_config and lead_card_config['repo']:
        [repo] = [x for x in repos if x['full_name'] == lead_card_config['reponame']]
        a = get_configurable(lead_card_soup, 'lead_card_read_time')
        a.string = str(repo['stargazers_count']) + " ☆ "
        if repo['language'] is not None:
            a.string += " " + repo['language']
        a = get_location(lead_card_soup, 'avatar')
        a.attrs['src'] = repo['owner']['avatar_url']
        if repo['forks_count'] == 0:
            a.attrs['data-tippy-content'] = username
        else:
            a.attrs['data-tippy-content'] = "michaelb and other contributors"


    else:
        a = get_configurable(lead_card_soup, 'lead_card_read_time')
        a.string = lead_card_config['read_time']

    b = get_location(soup, 'card_container')
    b.insert_before(lead_card_soup)


repos = None
def get_repos(username):
    global repos
    token = sys.argv[1]
    repos_url = 'https://api.github.com/user/repos?per_page=500'
    gh_session = requests.Session()
    gh_session.auth = (username, token)
    repos = json.loads(gh_session.get(repos_url).text)


def fill_card_from_repo(soup, card_config):
    global repos
    username, reponame = card_config['name'].split('/')
    [repo] = [x for x in repos if x['full_name'] == card_config['name']]

    # repo is a dict with every information we want

    with open("template/card.html", 'r') as f:
        card_soup = BeautifulSoup(f, 'html.parser')
    a = get_configurable(card_soup, "card_title")
    a.string = reponame
    a = get_configurable(card_soup, "bold_message")
    if 'description' in repo and repo['description'] != None:
        a.string = repo['description']
        a = get_configurable(card_soup, 'message')
        a.string = card_config['message']
    else:
        a.string = card_config['message']
        a = get_configurable(card_soup, 'message')
        a.string = ""

    a = get_configurable(card_soup, 'read_time')
    a.string = str(repo['stargazers_count']) + " ☆ "
    if repo['language'] is not None:
        a.string += " " + repo['language']

    a = get_location(card_soup, 'avatar')
    a2 = get_location(card_soup, 'avatarlink')
    a.attrs['src'] = repo['owner']['avatar_url']
    if repo['forks_count'] == 0:
        a.attrs['data-tippy-content'] = username
        a2.attrs['href'] = repo['owner']['html_url']
    else:
        a.attrs['data-tippy-content'] = "See all contributors"
        a2.attrs['href'] = "https://github.com/"+username+"/"+reponame+"/graphs/contributors"


    if card_config['size'] in ["1/3", "1/2", "2/3"]:
        size_class = "w-bfull md:w-" + \
            card_config['size'] + " p-6 flex flex-col flex-grow flex-shrink"
        a = get_location(card_soup, 'size')
        a.attrs['class'] = size_class

    a = get_location(card_soup, 'cover')
    a.attrs['src'] = card_config['cover']

    if not repo['private']:
        a = get_location(card_soup, 'linkto')
        a.attrs['href'] = repo['html_url']

    b = get_location(soup, 'card_container')
    b.append(card_soup)



def fill_card(soup, name, card_config):
    with open("template/card.html", 'r') as f:
        card_soup = BeautifulSoup(f, 'html.parser')
    a = get_configurable(card_soup, "card_title")
    a.string = name
    a = get_configurable(card_soup, "bold_message")
    a.string = card_config['bold_message']
    a = get_configurable(card_soup, 'message')
    a.string = card_config['message']
    a = get_configurable(card_soup, 'read_time')
    a.string = card_config['read_time']
    a = get_location(card_soup, 'avatar')
    a.attrs['src'] = card_config['avatar']
    a.attrs['data-tippy-content'] = card_config['author_name']
    a = get_location(card_soup, 'linkto')
    a.attrs['href'] = card_config['links_to']

    a = get_location(card_soup, 'cover')
    a.attrs['src'] = card_config['cover']

    if "avatarlink" in card_config:
        a = get_location(card_soup, 'avatarlink')
        a.attrs['href'] = card_config['avatarlink']
    

    if card_config['size'] in ["1/3", "1/2", "2/3"]:
        size_class = "w-bfull md:w-" + \
            card_config['size'] + " p-6 flex flex-col flex-grow flex-shrink"
        a = get_location(card_soup, 'size')
        a.attrs['class'] = size_class

    b = get_location(soup, 'card_container')
    b.append(card_soup)


with open("config.yml", 'r') as config_file:
    d = ruamel.yaml.YAML().load(config_file)

    get_repos(d['github_username'])
    d.pop('github_username', None)

    webpage_name = d['webpage_name']
    d.pop('webpage_name', None)

    nav_list = []
    for page in d.values():
        with open("template/nav_item.html", 'r') as f:
            nav_item_soup = BeautifulSoup(f, 'html.parser')
            a = get_configurable(nav_item_soup, 'link_name')
            a.string = page['tab_name']
            a.attrs['href'] = page['file_location']
            nav_list.append(a)

    for page in d.values():
        if 'ignore' in page:
            continue
        with open("template/index.html", 'r') as f:
            soup = BeautifulSoup(f, "html.parser")
            add_main_page_text(soup, page)

            b = get_location(soup, "nav_list")
            b.extend(nav_list)

        a = get_location(soup, "title")
        a.string = webpage_name

        if 'lead_card' in page:
            fill_lead_card(soup, page['lead_card'])
        if 'cards' in page:
            for name, card in page['cards'].items():
                fill_card(soup, name, card)
        if 'cards_from_repo' in page:
            for name, card_in_repo in page['cards_from_repo'].items():
                fill_card_from_repo(soup,card_in_repo)

        print(soup, file=open(page['file_location'], 'w'))
