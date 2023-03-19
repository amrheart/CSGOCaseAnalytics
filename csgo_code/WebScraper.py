import requests
import os

# webscraper object facilitates all data gathering
# main_url is the url of the main hub for csgo cases
class WebScraper:
    def __init__(self, main_url):
        self.main_url = main_url
        
    # scrapes the html from a given url and places the html into a specified text file
    def ScrapePage(self, url, output_file):
        list_of_events = []
        cEvents = 0
        cEvents = requests.get(url)
        open(output_file, "w").close()
        open_file = open(output_file, "a")
        for line in cEvents.iter_lines():
            strline = str(line)
            strline = strline.strip('b')
            strline = strline.strip("'")
            open_file.write(strline + '\n')
            # print("Parsing line " + strline)
        open_file.close()

    def ScrapeCases(self):
        self.ScrapePage(self.main_url, "CaseData.txt")
        
    def ScrapeItems(self, list_of_cases):
        for case in list_of_cases:
            self.ScrapePage(case.url, "gun_data\\" + case.name.replace(':', 'L') + ".txt")