import bs4
import sys
from bs4 import BeautifulSoup
import ruamel.yaml
from pathlib import Path
from pprint import pprint
import copy


def get_location(soup, name):
    return soup.find(location=lambda x: x == name)


img_soup = BeautifulSoup(" <div class=\"w-full rounded\"> <a class=\"my-auto object-center\" href=\"https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=989&q=80\"> <img class=\"inline-block align-middle object-center content-center my-auto\" src=\"https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=989&q=80\" alt=\"image\"> </a> </div> ", 'html.parser')

with open("template/gallery.html", "r") as f:
    soup = BeautifulSoup(f, 'html.parser')

L_img = []
pathlist = Path("assets/gallery").glob('**/*.*')
for path in pathlist:
    # because path is object not string
    path_in_str = str(path)
    L_img.append(path_in_str)

for i, path_in_str in enumerate(sorted(L_img)):
    a = get_location(soup, "img_container")

    new_img = copy.copy(img_soup)
    new_img.a.attrs['href'] = path_in_str
    new_img.img.attrs['src'] = path_in_str

    if (i+1)%6 in [1, 5]:
        new_img.div.attrs['class'] = "w-full col-span-2 row-span-2 m-auto rounded"

    a.append(new_img)

print(soup)
