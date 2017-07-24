# -*- coding: utf-8 -*-

import time
import requests


with open('darksky_api_key.txt', 'r') as f:
    weather_api_key = f.readline()


URL = 'https://api.darksky.net/forecast/{}/{},{}?units=ca'
MAX_DATA_TTL = 60 * 60
WEATHER_CACHE = {}

ICONS = {
    'clear-day': '☀️', 
    'clear-night': '🌃', 
    'rain': '🌧', 
    'snow': '🌨', 
    'sleet': '💦', 
    'wind': '💨', 
    'fog': '🌫️', 
    'cloudy': '☁️', 
    'partly-cloudy-day': '🌤', 
    'partly-cloudy-night': '🌃☁️'}


def to_key(lat, lon):
    return (round(lat, 3), round(lon, 3))


def check_updates(geo_pos):
    t = time.time()
    if geo_pos not in WEATHER_CACHE or t - WEATHER_CACHE[geo_pos][0] > MAX_DATA_TTL:
        WEATHER_CACHE[geo_pos] = (t, requests.get(URL.format(weather_api_key, *geo_pos)).json())


def get_cur_forecast(lat, lon):
    key = to_key(lat, lon)
    check_updates(key)
    return pretty_format_data_point(WEATHER_CACHE[key][1]['currently'])


def get_today_forecast(lat, lon):
    key = to_key(lat, lon)
    check_updates(key)
    return pretty_format_data_block(WEATHER_CACHE[key][1]['hourly'])


def get_tomorrow_forecast(lat, lon):
    key = to_key(lat, lon)
    check_updates(key)
    return pretty_format_data_block(WEATHER_CACHE[key][1]['daily'])


def pretty_format_data_point(data_point):
    ans = []
    try:
        ans.append(data_point['summary'] + ICONS[data_point['icon']])
    except KeyError:
        pass

    try:
        ans.append('Temperature: {}°C (feels like {}°С)'.format(
            data_point['temperature'], 
            data_point['apparentTemperature']))
    except KeyError:
        pass

    try:
        ans.append('Wind Speed: {} km/h'.format(data_point['windSpeed']))
    except KeyError:
        pass

    try:
        ans.append('Visibility: {} m'.format(data_point['visibility']))
    except KeyError:
        pass

    try:
        ans.append('Pressure: {} mm Hg'.format(
            round(float(data_point['pressure']) * 100 / 133.322)))
    except KeyError:
        pass

    return '\n'.join(ans)


def short_format_data_point(data_point):
    ans = ''
    try:
        ans = data_point['summary'] + ICONS[data_point['icon']]
    except KeyError:
        pass

    try:
        ans += ' {}°C'.format(data_point['temperature'])
    except KeyError:
        pass

    return ans


def pretty_format_data_block(data_block):
    ans = []

    try:
        ans.append(data_block['summary'] + ICONS[data_block['icon']])
    except KeyError:
        pass

    try:
        for i, dp in enumerate(data_block['data']):
            if (i > 23):
                break
            ans.append('\n•' + time.ctime(dp['time']))
            ans.append(short_format_data_point(dp))
    except KeyError:
        pass

    return '\n'.join(ans)
