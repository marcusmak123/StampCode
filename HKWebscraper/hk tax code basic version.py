from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime 
import re

 
url= "https://www.gov.hk/en/residents/taxes/stamp/stamp_duty_rates.htm"
page = requests.get(url)


soup = BeautifulSoup(page.content, "html.parser")

taxIndicator = "% of the amount of the consideration or of its value on every sold note and every bought note"

target_element= soup.find(string= lambda text: taxIndicator in str(text))

if target_element: 
    parent = target_element.parent

    full = parent.get_text()

    parts = full.split(taxIndicator)

    hkstamp = parts[0]
    numbers = re.findall(r"[\d\.]+%?", hkstamp)

    if numbers:
        print(float(hkstamp))
    else:
        print("Error")



    
    
    
    








