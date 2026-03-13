import streamlit as st
import pandas as pd
from io import BytesIO
from distance_calculation import * 
from rate_calculation import * 

def process_df(df):
  add_distance_to_data(df)
  df ["payable_rate"] = df.apply(calculate_payable_rate, axis=1)
  df ["zone"] = df.apply(find_zone_code, axis=1)
  df ["base_rate"] = df.apply(calculate_base_rate, axis=1)
  df ["revenue"] = df.apply(calculate_revenue, axis=1)
  return df 

# file uploader module - converts a csv to a dataframe 
packages_raw_csv = st.file_uploader("choose a csv")
st.write("Excel Formatting: Zipcodes need to have leading 0s ex. 08844, not 8844")
st.write("Excel Formatting: Size needs to be in l\*w\*h format, not lxwxh")
# if file is uploaded to the module 
if packages_raw_csv is not None:
  packages_raw_df = pd.read_csv(packages_raw_csv, on_bad_lines="skip", encoding="utf-8-sig", dtype={"From Zipcode": str, "To Zipcode": str})
  # print(packages_raw_df)
  st.write("excel data:")
  st.write(packages_raw_df)
  result_df = process_df(packages_raw_df)
  st.write("after calculating:")
  st.write(result_df)
  csv = result_df.to_csv(index=False)
  st.download_button(
    label="Download CSV",
    data=csv,
    file_name="processed_packages.csv",
    mime="text/csv"
  )
# else, load data from test data to run the program 
else:
  st.write("test data:")
  testdata_df = pd.read_csv("data/testdata2.csv", on_bad_lines="skip", encoding="utf-8-sig", dtype={"From Zipcode": str, "To Zipcode": str})
  st.write(testdata_df)
  result_df = process_df(testdata_df)
  st.write("after calculating:")
  st.write(result_df)
  csv = result_df.to_csv(index=False)
  st.download_button(
    label="Download CSV",
    data=csv,
    file_name="processed_packages.csv",
    mime="text/csv"
)