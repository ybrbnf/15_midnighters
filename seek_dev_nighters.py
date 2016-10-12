import requests
import datetime
from pytz import timezone


def load_attempts():
    url = 'http://devman.org/api/challenges/solution_attempts/'
    number_of_pages = requests.get(url).json()['number_of_pages']
    for page in range(1, number_of_pages):
        key = {'page': page}
        record = requests.get(url, params=key).json()['records']
        for item in record:
            yield item


def get_midnighters():
    users = set()
    midnight = datetime.time(0)
    morning = datetime.time(6)
    for item in data:
        if item['timestamp']:
            tz = timezone(item['timezone'])
            srv_time = item['timestamp']
            user_time = tz.localize(datetime.datetime.fromtimestamp(srv_time))
            if user_time.time() > midnight and user_time.time() < morning:
                users.add(item['username'])
    return users


if __name__ == '__main__':
    data = load_attempts()
    users = get_midnighters()
    print (users)
