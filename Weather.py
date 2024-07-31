# a simple program that gives weather data based on inputted location
import requests
import time

# https://home.openweathermap.org/api_keys
API_KEY = "46b6aba9416e4c037d9432162d5019ec"


# main code
def main():
    print(
        "\nThis program provides real-time weather data based on your location/city.\n"
    )
    time.sleep(1)
    print(
        "Please note, the city or country name that you input might not be recognised by the weather service."
    )
    print("The data returned might be based on a similar city/country name found.\n")
    time.sleep(2)

    # prompts the user for input
    city = input("Kindly enter the name of your city and press enter: ").strip().title()
    if city.isnumeric():
        print("Please input valid city name! ")

        time.sleep(1)
        input("\nPress any key to exit...")
        exit()

    print("\nPlease wait... \n\n")

    # calls the get_weather function to get weather data
    get_weather(city)


# a function that returns weather data by accepting city name as an argument
def get_weather(city):
    try:
        # gets weather data from OpenWeatherMap
        weather_data = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        )
        final_weather_data = weather_data.json()

        # extracts country code and converts it to country name
        country_code = final_weather_data["sys"]["country"]
        country_json = requests.get(
            f"https://restcountries.com/v3/alpha/{country_code}"
        )
        country_name = country_json.json()[0]["name"]["common"]

        # prints the overall weather conditions
        print(f"Displaying weather data for {city} (Country: {country_name})\n")
        print(f"Weather: {final_weather_data["weather"][0]["main"]}")

        # collects important weather values in the form of a dictionary
        data_dict = final_weather_data["main"]

        temperature = round((data_dict["temp"] - 273.15), 1)
        feels_like = round((data_dict["feels_like"] - 273.15), 1)
        humidity = data_dict["humidity"]

        # collects wind data
        wind_data = final_weather_data["wind"]

        wind_speed = round(wind_data["speed"], 1)
        wind_direction_value = wind_data["deg"]

        wind_direction = wind_calc(wind_direction_value)

        # prints all the collected data
        print(f"Temperature: {temperature}°C")
        print(f"Feels like: {feels_like}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind speed: {wind_speed} m/s")
        print(f"Wind direction: {wind_direction_value}° ({wind_direction})")

    # prompts the user if there is a connection error
    except requests.exceptions.ConnectionError:
        print(
            "Connection Error. Please make sure you have a valid internet connection."
        )
        time.sleep(1)
        input("\nPress any key to exit...")
        exit()

    except KeyError:
        print("No data found. Perhaps you entered the wrong city name?")
        time.sleep(1)
        input("\nPress any key to exit...")
        exit()

    # prompts user to exit the program once data is displayed
    time.sleep(2)
    input("\nPress any key to exit...")


# calculates cardinal or inter-cardinal wind direction
def wind_calc(deg):
    wind_direction = ""
    if 338 <= deg <= 360 or 0 <= deg <= 22:
        wind_direction = "North"
    elif 23 <= deg <= 67:
        wind_direction = "North-east"
    elif 68 <= deg <= 112:
        wind_direction = "East"
    elif 113 <= deg <= 157:
        wind_direction = "South-east"
    elif 158 <= deg <= 202:
        wind_direction = "South"
    elif 203 <= deg <= 247:
        wind_direction = "South-west"
    elif 248 <= deg <= 292:
        wind_direction = "West"
    elif 293 <= deg <= 337:
        wind_direction = "North-west"

    return wind_direction


if __name__ == "__main__":
    main()
