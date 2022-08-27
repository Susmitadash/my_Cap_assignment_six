# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 15:12:01 2022

@author: LENOVO
"""
#project 2: Web scrapper using BeautifulSoup4 and requests
import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connect

parser = argparse.ArgumentParser()
parser.add_argument("--page_num-max", helps="Enter the number of parse", type=int)
parser.add_argument("--dbname", helps="Enter the name of db", type=str)
args = parser.parser.parse_args()

Oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="
page_num_MAX = 3
scrapped_info_list = []
connect.connect(args.dbname)

for page_num in range(1, page_num_MAX):
     req = requests.get(Oyo_url + str(page_num))
     content = req.content
     
     soup = BeautifulSoup(content, "html.parser")
     
     all_hotels = soup.find_all("div", {"class": "hotelCardListing"})
     scrapped_info_list = []
     for hotel in all_hotels:
         hotel_dict = {}
         hotel_dict["name"] = hotel. find("h3", {"class": "listingHotelDescription__hotelName"}). text 
         hotel_dict["address"] = hotel. find("span", {"itemprop": "streetAddress"}). text
         hotel_price = hotel. find("span", {"class": "listingPrice_finalPrice"}). text
         #try....except
         try:
             hotel_rating = hotel. find("span", {"clas hotelRating__ratingSummary"}).text
         except AttributeError:
             pass
         parent_amenities_element = hotel.find("div", {"class": "amenityWrapper"})
             
         amenities_list = []
         for amenity in parent_amenities_element.find_all("div", {"class": "amenityWrapper__amenity"}):
             amenities_list.append(amenity.find("span", {"class": "d-body—sm"}).text.strip())
             
         hotel_dict["amenities"] = ','.join(amenities_list[-1])
         
         scrapped_info_list.append(hotel-dict)
         
         #print(hotel_name, hotel_address, hotel_price, hotel_rating, amenities_list)

dataFrame = pandas.DataFrame( scrapped_info_list)
print("Creating csv file...")
dataFrame.to_csv("Oyo.csv")         
             





