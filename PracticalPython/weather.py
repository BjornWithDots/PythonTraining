# Note you need to run 'pip install requests' to use the requests module
import requests

def read_credentials(fpath):
    #reads first line of a path
    fo= open(fpath, "r")
    return fo.readline()

def get_weather_desc_and_temp():
    api_key = read_credentials(f'credentials/openweathermap.txt')
    city = 'Borås'
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key + "&units=metric"
    request = requests.get(url)

    json = request.json()

    description = json.get("weather")[0].get("description")
    temp_min = json.get("main").get("temp_min")
    temp_max = json.get("main").get("temp_max")

    return {'description': description,
            'temp_min': temp_min,
            'temp_max': temp_max}


# Print the results
def main():
    weather_dict = get_weather_desc_and_temp()
    print("Today's forecast is", weather_dict.get('description'))
    print("Lowest temp:", weather_dict.get('temp_min'), "and highest temp:", weather_dict.get('temp_max'))


main()
