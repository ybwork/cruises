#/usr/bin/env Python3
from datetime import datetime

import requests
from bs4 import BeautifulSoup


domain = 'https://www.lueftner-cruises.com'
user_agent = 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'
headers = {'User-Agent': user_agent}
scraper = BeautifulSoup


def generate_cruises_info():
    result = []

    for link in get_cruise_links():
        cruise_page = do_request(link, headers)

        content = scrape_data(content=cruise_page.text, parser='html.parser')

        cruise_info = {
            'name': get_name(content),
            'days': get_days(content),
            'itinerary': get_itinerary(content),
            'dates': get_dates(content)
        }

        result.append(cruise_info)

        if len(result) == 4:
            break

    return result


def get_cruise_links():
    url = domain + '/en/river-cruises/cruise.html'
    page = do_request(url, headers)
    data = scrape_data(page.text, 'html.parser')
    block = data.find(class_='content')
    blocks = data.find_all(class_='travel-box-container')
    return [domain + block.find('a').get('href') for block in blocks]


def do_request(url, headers):
    return requests.get(url=url, headers=headers)


def scrape_data(content, parser):
    return scraper(content, parser)


def get_name(content):
    return content.find(class_='river-site-highlight').h1.get_text('', strip=True)


def get_days(content):
    return content.find(class_='cruise-duration').text.strip(' Days')


def get_itinerary(content):
    block = content.find(class_='route')
    return [route.get_text('', strip=True).split('>')[0] for route in block.find_all(class_='route-city')]


def get_dates(content):
    block = content.find(class_='accordeon-data-price')

    dates = []
    for date in block.find_all(class_='accordeon-panel-default'):
        start_date = date.find(class_='price-duration').text.split('-')[0].strip()
        new_format_start_date = transform_date(start_date)

        result = {
            new_format_start_date: {
                'ship': date.find(class_='table-ship-name').get_text('', strip=True),
                'price': date.find(class_='big-table-font').get_text('', strip=True)[2:]
            }
        }

        dates.append(result)

    return dates


def transform_date(date):
    return datetime.strptime(date, '%d. %b %Y').strftime('%Y-%m-%d')


def main():
    try:
        print(generate_cruises_info())
    except (NameError, AttributeError, ImportError, KeyError, NameError, SyntaxError, ValueError, TypeError) as err:
        print('Something went wrong, try again later.')


if __name__ == '__main__':
    main()