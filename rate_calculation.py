import streamlit as st
import pandas as pd
import numpy as np

# given a row of a data frame that has the distance in miles, calculate the payable weight of the package. 
def calculate_payable_rate(row):
  # throw an error if it doesn't have distance in miles yet 
  # had to change the csv from unit /newline count to unit space count. have to do this to the original csv now, or change it to unit_count 

  # given a format of num*num*num, split the string 
  dimensions = [int(x) for x in row["Size (Inch)"].split("*")]
  # calculate the size multiplier, never less than 1: calculation is based off of just length x width for some reason 
  size_multiplier = (dimensions[0]*dimensions[1]) / (48 * 40)
  if (size_multiplier < 1):
    size_multiplier = 1 

  destination_city = row["To City"]
  distance_miles = row["distance_miles"]
  pallet_count = row["Unit Count"]
  payable_rate = 0

  # try to simplify this one day 
  if(pallet_count > 8 ):
    if (destination_city == "Bronx"):
      payable_rate = 80 * pallet_count * size_multiplier
    elif (destination_city == "Staten Island"):
      payable_rate = 70 * pallet_count * size_multiplier
    elif (destination_city == "Manhattan"):
      payable_rate = 100 * pallet_count * size_multiplier
    elif (destination_city == "Brooklyn" or destination_city == "Queens"):
      payable_rate = 80 * pallet_count * size_multiplier
    elif (destination_city == "Long Island"):
      if (distance_miles > 60):
        payable_rate = 130 *  pallet_count * size_multiplier
      else: 
        payable_rate = 85 *  pallet_count * size_multiplier
    elif(distance_miles < 31):
      payable_rate = 50 * pallet_count * size_multiplier
    elif(distance_miles < 41):
      payable_rate = 60 * pallet_count * size_multiplier
    elif(distance_miles < 51):
      payable_rate = 65 * pallet_count * size_multiplier
    elif(distance_miles < 61):
      payable_rate = 70 * pallet_count * size_multiplier
    elif(distance_miles < 71):
      payable_rate = 75 * pallet_count * size_multiplier
    elif(distance_miles < 81):
      payable_rate = 85 * pallet_count * size_multiplier
    elif(distance_miles < 91):
      payable_rate = 95 * pallet_count * size_multiplier
    else:
      payable_rate = 120 * pallet_count * size_multiplier
  else: 
    if (destination_city == "Bronx"):
      payable_rate = 85 *  pallet_count * size_multiplier
    elif (destination_city == "Staten Island"):
      payable_rate = 75 *  pallet_count * size_multiplier
    elif (destination_city == "Manhattan"):
      payable_rate = 105 *  pallet_count * size_multiplier
    elif (destination_city == "Brooklyn" or destination_city == "Queens"):
      payable_rate = 85 *  pallet_count * size_multiplier
    elif (destination_city == "Long Island"):
      if (distance_miles > 60):
        payable_rate = 135 *  pallet_count * size_multiplier
      else: 
        payable_rate = 90 *  pallet_count * size_multiplier
    elif(distance_miles < 31):
      payable_rate = 55 * pallet_count * size_multiplier
    elif(distance_miles < 41):
      payable_rate = 65 * pallet_count * size_multiplier
    elif(distance_miles < 51):
      payable_rate = 70 * pallet_count * size_multiplier
    elif(distance_miles < 61):
      payable_rate = 75 * pallet_count * size_multiplier
    elif(distance_miles < 71):
      payable_rate = 80 * pallet_count * size_multiplier
    elif(distance_miles < 81):
      payable_rate = 90 * pallet_count * size_multiplier
    elif(distance_miles < 91):
      payable_rate = 100 * pallet_count * size_multiplier
    else:
      payable_rate = 120 * pallet_count * size_multiplier
  # add service charge 
  return payable_rate + 5

@st.cache_data
def load_zone_zips():
  return pd.read_csv("data/Fimile-nj-zone-zips.csv", dtype={"Postal Code": str})

# takes in a row of a dataframe and returns the zone code 
def find_zone_code(row):
  zone_zip_df = load_zone_zips()
  zone_df = zone_zip_df.loc[zone_zip_df["Postal Code"] == row["To Zipcode"], ["Zone"]]
  print(zone_df)
  return zone_df.iloc[0]["Zone"]
  
# takes in a row of a dataframe that has a zone code
def calculate_base_rate(row):
  # taken from payable rate calculation -- need to abstract 
  # given a format of num*num*num, split the string 
  dimensions = [int(x) for x in row["Size (Inch)"].split("*")]
  # calculate the size multiplier, never less than 1: calculation is based off of just length x width for some reason 
  size_multiplier = (dimensions[0]*dimensions[1]) / (48 * 40)
  if (size_multiplier < 1):
    size_multiplier = 1 

  pallet_count = row["Unit Count"]
  base_rate = 0

  if row["zone"] == "NJ-EDS-A":
    base_rate = 70 * pallet_count * size_multiplier
  elif row["zone"] == "NJ-EDS-B":
    base_rate = 110 * pallet_count * size_multiplier
  elif row["zone"] == "NJ-EDS-C":
    base_rate = 150 * pallet_count * size_multiplier  
  else:
    return "error: no valid zone"
  
  return base_rate

def calculate_revenue (row):
  return row["base_rate"]-row["payable_rate"]