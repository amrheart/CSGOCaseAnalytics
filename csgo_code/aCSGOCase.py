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
        self.total_value = 0
        for rarity in self.rarities:
            total_price = 0
            for item in self.dict_of_items[rarity]:
                total_price = total_price + item.price_average
            # rarity did not exist in the dictionary, should be rare
            if len(self.dict_of_items[rarity]) > 0:
                total_price = total_price / len(self.dict_of_items[rarity])
                # sloppy way to get rarity chance, consider changing
                total_price = total_price * self.dict_of_items[rarity][0].rarity_chance
            self.total_value = self.total_value + total_price
        self.total_value = self.total_value / (self.fprice + 1)
        self.total_value = round(self.total_value, 2)
        
if __name__ == "__main__":
    new_case = aCSGOCase("My Case", 100, "https://csgocases.com/fake_case")
    print(new_case)