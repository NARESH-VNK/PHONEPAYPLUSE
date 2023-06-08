# PHONEPAYPLUSE


![Logo](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQy5zPAtayVq0SRGCBAzrmPprN-BUvj8YUOK5ocPZoLZn6BBozmBFskB09fo_FwzuJqVpM&usqp=CAU.png)



# PHONEPAY PULSE ANALYSIS

- PhonePe Private Limited is a leading e-commerce payment platform in India. The digital wallet company was founded in December 2015. This platform offers services in over 11 Indian regional languages.

- PhonePe Pulse analysis offers users a comprehensive overview of their financial transactions, empowering them to make informed decisions, manage their finances effectively, and gain insights into their spending patterns and habits.



## Need For PhonePay Pulse Analysis

- PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.


- PhonePe Pulse is a feature provided by the PhonePe app that offers insights and analysis of our financial transactions and spending patterns. It allows you to track and analyze our expenses, income, and other financial activities.

Some common use cases and benefits of using PhonePe Pulse analysis:

- Expense Tracking
- Budgeting
- Spending Analysis
- Income Analysis
- Goal Tracking
- Transaction Insights
## Installation

Clone the project

```bash
  git clone https://github.com/PhonePe/pulse.git
```


Install dependencies

```bash
import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import psycopg2
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
```


Install streamlit application run 

```bash
  streamlit run phonepayst.py
```
    
## Demo

https://youtu.be/c_1H6vivsiA


## Format of Phonepay Data

This data has been structured to provide details of following two sections with data cuts on Transactions and Users of PhonePe Pulse - Explore tab.

- Aggregated - Aggregated values of various payment categories as shown under Categories section.

- Map - Total values at the State and District levels.
- Top - Totals of top States / Districts /Pin Codes

All the data provided in these folders is of JSON format. For more details on the structure/syntax you can refer to the JSON Structure / Syntax section of the documentation.


## Example Format 
Each and every data format like this in all sections like Aggregated,Map and Top users and Transactions.


data
|___ aggregated
    |___ transactions
        |___ country
            |___ india
                |___ 2018
                |    1.json
                |    2.json
                |    3.json
                |    4.json
                
                |___ 2019
                |    ...
                |___ 2019
                |___ state 
                    |___ andaman-&-nicobar-islands
                        |___2018
                        |   1.json
                        |   2.json
                        |   3.json
                        |   4.json

                    |___ andhra-pradesh
                    |    ...
                    |    ...
## WORK FLOW 

Step 1 :Firstly, understand the phonepay data given.By git cloning, clone the data from the github profile.

Step 2: Extract all the data from directory by OS package.

Step 3: Necessary Data extraction and Data cleaning is done.

Step 4: Using Pandas package from python, convert the extracted data into DataFrame.

Step 5: Now, using sqlalchemy package import the all dataframe from python into SQL database.
  - Tables are in proper datatype format.

Step 6: Streamlit application is used to deploy our datas in visualization.
  - Create the streamlit app and deploy our datas into graphs and charts.

Step 7: visualization the required data by entering the desired year,state and quater.




## 🛠 Tools
Python,SQL,Visualization Tools...


## Data Reference

Dataset
```http
https://github.com/PhonePe/pulse.git

```

Phonepe Link

```http
https://www.phonepe.com/pulse/

```

## Lessons Learned

Learning is always fun. Extracting a huge amount of data which is in nested dictionary is good. SQL quering and visualize the data into understable format are clearly done.


## Outcomes of this project

- PhonePe Pulse analysis can provide businesses with valuable insights into sales, revenue, customer behavior, expenses, cash flow, and financial performance. By leveraging this analysis, businesses can make data-driven decisions, optimize their operations, and enhance their overall business approach.
