from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import re


def get_current_rate():
    
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
        return float(hkstamp)
    

def update_rates():
    current_rate = get_current_rate()
    if current_rate is None:
        print("Rate scrape failed")
        return
    
    current_ym = datetime.now().strftime("%Y-%-m")  
    
    try:
        df = pd.read_csv("combined.csv")
    except FileNotFoundError:
        df = pd.DataFrame()
    
   
    df[current_ym] = [f"{current_rate}%"]
    
    # Save (will automatically add new columns for new months)
    df.to_csv("combined.csv", index=False)
    print(f"Updated {current_ym}: {current_rate}%")

if __name__ == "__main__":
    update_rates()
    