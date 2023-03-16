import requests

# line 610 is where the information should be drawn from, ends 1144

print("This program is designed to grab skin prices and determine what trade ups are worth")
# first grab the html from the universal cases page
list_of_events = []
cEvents = 0
cEvents = requests.get("https://csgostash.com/containers/skin-cases")
open("CaseData.txt", "w").close()
open_file = open("CaseData.txt", "a")
for line in cEvents.iter_lines():
	strline = str(line)
	strline = strline.strip('b')
	strline = strline.strip("'")
	open_file.write(strline + '\n')
	print("Parsing line " + strline)
open_file.close()

print("Finished storing case data in file.")
input("Press enter to continue.")

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
		if (ident_string in line) and ((cur_line > 610) and (cur_line < 1145)):
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
			full_price = line[full_price_index:full_price_end]
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
	print(all_names[case] + " :  Price --> " + all_prices[case])