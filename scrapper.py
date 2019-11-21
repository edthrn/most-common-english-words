#!/usr/bin/env python
from pathlib import Path
from typing import Sequence, Optional, Union

import requests
from bs4 import BeautifulSoup

URL = 'https://www.talkenglish.com/vocabulary/top-1500-nouns.aspx'


def get_raw_html(url: Optional[str] = URL) -> str:
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f'Failed to fetch HTML from {url}.')
    return resp.text


def get_html_parser(html_content: str) -> BeautifulSoup:
    return BeautifulSoup(html_content, 'html.parser')


def extract_noun_list_from_parser(parser: BeautifulSoup) -> Sequence[str]:
    rows = parser.find_all('tr')
    nouns = [tag.find('a').text for tag in rows if tag.find('a') is not None]
    return set([noun for noun in nouns if noun])


def write_noun_list_to_file(nouns: Sequence[str], 
                            filepath: Optional[Union[str, Path]] = '') -> None:
    if not filepath:
        filepath = Path(__file__).resolve().parent / 'nouns.txt'
    with open(filepath, 'w') as fp:
        fp.write('\n'.join(nouns))


def main() -> None:
    html = get_raw_html()
    parser = get_html_parser(html)
    nouns = extract_noun_list_from_parser(parser)
    write_noun_list_to_file(nouns)
    print(f'SUCCESS! {len(nouns)} written to file.')


if __name__ == '__main__':
    main()

