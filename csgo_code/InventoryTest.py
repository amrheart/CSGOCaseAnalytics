from WebScraper import *
import requests

sc = WebScraper("https://steamcommunity.com/profiles/76561198056863526/inventory/#730")
sc.ScrapePage("https://steamcommunity.com/profiles/76561198056863526/inventory/#730", "inventory.txt")