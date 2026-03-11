import streamlit as st
import pandas as pd
import numpy as np
from distance_calculation import * 
from payable_rate_calculation import * 

# file uploader module - converts a csv to a dataframe 
packages_raw_csv = st.file_uploader("choose a csv")
# if file is uploaded to the module 
if packages_raw_csv is not None:
  packages_raw_df = pd.read_csv(packages_raw_csv)
  # print(packages_raw_df)
# else, load data from test data to run the program 
else:
  st.write("test data:")
  testdata_df = pd.read_csv("data/testdata.csv", on_bad_lines="skip", encoding="utf-8-sig", dtype={"From Zipcode": str, "To Zipcode": str})
  st.write(testdata_df)
  add_distance_to_data(testdata_df)
  testdata_df ["payable_rate"] = testdata_df.apply(calculate_payable_rate, axis=1)
  st.write("test data with payable rate calculation:")
  st.write(testdata_df)