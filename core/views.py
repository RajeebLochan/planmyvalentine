from django.shortcuts import render
from django.http import Http404
from .prompts import CITY_SUGGESTIONS, generate_city_experience


def _build_city_list(filter_fn=None):
    """Build a list of city dicts from CITY_SUGGESTIONS, optionally filtered."""
    cities = []
    for slug, data in CITY_SUGGESTIONS.items():
        if filter_fn and not filter_fn(data):
            continue
        cities.append({
            'slug': slug,
            'display_name': data['display_name'],
            'tagline': data['tagline'],
            'hero_emoji': data.get('hero_emoji', '💕'),
            'romantic_desc': data['romantic_desc'],
            'state': data.get('state', ''),
        })
    return cities


METRO_STATES = {'Delhi', 'Maharashtra', 'Karnataka', 'West Bengal', 'Telangana', 'Tamil Nadu', 'Gujarat', 'Uttar Pradesh', 'Chandigarh', 'Punjab'}
GETAWAY_STATES = {'Rajasthan', 'Himachal Pradesh', 'Uttarakhand', 'Goa', 'Puducherry', 'Kerala', 'Jammu & Kashmir', 'Ladakh', 'Andaman & Nicobar'}


def home(request):
    """Landing page with three main options"""
    odisha_cities = _build_city_list(lambda d: d.get('state') == 'Odisha')
    metro_cities = _build_city_list(lambda d: d.get('state') in METRO_STATES)
    getaway_cities = _build_city_list(lambda d: d.get('state') in GETAWAY_STATES)
    all_cities = _build_city_list()
    return render(request, 'home.html', {
        'cities': all_cities,
        'odisha_cities': odisha_cities,
        'metro_cities': metro_cities,
        'getaway_cities': getaway_cities,
    })


def city_landing(request, city_slug):
    """City-specific Valentine experience landing page"""
    city_data = CITY_SUGGESTIONS.get(city_slug)
    if not city_data:
        raise Http404("City not found")

    experience = generate_city_experience(city_slug)

    context = {
        'city': city_data,
        'city_slug': city_slug,
        'experience': experience,
    }
    return render(request, 'city.html', context)

