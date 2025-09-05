"""
Movie information retrieval module.

This module connects to the OMDb API to fetch movie details such as title,
release year, rating, and poster URL. The API key is securely loaded from
environment variables using a `.env` file.

Functions:
    get_movie_info(title): Fetch details for a movie by its title.
"""


import os
import requests
from dotenv import load_dotenv


API_URL = "http://www.omdbapi.com/?t="
CONNECT_TIMEOUT = 5  # seconds
READ_TIMEOUT = 10  # seconds
ENCODING = "utf-8"


def get_movie_info(title):
    """Fetch movie details (title, year, rating, poster) from the API by title."""
    try:
        # Load environment variables from .env
        load_dotenv()
        response = requests.get(f"{API_URL + title}&apikey={os.getenv('API_KEY')}",
                                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
        response.encoding = ENCODING
        data = response.json()

        # Check if API response was successful
        if data.get("Response") == "False":
            print(f"API error: {data.get('Error', 'Unknown error')}")
            return None
        return (data['Title'], data['Director'], int(data['Released'][-4:]), data['Poster'])
    except requests.exceptions.Timeout:
        print("The API request timed out")
    except (KeyError, IndexError, ValueError) as error:
        print(f"Data parsing error: {error}")
    except requests.RequestException as error:
        print(f"Request error: {error}")
    return None


if __name__ == "__main__":
    print(get_movie_info("Braveheart"))
