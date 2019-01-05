#!/usr/bin/python3

"""
Weather app project.
"""
import sys
import html
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/324561"
ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')

RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_%D0%9B%D1"
           "%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1%96%D0%B2%D1%81%D1"
           "%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C")
RP5_TAGS = ('<div class="t_0"><b>', 
            """<div class="cn6" onmouseover="tooltip(this, '<b>""") 


def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}


def get_page_source(url):
    """
    """

    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')


def get_weather_info_accu(page_content):
    """
    """
    
    city_page = BeautifulSoup(page_content, 'html.parser')
    current_day_section = city_page.find(
        'li', class_='night current first cl')

    weather_info = {}
    if current_day_section:
        current_day_url = current_day_section.find('a').attrs['href']
        if current_day_url:
            current_day_page = get_page_source(current_day_url)
            if current_day_page:
                current_day = \
                    BeautifulSoup(current_day_page, 'html.parser')
                weather_details = \
                    current_day.find('div', attrs={'id': 'detail-now'})
                temp = weather_details.find('span', class_='large-temp')
                if temp:
                    weather_info['temp'] = temp.text
                feal_temp = weather_details.find('span', class_='small-temp')
                if feal_temp:
                    weather_info['feal_temp'] = feal_temp.text
                condition = weather_details.find('span', class_='cond')
                if condition:
                    weather_info['cond'] = condition.text
                wind_info = weather_details.find_all('li', class_='wind')
                if wind_info:
                    weather_info['wind'] = \
                        ' '.join(map(lambda t: t.text.strip(), wind_info))
    return weather_info


def get_weather_info_rp5(page_content):
    """
    """

    city_page = BeautifulSoup(page_content, 'html.parser')
    current_day = city_page.find('div', id='archiveString')

    weather_info = {'temp': '', 'feal_temp': '', 'cond': '', 'wind': ''}
    if current_day:
        archive_temp = current_day.find('div', class_='ArchiveTemp')
        if archive_temp:
            temp = archive_temp.find('span', class_='t_0')
            if temp:
                weather_info['temp'] = temp.text
        archive_temp_feeling = current_day.find('div', class_='ArchiveTempFeeling')
        if archive_temp_feeling:
            feal_temp = archive_temp_feeling.find('span', class_='t_0')
            if feal_temp:
                weather_info['feal_temp'] = feal_temp.text
        archive_info = current_day.find('div', class_='ArchiveInfo')
        if archive_info:
            archive_text = archive_info.text
            info_list = archive_text.split(',')
            weather_info['cond'] = info_list[1].strip()
            wind = info_list[4].strip()[:info_list[4].find(')')]
            if wind:
                weather_info['wind'] = wind 

    return weather_info
    

def produce_output(info):
    """
    """

    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')
    

def main(argv):
    """Main entry point.
    """

    KNOWN_COMMANDS = {'accu': 'AccuWeather', 'rp5': 'RP5'}
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    params = parser.parse_args(argv)

    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS), 
                     "RP5": (RP5_URL, RP5_TAGS)} 
    
    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            weather_sites = {
                KNOWN_COMMANDS[command]:weather_sites[KNOWN_COMMANDS[command]]
            }
            print(f'{KNOWN_COMMANDS[command]}: \n')
        else:
            print("Unknown command provided!")
            sys.exit(1)


    for name in weather_sites:
        url, tags = weather_sites[name] 
        content = get_page_source(url)
        if name == 'AccuWeather':
            produce_output(get_weather_info_accu(content))
        if name == 'RP5':
            produce_output(get_weather_info_rp5(content))


if __name__ == '__main__':
    main(sys.argv[1:])