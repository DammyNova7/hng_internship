#!/usr/bin/python3

#importing modules
from flask import Flask, request, jsonify
from collections import OrderedDict
import requests


app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def get_endpoint():
    visitor_name = request.args.get('visitor_name')

    try:
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip.startswith('127.0.0.1'):
            client_ip = requests.get('https://api.ipify.org').text
    except:
        visitor_ip = "Unable to get IP"

    try:
        location_info = requests.get(f"https://ipapi.co/{client_ip}/json/").json()
        city = location_info.get('city', 'Unknown')

        weather_api_key = '2cd8bb028638cff45e4cb2c285a26a90'
        weather_info = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric").json()
        temperature = round(weather_info['main']['temp']) if 'main' in weather_info else "Not available"
    except requests.RequestException as e:
        location_info = {"error": "Unable to fetch location data"}

    greeting = f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {city}"

    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    }
    
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
