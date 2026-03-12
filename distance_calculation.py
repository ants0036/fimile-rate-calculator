import streamlit as st
import pandas as pd
import numpy as np

# Loads the us zipcode file for lat/long conversion. 
@st.cache_data
def load_zip_lookup():
  return pd.read_csv("data/uszips.csv", dtype={"zip": str})

# Using latitude and longitude, calculate the zipcode distance in miles 
def calculate_zipcode_distance(sender_lat, sender_lon, receiver_lat, receiver_lon):
  sender_lat_radians = np.radians(sender_lat)
  sender_lon_radians = np.radians(sender_lon)
  receiver_lat_radians = np.radians(receiver_lat)
  receiver_lon_radians = np.radians(receiver_lon)

  distance_lat = receiver_lat_radians - sender_lat_radians
  distance_lon = receiver_lon_radians - sender_lon_radians

  # haversine function 
  a = np.sin(distance_lat / 2) ** 2 + np.cos(sender_lat_radians) * np.cos(receiver_lat_radians) * np.sin(distance_lon / 2) ** 2
  c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

  earth_radius_miles = 3958.8
  return earth_radius_miles * c

# takes in a zipcode and dataframe of all zip codes and returns a dataframe of the lat & longitude numbers
def zip_to_lat_lon(zip, allzips_df):
  zip_lat_lon = allzips_df.loc[allzips_df["zip"] == zip, ["lat","lng"]]
  # print(zip_lat_lon)
  return zip_lat_lon

# given a row of the package dataframe, compute the distance between the sender and reciever
def compute_distance(row):
    allzips_df = load_zip_lookup()
    zip_lat_lon_sender = zip_to_lat_lon(row["From Zipcode"], allzips_df)
    zip_lat_lon_reciever = zip_to_lat_lon(row["To Zipcode"], allzips_df)

    if zip_lat_lon_sender.empty or zip_lat_lon_reciever.empty:
      return 0
    else: 
      return calculate_zipcode_distance(zip_lat_lon_sender.iloc[0]["lat"], zip_lat_lon_sender.iloc[0]["lng"], zip_lat_lon_reciever.iloc[0]["lat"], zip_lat_lon_reciever.iloc[0]["lng"])

# takes in a dataframe with package info and adds a new column with the distance in miles
def add_distance_to_data(packages_df):
  packages_df ["distance_miles"] = packages_df.apply(compute_distance, axis=1)