from bs4 import BeautifulSoup

import socket

HOSTNAME = 'http://127.0.0.1:8000'


def replace_content(content):
    soup = BeautifulSoup(content, "html.parser")
    for img in soup.findAll('img'):
        if not img['src'].startswith('http'):
            img['src'] = f'{HOSTNAME}{img["src"]}'
        img['width'] = '100%'
        img['height'] = ''
    for figure in soup.findAll('figure'):
        figure['style'] = ''
        figure['width'] = '100%'
    # for iframe in soup.findAll('iframe'):
    #     iframe['style'] = ''
    #     iframe['height'] = '500px'
    #     iframe['width'] = '100%'
    #     if 'youtube' in iframe['src']:
    #         iframe['src'] = f'{iframe["src"].replace("watch?v=", "embed/")}'
    return soup.__str__()
