from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.utils.translation import get_language
from django.conf import settings

import requests
from datetime import datetime, timedelta
import math
from functools import reduce

WEATHER_API_BASE_URL='http://api.weatherapi.com/v1/'
LOCATION = 'Burkina Faso'
IMPLEMENTED_LANGUAGES = ['en', 'fr']

def get_precipitation_intensity(hourlyprecip_next_24_hrs):
    # https://www.researchgate.net/figure/Rain-classification-and-precipitation-intensity-range_tbl1_340317722
    HOURLY_PRECIPITATION_INTENSITY_THRESHOLDS = {
        _('None'): 0.5,
        _('Weak'): 2,
        _('Moderate'): 6,
        _('Heavy'): 10,
        _('Very heavy'): 18,
        _('Extreme'): 30,
        _('Very extreme'): math.inf
    }

    if not any(hourlyprecip_next_24_hrs):
        return _('None')

    for intensity, threshold in HOURLY_PRECIPITATION_INTENSITY_THRESHOLDS.items():
        if max(hourlyprecip_next_24_hrs) < threshold:
            return intensity

def get_first_day_hourly_rainfall(daily_data):
    return daily_data[0]['hourlyprecip_mm']

def get_all_hourly_rainfall(daily_data):
    return reduce(lambda x, y: x + y, [day['hourlyprecip_mm'] for day in daily_data])

def get_forecast_data():
    weather_api_forecast_request = requests.get(WEATHER_API_BASE_URL + 'forecast.json', params={
        'key': settings.WEATHER_API_KEY,
        'lang': get_language(),
        'q': LOCATION,
        'days': 7,
    })

    if not weather_api_forecast_request.ok:
        raise Exception('Failed to fetch weather data')

    forecast_data = weather_api_forecast_request.json()
    forecast_by_day  = forecast_data['forecast']['forecastday']

    local_time = datetime.strptime(forecast_data['location']['localtime'], '%Y-%m-%d %H:%M')

    return local_time, [{
            'date': day['date'],
            # 'totalprecip_mm': day['day']['totalprecip_mm'],
            'hourlyprecip_mm': [hour['precip_mm'] for hour in day['hour']],
            # 'hourly_chance_of_rain': [hour['chance_of_rain'] for hour in day['hour']],
            # 'will_it_rain': day['day']['daily_will_it_rain'],
            # 'daily_code': day['day']['condition']['code'],
            # 'hourly_code': [hour['condition']['code'] for hour in day['hour']],
            # 'daily_text': day['day']['condition']['text'],
            # 'hourly_text': [hour['condition']['text'] for hour in day['hour']]
        } for day in forecast_by_day]

def get_rainfall_next_24hrs(local_time, precipation_forecast_data):
    hourlyprecip_today, hourlyprecip_tomorrow = precipation_forecast_data[0]['hourlyprecip_mm'], precipation_forecast_data[1]['hourlyprecip_mm']
    return hourlyprecip_today[local_time.hour:] + hourlyprecip_tomorrow[:local_time.hour]

def get_history_data(local_time):
    weather_api_history_request = requests.get(WEATHER_API_BASE_URL + 'history.json', params={
        'key': settings.WEATHER_API_KEY,
        'lang': get_language(),
        'q': LOCATION,
        'dt': (local_time - timedelta(days=1)).strftime('%Y-%m-%d'),
    })

    if not weather_api_history_request.ok:
        print(weather_api_history_request.json())
        raise Exception('Failed to fetch weather data')

    history_data = weather_api_history_request.json()

    return [{
        'date': history_data['forecast']['forecastday'][0]['date'],
        'hourlyprecip_mm': [hour['precip_mm'] for hour in history_data['forecast']['forecastday'][0]['hour']]
    }]

def get_rainfall_duration(hourly_rainfall):
    for i, rainfall in enumerate(hourly_rainfall):
        if not rainfall:
            return i

    return len(hourly_rainfall)

def index(request):
    if get_language() not in IMPLEMENTED_LANGUAGES:
        return render(request, 'language_not_available.xml', content_type='text/xml', status=404)

    try:
        local_time, forecast_data = get_forecast_data()
        history_data = get_history_data(local_time)
        
        # Previous 24 hours rainfall intensity
        rainfall_today            = get_first_day_hourly_rainfall(forecast_data)
        rainfall_yesterday        = get_first_day_hourly_rainfall(history_data)
        rainfall_past_24hrs       = rainfall_yesterday[local_time.hour:] + rainfall_today[:local_time.hour]
        history_intensity_rating  = get_precipitation_intensity(rainfall_past_24hrs)

        # Next 24 hours rainfall intensity
        rainfall_next_24hrs       = get_rainfall_next_24hrs(local_time, forecast_data)
        forecast_intensity_rating = get_precipitation_intensity(rainfall_next_24hrs)

        # Rainfall duration
        hourly_rainfall_from_now = get_all_hourly_rainfall(forecast_data)[local_time.hour:]
        rainfall_duration_hours = get_rainfall_duration(hourly_rainfall_from_now)

        rainfall_duration_friendly_text = ngettext(
            "%(count)d hour",
            "%(count)d hours",
            rainfall_duration_hours
        ) % { 'count': rainfall_duration_hours }
    except Exception as e:
        return render(request, 'error.xml', content_type='text/xml', status=500)

    return render(request, 'index.xml', {
        'rainfall_intensity_today': forecast_intensity_rating,
        'rainfall_intensity_yesterday': history_intensity_rating,
        'rainfall_duration': rainfall_duration_friendly_text,
        'FEEDBACK_URI': f'{settings.HOST}/{get_language()}/feedback'
    }, content_type='text/xml')
