import googlemaps
import pprint
import time
import requests,json

city = input("Please enter in the city: ")

apikey = "AIzaSyAdxLALmR710RguCaLq3E7UmsHCe_cHPIc"

url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

query = "Activities in " + city

res = requests.get(url + 'query=' + query + '&key=' + apikey)

x = res.json()

y = x['results']

for i in range(len(y)):
    print(y[i]['name'])
