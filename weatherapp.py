#!/usr/bin/python3

"""
Weather app project.
"""
import html
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/324561"
ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')
ACCU_CONTAINER_TAGS = ((), ('>Поточна погода</a>'))  

RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_%D0%9B%D1"
           "%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1%96%D0%B2%D1%81%D1"
           "%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C")
RP5_TAGS = ('<div class="t_0"><b>', 
            """<div class="cn6" onmouseover="tooltip(this, '<b>""") 
RP5_CONTAINER_TAGS = (('<div id="ftab_1_content"', 
                       '<td class="title underlineRow toplineRow">'), 
                      ('<div id="ftab_1_content"', 
                       '<td class="title">', '<div class="cc_0">')) 


def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}

def get_page_source(url):
    """
    """

    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')


def get_weather_info(page_content, tags, container_tags_list):
    """
    """

    weather_info_list = []
    
    for tag in tags:
        
        for container_tags in container_tags_list:
            container_tag_index = 0
            for container_tag in container_tags:
                container_tag_index = page_content.find(container_tag, container_tag_index)

        tag_index = page_content.find(tag, container_tag_index)
        tag_size = len(tag)
        value_start = tag_index + tag_size
        
        content = ''
        for c in page_content[value_start:]:
            if c != '<':
                content += c
            else:
                break
            
        weather_info_list.append(content)
            
    return weather_info_list 
    

def produce_output(provider_name, temp, condition):
    """
    """

    print(f'\n{provider_name}:')
    print(f'Temperature: {html.unescape(temp)}')
    print(f'Condition:   {condition}\n')


def main():
    """Main entry point.
    """

    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS, ACCU_CONTAINER_TAGS),
                     "RP5": (RP5_URL, RP5_TAGS, RP5_CONTAINER_TAGS)}
    for name in weather_sites:
        url, tags, container_tags_list = weather_sites[name]
        content = get_page_source(url)
        temp, condition = get_weather_info(content, tags, container_tags_list)
        produce_output(name, temp, condition)


if __name__ == '__main__':
    main()