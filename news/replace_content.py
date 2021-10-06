from bs4 import BeautifulSoup

import socket

HOSTNAME = 'http://localhost:8000'


def replace_content(content):
    soup = BeautifulSoup(content, "html.parser")
    for img in soup.findAll('img'):
        img['src'] = f'{HOSTNAME}{img["src"]}'
        img['height'] = '100%'
        img['width'] = '100%'
    for iframe in soup.findAll('iframe'):
        iframe['style'] = ''
        iframe['height'] = '500px'
        iframe['width'] = '100%'
    return soup.__str__()
