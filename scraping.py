#/usr/bin/env Python3
from datetime import datetime

import requests
from bs4 import BeautifulSoup

domain = 'https://www.lueftner-cruises.com'
user_agent = 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'
headers = {'User-Agent': user_agent}
scraper = BeautifulSoup


def do_request(url, headers):
    return requests.get(url=url, headers=headers)


def scrape_data(content, parser):
    return scraper(content, parser)


def get_routes(content):
    return [route.text.strip() for route in content.find_all(class_='route-city')]


def get_dates_prices(content):
    dates_prices = []
    for date_price in content.find_all(class_='accordeon-panel-default'):
        period = date_price.find(class_='price-duration').text
        start_date = period.split('-')[0].strip()
        transformed_start_date = datetime.strptime(start_date, '%d. %b %Y').strftime('%Y-%m-%d')

        data = {
            transformed_start_date: {
                'ship': date_price.find(class_='table-ship-name').text,
                'price': date_price.find(class_='big-table-font').string.strip('\n').strip()[2:]
            }
        }
        dates_prices.append(data)
    return dates_prices


url = domain + '/en/river-cruises/cruise.html'
home_page = do_request(url, headers)

soup = BeautifulSoup(home_page.text, 'html.parser')

cruise_list = soup.find(class_='content')

links_on_each_cruise = cruise_list.find_all('a')

result = []
for link_on_cruise in links_on_each_cruise:
    url = domain + link_on_cruise.get('href')
    cruise_page = do_request(url, headers)

    content = scrape_data(content=cruise_page.text, parser='html.parser')

    cruise_info = {
        'name': content.find(class_='river-site-highlight').h1.string.strip('\n').strip(),
        'days': content.find(class_='cruise-duration').text.strip(' Days'),
        'itinerary': get_routes(content.find(class_='route')),
        'dates': get_dates_prices(content.find(class_='accordeon-data-price'))
    }

    result.append(cruise_info)

    if len(result) == 4:
        break

print(result)
