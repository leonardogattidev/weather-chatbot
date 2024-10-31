import logging
import os
import httpx
from openai import OpenAI


def get_weather(city_name) -> str:
    api_key = os.getenv("WEATHER_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        response = httpx.get(url)
        json = response.json()
        error = json.get("message")
        if error and "not found" in error:
            return f'We couldn\'t find "{city_name}" as a city.'
        return human_readable_weather(json)
    except httpx.RequestError as e:
        logging.error(f"Error while requesting {e.request.url}", exc_info=True)
        return "Something went wrong while fetching weather data."


def human_readable_weather(data: str) -> str:
    # TODO: avoid instantiating a new openai client for each call
    # (connection/client pooling? though its a single client)
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
    response = completion.choices[0].message.content
    assert response, "Non-null response was expected from OpenAI"
    return response
