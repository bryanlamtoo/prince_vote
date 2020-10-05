import requests
from time import sleep


def get_url():
    return 'https://artstalentafrica.com/wp-admin/admin-ajax.php'


counter = 0
max_retries = 0


def vote_via_api():
    global counter
    global max_retries

    while True:

        try:
            resp = requests.post(url=get_url(),
                                 data={"action": "it_epoll_vote", "option_id": 413315, "poll_id": 2375},
                                 )
            resp.raise_for_status()
            counter += 1
            print(counter)
            print(resp.json())
            sleep(0.5)

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
