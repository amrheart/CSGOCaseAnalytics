from WebScraper import WebScraper
from aCSGOCase import aCSGOCase
from Item import Item
import requests
import time

class ProcessWrapper:
    def __init__(self):
        self.list_of_cases = []
        self.rarities = ["Mil-Spec", "Restricted", "Classified", "Covert"]
        self.rarity_chart = {
            "Mil-Spec" : .80,
            "Restricted" : .16,
            "Classified" : .032,
            "Covert" : .006
            }
        self.web_scraper = WebScraper("https://csgostash.com/containers/skin-cases")
    
    def ProcessCaseData(self):
        self.list_of_cases = []
        open_file = open("CaseData.txt", "r")
        ident_string = "https://csgostash.com/case/"
        all_urls = []
        all_prices = []
        all_names = []
        cur_line = 0
        counter = 0
        found_case = False
        for line in open_file:
            # when a case is found, need to get the price which is 4 lines down
            if found_case != True:
                # found a url
                if (ident_string in line) and ((cur_line > 581) and (cur_line < 1157)):
                    index_of_url = line.find(ident_string)
                    end_of_url = line.find('"', index_of_url)
                    full_url = line[index_of_url:end_of_url]
                    all_urls.append(full_url)
                    full_name = full_url[27:end_of_url]
                    full_name_index = full_name.find("/") + 1
                    full_name = full_name[full_name_index:end_of_url]
                    all_names.append(full_name)
                    counter = 3
                    found_case = True
            else:
                if (counter == 0):
                    # format the string
                    full_price_index = line.find("$")
                    full_price_end = line.find("<", full_price_index)
                    full_price = line[full_price_index+1:full_price_end]
                    all_prices.append(full_price)
                    found_case = False
                else:
                    counter -= 1

            cur_line += 1
        open_file.close()
        for num in range(len(all_urls)):
            new_case = aCSGOCase(all_names[num].replace(':', 'L'), all_prices[num], all_urls[num])
            print(new_case)
            self.list_of_cases.append(new_case)
    
    # This function will take a file with case data and be able to pick all items out of it with their prices and rarities
    # it will return a dictionary, where the keys are the raraties, and the values are lists of item objects
    def ProcessItemData(self, file):
        full_dict = {}
        ident_string = '<p class="nomargin">'
        open_file = open(file, "r")
        cur_line = 0
        offset = 10
        the_file = open_file.readlines()
        cur_tier = []
        for rarity in self.rarities:
            cur_line = 0
            cur_tier = []
            for line in the_file:
                # found an identifier line
                if ident_string + rarity in line:
                    # need to clean the line up so the data can be extracted
                    if '<div class="price">' in the_file[cur_line + 10]:
                        offset = offset+1
                    dirty_string = the_file[cur_line + offset]
                    dirty_string = dirty_string.strip('<p class="nomargin"><a href=')
                    dirty_string = dirty_string.strip("</a></p>\n")
                    location_of_divider = dirty_string.find(">")
                    url = dirty_string[:location_of_divider - 1]
                    price = dirty_string[location_of_divider + 1:]
                    name_identifier = url.rfind("/")
                    name = url[name_identifier+1:]
                    url = 'h' + url
                    print(url)
                    print(name)
                    print(price)
                    new_item = Item(name, price, url, rarity, self.rarity_chart[rarity])
                    new_item.CleanPrice()
                    new_item.CalculateValueScore()
                    cur_tier.append(new_item)
                cur_line = cur_line + 1
                offset = 10
            full_dict[rarity] = cur_tier
        # test to see if dictionary is filled
        #for rarity in rarities:
             #for gun in full_dict[rarity]:
                #print(gun)
        return full_dict
    
    # runs a full scrape of all data
    # must first process main page data for urls to individual cases
    def CollectData(self):
        self.web_scraper.ScrapeCases()
        self.ProcessCaseData()
        self.web_scraper.ScrapeItems(self.list_of_cases)
    
    # populates the cases with their dictionary of items
    def PopulateCases(self):
        self.ProcessCaseData()
        for case in self.list_of_cases:
            case.dict_of_items = self.ProcessItemData("gun_data\\" + case.name + ".txt")
    
    # find the average price of all the cases
    def GetCaseAveragePrice(self):
        average = 0.0
        for case in self.list_of_cases:
            average = float(average) + case.fprice
            average = round(average, 2)
            
        average = average / len(self.list_of_cases)
        return average
    
    # utility function for sort functionality
    def CaseValue(self, case):
        return case.fprice
    
    def ListCases(self):
        for case in self.list_of_cases:
            print(case)
            print(case.dict_of_items)
            
    def ListCaseValues(self):
        self.list_of_cases.sort(key=self.CaseValue)
        for case in self.list_of_cases:
            case.CalculateValueScore()
            print(case)
            print(case.total_value)
