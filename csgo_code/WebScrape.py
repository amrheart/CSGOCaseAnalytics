import requests
import os

# scrapes the html from a given url and places the html into a specified text file
def ScrapePage(url, output_file):
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
    
# utility function to count the number of files in a directory
def CountDirectory(directory):
    count = 0
    for path in os.listdir(directory):
        count = count + 1
    return count
    
if __name__ == "__main__":
    ScrapePage("https://csgostash.com/containers/skin-cases", "googleoutput.txt")
    num_files = CountDirectory("gun_data")
    print(num_files)