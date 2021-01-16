import requests
from bs4 import BeautifulSoup
import os
import json
from types import SimpleNamespace
from Weapon import Weapon


def clear_screen(): 
  
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux (here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 
    
    return


# customDecoder function 
def custom_decoder(dct): 
    return SimpleNamespace(**dct) 


def read_json_file():
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, "rps101_data.json")
    with open(path) as f:
        json_load = json.load(f)
    return json_load


def process_json(json_load):
    for weapon_dict in json_load:
        weapon = Weapon(**weapon_dict)
        print(weapon.title)
    return


if __name__ == "__main__":
    json_load = read_json_file()
    process_json(json_load)
