import requests
import datetime
from pytz import timezone


def get_number_of_pages(url):
    return requests.get(url).json()['number_of_pages']


def get_records(number_of_pages, url):
    paged_list = []
    for number_of_page in range(1, number_of_pages):
        key = {'page': number_of_page}
        response = requests.get(url, params=key).json()['records']
        paged_list.append(response)
    return paged_list


def get_attempts(paged_list):
    list_attempts = []
    for item in paged_list:
        list_attempts.extend(item)
    return list_attempts


def get_midnighters(attempts):
    midnighters = set()
    midnight = datetime.time(0)
    morning = datetime.time(6)
    for attempt in attempts:
        if attempt['timestamp']:
            tz = timezone(attempt['timezone'])
            srv_time = attempt['timestamp']
            user_time = tz.localize(datetime.datetime.fromtimestamp(srv_time))
            if midnight < user_time.time() < morning:
                midnighters.add(attempt['username'])
    return midnighters

if __name__ == '__main__':
    url = 'http://devman.org/api/challenges/solution_attempts/'
    number_of_pages = get_number_of_pages(url)
    paged_list = get_records(number_of_pages, url)
    attempts = get_attempts(paged_list)
    print (get_midnighters(attempts))
