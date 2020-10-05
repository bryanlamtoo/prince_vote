from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from seleniumrequests import Chrome


def get_driver():
    # Initialize the browser
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument("--incognito")
    _driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    _driver.maximize_window()
    _driver.implicitly_wait(20)
    return _driver


def get_url():
    return 'https://artstalentafrica.com/vote-for-your-favourite-artist-in-the-artta-covid-challenge/'


browser = get_driver()
max_retries = 0
counter = 0


def vote():

    global max_retries
    global counter
    while True:
        print(f'Vote {counter}')

        try:
            # browser = get_driver()
            browser.get(get_url())

            # Find the vote button
            vote_button = browser.find_element_by_xpath("//input[@value='413315']/following-sibling::input")
            container = vote_button.find_element_by_xpath('./../../..')

            # scroll browser to the view
            browser.execute_script("arguments[0].scrollIntoView();", container)

            # click to vote
            vote_button.click()
            sleep(7)

            # clear all cookies to enable re-voting
            # browser.close()
            browser.delete_all_cookies()
            counter += 1

            # reset the maximum error retries
            max_retries = 0
        except Exception as ex:
            print(str(ex))

            max_retries += 1
            print(f'Resuming: {max_retries}')

            # If we have retried too many times, stop
            if max_retries == 100:
                exit(1)

            # try again
            vote()




web_driver = Chrome(ChromeDriverManager().install())

def vote_via_api():
    # while True:
    response = web_driver.request('POST', 'https://artstalentafrica.com/wp-admin/admin-ajax.php',
                                 data={"action": "it_epoll", "option_id": 413315, "poll_id": "2375"})
    print(response)

if __name__ == '__main__':
    vote_via_api()
