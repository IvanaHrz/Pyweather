import sqlite3
from flask import render_template,request,redirect,url_for
from Models.admin import Administrator
from Assets import DBcon
import json
import pandas
import matplotlib.pyplot as plt
import requests
import datetime



def setup(app):

    @app.route("/index")
    def index():
        return render_template("index.html")
  
    @app.route("/login",methods=["POST","GET"])
    def login():
        dbSession = DBcon.createSession()
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            admini = dbSession.query(Administrator).filter(Administrator.Email == email)
            if len(list(admini)) == 0:
                return render_template("login.html",message="Invalid email or password.")
            admin = admini[0]
            if admin.Password != password:
                return render_template("login.html",message="Invalid email or password.")
            return redirect(url_for("weather"))
        else:
            return render_template("login.html",message="")
 

    @app.route("/register",methods=["POST","GET"])
    def register():
        if request.method == "POST":
            dbSession = DBcon.createSession()
            name = request.form.get("name")
            surname = request.form.get("surname")
            email = request.form.get("email")
            password = request.form.get("password")
            newadmin = Administrator(Name = name,Surname = surname,Email = email, Password = password)
            dbSession.add(newadmin)
            dbSession.commit()
            return render_template("register.html",message="You have successfully registered.")
        
        return render_template("register.html",message="")
    
    @app.route("/users",methods=["GET"])
    def users():
        dbSession = DBcon.createSession()
        userQuery = dbSession.query(Administrator).all()
        return render_template("users.html",users = userQuery)
    
    @app.route("/history")
    def history():
        dataFrame = pandas.read_csv("./Assets/images/forecast.csv")
        dataFrame1 = pandas.read_csv("./Assets/images/archive2.csv")

        plt.figure(figsize=(10,6))
        plt.subplot(1,2,1)
        plt.title("March 2022.")
        plt.xlabel("Day")
        plt.ylabel("Temperature °C")
        plt.ylim(0,25)
        plt.plot(dataFrame["temperature_2m_max (°C)"],color="red")


        plt.subplot(1,2,2)
        plt.title("March 2023.")
        plt.xlabel("Day")
        plt.ylabel("Temperature °C")
        plt.ylim(0,25)
        plt.plot(dataFrame1["temperature_2m_max (°C)"],color="green")

        #plt.savefig("./Assets/images/Temp_in_march.png")
        #plt.show()
        return render_template("history.html")
    
    @app.route("/weather")
    def weather():
        my_lat = 45.815010 
        my_long = 15.981919
        parameters = {
            "latitude": my_lat,
            "longitude": my_long
            }
        response = requests.get("https://api.open-meteo.com/v1/forecast?hourly=relativehumidity_2m&daily=temperature_2m_max&daily=temperature_2m_min&daily=precipitation_sum&daily=weathercode&daily=windspeed_10m_max&daily=winddirection_10m_dominant&forecast_days=4&timezone=GMT",params=parameters)
        data = response.text
        file = json.loads(data)
        def get_weather_code(weather_code:int):
            if weather_code == 0:
                return "Clear sky"
            elif weather_code == 1:
                return "Mainly clear"
            elif weather_code == 2:
                return "Partly cloudy"
            elif weather_code == 3:
                return "Overcast"
            elif weather_code == 45:
                return "Fog"
            elif weather_code == 48:
                return "Depositing rime fog"
            elif weather_code == 51:
                return "Light drizzle"
            elif weather_code == 53:
                return "Moderate drizzle"
            elif weather_code == 55:
                return "Dense intensity drizzle"
            elif weather_code == 56:
                return "Light freezing drizzle"
            elif weather_code == 57:
                return "Dense intensity freezing drizzle"
            elif weather_code == 61:
                return "Slight rain"
            elif weather_code == 63:
                return "Moderate rain"
            elif weather_code == 65:
                return "Heavy intensity rain"
            elif weather_code == 66:
                return "Light freezing rain"
            elif weather_code == 67:
                return "Heavy intensity freezing rain"
            elif weather_code == 71:
                return "Slight snow fall"
            elif weather_code == 73:
                return "Moderate snow fall"
            elif weather_code == 75:
                return "Heavy intensity snow fall"
            elif weather_code == 80:
                return "Slight rain showers"
            elif weather_code == 81:
                return "Moderate rain showers"
            elif weather_code == 82:
                return "Violent rain showers"
            elif weather_code == 85:
                return "Slight snow showers"
            elif weather_code == 86:
                return "Heavy snow showers"
            elif weather_code == 95:
                return "Slight or moderate thunderstorm"
            elif weather_code == 96:
                return "Thunderstorm with slight hail"
            elif weather_code == 99:
                return "Thunderstorm with heavy hail"
            else: 
                return "Error"
        weather_code0 = int(file["daily"]["weathercode"][0])
        weather_code1 = int(file["daily"]["weathercode"][1])
        weather_code2 = int(file["daily"]["weathercode"][2])
        weather_code3 = int(file["daily"]["weathercode"][3])

        max_temp = int(file["daily"]["temperature_2m_max"][0])
        min_temp = int(file["daily"]["temperature_2m_min"][0])
        precipitation = int(file["daily"]["precipitation_sum"][0])
        humidity = int(file["hourly"]["relativehumidity_2m"][0])
        wind_speed = int(file["daily"]["windspeed_10m_max"][0])

        def wind(wind_direction:int):
            wind_direction = int(file["daily"]["winddirection_10m_dominant"][0]) 
            if wind_direction <20:
                return "N"
            elif wind_direction>=20 and wind_direction<65:
                return "NE"
            elif wind_direction>=65 and wind_direction<110:
                return "E"
            elif wind_direction>=110 and wind_direction<155:
                return "SE"
            elif wind_direction>=155 and wind_direction<200:
                return "S"
            elif wind_direction>=200 and wind_direction<245:
                return "SW"
            elif wind_direction>=245 and wind_direction<290:
                return "W"
            elif wind_direction>=290 and wind_direction<335:
                return "NW"
            else:
                return "N"
   
        def getweather_icon(weather_code0:int):
            if weather_code0 == 0:
                return "sun"
            elif weather_code0 == 1 or weather_code0 == 2:
                return "cloud_sun"
            elif weather_code0 >= 3 and weather_code0 <=48:
                return "cloud"
            elif weather_code0 >=51 and weather_code0 <=67:
                return "cloud_rain"
            elif weather_code0 >=71 and weather_code0 <=77:
                return "snow"
            elif weather_code0 >=80 and weather_code0 <=82:
                return "cloud_rain"
            elif weather_code0 ==85 or weather_code0 ==86:
                return "snow"
            else:
                return "thunderstorm"

        x = datetime.datetime.now()
        today = x.strftime("%A")
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        result = days[days.index(today)+1:] + days[:days.index(today)]
        max_temp1 = int(file["daily"]["temperature_2m_max"][1])
        max_temp2 = int(file["daily"]["temperature_2m_max"][2])
        max_temp3 = int(file["daily"]["temperature_2m_max"][3])
        return render_template("weather.html",today_weather=get_weather_code(weather_code0),t_weather1=get_weather_code(weather_code1),t_weather2=get_weather_code(weather_code2),t_weather3=get_weather_code(weather_code3),today_max=max_temp,today_min=min_temp,precipitation=precipitation,humidity=humidity,wind_speed = wind_speed,wind_direction=wind(wind_direction=True),tomorrow = result[0],tomorrow1=result[1],tomorrow2=result[2],today=today,tomorrow_temp=max_temp1,max_temp2=max_temp2,max_temp3=max_temp3,icon=getweather_icon(weather_code0))
        
    app.add_url_rule("/", "index", index)
    app.run(debug=True)