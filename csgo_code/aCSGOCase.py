# this class is used to store csgo case data or act as a proxy to defer processing of gun data

class aCSGOCase:
    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.fprice = float(price)
        self.url = url
        self.dict_of_items = {}
        self.rarities = ["Mil-Spec", "Restricted", "Classified", "Covert"]
        self.total_value = float(self.price)
        self.normalized_case_value = self.price
        
    def __str__(self):
        case_data = "Name: {}, Price: {}, URL: {}".format(self.name, self.price, self.url)
        return case_data
    
    # lists off the cosmetics available in the case
    def ListContents(self):
        print(self.name)
        for rarity in self.rarities:
            print("[-- {} --]".format(rarity))
            for item in self.dict_of_items[rarity]:
                print(item)
    
    # calculate the value of the ENTIRE case. This include all items and the price of the case.
    def CalculateValueScore(self):
        for rarity in self.rarities:
            for item in self.dict_of_items[rarity]:
                self.total_value = self.total_value + float(item.value_score)
        self.total_value = self.total_value / self.normalized_case_value
        
if __name__ == "__main__":
    new_case = aCSGOCase("My Case", 100, "https://csgocases.com/fake_case")
    print(new_case)