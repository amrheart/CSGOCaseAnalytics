
class Item:
    def __init__(self, name, price_range, url, rarity, rarity_chance):
        self.name = name
        self.price_range = price_range
        self.price_average = 1
        self.value_score = 0
        self.url = url
        self.rarity = rarity
        self.rarity_chance = 0
        
    def __str__(self):
        return_string = "{} -- {} -- {}".format(self.name, self.rarity, self.price_range)
        return return_string
    
    # clean price function takes a price string and finds the average of both the high and low values
    # if only one number is present, just return the float
    def CleanPrice(self):
        average = -1
        unrefined_price = self.price_range.split("-")
        for price in range(len(unrefined_price)):
            unrefined_price[price] = unrefined_price[price].strip()
            unrefined_price[price] = unrefined_price[price].strip('$')
            if ',' in unrefined_price[price]:
                unrefined_price[price] = unrefined_price[price].replace(',', '')
        if len(unrefined_price) > 1:
            average = (float(unrefined_price[0]) + float(unrefined_price[1])) / 2
        else:
            average = float(unrefined_price[0])
        self.price_average = average
        
    
    def CalculateValueScore(self):
        self.value_score = self.rarity_chance * self.price_average