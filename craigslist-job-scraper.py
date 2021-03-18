from selenium import  webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import json



class CraiglistJobScraper(object):
    
    def __init__(self):
        # self.job_type = job_type
        self.url = 'https://paris.craigslist.fr/d/temp-jobs/search/ggg?lang=en&cc=gb'
        self.driver = webdriver.Chrome()
        self.delay = 3

    def run_driver(self):
        """
        tells driver to get the url, and to try to load it if 'searchform' is present,
        if not, a timeout exception will be raised, warning the user tha the page took
        too long to load
        :return: has no return
        """
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
        except TimeoutException:
            print("Page took too long to load")

    def close_driver(self):
        self.driver.close()

    def get_post_titles(self):
        all_posts = self.driver.find_elements_by_css_selector(".result-title.hdrlnk")
        post_title_list = [post.text for post in all_posts]
        # print(post_title_list)
        return post_title_list

    def get_post_urls(self):
        all_posts = self.driver.find_elements_by_css_selector(".result-title.hdrlnk")
        post_url_list = [post.get_attribute('href') for post in all_posts]
        # print(post_url_list)
        return post_url_list

    def get_post_date(self):
        get_date = self.driver.find_elements_by_class_name('result-date')
        post_date_list = [post.get_attribute('title') for post in get_date]
        # print(post_date_list)
        return post_date_list

    def get_post_desc(self, link):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        # Load a page
        self.driver.get(link)
        get_desc = self.driver.find_elements_by_id('postingbody')
        post_desc_list = [post.text for post in get_desc]
        return post_desc_list


def word_list_cleanup_alt(alist):
    """
    :param: accepts a list
    strips white spaces, then extends the list with all values
    being passed through , 'upper()' and 'capitalize()' functions to return
    :return: a final list that has all the original words, plus all their variations
    """
    alist = [x.strip() for x in alist]
    a = [x.capitalize() for x in alist]
    b = [x.upper() for x in alist]
    alist = alist + a + b
    return alist


# stores words, splits by commas, passes through function
keywords = (list(input("Enter the keywords you want to search jobs for, separated by commas:\n").split(',')))
keywords = word_list_cleanup_alt(keywords)

# scraper object created, functions called
scraper = CraiglistJobScraper()
scraper.run_driver()
titles = scraper.get_post_titles()
urls = scraper.get_post_urls()
dates = scraper.get_post_date()

# dictionary created to combine all pulled info
post_dict = dict(zip(titles, zip(dates, urls)))
# new lists to hold hits
hit_titles =[]
hit_dates =[]
hit_urls = []
# if a keyword is found in dictionary, its added to a list
for (key, value) in post_dict.items():
    for word in keywords:
        if word  in key:
            hit_titles.append(key)
            hit_dates.append(value[0])
            hit_urls.append(value[1])

hit_desc = [scraper.get_post_desc(u) for u in hit_urls]
# final dictionary created
hit_dict = dict(zip(hit_titles, zip(hit_dates, hit_urls, hit_desc)))

for key, value in hit_dict.items():
    print("Title ::: {0}': DATE ::: '{1}".format(key, value[0]))
    print("LINK ::: " + value[1])
    print("Description :::")
    print("\n".join(value[2]))
    print("\n")

print(str(len(hit_titles)) + ' hits found from ' + str(len(titles)))
with open('file.txt', 'w') as file:
    # file.write(json.dumps(hit_dict))
    for key, value in hit_dict.items():
        file.write("Title : {0}   DATE : {1}\nLink : '{2}' \n ".format(key, value[0] , value[1]) + "\n".join(value[2]) +
                                                                                                             "\n")

scraper.close_driver()
