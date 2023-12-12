import datetime
import json
import os

import requests
import FlaskCode

from FlaskCode import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, flash, session
from flask_mail import Message, Mail
from .forms import ContactForm
from flask import request, redirect, url_for
from flaskext.mysql import MySQL
from builtins import float

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
googleMapsApiKey = os.getenv('googleMapsApiKey')
hotelkey =  os.getenv('hotelkey')

#from flight_prices import flightPrices
import FlaskCode.Weather as Weather
import FlaskCode.flight_prices as FlightPrices
@app.template_filter('format_datetime')
def format_datetime(value, format='%B %d, %Y at %I:%M %p'):
    dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    return dt.strftime(format)

@app.template_filter('format_datetime2')
def format_datetime2(value, format='%Y-%m-%d'):
    dt = datetime.strptime(value, '%Y-%m-%d')
    return dt.strftime(format)


@app.template_filter('format_price')
def format_price(value, currency_symbol='$', decimal_places=2):
    return f"{currency_symbol}{value:,.{decimal_places}f}"

@app.template_filter('format_duration')
def format_duration(value):
    hours = value // 60
    minutes = value % 60
    return f"{hours}h {minutes}m"

    
mysql = MySQL(app)

affil_id = 'gad50onewayflighticaocode'
apikey = 'so12lCy6yDiAwVdJHol-O-I5fotLVa5k'

#The mail_user_name and mail_app_password values are in the .env file
#Google requires an App Password as of May, 2022: 
#https://support.google.com/accounts/answer/6010255?hl=en&visit_id=637896899107643254-869975220&p=less-secure-apps&rd=1#zippy=%2Cuse-an-app-password


app.config['MAIL_PORT'] = 465


mail = Mail(app)
@app.route('/')
def home():
    return render_template('home.html',api_key=googleMapsApiKey)

