from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from movie_search_creds import *


class MoviesSearch(object):
    def __init__(self):
        self.url1 = url1
        self.driver = webdriver.Chrome()
        self.delay = 3
        self.netflix_user = net_username
        self.netflix_pass = net_password
        self.amazon_user = ama_username
        self.amazon_pass = ama_password
        self.search_list = keywords
        self.url2 = url2
        self.url3 = url3

    def run_driver(self):
        """
        tells driver to get the url, and to try to load it if 'searchform' is present,
        if not, a timeout exception will be raised, warning the user tha the page took
        too long to load
        :return: has no return
        """
        self.driver.get(self.url1)

    def close_driver(self):
        self.driver.close()

    def sign_in_netflix(self):
        time.sleep(2)
        self.driver.find_element_by_id("id_userLoginId").send_keys(self.netflix_user)
        self.driver.find_element_by_id("id_password").send_keys(self.netflix_pass)
        self.driver.find_element_by_css_selector(".btn.login-button.btn-submit.btn-small").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//ul[@class='choose-profile']/li[3]").click()
        time.sleep(2)

    def sign_in_amazon(self):
        self.driver.get(self.url2)
        time.sleep(2)
        self.driver.find_element_by_id("ap_email").send_keys(self.amazon_user)
        self.driver.find_element_by_id("ap_password").send_keys(self.amazon_pass, Keys.ENTER)

    def search_movie_in_netflix(self):
        final = set()
        for title in self.search_list:
            url = f'https://www.netflix.com/search?q={title}'
            self.driver.get(url)
            all_hits = self.driver.find_elements_by_class_name("slider-refocus")
            hits = [post.text for post in all_hits]
            for hit in hits:
                if title == hit:
                    final.add(hit)
        return final

    def search_movie_in_amazon(self):
        final = set()
        for title in self.search_list:
            url = f'https://www.primevideo.com/search/ref=atv_nb_sr?phrase={title}&ie=UTF8'
            self.driver.get(url)
            all_hits = self.driver.find_elements_by_class_name("av-beard-title-link")
            hits = [post.text for post in all_hits]
            for hit in hits:
                if title == hit:
                    final.add(hit)
        return final

    def search_movie_on_yts(self):
        self.driver.get(self.url3)
        final = set()
        for title in self.search_list:
            url = f'https://yts.pt/browse-movies/{title}/1080p/all/0/latest'
            self.driver.get(url)
            all_hits = self.driver.find_elements_by_class_name("browse-movie-title")
            hits = [post.text for post in all_hits]
            for hit in hits:
                if title == hit:
                    final.add(hit)
        return final


# stores words
keywords = (list(input("Enter the movie titles you want to search for, separated by commas:\n").split(',')))
keywords = [x.strip() for x in keywords]

url1 = 'https://www.netflix.com/fr-en/login'

url2 = 'https://www.amazon.com/ap/signin?accountStatusPolicy=P1&clientContext='\
        '257-0011667-1663328&language=fr_' \
       'FR&openid.assoc_handle=amzn_prime_video_desktop_us&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.' \
       '0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.' \
       'mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.' \
       'openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.primevideo.' \
       'com%2Fauth%2Freturn%2Fref%3Dav_auth_ap%3F_encoding%3DUTF8%26location%3D%252Fsignup%252Fref%253Ddv_auth_ret'

url3 = 'https://yts.pt/browse-movies'

scraper = MoviesSearch()
scraper.run_driver()

# # Netflix
scraper.sign_in_netflix()
print("Netflix has :")
netflix_list = scraper.search_movie_in_netflix()
print(netflix_list)
# # # Amazon Video
scraper.sign_in_amazon()
print("Amazon Video has :")
amazon_list = scraper.search_movie_in_amazon()
print(amazon_list)
# # # YTS
print("YTS has :")
yts_list = scraper.search_movie_on_yts()
print(yts_list)

scraper.close_driver()
