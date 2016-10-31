import requests
import datetime
from pytz import timezone


def get_number_of_pages(url):
    return requests.get(url).json()['number_of_pages']


def get_list_of_attempts(number_of_pages, url):
    attempts = []
    for number_of_page in range(1, number_of_pages):
        page = {'page': number_of_page}
        response = requests.get(url, params=page).json()['records']
        for item in range(1, len(response)):
            attempts.append(response[item])
    return attempts


def get_midnighters(attempts):
    midnighters = set()
    midnight = datetime.time(0)
    morning = datetime.time(6)
    existing_timestamp = filter(lambda x: x['timestamp'] is not None, attempts)
    for attempt in existing_timestamp:
        tz = timezone(attempt['timezone'])
        srv_time = attempt['timestamp']
        user_time = tz.localize(datetime.datetime.fromtimestamp(srv_time))
        if midnight < user_time.time() < morning:
            midnighters.add(attempt['username'])
    return midnighters


if __name__ == '__main__':
    url = 'http://devman.org/api/challenges/solution_attempts/'
    number_of_pages = get_number_of_pages(url)
    attempts = get_list_of_attempts(number_of_pages, url)
    print (get_midnighters(attempts))
