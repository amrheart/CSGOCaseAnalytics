import requests
import os


    
# utility function to count the number of files in a directory
def CountDirectory(directory):
    count = 0
    for path in os.listdir(directory):
        count = count + 1
    return count
    
if __name__ == "__main__":
    num_files = CountDirectory("gun_data")
    print(num_files)