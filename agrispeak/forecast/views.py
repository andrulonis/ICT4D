from django.http import HttpResponse
from django.shortcuts import render

from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.conf import settings

import requests
from datetime import datetime
import math
from pprint import pprint

WEATHER_API_URL='http://api.weatherapi.com/v1/forecast.json'
LOCATION = 'Burkina Faso'


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


def index(request):
    weather_api_request = requests.get(WEATHER_API_URL, params={
        'key': settings.WEATHER_API_KEY,
        'lang': get_language(),
        'q': LOCATION,
        'days': 2,
        })

    if not weather_api_request.ok:
        return render(request, 'error.xml', content_type='text/xml'), 500
    else:
        weather_api_data = weather_api_request.json()
        forecast_by_day  = weather_api_data['forecast']['forecastday']


        precipation_data = [{
                'date': day['date'],
                'totalprecip_mm': day['day']['totalprecip_mm'],
                'hourlyprecip_mm': [hour['precip_mm'] for hour in day['hour']],
                'hourly_chance_of_rain': [hour['chance_of_rain'] for hour in day['hour']],
                'will_it_rain': day['day']['daily_will_it_rain'],
            } for day in forecast_by_day]
        pprint(precipation_data)

        local_time = datetime.strptime(weather_api_data['location']['localtime'], '%Y-%m-%d %H:%M')

        hourlyprecip_today, hourlyprecip_tomorrow = precipation_data[0]['hourlyprecip_mm'], precipation_data[1]['hourlyprecip_mm']
        hourlyprecip_next_24_hrs = hourlyprecip_today[local_time.hour:] + hourlyprecip_tomorrow[:local_time.hour]

        intensity_rating = get_precipitation_intensity(hourlyprecip_next_24_hrs)

    return render(request, 'index.xml', {
        'rainfall_intensity_today': intensity_rating
    }, content_type='text/xml')
