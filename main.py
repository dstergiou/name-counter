import os
from collections import Counter

import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.hibob.com/v1/people"


def get_data_from_hibob(api_url: str = API_URL) -> list:
    headers = {
        'Authorization': os.getenv("API_KEY")
    }

    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["employees"]

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.ConnectTimeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def create_plot(results: list) -> None:
    names = list(results.keys())
    values = list(results.values())

    plt.bar(range(len(results)), values, tick_label=names)
    plt.xlabel("Names")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.title("Name Frequency")
    plt.show()


def create_frequency_list(data: list) -> list:
    names = []
    for entry in data:
        if "firstName" in entry:
            names.append(entry["firstName"])

    return names


if __name__ == "__main__":
    data = get_data_from_hibob()
    frequency = create_frequency_list(data=data)
    results = dict(Counter(frequency).most_common(10))

    create_plot(results=results)
