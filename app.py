#!/usr/bin/python3

#importing modules
from flask import Flask, request, jsonify
import requests


app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def get_endpoint():
    name = request.args.get('name')

    try:
        visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if visitor_ip.startswith('127.0.0.1'):
            visitor_ip = requests.get('https://api.ipify.org').text
    except:
        visitor_ip = "Unable to get IP"

    try:
        location_info = requests.get(f"https://ipinfo.io/{visitor_ip}/json").json()
        city = location_info.get('city', 'Unknown')

        weather_api_key = '2cd8bb028638cff45e4cb2c285a26a90'
        weather_info = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric").json()
        temperature = weather_info['main']['temp'] if 'main' in weather_info else "Not available"
        greeting = f"Hello, {name}! The temperature is {temperature} degrees Celsius in {city}"

        response = {
            'client ip': visitor_ip,
            'location': city,
            'greeting': greeting
        }
    except requests.RequestException as e:
        location_info = {"error": "Unable to fetch location data"}

    
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
