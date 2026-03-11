import streamlit as st
import pandas as pd
import numpy as np
from distance_calculation import * 
from rate_calculation import * 

# file uploader module - converts a csv to a dataframe 
packages_raw_csv = st.file_uploader("choose a csv")
# if file is uploaded to the module 
if packages_raw_csv is not None:
  packages_raw_df = pd.read_csv(packages_raw_csv, on_bad_lines="skip", encoding="utf-8-sig", dtype={"From Zipcode": str, "To Zipcode": str})
  # print(packages_raw_df)
  st.write("excel data:")
  st.write(packages_raw_df)
  add_distance_to_data(packages_raw_df)
  packages_raw_df ["payable_rate"] = packages_raw_df.apply(calculate_payable_rate, axis=1)
  packages_raw_df ["zone"] = packages_raw_df.apply(find_zone_code, axis=1)
  packages_raw_df ["base_rate"] = packages_raw_df.apply(calculate_base_rate, axis=1)
  packages_raw_df ["revenue"] = packages_raw_df.apply(calculate_revenue, axis=1)
  st.write(packages_raw_df)
# else, load data from test data to run the program 
else:
  st.write("test data:")
  testdata_df = pd.read_csv("data/testdata2.csv", on_bad_lines="skip", encoding="utf-8-sig", dtype={"From Zipcode": str, "To Zipcode": str})
  st.write(testdata_df)
  add_distance_to_data(testdata_df)
  testdata_df ["payable_rate"] = testdata_df.apply(calculate_payable_rate, axis=1)
  st.write("test data with payable rate calculation:")
  st.write(testdata_df)
  testdata_df ["zone"] = testdata_df.apply(find_zone_code, axis=1)
  testdata_df ["base_rate"] = testdata_df.apply(calculate_base_rate, axis=1)
  testdata_df ["revenue"] = testdata_df.apply(calculate_revenue, axis=1)
  st.write(testdata_df)