import os
import requests
from openai import OpenAI


def get_weather(city_name) -> str:
    api_key = os.getenv("WEATHER_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    json = response.json()
    print(json)
    error = json.get("message")
    if error and "not found" in error:
        return f'We couldn\'t find "{city_name}" as a city.'
    return human_readable_weather(json)


def human_readable_weather(data):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Discarding information irrelevant to someone who just wants a brief overview of the weather, transform the following weather data into human readable text: \n{data}\n",
            }
        ],
    )
    return completion.choices[0].message.content
