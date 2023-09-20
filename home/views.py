from django.shortcuts import render
import requests
from home.models import City
from .forms import CityForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from django.core.serializers import serialize 
import json


def home_view(request):
    template = "index.html"
    context = {
        "failed": True,
    }
    try:
        if request.method == "GET":
            form = CityForm(request.GET)
            if form.is_valid():
                data = form.cleaned_data
                field = data['city']
                cities = City.objects.filter(pk__icontains=field)
                city = cities.first()
                response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={city.lat}&longitude={city.lng}&current_weather=true")
            else:
                form = CityForm()
        response_object = response.json()
        flag = True
    except Exception:
        context["message"] = "Please enter a city name"
        flag = False

    
    try:
        if flag:
            context = {
                "failed": False,
                "city": city.name,
                "country": city.country_name,
                'latitude': response_object['latitude'],
                'longitude': response_object['longitude'],
                'timezone': response_object['timezone'],
                'elevation': response_object['elevation'],
                'temperature': response_object['current_weather']['temperature'],
                'windspeed': response_object['current_weather']['windspeed'],
                'winddirection': response_object['current_weather']['winddirection'],
                'is_day': response_object['current_weather']['is_day'],
                'date': response_object['current_weather']['time'][:10],
            }
    except Exception:
        context["message"] = "Failed to get weather data"

    return render(request, template, context)

class api_view(APIView):
    def get(self, request):
        city_name = request.GET.get('city')
        full_data = request.GET.get('full_data')
        if (city_name is not None) and (city_name != "") and (len(city_name) > 0):
            cities = City.objects.filter(pk__icontains=city_name)
            if full_data == "full":
                city = cities.first()
                response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={city.lat}&longitude={city.lng}&daily=weathercode,temperature_2m_max,temperature_2m_min,rain_sum,precipitation_probability_max&current_weather=true&timezone=GMT&forecast_days=5")
                response_object = response.json()
                output = {
                    "name": city.name,
                    "iso": city.iso,
                    'latitude': response_object['latitude'],
                    'longitude': response_object['longitude'],
                    'timezone': response_object['timezone'],
                    'elevation': response_object['elevation'],
                    'temperature': response_object['current_weather']['temperature'],
                    'windspeed': response_object['current_weather']['windspeed'],
                    'winddirection': response_object['current_weather']['winddirection'],
                    'date': response_object['current_weather']['time'][:10],
                    'past_forcast_dates': response_object['daily']['time'],
                    'past_forcast_max': response_object['daily']['temperature_2m_max'],
                    'past_forcast_min': response_object['daily']['temperature_2m_min'],
                    'precipitation_probability_max': response_object['daily']['precipitation_probability_max'],
                    'weathercode': response_object['daily']['weathercode'],
                }
                return Response(output)
            else:
                if len(cities) >= 5:
                    cities = cities[0: 6]               
                output = [
                    {
                        "name": output.name,
                        "iso": output.iso
                    }
                    for output in cities
                ]
                return Response(output[0: 10])
        else: return Response([])

def add_data_view(request):
    from home.models import City
    import json
    template = "index.html"

    with open('worldcities.json', 'r') as f:
        data = json.load(f)

    i = 0
    for key, value in data.items():
        i+=1
        city = City(name=key, country_name=value["country"], lat=value["lat"], lng=value["lng"], iso=value["iso"])
        city.save()
        print(f"{(i/len(data.items())) * 100}%")

    return render(request, template, {"failed": True})
    