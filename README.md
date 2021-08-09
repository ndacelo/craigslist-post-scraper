## Craigslist Post Scraping
This is simple Functional approach to scraping Craigslist for posts by using a list of keywords to be found in a post's title.
A dictionary is created with the post's: title, publication date, compensation, contract type, and the main body of the post.
This is saved as a TXT file, but can easily be modified to be saved as a CSV or pickled for later use. 

## Getting Started
You will need to have Python3 install on your system. SSH or download this repo as a ZIP. Unpack it if ZIP or open a terminal to where you cloned the repo.
In your terminal type Python3 craigslist-post-scraper.py
You will then be prompted by a choice of 1-8 correlating to the 8 different subsections of Craigslist. 
Enter in the number you choose to begin your search in.
Press 'Enter'
Finally you will be prompted to enter in the keywords you want to use to check within a post's title.
Write as many as you need, making sure to separate them by commas.
Press 'Enter'
The program will take a few seconds to run, and a print statement in the terminal will notify you of how many results were found
based off of your keywords.
A TXT/CSV file named 'results_from_CL' will be made in the same directory.
