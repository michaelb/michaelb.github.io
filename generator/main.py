import bs4
import sys
from bs4 import BeautifulSoup
import ruamel.yaml
from pathlib import Path
from pprint import pprint


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
    b = get_configurable(soup, "bottom_author_name")
    b.string = page['bottom_author_name']
    a = get_location(soup, 'author_icon')
    a.attrs['src'] = page['avatar']

def fill_lead_card(soup, lead_card_config):
    with open("template/lead_card.html", 'r') as f:
        lead_card_soup = BeautifulSoup(f,'html.parser')
    a = get_configurable(lead_card_soup, "lead_card_title")
    a.string = lead_card_config['title']
    a = get_configurable(lead_card_soup, "lead_card_welcome_bold_message")
    a.string = lead_card_config['bold_message']
    a = get_configurable(lead_card_soup, 'lead_card_message')
    a.string = lead_card_config['message']
    a = get_configurable(lead_card_soup, 'lead_card_read_time')
    a.string = lead_card_config['read_time']
    a = get_location(lead_card_soup, 'author_icon')
    a.attrs['src'] = lead_card_config['avatar']
    a.attrs['data-tippy-content'] = lead_card_config['author_name']
    a = get_location(lead_card_soup, 'linkto')
    a.attrs['href'] = lead_card_config['links_to']

    a = get_location(lead_card_soup, 'cover')
    a.attrs['src'] = lead_card_config['cover']

    b = get_location(soup, 'card_container')
    b.insert_before(lead_card_soup)




with open("config.yml", 'r') as config_file:
    d = ruamel.yaml.YAML().load(config_file)

    nav_list = []
    for page in d.values():
        with open("template/nav_item.html", 'r') as f:
            nav_item_soup = BeautifulSoup(f, 'html.parser')
            a = get_configurable(nav_item_soup, 'link_name')
            a.string = page['tab_name']
            a.attrs['href'] = page['file_location']
            print(a)
            nav_list.append(a)

    for page in d.values():
        with open("template/index.html", 'r') as f:
            soup = BeautifulSoup(f, "html.parser")
            add_main_page_text(soup, page)

            b = get_location(soup, "nav_list")
            b.extend(nav_list)

        if 'lead_card' in page:
            fill_lead_card(soup, page['lead_card'])




print(soup, file=sys.stderr)
