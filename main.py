from ast import Delete
import string
import requests
import json
import sys
import os 
import time
import itertools
import threading
import datetime
import numpy

def reqCity():
    city = input('What city to fetch?\n').replace(' ', '%20', -1)
    city = city.title()
    if len(city) > 0:
        return city
    else:
        print('You need')

def startLoad():
    load = threading.Thread(target=loading)
    load.start()

def loading():
    for i in itertools.cycle(['|', '/', '-', '\\']):
        if fetched:
            if os.name =='nt':
                os.system('cls')
            else:
                os.system('clear')
            break
        sys.stdout.write(f'\rSearching ' + i)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r')

def cityInfoURL(geocodingURL, cityName):
    cityInfoURL = f'{geocodingURL}?name={cityName}&count=1'
    return(cityInfoURL)

def fURL(forecastURL, fetchedLongitude, fetchedLatitude):
    forecastURL = f'{forecastURL}?timezone=auto&latitude={fetchedLatitude}&longitude={fetchedLongitude}&current_weather=true&hourly=relativehumidity_2m,apparent_temperature,surface_pressure,pressure_msl'
    return(forecastURL)

def aQURL(airQualityURL, fetchedLongitude, fetchedLatitude):
    airQualityURL = f'{airQualityURL}?timezone=auto&latitude={fetchedLatitude}&longitude={fetchedLongitude}&hourly=uv_index'
    return(airQualityURL)

def fetch(cityInfoURL):

    response = requests.get(cityInfoURL)
    json_data = response.json() if response and response.status_code == 200 else None
    return json_data

def cIData(fetchData):
    fetchedCityName = fetchData['results'][0]['name']
    fetchedCountryName = fetchData['results'][0]['country']
    fetchedLatitude = fetchData['results'][0]['latitude']
    fetchedLongitude = fetchData['results'][0]['longitude']
    fetchedTimezone = fetchData['results'][0]['timezone']
    fetchedPopulation = fetchData['results'][0]['population']
    return fetchedCityName, fetchedCountryName, fetchedLatitude, fetchedLongitude, fetchedTimezone, fetchedPopulation

def forecastData(fetchData):
    fetchedTemperature = fetchData['current_weather']['temperature']
    fetchedWindSpeed = fetchData['current_weather']['windspeed']
    fetchedWindDirection = fetchData['current_weather']['winddirection']
    fetchedWeatherCode = fetchData['current_weather']['weathercode']
    fetchedHumidity = fetchData['hourly']['relativehumidity_2m']
    fetchedRealFeel = fetchData['hourly']['apparent_temperature']
    fetchedSurfacePressure = fetchData['hourly']['surface_pressure']
    fetchedSealevelPressure = fetchData['hourly']['pressure_msl']

    #current humidity for the day
    fetchedHumidityCurrent = fetchedHumidity[datetime.datetime.now().hour]
    fetchData['hourly']['relativehumidity_2m'] = fetchedHumidityCurrent
    fetchedRealFeelCurrent = fetchedRealFeel[datetime.datetime.now().hour]

    fetchData['hourly']['apparent_temperature'] = fetchedRealFeelCurrent
    fetchedSurfacePressureCurrent = fetchedSurfacePressure[datetime.datetime.now().hour]
    fetchData['hourly']['surface_pressure'] = fetchedSurfacePressureCurrent
    fetchedSealevelPressureCurrent = fetchedSealevelPressure[datetime.datetime.now().hour]
    fetchData['hourly']['pressure_msl'] = fetchedSealevelPressureCurrent

    Delete(fetchData['hourly']['time'])

    return(fetchedTemperature, fetchedWindSpeed, fetchedWindDirection, fetchedWeatherCode, fetchedHumidityCurrent, fetchedRealFeelCurrent, fetchedSurfacePressureCurrent, fetchedSealevelPressureCurrent)

def airQualityData(fetchData):
    fetchedUVIndex = fetchData['hourly']['uv_index']
    fetchedUVIndexMax = maxUV(fetchedUVIndex)
    fetchData['hourly']['uv_index'] = fetchedUVIndexMax
    Delete(fetchData['hourly']['time'])
    return fetchedUVIndexMax

def maxUV(fetchedUVIndex):
    i = 0
    fetchedUVIndexMax = 0
    while i < 24:
        if fetchedUVIndex[i] > fetchedUVIndexMax:
            fetchedUVIndexMax = fetchedUVIndex[i]
        i += 1
    return fetchedUVIndexMax

