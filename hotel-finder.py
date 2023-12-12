import requests
import json
import pprint

url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

destination = input("Please enter in your destination: ") 
querystring = {"name":destination,"locale":"en-us"}

headers = {
    "X-RapidAPI-Key": "2e3a55f731msh0a13c92a6e237d9p1c9e76jsnd2021b8be4f4",
    "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

if response.status_code == 200:
    data = json.loads(response.text)
    size = len(data)
    options = 0
    for i in range(size):
        type = data[i]['dest_type']
        if type == 'city':
            options = options+1
    #print("There are ", options ," locations with this name. Which location are you looking for?")
    #for i in range(size): 
    #    type = data[i]['dest_type']   
    #    if type == 'city':
            #country = data[i]['country']
            #print("One location is in " + country)
        ##pprint.pprint(data)
    #answer = input("Enter the country in which your city is in: ")
    answer = 'United States'
    for i in range(size):
        if data[i]['country'] == answer and data[i]['dest_type'] == 'city':
            destID = data[i]['dest_id']
else:
    print(f"Error: {response.status_code}")

print(destID)


url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

querystring = {"checkin_date":"2023-09-27","dest_type":"city","units":"metric","checkout_date":"2023-09-28","adults_number":"2","order_by":"price","dest_id":destID,"filter_by_currency":"USD","locale":"en-us","room_number":"1"}

headers = {
    "X-RapidAPI-Key": "2e3a55f731msh0a13c92a6e237d9p1c9e76jsnd2021b8be4f4",
    "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

if response.status_code == 200:
    data = json.loads(response.text)
    size = len(data['result'])
    print("Here are ", size ," available Hotels in the Area: ")
    for i in range(size):
        name = data['result'][i]['hotel_name']
        price = data['result'][i]['price_breakdown']['gross_price']
        address = data['result'][i]['address'] + " " + data['result'][i]['zip']
        photo = data ['result'][i]['max_photo_url']
        print("name: " + name + " Address: " + address + " Average Price: " + str(price) + photo)
else:
    print(f"Error: {response.status_code}")
#pprint.pprint(data)



