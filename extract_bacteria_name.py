import requests
import pandas as pd
from bs4 import BeautifulSoup

base_url = "https://mic.eucast.org"
url : str = "https://mic.eucast.org/search/?search%5Bmethod%5D=mic&search%5Bantibiotic%5D=-1&search%5Bspecies%5D=76&search%5Bdisk_content%5D=-1&search%5Blimit%5D=50"

def get_html(url : str = url) -> requests.Response:
    session = requests.Session()
    _ =session.get(base_url)
    if _.status_code == 200:
        response = session.get(url)
        if response.status_code == 200:
            return response
        else:
            exit("Error getting HTML page")
    else:
        exit("Error getting cookies")
    
def get_bacterias(response : requests.Response)-> list[str]:
    bacterias = list()
    soup =  BeautifulSoup(response.text, features="html.parser")
    bacteries_dropdown = soup.find('select',{"id" : "search_species"})
    for item in bacteries_dropdown.find_all('option'):
        bacteria = ''.join(str(item.find(string=True))).strip().upper()
        bacteria = bacteria.replace("GROUP","").replace("EUCAST","")
        bacterias.append(bacteria)
    return bacterias[1:]

def save_csv(bac_list : list)->None:
    df = pd.DataFrame(bac_list,columns=["Name"])
    df.to_csv("bacteria_name_list.csv", index = False, sep = ";")

if __name__ == "__main__":
    page = get_html()
    bac_list =  get_bacterias(page)
    save_csv(bac_list)