def weatherCode(code):
    code = int(code)
    code = str(code)
    if code == '0':
        return 'Clear Sky'
    elif code ==  '1':
        return 'Mainly Clear'
    elif code ==  '2':
        return 'Partly Cloudy'
    elif code ==  '3':
        return 'Overcast'
    elif code ==  '45':
        return 'Fog'
    elif code ==  '48':
        return 'Depositing Rime Fog'
    elif code ==  '51':
        return 'Light Drizzle'
    elif code ==  '53':
        return 'Moderate Drizzle'
    elif code ==  '55':
        return 'Dense Drizzle'
    elif code ==  '56':
        return 'Light Freezing Drizzle'
    elif code ==  '57':
        return 'Dense Freezing Drizzle'
    elif code ==  '61':
        return 'Slight Rain'
    elif code ==  '63':
        return 'Moderate Rain'
    elif code ==  '65':
        return 'Heavy Rain'
    elif code ==  '66':
        return 'Light Freezing Rain'
    elif code ==  '67':
        return 'Heavy Freezing Rain'
    elif code ==  '71':
        return 'Slight Snow Fall'
    elif code ==  '73':
        return 'Moderate Snow Fall'
    elif code ==  '75':
        return 'Heavy Snow Fall'
    elif code ==  '77':
        return 'Snow Grains'
    elif code ==  '80':
        return 'Slight Rain Showers'
    elif code ==  '81':
        return 'Moderate Rain Showers'
    elif code ==  '82':
        return 'Violent Rain Showers'
    elif code ==  '85':
        return 'Slight Snow Showers'
    elif code ==  '86':
        return 'Heavy Snow Showers'
    elif code ==  '95':
        return 'Thunderstorm'
    elif code ==  '96':
        return 'Thunderstorm With Light Hail'
    elif code ==  '99':
        return 'Thunderstorm With Heavy Hail'

def output(fetchedCityName, fetchedCountryName, fetchedLatitude, fetchedLongitude, fetchedTimezone, fetchedPopulation, fetchedTemperature, fetchedWindSpeed, fetchedWindDirection, weatherCode, fetchedHumidityCurrent, fetchedRealFeelCurrent, fetchedSurfacePressureCurrent, fetchedSealevelPressureCurrent, fetchedUVIndexMax):
    print(f'City: {fetchedCityName}')
    print(f'Country: {fetchedCountryName}')
    print(f'Latitude: {fetchedLatitude}')
    print(f'Longitude: {fetchedLongitude}')
    print(f'Timezone: {fetchedTimezone}')
    print(f'Population: {fetchedPopulation}')
    print(f'Temperature: {fetchedTemperature} °C')
    print(f'Wind Speed: {fetchedWindSpeed}')
    print(f'Wind Direction: {fetchedWindDirection}')
    print(f'Weather Condition: {weatherCode}')
    print(f'Humidity: {fetchedHumidityCurrent}')
    print(f'Real Feel: {fetchedRealFeelCurrent}')
    print(f'Surface Pressure: {fetchedSurfacePressureCurrent}')
    print(f'Sea Level Pressure: {fetchedSealevelPressureCurrent}')
    print(f'UV Index: {fetchedUVIndexMax}')


#load vars
fetched = False
geocodingURL = 'https://geocoding-api.open-meteo.com/v1/search'
forecastURL = 'https://api.open-meteo.com/v1/forecast'
airQualityURL = 'https://air-quality-api.open-meteo.com/v1/air-quality'

cityName = reqCity()

startLoad()

fetched = True
fetchedCityName, fetchedCountryName, fetchedLatitude, fetchedLongitude, fetchedTimezone, fetchedPopulation = cIData(fetchData=fetch(cityInfoURL(geocodingURL, cityName)))
fetchedTemperature, fetchedWindSpeed, fetchedWindDirection, fetchedWeatherCode, fetchedHumidityCurrent, fetchedRealFeelCurrent, fetchedSurfacePressureCurrent, fetchedSealevelPressureCurrent = forecastData(fetch(fURL(forecastURL, fetchedLongitude, fetchedLatitude)))
fetchedUVIndexMax = airQualityData(fetch(aQURL(airQualityURL, fetchedLongitude, fetchedLatitude)))
weatherCode = weatherCode(fetchedWeatherCode)
output(fetchedCityName, fetchedCountryName, fetchedLatitude, fetchedLongitude, fetchedTimezone, fetchedPopulation, fetchedTemperature, fetchedWindSpeed, fetchedWindDirection, weatherCode, fetchedHumidityCurrent, fetchedRealFeelCurrent, fetchedSurfacePressureCurrent, fetchedSealevelPressureCurrent, fetchedUVIndexMax)
