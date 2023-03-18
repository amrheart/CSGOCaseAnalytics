from ProcessWrapper import *
from WebScraper import *

main = ProcessWrapper()
user_input = input("Enter 1 to gather new data or 2 to process case data: ")
if user_input == "1":
    main.CollectData()

elif user_input == "2":
    main.PopulateCases()
    main.ListCaseValues()

    
