from django.shortcuts import render
from .models import City
import requests
from .forms import CityForm
def index(request):
    appid = '07e9aa153a225feafa7d0de0d739dce3'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if(request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm()  #Для очистки поля City после перезагрузки страницы

    cities = City.objects.all()

    all_cities = []
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        City_info = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'feels_like': res["main"]["feels_like"],
            'icon': res["weather"][0]["icon"],
            'wind': [res['wind']['speed'],res['wind']['speed']]
        }

        all_cities.append(City_info)

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather\index.html', context)

"""Example JSON from http://api.openweathermap.org/data/2.5/...
{"coord":{"lon":-0.1257,"lat":51.5085},"weather":[{"id":801,"main":"Clouds","description
":"few clouds","icon":"02d"}],"base":"stations","main":{"temp":285.26,"feels_like":284.3
8,"temp_min":283.71,"temp_max":286.48,"pressure":1007,"humidity":71},"visibility":10000,
"wind":{"speed":4.12,"deg":90},"clouds":{"all":20},"dt":1620719538,"sys":{"type":1,"id":
1414,"country":"GB","sunrise":1620706480,"sunset":1620761950},"timezone":3600,"id":26437
43,"name":"London","cod":200}
"""
