# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
### Question 1 Part1
import requests
from bs4 import BeautifulSoup

seed_url = "https://press.un.org/en"
response = requests.get(seed_url)
soup = BeautifulSoup(response.content, "html.parser")

def get_hyper_links(soup):
	return ["https://press.un.org" + a["href"]
			for a in soup.find_all("a", href=True)
			if a.get("href").startswith("/")]

def is_press_release(soup):
    return soup.find('a', {'href': '/en/press-release', 'hreflang': 'en'}) is not None
    
    
def extract_press_release_by(seed_url, by = "crisis", count = 10):
    to_visit_links = [seed_url]
    visited_links = []
    num_press_release = 0
    target_url = []
    
    while to_visit_links and num_press_release < count:
        link = to_visit_links.pop()
        if link not in visited_links:
            soup = BeautifulSoup(requests.get(link).content, 'html.parser')
            if by.lower() in soup.text.lower() and is_press_release(soup):
                num_press_release += 1
                target_url.append(link)
                with open("1_"+str(num_press_release)+".txt", 'w') as f:
                    f.write(soup.prettify())
            
            hyper_links = get_hyper_links(soup)
            [to_visit_links.append(link0) for link0 in hyper_links if link0 not in visited_links]
            visited_links.append(link)
    return target_url
                
            
seed_url = "https://press.un.org/en"   
extract_press_release_by(seed_url)
    
    
 