@app.route('/Login', )
def Login():
  return render_template('Login.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    session['user_input'] = user_input
    return redirect(url_for('choice'))   

@app.route('/choice', methods=['POST'])
def choice():
    user_input = session.get('user_input')
    if user_input is None:
        return redirect(url_for('home'))
    return render_template('choice.html', user_input=user_input, api_key=googleMapsApiKey)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate input data
        if not name or not email or not password or not confirm_password:
            flash('Please fill in all fields')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        # Check if email already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            flash('Email already exists')
            return redirect(url_for('register'))

        # Create new user record in the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur.close()

        flash('Account created successfully')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/flight_info', methods=['POST','GET'])
def flight_info():
    return render_template('FlightInfo.html')


@app.route('/result', methods=['POST'])
def result():
    user_input = request.form.get('user_input')

    date = request.form.get('depart')
    date1= request.form.get('return')

    date_obj = datetime.strptime(date, '%Y-%m-%d')
    depart = date_obj.strftime('%Y-%m-%d')
    date_obj = datetime.strptime(date1, '%Y-%m-%d')
    return1 = date_obj.strftime('%Y-%m-%d')
    

    origin = request.form.get('origin')
    destination = request.form.get('destination')
    origin_city_name = origin
    dest_city_name = destination
    dest_weather = Weather.openWeather(destination)

    destination_dict = FlightPrices.search_airport(destination)
    destination_dict = destination_dict['PlaceId']    
    origin_dict = FlightPrices.search_airport(origin)
    origin_dict = origin_dict['PlaceId']

    adults = request.form.get('adults')
    children = request.form.get('children')
    infants = request.form.get('infants')

    sortby = request.form.get('sortBy')
    cabinClass = request.form.get('cabinClass')

    minPrice = request.form.get('minPrice')
    maxPrice = request.form.get('maxPrice')

    results = FlightPrices.flightPrices(origin,destination,origin_dict,destination_dict,depart,return1,adults,children,infants,cabinClass,sortby,maxPrice,minPrice)
    return render_template('flightPrice.html', flights=results, origin=origin, destination=destination,dest_weather=dest_weather, adults = adults,return1=return1,depart=depart,api_key=googleMapsApiKey, origin_city_name=origin_city_name, dest_city_name=dest_city_name)



@app.route('/act', methods=['POST'])
def act():
    user_input = request.form.get('act_input')
    print(user_input)
    apikey = googleMapsApiKey
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    query = "Activities in " + user_input
    res = requests.get(url + 'query=' + query + '&key=' + apikey)
    x = res.json()
    y = x['results']
    #print(y)
    places = {}
    for result in y:
        name = result['name']
        address = result['formatted_address']
        place = {'name': name, 'address': address}
        places[name] = address

    print(places)

    data = [y[i]['name'] for i in range(len(y))]
    dest_weather = Weather.openWeather(user_input)
    return render_template('act.html', user_input=user_input, dest_weather=dest_weather, data=data,places=places,api_key=googleMapsApiKey)

@app.route('/hotels', methods=['GET', 'POST'])
def hotels():
    user_input = request.form.get('user_input')


    return render_template('hotel_info.html', user_input = user_input)

@app.route('/hotelResult', methods=['GET', 'POST']) 
def hotelResult():
    user_input = request.form.get('user_input')
    city_name = user_input
    adultNum = request.form.get('people')
    checkIn = request.form.get('checkIn')
    checkOut = request.form.get('checkOut')
    url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
    dest_weather = Weather.openWeather(user_input)
    querystring = {"name":user_input,"locale":"en-us"}

    headers = {
        "X-RapidAPI-Key": hotelkey,
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)
    size = len(data)
    print(data)
    options = 0
    for i in range(size):
        type = data[i]['dest_type']
        if type == 'city':
            options = options+1
        answer = 'United States'
        for i in range(size):
            if data[i]['country'] == answer and data[i]['dest_type'] == 'city':
                destID = data[i]['dest_id']
    
    session['destID'] = destID
    url2 = "https://booking-com.p.rapidapi.com/v1/hotels/search"

    querystring2 = {"checkin_date":checkIn,"dest_type":"city","units":"metric",
                   "checkout_date":checkOut,"adults_number":adultNum,"order_by":"price",
                   "dest_id":destID,"filter_by_currency":"USD","locale":"en-us","room_number":"1"}

   

    response = requests.request("GET", url2, headers=headers, params=querystring2)
    
    data = json.loads(response.text)
    size = len(data['result'])
    hotels = {}
    for i in range(size):
        name = data['result'][i]['hotel_name']
        price = data['result'][i]['price_breakdown']['gross_price']
        address = data['result'][i]['address'] + " " + data['result'][i]['zip']
        hotels[name] = city_name
    print(hotels)
    return render_template('hotels.html', data = data, user_input = user_input, checkIn = checkIn,
                            checkOut = checkOut, adultNum = adultNum , dest_weather=dest_weather, hotels=hotels,api_key= googleMapsApiKey, len =len)

@app.route('/book', methods=['POST'])
def book():
    flight_id = request.form.get('flight_id')
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    depart = request.form.get('departure')
    arrival = request.form.get('arrival')
    adults = request.form.get('adults')
    children = request.form.get('children')
    infants = request.form.get('infants')
    price = request.form.get('price')
    
    destination_dict = FlightPrices.search_airport(destination)
    destination = destination_dict['PlaceId']    
    origin_dict = FlightPrices.search_airport(origin)
    origin = origin_dict['PlaceId']
 
    
    depart = depart.split('T')[0]
    date_obj = datetime.strptime(depart, '%Y-%m-%d')
    depart = date_obj.strftime('%Y-%m-%d')
    arrival = arrival.split('T')[0]
    date_obj = datetime.strptime(arrival, '%Y-%m-%d')
    arrival = date_obj.strftime('%Y-%m-%d')
    url = FlightPrices.returnFlightUrl(flight_id,origin,destination,depart,arrival,adults,children,infants,price)
    print(url)
    return redirect(url)
