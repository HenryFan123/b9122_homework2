#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 23:01:52 2023

@author: hanyaofan
"""

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

import requests

def get_hyper_links(url, soup):
	return [urllib.parse.urljoin(url, a['href'])
			for a in soup.find_all("a", href=True)
			if a.get("href")]

def is_plenary_session(soup):
    return soup.find('span', class_='ep_name', text='Plenary session')

def extract_press_release_by(seed_url, by = "crisis", count = 10):
    to_visit_links = []
    visited_links = []
    results = []
    page = 0
    
    to_visit_links.append(seed_url+str(page))
    
    while to_visit_links and len(results) < count:
        link = to_visit_links.pop()
        if link not in visited_links:
            soup = BeautifulSoup(requests.get(link).content, 'html.parser')
            plenary_session_tag = soup.find('span', class_='ep_name', text='Plenary session')
            if by.lower() in soup.text.lower() and is_plenary_session(soup):
                results.append(link)
                with open("2_"+str(len(results))+".txt", 'w') as f:
                    f.write(soup.prettify())
            
            hyper_links = get_hyper_links(seed_url, soup)
            [to_visit_links.append(link0) for link0 in hyper_links if link0 not in visited_links]
            visited_links.append(link)
        
        if len(results) < count:
            page += 1
            new_link = seed_url + str(page)
            if new_link not in visited_links:
                to_visit_links.append(new_link)
    return results
        
        
    
seed_url = "https://www.europarl.europa.eu/news/en/press-room/page/"
extract_press_release_by(seed_url)