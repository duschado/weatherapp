#!/usr/bin/python3

"""
Weather app project.
"""
import html
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/324561"
ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')

#RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_%D0%9B%D1"
#           "%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1%96%D0%B2%D1%81%D1"
#          "%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C")


#RP5_TEMP_TAG = '<span class="t_0" style="display: block;">'

#RP5_CONTAINER_TAG = '<div class="cc_0">'
#RP5_COND_TAG = """<div class="cn4" onmouseover="tooltip(this, '<b>"""
#rp5_cond_tag_size = len(RP5_COND_TAG)
#rp5_cond_tag_index = rp5_page.find(RP5_COND_TAG, rp5_page.find(RP5_CONTAINER_TAG))
#rp5_cond_value_start = rp5_cond_tag_index + rp5_cond_tag_size
#rp5_cond = ''
#for char in rp5_page[rp5_cond_value_start:]:
#    if char != '<':
#        rp5_cond += char
#    else:
#        break



def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}

def get_page_source(url):
    """
    """

    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')

def get_tag_content(page_content, tag):
    """
    """
    print(tag)
    tag_index = page_content.find(tag)
    tag_size = len(tag)
    value_start = tag_index + tag_size

    content = ''
    for c in page_content[value_start:]:
        if c != '<':
            content += c
        else:
            break
    return content


def get_weather_info(page_content, tags):
    """
    """

    return tuple([get_tag_content(page_content, tag) for tag in tags])

def produce_output(provider_name, temp, condition):
    """
    """

    print(f'\n{provider_name}:')
    print(f'Temperature: {html.unescape(temp)}\n')
    print(f'Condition: {condition}\n')


def main():
    """Main entry point.
    """

    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS)} #,
#                     "RP5": (RP5_URL, RP5_TAGS)}
    for name in weather_sites:
        url, tags = weather_sites[name]
        content = get_page_source(url)
        temp, condition = get_weather_info(content, tags)
        produce_output(name, temp, condition)


if __name__ == '__main__':
    main()










