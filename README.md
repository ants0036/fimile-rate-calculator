# Rate Calculator

A calculator for package rates using a streamlit dashboard. It uses the sender and reciever zip code to calculate the distance a package has traveled, and uses that distance to calculate a distance-based rate for the package. In addition, it uses company-defined zones and zipcodes to define a second set of rates, the base & payable rate. These are then subtracted to give the average revenue for the package.

This app uses the zipcode database from https://simplemaps.com/data/us-zips to calculate the distance between a package's starting zip code and destination zip code.

# Usage

This app assumes that the user is using an internal excel sheet format. It will not work unless your excel sheet has collumns that match the format. Upload the excel sheet to the streamlit dashboard to use the calculator. 
