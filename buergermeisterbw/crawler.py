import re
import urllib.request
import urllib.error
from .models import Municipality, BuergermeisterArt
from bs4 import BeautifulSoup
from typing import List
from tqdm import tqdm
import logging
import os
import time
import pandas as pd


class Crawler(object):
    def __init__(self):
        self.municipalities: List[Municipality] = []

    def start(self):
        if not os.path.exists('.html'):
            os.makedirs('.html', exist_ok=True)

        self.get_municipalities()

        for municipality in tqdm(self.municipalities):
            self.get_municipality(municipality)

        logging.info('Collected info for all municipalities')

    def get_municipalities(self):
        with urllib.request.urlopen(
                'https://www.staatsanzeiger.de/staatsanzeiger/wahlen/buergermeisterwahlen') as response:
            html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, features="html.parser")
        for link_element in soup.find_all('dt'):
            link = link_element.find('a')
            municipality = Municipality(link.text, link.get('href'))
            self.municipalities.append(municipality)

        logging.info(f'Loaded list of {len(self.municipalities)} municipalities in Baden-Württemberg')

    def get_municipality(self, municipality: Municipality):
        html_path = f".html/{municipality.name.replace('/', '_')}.html"

        if os.path.exists(html_path):
            with open(html_path, 'r') as file:
                html = file.read()
        else:
            try:
                with urllib.request.urlopen(municipality.link) as response:
                    html = response.read().decode('utf-8')
            except urllib.error.HTTPError as e:
                logging.exception(f'Error while loading {municipality.link}')
                logging.info('Waiting 5s')
                time.sleep(5)

            with open(html_path, 'w+') as file:
                file.write(html)
        try:
            soup = BeautifulSoup(html, features="html.parser")
        except Exception as e:
            logging.exception(f'Error with {municipality} in \n {html}')
            return

        try:
            div = soup.find('div', class_='row i0134')
            div = next(div.children)
        except:
            logging.exception(f'Error did not find row i0134 for {municipality}')

        try:
            bodytext = div.findNext('p')
            municipality.comment = bodytext.text.replace(u'\xa0', ' ').replace('"', '').replace('\n', ' ').strip()

            if 'oberbürgermeister' in municipality.comment.lower():
                municipality.buergermeister_art = BuergermeisterArt.Oberbuergermeister
            else:
                municipality.buergermeister_art = BuergermeisterArt.Buergermeister

            ul = div.findNext('ul')
            list_elements = ul.find_all('li')
            list_elements = [el.text.replace(u'\xa0', ' ').replace('\t', ' ').strip() for el in list_elements]
            list_elements = [re.sub(' +', ' ', el).replace('\u200a', '') for el in list_elements]

            for list_element in list_elements:
                if 'wahlsieger' in list_element.lower() or 'wahlergebnis' in list_element.lower():
                    if '(' not in list_element and ')' not in list_element:
                        municipality.partei = 'keine Angabe'
                        municipality.wahlsieger = list_element[list_element.find(':') + 2:list_element.find('mit') - 1]
                    else:
                        municipality.partei = list_element[list_element.find('(') + 1:list_element.find(')')]
                        municipality.wahlsieger = list_element[list_element.find(':') + 2:list_element.find('(') - 1]
                    if list_element.count('(') > 1:
                        zustimmung = ''.join(filter(str.isdigit, list_element.split(',')[0])).strip()
                    else:
                        zustimmung = ''.join(filter(str.isdigit, list_element)).strip()
                    if zustimmung != '':
                        if int(zustimmung) > 10000 or int(zustimmung) < 10:
                            logging.warning(f'Empty zustimmung since too many digits in field for {municipality.name}')
                        else:
                            municipality.zustimmung = float(f'0.{zustimmung}')
                    else:
                        logging.warning(f'Empty zustimmung for {municipality.name}')
                elif 'wahlbeteiligung' in list_element.lower():
                    wahlbeteiligung = ''.join(filter(str.isdigit, list_element)).strip()
                    if wahlbeteiligung != '':
                        municipality.wahlbeteiligung = float(f'0.{wahlbeteiligung}')
                    else:
                        logging.warning(f'Empty Wahlbeteiligung for {municipality.name}')
                elif 'einwohner' in list_element.lower():
                    einwohner = ''.join(filter(str.isdigit, list_element))
                    municipality.einwohnerzahl = int(einwohner)
                elif 'wahlberechtigte' in list_element.lower():
                    wahlberechtigte = ''.join(filter(str.isdigit, list_element))
                    municipality.wahlberechtigte = int(wahlberechtigte)
                else:
                    logging.error(
                        f'List element that does not match a pattern: "{list_element}" in {municipality.name} {municipality.link}')

        except Exception as e:
            logging.error(
                f'{e} while parsing "{list_element}" in {municipality.name} {municipality.link}. All elements \n {list_elements}',
                stack_info=False)

    def save(self, file):
        df = pd.DataFrame(
            columns=['gemeinde', 'art', 'buergermeister', 'partei', 'zustimmung', 'einwohner', 'wahlberechtigte',
                     'wahlbeteiligung', 'volltext', 'link'])

        for municipality in self.municipalities:
            df = df.append({'gemeinde': municipality.name,
                            'art': municipality.buergermeister_art.name,
                            'buergermeister': municipality.wahlsieger,
                            'partei': municipality.partei,
                            'zustimmung': municipality.zustimmung,
                            'einwohner': municipality.einwohnerzahl,
                            'wahlberechtigte': municipality.wahlberechtigte,
                            'wahlbeteiligung': municipality.wahlbeteiligung,
                            'volltext': municipality.comment,
                            'link': municipality.link
                            }, ignore_index=True)

        # l = [m.to_dict() for m in self.municipalities]

        # with open(file, 'w+') as f:
        #    json.dump(l, f)
        df.to_csv(file, sep=';', index=False)

        logging.info(f'Wrote csv file to {file}')
