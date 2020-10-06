import requests
from time import sleep
import json

def get_url():
    return 'https://artstalentafrica.com/wp-admin/admin-ajax.php'


counter = 0
max_retries = 0
vote_cache_counter = 0
vote_cache = None


def reset_cache():
    global vote_cache_counter
    try:
        vote_cache_counter += 1

        if vote_cache_counter == 2:
            print(f'Clearing cache...')
            resp = requests.post(url=get_url(),
                                 data={"action": "it_epoll_vote", "option_id": 460318, "poll_id": 2375},
                                 )
            resp.raise_for_status()
            vote_cache_counter = 0
    except Exception as e:
        print(str(e))


def vote_via_api():
    global counter
    global max_retries
    global vote_cache_counter
    global vote_cache

    while True:

        try:
            resp = requests.post(url=get_url(),
                                 data={"action": "it_epoll_vote", "option_id": 413315, "poll_id": 2375},
                                 )
            resp.raise_for_status()
            counter += 1
            print(counter)

            resp_data = resp.json()

            if resp_data['total_opt_vote_count'] == vote_cache:
                reset_cache()

            vote_cache = resp_data['total_opt_vote_count']

            print(resp_data)
            sleep(3)

            max_retries = 0

        except Exception as ex:
            print(str(ex))

            max_retries += 1
            # sleep(10)
            print(f'Resuming: {max_retries}')

            # If we have retried too many times, stop
            if max_retries == 100:
                exit(1)

            # try again
            vote_via_api()


if __name__ == '__main__':
    vote_via_api()
