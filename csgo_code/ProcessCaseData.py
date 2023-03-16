from Item import Item

# This function will take a case file and find which rarities are present
# most of the time all rarities will be present but we need to check for outliers
# will return a list of all rarities present
def DetermineRarities(file):
    # all possible rarities
    rarities = ["Mil-Spec", "Restricted", "Classified", "Covert"]
    rarities_present = []
    ident_string = '<p class="nomargin">'
    open_file = open(file, "r")
    the_file = open_file.readlines()
    for rarity in rarities:
        for line in the_file:
            # found an identifier line
            if ident_string + rarity in line:
                rarities_present.append(rarity)
                break
            
    return rarities_present

# This function will take a file with case data and be able to pick all items out of it with their prices and rarities
# it will return a dictionary, where the keys are the raraties, and the values are lists of item objects
def ProcessCaseData(file):
    full_dict = {}
    rarities = ["Mil-Spec", "Restricted", "Classified", "Covert"]
    rarity_chart = {
        "Mil-Spec" : .79,
        "Restricted" : .16,
        "Classified" : .03,
        "Covert" : .006
        }
    ident_string = '<p class="nomargin">'
    open_file = open(file, "r")
    cur_line = 0
    offset = 10
    the_file = open_file.readlines()
    cur_tier = []
    for rarity in rarities:
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
                new_item = Item(name, price, url, rarity, rarity_chart[rarity])
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

# find the average price of all the cases
def GetCaseAveragePrice(list_of_cases):
    average = 0.0
    print(list_of_cases[-1])
    for case in list_of_cases:
        print(case.fprice)
        average = float(average) + case.fprice
        average = round(average, 2)
        print("average : " + str(average))
        
    average = average / len(list_of_cases)
    return average

if __name__ == "__main__":
    print(DetermineRarities("gun_data\\X-Ray-P250-Package.txt"))
    ProcessCaseData("gun_data\\X-Ray-P250-Package.txt")
    print(CleanPrice("$2.50 - $5.00"))
    print(CleanPrice("$6.69"))