import requests
import time
from aCSGOCase import aCSGOCase
from WebScrape import ScrapePage
from ProcessCaseData import ProcessCaseData, GetCaseAveragePrice
# line 610 is where the information should be drawn from, ends 1144
user_input = input("Enter 1 to gather new data or 2 to process case data: ")
my_cases = []
if user_input == "1":
    print("This program is designed to grab skin prices and determine what trade ups are worth")
    ScrapePage("https://csgostash.com/containers/skin-cases", "CaseData.txt")

    print("Finished storing case data in file.")
    input("Press enter to continue.")

elif user_input == "2":
    # next gather the urls, names, and price data of each case using the html gathered
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
    for line in all_urls:
        print(line)
    print("Number of cases found: " + str(len(all_urls)))
    print("Number of prices found: " + str(len(all_prices)))

    for case in range(len(all_urls)):
        print(all_names[case] + " :  Price --> " + all_prices[case] + " :  URL --> " + all_urls[case])
    
    # create a csgo case object for each case then put them into a list
    for num in range(len(all_urls)):
        new_case = aCSGOCase(all_names[num].replace(':', 'L'), all_prices[num], all_urls[num])
        my_cases.append(new_case)
        
    for case in my_cases:
        print(case)
    
    for case in my_cases:
        case.dict_of_items = ProcessCaseData("gun_data\\" + case.name + ".txt")
    
    # normalize the value (price) of every case so that the averages are at 1
    average = GetCaseAveragePrice(my_cases)
    difference = 1 - average
    for case in my_cases:
        case.normalized_case_value = round(average/case.fprice,2)
        print("normalized case values" + str(case.normalized_case_value))
    
    for case in my_cases:
        case.ListContents()
        
    for case in my_cases:
        case.CalculateValueScore()
        
    for case in my_cases:
        print(case.total_value)

user_input = input("Would you like to collect gun data from these cases? Type 1 for yes ")

if user_input == "1":
    print("beginning gun data collection")
    counter = 1
    # grab the html for each cases page
    for case in my_cases:
        print("Serviceing " + case.name + " " + str(counter))
        ScrapePage(case.url, "gun_data\\" + case.name.replace(':', 'L') + ".txt")
        time.sleep(.5)
        counter = counter + 1
    
