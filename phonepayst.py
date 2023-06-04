import streamlit as st

import pandas as pd
import numpy as np
import os
import json
import psycopg2
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# create a PostgreSQL connection
conn = psycopg2.connect(
    host= 'localhost',
    user="postgres",
    password="naresh",
    port=5432,
    database="phonepay"
)
nk = conn.cursor()

# --------------------------------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="PHONEPAY PULSE",
    page_icon="📱",
    layout="wide",
     initial_sidebar_state="expanded"
)

state = ['All','delhi','tamil-nadu','goa','punjab','jharkhand','sikkim','bihar','maharashtra','west-bengal','ladakh','manipur','andaman-&-nicobar-islands','mizoram','arunachal-pradesh',
       'tripura','gujarat','andhra-pradesh','chandigarh','puducherry','uttar-pradesh','madhya-pradesh','uttarakhand','himachal-pradesh','nagaland','karnataka','rajasthan','odisha',
       'telangana','jammu-&-kashmir','assam','chhattisgarh','lakshadweep','kerala','meghalaya','dadra-&-nagar-haveli-&-daman-&-diu','haryana']

year = ['All',2018,2019,2020,2021,2022]
quater = ['All',1,2,3,4]

def agg_trs():
       col1, col2, col3 = st.columns(3)
       with col1:
              agg_trs_state = st.selectbox('PICK A STATE : ', state)
       with col2:
              agg_trs_year = st.selectbox('PICK A YEAR : ', year)
       with col3:
              agg_trs_quater = st.selectbox('PICK A QUATER : ', quater)

       if agg_trs_state=='All' and agg_trs_year=='All' and agg_trs_quater=='All':
              query = "select * from AGGREGATED_TRANSACTIONS"
       elif agg_trs_state=='All' and agg_trs_year=='All' and agg_trs_quater!='All':
              query = "select * from AGGREGATED_TRANSACTIONS where quater = {a}".format(a=agg_trs_quater)
       elif agg_trs_state == 'All' and agg_trs_year != 'All' and agg_trs_quater != 'All':
              query = "select * from AGGREGATED_TRANSACTIONS where year = {a} and  quater = {b}".format(a=agg_trs_year,b =agg_trs_quater)
       elif agg_trs_state!= 'All' and agg_trs_year =='All' and agg_trs_quater =='All':
              query = "select * from AGGREGATED_TRANSACTIONS where state = \'{a}\'".format(a = agg_trs_state)
       elif agg_trs_state!= 'All' and agg_trs_year =='All' and agg_trs_quater !='All':
              query = "select * from AGGREGATED_TRANSACTIONS where state = \'{a}\' and quater = {b}".format(a = agg_trs_state,b = agg_trs_quater)
       elif agg_trs_state=='All' and agg_trs_year!='All' and agg_trs_quater=='All':
              query = "select * from AGGREGATED_TRANSACTIONS where year = {a}".format(a=agg_trs_year)
       elif agg_trs_state!='All' and agg_trs_year!='All' and agg_trs_quater=='All':
              query = "select * from AGGREGATED_TRANSACTIONS where year = {a} and state =\'{b}\'".format(a=agg_trs_year,b=agg_trs_state)
       else:
              query = "select * from AGGREGATED_TRANSACTIONS  where state =\'{a}\' and year = {b} and quater = {c}".format(a=agg_trs_state,b=agg_trs_year,c=agg_trs_quater)

       nk.execute(query)
       x = nk.fetchall()
       df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'Transaction_Type', 'Transaction_count','Transaction_Amount'])
       st.dataframe(df)
       st.markdown("CHOOSE A REQUIRED DATA AND DOWNLOAD IT....")
       csv = df.to_csv()
       st.download_button(
              label="Download data as CSV",
              data = csv,
              file_name='AGGREGATED_TRANSACTION.csv',
              mime='text/csv',)
def agg_trs1():
       tab1, tab2, tab3 = st.tabs(["Transaction_Type", "Transaction_Count", "Transaction_Amount"])

       with tab1:
              st.subheader("State VS Transaction_Type")
              col1, col2, col3 = st.columns(3)
              with col1:
                     agg_trs_state = st.selectbox('CHOOSE  STATE  ', state)
              with col2:
                     agg_trs_year = st.selectbox('CHOOSE YEAR : ', year)
              with col3:
                     agg_trs_quater = st.selectbox('CHOOSE QUATER : ', quater)

              if agg_trs_state == 'All' and agg_trs_year == 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS"
              elif agg_trs_state == 'All' and agg_trs_year == 'All' and agg_trs_quater != 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where quater = {a}".format(a=agg_trs_quater)
              elif agg_trs_state == 'All' and agg_trs_year != 'All' and agg_trs_quater != 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where year = {a} and  quater = {b}".format(
                            a=agg_trs_year, b=agg_trs_quater)
              elif agg_trs_state != 'All' and agg_trs_year == 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where state = \'{a}\'".format(a=agg_trs_state)
              elif agg_trs_state != 'All' and agg_trs_year == 'All' and agg_trs_quater != 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where state = \'{a}\' and quater = {b}".format(
                            a=agg_trs_state, b=agg_trs_quater)
              elif agg_trs_state == 'All' and agg_trs_year != 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where year = {a}".format(a=agg_trs_year)
              elif agg_trs_state != 'All' and agg_trs_year != 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where year = {a} and state =\'{b}\'".format(
                            a=agg_trs_year, b=agg_trs_state)
              else:
                     query = "select * from AGGREGATED_TRANSACTIONS  where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=agg_trs_state, b=agg_trs_year, c=agg_trs_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'Transaction_Type', 'Transaction_count',
                                            'Transaction_Amount'])
              st.write(df)
              fig = go.Figure(go.Pie(labels=df["Transaction_Type"], values=df['Transaction_count'], hole=0.5))
              fig.update_layout(width=900, height=800)
              st.plotly_chart(fig)
              fig = px.bar(df, y="Transaction_count", x="Transaction_Type", title=f'View of Transaction_Type vs Transaction_count ',
                           color="Transaction_Type", hover_data=['State', 'Year', "Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)

       with tab2:
              st.subheader("State VS Transaction_Count")
              col1, col2, col3 = st.columns(3)


              with col1:
                     agg_trs_state = st.selectbox('CHOOSE  A STATE  ', state)
              with col2:
                     agg_trs_year = st.selectbox('CHOOSE A YEAR : ', year)
              with col3:
                     agg_trs_quater = st.selectbox('CHOOSE A QUATER : ', quater)

              if agg_trs_state == 'All' and agg_trs_year == 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS"
              elif agg_trs_state == 'All' and agg_trs_year == 'All' and agg_trs_quater != 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where quater = {a}".format(a=agg_trs_quater)
              elif agg_trs_state == 'All' and agg_trs_year != 'All' and agg_trs_quater != 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where year = {a} and  quater = {b}".format(
                            a=agg_trs_year, b=agg_trs_quater)
              elif agg_trs_state != 'All' and agg_trs_year == 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where state = \'{a}\'".format(a=agg_trs_state)
              elif agg_trs_state != 'All' and agg_trs_year == 'All' and agg_trs_quater != 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where state = \'{a}\' and quater = {b}".format(
                            a=agg_trs_state, b=agg_trs_quater)
              elif agg_trs_state == 'All' and agg_trs_year != 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where year = {a}".format(a=agg_trs_year)
              elif agg_trs_state != 'All' and agg_trs_year != 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where year = {a} and state =\'{b}\'".format(
                            a=agg_trs_year, b=agg_trs_state)
              else:
                     query = "select * from AGGREGATED_TRANSACTIONS  where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=agg_trs_state, b=agg_trs_year, c=agg_trs_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'Transaction_Type', 'Transaction_count',
                                            'Transaction_Amount'])
              st.dataframe(df)

              fig = px.bar(df, y="Transaction_count", x="State", title=f'View of {agg_trs_state} vs Transaction_count ',
                    color="Transaction_Type",hover_data=['State','Year',"Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)

       with tab3:
              st.subheader("State VS Transaction_amount")
              col1, col2, col3 = st.columns(3)
              with col1:
                     agg_trs_state = st.selectbox('STATE  ', state)
              with col2:
                     agg_trs_year = st.selectbox('YEAR : ', year)
              with col3:
                     agg_trs_quater = st.selectbox('QUATER : ', quater)

              if agg_trs_state == 'All' and agg_trs_year == 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS"
              elif agg_trs_state == 'All' and agg_trs_year == 'All' and agg_trs_quater != 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where quater = {a}".format(a=agg_trs_quater)
              elif agg_trs_state == 'All' and agg_trs_year != 'All' and agg_trs_quater != 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where year = {a} and  quater = {b}".format(a=agg_trs_year,
                                                                                                               b=agg_trs_quater)
              elif agg_trs_state != 'All' and agg_trs_year == 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where state = \'{a}\'".format(a=agg_trs_state)
              elif agg_trs_state != 'All' and agg_trs_year == 'All' and agg_trs_quater != 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where state = \'{a}\' and quater = {b}".format(
                            a=agg_trs_state, b=agg_trs_quater)
              elif agg_trs_state == 'All' and agg_trs_year != 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where year = {a}".format(a=agg_trs_year)
              elif agg_trs_state != 'All' and agg_trs_year != 'All' and agg_trs_quater == 'All':
                     query = "select * from AGGREGATED_TRANSACTIONS where year = {a} and state =\'{b}\'".format(a=agg_trs_year,
                                                                                                                b=agg_trs_state)
              else:
                     query = "select * from AGGREGATED_TRANSACTIONS  where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=agg_trs_state, b=agg_trs_year, c=agg_trs_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'Transaction_Type', 'Transaction_count','Transaction_Amount'])
              st.write(df)
              fig = px.bar(df, y="Transaction_Amount", x="State", title=f'View of {agg_trs_state} vs Transaction_Amount ',
                           color="Transaction_Type",hover_data=['State','Year',"Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)

def agg_usr():
       col1, col2, col3 = st.columns(3)
       with col1:
              agg_usr_state= st.selectbox('PICK  A STATE : ', state)
       with col2:
              agg_usr_year = st.selectbox('PICK A YEAR : ', year)
       with col3:
              agg_usr_quater = st.selectbox('PICK A QUATER : ', quater)
       if agg_usr_state=="All" and agg_usr_year=="All" and agg_usr_quater=="All":
              query = "select * from AGGREGATED_USER"
       elif agg_usr_state=="All" and agg_usr_year=="All" and agg_usr_quater!="All":
              query =  "select * from AGGREGATED_USER where quater = {a}".format(a=agg_usr_quater)
       elif agg_usr_state=="All" and agg_usr_year!="All" and agg_usr_quater!="All":
              query = "select * from AGGREGATED_USER where year = {a} and quater = {b}".format(a=agg_usr_year,b=agg_usr_quater)
       elif agg_usr_state!="All" and agg_usr_year=="All" and agg_usr_quater=="All":
              query = "select * from AGGREGATED_USER where state = \'{a}\'".format(a=agg_usr_state)
       elif agg_usr_state!="All" and agg_usr_year=="All" and agg_usr_quater!="All":
              query = "select * from AGGREGATED_USER where state = \'{a}\' and quater = {b}".format(a=agg_usr_state, b=agg_usr_quater)
       elif agg_usr_state=="All" and agg_usr_year!="All" and agg_usr_quater=="All":
              query = "select * from AGGREGATED_USER where year = {a}".format(a=agg_usr_year)
       elif agg_usr_state!="All" and agg_usr_year!="All" and agg_usr_quater=="All":
              query = "select * from AGGREGATED_USER where year = {a} and state =\'{b}\'".format(a=agg_usr_year,b=agg_usr_state)
       else:
              query = "select * from AGGREGATED_USER  where state =\'{a}\' and year = {b} and quater = {c}".format(a=agg_usr_state, b=agg_usr_year, c=agg_usr_quater)

       nk.execute(query)
       x = nk.fetchall()
       df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'Registered_User', 'AppOpens','BrandName','Count','Percentage'])
       st.dataframe(df)
       st.markdown("CHOOSE A REQUIRED DATA AND DOWNLOAD IT....")
       csv = df.to_csv()
       st.download_button(
              label="Download data as CSV",
              data=csv,
              file_name='AGGREGATED_USER.csv',
              mime='text/csv' )

def agg_usr1():
       tab1,tab2,tab3 = st.tabs(['Registered User','AppOpens','Brand Values'])
       with tab1:
              col1, col2, col3 = st.columns(3)
              with col1:
                     agg_usr_state = st.selectbox('STATES', state)
              with col2:
                     agg_usr_year = st.selectbox('YEARS', year)
              with col3:
                     agg_usr_quater = st.selectbox('QUATERS', quater)
              if agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "select State, Year,Quater, Registered_User from AGGREGATED_USER"
              elif agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select State, Year,Quater, Registered_User from AGGREGATED_USER where quater = {a}".format(a=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater != "All":
                     query = "select State, Year,Quater, Registered_User from AGGREGATED_USER where year = {a} and quater = {b}".format(a=agg_usr_year,
                                                                                                      b=agg_usr_quater)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "select State, Year,Quater, Registered_User from AGGREGATED_USER where state = \'{a}\'".format(a=agg_usr_state)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select State, Year,Quater, Registered_User from AGGREGATED_USER where state = \'{a}\' and quater = {b}".format(
                            a=agg_usr_state,
                            b=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select State, Year,Quater, Registered_User from AGGREGATED_USER where year = {a}".format(a=agg_usr_year)
              elif agg_usr_state != "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select State, Year,Quater, Registered_User from AGGREGATED_USER where year = {a} and state =\'{b}\'".format(a=agg_usr_year,
                                                                                                        b=agg_usr_state)
              else:
                     query = "select State, Year,Quater, Registered_User from AGGREGATED_USER  where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=agg_usr_state, b=agg_usr_year, c=agg_usr_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x,columns=['State', 'Year', 'Quater', 'Registered_User'])
              df.drop_duplicates(keep='first',inplace=True)
              df= df.reset_index(drop=True)
              st.dataframe(df)
              fig = px.bar(df, y="Registered_User", x="State",
                           title=f'View of {agg_usr_state} vs Registered_User',
                           color="Quater", hover_data=['State', 'Year', "Registered_User"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)

              

       with tab2:
              col1, col2, col3 = st.columns(3)
              with col1:
                     agg_usr_state = st.selectbox('STATE', state)
              with col2:
                     agg_usr_year = st.selectbox('YEAR', year)
              with col3:
                     agg_usr_quater = st.selectbox('QUATER', quater)
              if agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER"
              elif agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER where quater = {a}".format(a=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater != "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER where year = {a} and quater = {b}".format(a=agg_usr_year,
                                                                                                      b=agg_usr_quater)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER where state = \'{a}\'".format(a=agg_usr_state)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER where state = \'{a}\' and quater = {b}".format(
                            a=agg_usr_state,
                            b=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER where year = {a}".format(a=agg_usr_year)
              elif agg_usr_state != "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER where year = {a} and state =\'{b}\'".format(a=agg_usr_year,
                                                                                                        b=agg_usr_state)
              else:
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER  where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=agg_usr_state, b=agg_usr_year, c=agg_usr_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x,columns=['State', 'Year', 'Quater',  'AppOpens'])
              df.drop_duplicates(keep='first', inplace=True)
              df = df.reset_index(drop=True)
              st.dataframe(df)
              fig = px.bar(df, y="AppOpens", x="State",
                           title=f'View of {agg_usr_state} vs AppOpens',
                           color="Quater", hover_data=['State', 'Year', "AppOpens"])
              fig.update_traces(texttemplate='%{y}', textposition='outside',textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)

       with tab3:
              col1, col2, col3 = st.columns(3)
              with col1:
                     agg_usr_state = st.selectbox('A STATE', state)
              with col2:
                     agg_usr_year = st.selectbox('A YEAR', year)
              with col3:
                     agg_usr_quater = st.selectbox('A QUATER', quater)
              if agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "select State,Year,Quater,Brand_Name, Count,Percentage from AGGREGATED_USER"
              elif agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select State,Year,Quater,Brand_Name, Count,Percentage from AGGREGATED_USER where quater = {a}".format(a=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater != "All":
                     query = "select State,Year,Quater,Brand_Name, Count,Percentage from AGGREGATED_USER where year = {a} and quater = {b}".format(a=agg_usr_year,
                                                                                                      b=agg_usr_quater)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "select State,Year,Quater,Brand_Name, Count,Percentage from AGGREGATED_USER where state = \'{a}\'".format(a=agg_usr_state)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select State,Year,Quater,Brand_Name, Count,Percentage from AGGREGATED_USER where state = \'{a}\' and quater = {b}".format(a=agg_usr_state,
                                                                                                           b=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select State,Year,Quater,Brand_Name, Count,Percentage from AGGREGATED_USER where year = {a}".format(a=agg_usr_year)
              elif agg_usr_state != "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select State,Year,Quater,Brand_Name, Count,Percentage from AGGREGATED_USER where year = {a} and state =\'{b}\'".format(a=agg_usr_year,
                                                                                                        b=agg_usr_state)
              else:
                     query = "select State,Year,Quater,Brand_Name, Count,Percentage from AGGREGATED_USER  where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=agg_usr_state, b=agg_usr_year, c=agg_usr_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater',  'BrandName', 'Count','Percentage'])
              st.dataframe(df)
              fig = px.bar(df, x="BrandName", y="Count",
                           title=f'View of Brand Name VS Count  ',
                           color="BrandName", hover_data=['State', 'Year', "Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)


def map_trs():
       col1, col2, col3 = st.columns(3)
       with col1:
              map_trs_state = st.selectbox('PICK A STATE NAME : ', state)
       with col2:
              map_trs_year = st.selectbox('PICK A YEAR : ', year)
       with col3:
              map_trs_quater = st.selectbox('PICK A QUATER : ', quater)

       if map_trs_state=='All' and map_trs_year=='All' and map_trs_quater=='All':
              query = "select * from MAP_TRANSACTION"
       elif map_trs_state=='All' and map_trs_year=='All' and map_trs_quater!='All':
              query = "select * from MAP_TRANSACTION where quater = {a}".format(a=map_trs_quater)
       elif map_trs_state == 'All' and map_trs_year != 'All' and map_trs_quater != 'All':
              query = "select * from MAP_TRANSACTION where year = {a} and  quater = {b}".format(a=map_trs_year,b =map_trs_quater)
       elif map_trs_state!= 'All' and map_trs_year =='All' and map_trs_quater =='All':
              query = "select * from MAP_TRANSACTION where state = \'{a}\'".format(a = map_trs_state)
       elif map_trs_state!= 'All' and map_trs_year =='All' and map_trs_quater !='All':
              query = "select * from MAP_TRANSACTION where state = \'{a}\' and quater = {b}".format(a = map_trs_state,b = map_trs_quater)
       elif map_trs_state=='All' and map_trs_year!='All' and map_trs_quater=='All':
              query = "select * from MAP_TRANSACTION where year = {a}".format(a=map_trs_year)
       elif map_trs_state!='All' and map_trs_year!='All' and map_trs_quater=='All':
              query = "select * from MAP_TRANSACTION where year = {a} and state =\'{b}\'".format(a=map_trs_year,b=map_trs_state)
       else:
              query = "select * from MAP_TRANSACTION  where state =\'{a}\' and year = {b} and quater = {c}".format(a=map_trs_state, b=map_trs_year, c=map_trs_quater)

       nk.execute(query)
       x = nk.fetchall()
       df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District','Total count','Total Amount'])
       st.dataframe(df)
       st.markdown("CHOOSE A REQUIRED DATA AND DOWNLOAD IT....")
       csv = df.to_csv()
       st.download_button(
              label="Download data as CSV",
              data=csv,
              file_name='MAP_TRANSACTION.csv',
              mime='text/csv', )
def map_trs1():
       tab1, tab2= st.tabs(["Total Count", "Total Amount"])
       with tab1:
              col1, col2, col3 = st.columns(3)
              with col1:
                     map_trs_state = st.selectbox('PREFER A STATE : ', state)
              with col2:
                     map_trs_year = st.selectbox('PREFER A YEAR : ', year)
              with col3:
                     map_trs_quater = st.selectbox('PREFER A QUATER : ', quater)

              if map_trs_state == 'All' and map_trs_year == 'All' and map_trs_quater == 'All':
                     query = "select * from MAP_TRANSACTION"
              elif map_trs_state == 'All' and map_trs_year == 'All' and map_trs_quater != 'All':
                     query = "select * from MAP_TRANSACTION where quater = {a}".format(a=map_trs_quater)
              elif map_trs_state == 'All' and map_trs_year != 'All' and map_trs_quater != 'All':
                     query = "select * from MAP_TRANSACTION where year = {a} and  quater = {b}".format(a=map_trs_year,
                                                                                                       b=map_trs_quater)
              elif map_trs_state != 'All' and map_trs_year == 'All' and map_trs_quater == 'All':
                     query = "select * from MAP_TRANSACTION where state = \'{a}\'".format(a=map_trs_state)
              elif map_trs_state != 'All' and map_trs_year == 'All' and map_trs_quater != 'All':
                     query = "select * from MAP_TRANSACTION where state = \'{a}\' and quater = {b}".format(a=map_trs_state,
                                                                                                           b=map_trs_quater)
              elif map_trs_state == 'All' and map_trs_year != 'All' and map_trs_quater == 'All':
                     query = "select * from MAP_TRANSACTION where year = {a}".format(a=map_trs_year)
              elif map_trs_state != 'All' and map_trs_year != 'All' and map_trs_quater == 'All':
                     query = "select * from MAP_TRANSACTION where year = {a} and state =\'{b}\'".format(a=map_trs_year,
                                                                                                        b=map_trs_state)
              else:
                     query = "select * from MAP_TRANSACTION  where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=map_trs_state, b=map_trs_year, c=map_trs_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District', 'Total count', 'Total Amount'])
              st.dataframe(df)
              fig = px.bar(df, x="Total count", y="District", title=f' {map_trs_state}  vs Transaction_count ',color="District",hover_data=['State','Year',"Quater"])
              fig.update_traces(texttemplate='%{x}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)
       with tab2:
              col1, col2, col3 = st.columns(3)
              with col1:
                     map_trs_state = st.selectbox('STATE :', state)
              with col2:
                     map_trs_year = st.selectbox('YEAR :', year)
              with col3:
                     map_trs_quater = st.selectbox('QUATER :', quater)

              if map_trs_state == 'All' and map_trs_year == 'All' and map_trs_quater == 'All':
                     query = "select * from MAP_TRANSACTION"
              elif map_trs_state == 'All' and map_trs_year == 'All' and map_trs_quater != 'All':
                     query = "select * from MAP_TRANSACTION where quater = {a}".format(a=map_trs_quater)
              elif map_trs_state == 'All' and map_trs_year != 'All' and map_trs_quater != 'All':
                     query = "select * from MAP_TRANSACTION where year = {a} and  quater = {b}".format(a=map_trs_year,
                                                                                                       b=map_trs_quater)
              elif map_trs_state != 'All' and map_trs_year == 'All' and map_trs_quater == 'All':
                     query = "select * from MAP_TRANSACTION where state = \'{a}\'".format(a=map_trs_state)
              elif map_trs_state != 'All' and map_trs_year == 'All' and map_trs_quater != 'All':
                     query = "select * from MAP_TRANSACTION where state = \'{a}\' and quater = {b}".format(
                            a=map_trs_state,
                            b=map_trs_quater)
              elif map_trs_state == 'All' and map_trs_year != 'All' and map_trs_quater == 'All':
                     query = "select * from MAP_TRANSACTION where year = {a}".format(a=map_trs_year)
              elif map_trs_state != 'All' and map_trs_year != 'All' and map_trs_quater == 'All':
                     query = "select * from MAP_TRANSACTION where year = {a} and state =\'{b}\'".format(a=map_trs_year,
                                                                                                        b=map_trs_state)
              else:
                     query = "select * from MAP_TRANSACTION  where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=map_trs_state, b=map_trs_year, c=map_trs_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District', 'Total count', 'Total Amount'])
              st.dataframe(df)
              fig = px.bar(df, y="Total Amount", x="District", title=f' {map_trs_state}  vs Transaction_Amount ',
                           color="District", hover_data=["State","Year","Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)


def map_usr():
       col1, col2, col3 = st.columns(3)
       with col1:
              map_usr_state = st.selectbox('PICK A STATE : ', state)
       with col2:
              map_usr_year = st.selectbox('PICK A YEAR : ', year)
       with col3:
              map_usr_quater = st.selectbox('PICK A QUATER : ', quater)

       if map_usr_state=='All' and map_usr_year=='All' and map_usr_quater=='All':
              query = "select * from MAP_USER"
       elif map_usr_state=='All' and map_usr_year=='All' and map_usr_quater!='All':
              query = "select * from MAP_USER where quater = {a}".format(a=map_usr_quater)
       elif map_usr_state == 'All' and map_usr_year != 'All' and map_usr_quater != 'All':
              query = "select * from MAP_USER where year = {a} and  quater = {b}".format(a=map_usr_year,b =map_usr_quater)
       elif map_usr_state!= 'All' and map_usr_year =='All' and map_usr_quater =='All':
              query = "select * from MAP_USER where state = \'{a}\'".format(a = map_usr_state)
       elif map_usr_state!= 'All' and map_usr_year =='All' and map_usr_quater !='All':
              query = "select * from MAP_USER where state = \'{a}\' and quater = {b}".format(a = map_usr_state,b = map_usr_quater)
       elif map_usr_state=='All' and map_usr_year!='All' and map_usr_quater=='All':
              query = "select * from MAP_USER where year = {a}".format(a=map_usr_year)
       elif map_usr_state!='All' and map_usr_year!='All' and map_usr_quater=='All':
              query = "select * from MAP_USER where year = {a} and state =\'{b}\'".format(a=map_usr_year,b=map_usr_state)
       else:
              query = "select * from MAP_USER  where state =\'{a}\' and year = {b} and quater = {c}".format(a=map_usr_state, b=map_usr_year, c=map_usr_quater)

       nk.execute(query)
       x = nk.fetchall()
       df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District','Registered_User', 'AppOpens'])
       st.dataframe(df)
       st.markdown("CHOOSE A REQUIRED DATA AND DOWNLOAD IT....")
       csv = df.to_csv()
       st.download_button(
              label="Download data as CSV",
              data=csv,
              file_name='MAP_USER.csv',
              mime='text/csv', )

def map_usr1():
       tab1, tab2 = st.tabs(["Registered User", "Appopens"])
       with tab1:
              col1, col2, col3 = st.columns(3)
              with col1:
                     map_usr_state = st.selectbox('SELECT STATE : ', state)
              with col2:
                     map_usr_year = st.selectbox('SELECT  YEAR : ', year)
              with col3:
                     map_usr_quater = st.selectbox('SELECT QUATER : ', quater)

              if map_usr_state == 'All' and map_usr_year == 'All' and map_usr_quater == 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER"
              elif map_usr_state == 'All' and map_usr_year == 'All' and map_usr_quater != 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER where quater = {a}".format(a=map_usr_quater)
              elif map_usr_state == 'All' and map_usr_year != 'All' and map_usr_quater != 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER where year = {a} and  quater = {b}".format(a=map_usr_year,
                                                                                                b=map_usr_quater)
              elif map_usr_state != 'All' and map_usr_year == 'All' and map_usr_quater == 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER where state = \'{a}\'".format(a=map_usr_state)
              elif map_usr_state != 'All' and map_usr_year == 'All' and map_usr_quater != 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER where state = \'{a}\' and quater = {b}".format(a=map_usr_state,
                                                                                                    b=map_usr_quater)
              elif map_usr_state == 'All' and map_usr_year != 'All' and map_usr_quater == 'All':
                     query = "select * from MAP_USER where year = {a}".format(a=map_usr_year)
              elif map_usr_state != 'All' and map_usr_year != 'All' and map_usr_quater == 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER where year = {a} and state =\'{b}\'".format(a=map_usr_year,
                                                                                                 b=map_usr_state)
              else:
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER  where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=map_usr_state, b=map_usr_year, c=map_usr_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District', 'Registered_User'])
              st.dataframe(df)
              fig = px.bar(df, y="Registered_User", x="District",
                           title=f'View of {map_usr_state} vs Registered_User',
                           color="District", hover_data=['State', 'Year', "Registered_User"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)

       with tab2:
              col1, col2, col3 = st.columns(3)
              with col1:
                     map_usr_state = st.selectbox('SELECTED STATE : ', state)
              with col2:
                     map_usr_year = st.selectbox('SELECTED  YEAR : ', year)
              with col3:
                     map_usr_quater = st.selectbox('SELECTED QUATER : ', quater)

              if map_usr_state == 'All' and map_usr_year == 'All' and map_usr_quater == 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER"
              elif map_usr_state == 'All' and map_usr_year == 'All' and map_usr_quater != 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER where quater = {a}".format(a=map_usr_quater)
              elif map_usr_state == 'All' and map_usr_year != 'All' and map_usr_quater != 'All':
                     query = "select State, Year,Quater,District,AppOpens * from MAP_USER where year = {a} and  quater = {b}".format(a=map_usr_year,
                                                                                                b=map_usr_quater)
              elif map_usr_state != 'All' and map_usr_year == 'All' and map_usr_quater == 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER where state = \'{a}\'".format(a=map_usr_state)
              elif map_usr_state != 'All' and map_usr_year == 'All' and map_usr_quater != 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER where state = \'{a}\' and quater = {b}".format(a=map_usr_state,
                                                                                                    b=map_usr_quater)
              elif map_usr_state == 'All' and map_usr_year != 'All' and map_usr_quater == 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER where year = {a}".format(a=map_usr_year)
              elif map_usr_state != 'All' and map_usr_year != 'All' and map_usr_quater == 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER where year = {a} and state =\'{b}\'".format(a=map_usr_year,
                                                                                                 b=map_usr_state)
              else:
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER  where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=map_usr_state, b=map_usr_year, c=map_usr_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District','AppOpens'])
              st.dataframe(df)
              fig = px.bar(df, y="AppOpens", x="District",
                           title=f'View of {map_usr_state} vs AppOpens',
                           color="District", hover_data=['State', 'Year', "AppOpens"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)


def top_trs_pn():
       col1, col2, col3 = st.columns(3)
       with col1:
              top_trs_pn_state = st.selectbox('PICK A STATE : ', state)
       with col2:
              top_trs_pn_year = st.selectbox('PICK A YEAR : ', year)
       with col3:
              top_trs_pn_quater = st.selectbox('PICK A QUATER : ', quater)

       if top_trs_pn_state=='All' and top_trs_pn_year=='All' and top_trs_pn_quater=='All':
              query = "select * from top_transaction_pincode"
       elif top_trs_pn_state=='All' and top_trs_pn_year=='All' and top_trs_pn_quater!='All':
              query = "select * from top_transaction_pincode where quater = {a}".format(a=top_trs_pn_quater)
       elif top_trs_pn_state== 'All' and top_trs_pn_year != 'All' and top_trs_pn_quater != 'All':
              query = "select * from top_transaction_pincode where year = {a} and  quater = {b}".format(a=top_trs_pn_year,b = top_trs_pn_quater)
       elif top_trs_pn_state!= 'All' and top_trs_pn_year =='All' and top_trs_pn_quater =='All':
              query = "select * from top_transaction_pincode where state = \'{a}\'".format(a = top_trs_pn_state)
       elif top_trs_pn_state!= 'All' and top_trs_pn_year =='All' and top_trs_pn_quater !='All':
              query = "select * from top_transaction_pincode where state = \'{a}\' and quater = {b}".format(a = top_trs_pn_state,b = top_trs_pn_quater)
       elif top_trs_pn_state=='All' and top_trs_pn_year!='All' and top_trs_pn_quater=='All':
              query = "select * from top_transaction_pincode where year = {a}".format(a=top_trs_pn_year)
       elif top_trs_pn_state!='All' and top_trs_pn_year!='All' and top_trs_pn_quater=='All':
              query = "select * from top_transaction_pincode where year = {a} and state =\'{b}\'".format(a=top_trs_pn_year,b=top_trs_pn_state)
       else:
              query = "select * from top_transaction_pincode where state =\'{a}\' and year = {b} and quater = {c}".format(a=top_trs_pn_state,b=top_trs_pn_year,c=top_trs_pn_quater)

       nk.execute(query)
       x = nk.fetchall()
       df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'Pincode_Name', 'Pincode_Count','Pincode_Amount'])
       st.dataframe(df)
       st.markdown("CHOOSE A REQUIRED DATA AND DOWNLOAD IT....")
       csv = df.to_csv()
       st.download_button(
              label="Download data as CSV",
              data=csv,
              file_name='TOP_TRANSACTION_PINCODE.csv',
              mime='text/csv', )
def top_trs_pn1():
       tab1, tab2 = st.tabs(["Pincode Count", "Pincode Amount"])
       with tab1:
              col1, col2, col3 = st.columns(3)
              with col1:
                     top_trs_pn_state = st.selectbox('SET A STATE : ', state)
              with col2:
                     top_trs_pn_year = st.selectbox('SET A YEAR : ', year)
              with col3:
                     top_trs_pn_quater = st.selectbox('SET A QUATER : ', quater)

              if top_trs_pn_state == 'All' and top_trs_pn_year == 'All' and top_trs_pn_quater == 'All':
                     query = "select State,Year,Quater,Pincode_Name,Pincode_Count from top_transaction_pincode"
              elif top_trs_pn_state == 'All' and top_trs_pn_year == 'All' and top_trs_pn_quater != 'All':
                     query = "select State,Year,Quater,Pincode_Name,Pincode_Count from top_transaction_pincode where quater = {a}".format(a=top_trs_pn_quater)
              elif top_trs_pn_state == 'All' and top_trs_pn_year != 'All' and top_trs_pn_quater != 'All':
                     query = "select State,Year,Quater,Pincode_Name,Pincode_Count from top_transaction_pincode where year = {a} and  quater = {b}".format(
                            a=top_trs_pn_year, b=top_trs_pn_quater)
              elif top_trs_pn_state != 'All' and top_trs_pn_year == 'All' and top_trs_pn_quater == 'All':
                     query = "select State,Year,Quater,Pincode_Name,Pincode_Count from top_transaction_pincode where state = \'{a}\'".format(a=top_trs_pn_state)
              elif top_trs_pn_state != 'All' and top_trs_pn_year == 'All' and top_trs_pn_quater != 'All':
                     query = "select State,Year,Quater,Pincode_Name,Pincode_Count from top_transaction_pincode where state = \'{a}\' and quater = {b}".format(
                            a=top_trs_pn_state, b=top_trs_pn_quater)
              elif top_trs_pn_state == 'All' and top_trs_pn_year != 'All' and top_trs_pn_quater == 'All':
                     query = "select State,Year,Quater,Pincode_Name,Pincode_Count from top_transaction_pincode where year = {a}".format(a=top_trs_pn_year)
              elif top_trs_pn_state != 'All' and top_trs_pn_year != 'All' and top_trs_pn_quater == 'All':
                     query = "select State,Year,Quater,Pincode_Name,Pincode_Count from top_transaction_pincode where year = {a} and state =\'{b}\'".format(
                            a=top_trs_pn_year, b=top_trs_pn_state)
              else:
                     query = "select State,Year,Quater,Pincode_Name,Pincode_Count from top_transaction_pincode where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=top_trs_pn_state, b=top_trs_pn_year, c=top_trs_pn_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'Pincode_Name', 'Pincode_Count'])
              st.dataframe(df)
              fig = px.bar(df, y='Pincode_Count', x="State", title=f' {top_trs_pn_state}  vs Pincode_Count',
                           color="Pincode_Name",hover_data=["State", "Year", "Quater","Pincode_Name"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)
       with tab2:
              col1, col2, col3 = st.columns(3)
              with col1:
                     top_trs_pn_state = st.selectbox('PICK-OUT STATE : ', state)
              with col2:
                     top_trs_pn_year = st.selectbox('PICK-OUT YEAR : ', year)
              with col3:
                     top_trs_pn_quater = st.selectbox('PICK-OUT QUATER : ', quater)

              if top_trs_pn_state == 'All' and top_trs_pn_year == 'All' and top_trs_pn_quater == 'All':
                     query = "select * from top_transaction_pincode"
              elif top_trs_pn_state == 'All' and top_trs_pn_year == 'All' and top_trs_pn_quater != 'All':
                     query = "select * from top_transaction_pincode where quater = {a}".format(a=top_trs_pn_quater)
              elif top_trs_pn_state == 'All' and top_trs_pn_year != 'All' and top_trs_pn_quater != 'All':
                     query = "select * from top_transaction_pincode where year = {a} and  quater = {b}".format(
                            a=top_trs_pn_year, b=top_trs_pn_quater)
              elif top_trs_pn_state != 'All' and top_trs_pn_year == 'All' and top_trs_pn_quater == 'All':
                     query = "select * from top_transaction_pincode where state = \'{a}\'".format(a=top_trs_pn_state)
              elif top_trs_pn_state != 'All' and top_trs_pn_year == 'All' and top_trs_pn_quater != 'All':
                     query = "select * from top_transaction_pincode where state = \'{a}\' and quater = {b}".format(
                            a=top_trs_pn_state, b=top_trs_pn_quater)
              elif top_trs_pn_state == 'All' and top_trs_pn_year != 'All' and top_trs_pn_quater == 'All':
                     query = "select * from top_transaction_pincode where year = {a}".format(a=top_trs_pn_year)
              elif top_trs_pn_state != 'All' and top_trs_pn_year != 'All' and top_trs_pn_quater == 'All':
                     query = "select * from top_transaction_pincode where year = {a} and state =\'{b}\'".format(
                            a=top_trs_pn_year, b=top_trs_pn_state)
              else:
                     query = "select * from top_transaction_pincode where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=top_trs_pn_state, b=top_trs_pn_year, c=top_trs_pn_quater)
              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x,columns=['State', 'Year', 'Quater', 'Pincode_Name', 'Pincode_Count','Pincode_Amount'])
              st.dataframe(df)
              fig = px.bar(df, y='Pincode_Amount', x="State", title=f' {top_trs_pn_state}  vs Pincode_Amount ',
                           color="Pincode_Name", hover_data=["State", "Year", "Quater", "Pincode_Name"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)


def top_trs_dis():
       col1, col2, col3 = st.columns(3)
       with col1:
              top_trs_ds_state= st.selectbox('PICK A STATE : ', state)
       with col2:
              top_trs_ds_year = st.selectbox('PICKE A YEAR : ', year)
       with col3:
              top_trs_ds_quater = st.selectbox('PICK A QUATER : ', quater)

       if top_trs_ds_state=='All' and top_trs_ds_year=='All' and top_trs_ds_quater=='All':
              query = "select * from top_transaction_district"
       elif top_trs_ds_state=='All' and top_trs_ds_year=='All' and top_trs_ds_quater!='All':
              query = "select * from top_transaction_district where quater = {a}".format(a=top_trs_ds_quater)
       elif top_trs_ds_state== 'All' and top_trs_ds_year != 'All' and top_trs_ds_quater != 'All':
              query = "select * from top_transaction_district where year = {a} and  quater = {b}".format(a=top_trs_ds_year,b = top_trs_ds_quater)
       elif top_trs_ds_state!= 'All' and top_trs_ds_year =='All' and top_trs_ds_quater =='All':
              query = "select * from top_transaction_district where state = \'{a}\'".format(a = top_trs_ds_state)
       elif top_trs_ds_state!= 'All' and top_trs_ds_year =='All' and top_trs_ds_quater !='All':
              query = "select * from top_transaction_district where state = \'{a}\' and quater = {b}".format(a = top_trs_ds_state,b = top_trs_ds_quater)
       elif top_trs_ds_state=='All' and top_trs_ds_year!='All' and top_trs_ds_quater=='All':
              query = "select * from top_transaction_district where year = {a}".format(a=top_trs_ds_year)
       elif top_trs_ds_state!='All' and top_trs_ds_year!='All' and top_trs_ds_quater=='All':
              query = "select * from top_transaction_district where year = {a} and state =\'{b}\'".format(a=top_trs_ds_year,b=top_trs_ds_state)
       else:
              query = "select * from top_transaction_district  where state =\'{a}\' and year = {b} and quater = {c}".format(a=top_trs_ds_state,b=top_trs_ds_year,c=top_trs_ds_quater)

       nk.execute(query)
       x = nk.fetchall()
       df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District', 'Total_Count', 'Total_Amount'])
       st.dataframe(df)
       st.markdown("CHOOSE A REQUIRED DATA AND DOWNLOAD IT....")
       csv = df.to_csv()
       st.download_button(
              label="Download data as CSV",
              data=csv,
              file_name='TOP_TRANSACTION_DISTRICT.csv',
              mime='text/csv', )

def top_trs_dis1():
       tab1, tab2 = st.tabs(["District Total Count", "District Total Amount"])
       with tab1:
              col1, col2, col3 = st.columns(3)
              with col1:
                     top_trs_ds_state = st.selectbox('NAME A STATE : ', state)
              with col2:
                     top_trs_ds_year = st.selectbox(' NAME A YEAR : ', year)
              with col3:
                     top_trs_ds_quater = st.selectbox(' NAME A QUATER : ', quater)

              if top_trs_ds_state == 'All' and top_trs_ds_year == 'All' and top_trs_ds_quater == 'All':
                     query = "select State,Year,Quater,District,Total_Count from top_transaction_district"
              elif top_trs_ds_state == 'All' and top_trs_ds_year == 'All' and top_trs_ds_quater != 'All':
                     query = "select State,Year,Quater,District,Total_Count from top_transaction_district where quater = {a}".format(a=top_trs_ds_quater)
              elif top_trs_ds_state == 'All' and top_trs_ds_year != 'All' and top_trs_ds_quater != 'All':
                     query = "select State,Year,Quater,District,Total_Count from top_transaction_district where year = {a} and  quater = {b}".format(
                            a=top_trs_ds_year, b=top_trs_ds_quater)
              elif top_trs_ds_state != 'All' and top_trs_ds_year == 'All' and top_trs_ds_quater == 'All':
                     query = "select State,Year,Quater,District,Total_Count from top_transaction_district where state = \'{a}\'".format(a=top_trs_ds_state)
              elif top_trs_ds_state != 'All' and top_trs_ds_year == 'All' and top_trs_ds_quater != 'All':
                     query = "select State,Year,Quater,District,Total_Count from top_transaction_district where state = \'{a}\' and quater = {b}".format(
                            a=top_trs_ds_state, b=top_trs_ds_quater)
              elif top_trs_ds_state == 'All' and top_trs_ds_year != 'All' and top_trs_ds_quater == 'All':
                     query = "select State,Year,Quater,District,Total_Count from top_transaction_district where year = {a}".format(a=top_trs_ds_year)
              elif top_trs_ds_state != 'All' and top_trs_ds_year != 'All' and top_trs_ds_quater == 'All':
                     query = "select State,Year,Quater,District,Total_Count from top_transaction_district where year = {a} and state =\'{b}\'".format(
                            a=top_trs_ds_year, b=top_trs_ds_state)
              else:
                     query = "select State,Year,Quater,District,Total_Count from top_transaction_district  where state =\'{a}\' and year = {b} and quater = {c}".format(a=top_trs_ds_state, b=top_trs_ds_year, c=top_trs_ds_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District', 'Total_Count'])
              st.dataframe(df)
              fig = px.bar(df, y="Total_Count", x="District", title=f' {top_trs_ds_state}  vs District Total_count ',
                           color="District", hover_data=["State","Year","Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)
       with tab2:
              col1, col2, col3 = st.columns(3)
              with col1:
                     top_trs_ds_state = st.selectbox('STATE:', state)
              with col2:
                     top_trs_ds_year = st.selectbox('YEAR:', year)
              with col3:
                     top_trs_ds_quater = st.selectbox('QUATER:', quater)

              if top_trs_ds_state == 'All' and top_trs_ds_year == 'All' and top_trs_ds_quater == 'All':
                     query = "select State,Year,Quater,District,Total_Amount from top_transaction_district"
              elif top_trs_ds_state == 'All' and top_trs_ds_year == 'All' and top_trs_ds_quater != 'All':
                     query = "select State,Year,Quater,District,Total_Amount from top_transaction_district where quater = {a}".format(a=top_trs_ds_quater)
              elif top_trs_ds_state == 'All' and top_trs_ds_year != 'All' and top_trs_ds_quater != 'All':
                     query = "select State,Year,Quater,District,Total_Amount from top_transaction_district where year = {a} and  quater = {b}".format(
                            a=top_trs_ds_year, b=top_trs_ds_quater)
              elif top_trs_ds_state != 'All' and top_trs_ds_year == 'All' and top_trs_ds_quater == 'All':
                     query = "select State,Year,Quater,District,Total_Amount from top_transaction_district where state = \'{a}\'".format(a=top_trs_ds_state)
              elif top_trs_ds_state != 'All' and top_trs_ds_year == 'All' and top_trs_ds_quater != 'All':
                     query = "select State,Year,Quater,District,Total_Amount from top_transaction_district where state = \'{a}\' and quater = {b}".format(
                            a=top_trs_ds_state, b=top_trs_ds_quater)
              elif top_trs_ds_state == 'All' and top_trs_ds_year != 'All' and top_trs_ds_quater == 'All':
                     query = "select State,Year,Quater,District,Total_Amount from top_transaction_district where year = {a}".format(a=top_trs_ds_year)
              elif top_trs_ds_state != 'All' and top_trs_ds_year != 'All' and top_trs_ds_quater == 'All':
                     query = "select State,Year,Quater,District,Total_Amount from top_transaction_district where year = {a} and state =\'{b}\'".format(
                            a=top_trs_ds_year, b=top_trs_ds_state)
              else:
                     query = "select State,Year,Quater,District,Total_Amount from top_transaction_district  where state =\'{a}\' and year = {b} and quater = {c}".format(
                            a=top_trs_ds_state, b=top_trs_ds_year, c=top_trs_ds_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District','Total_Amount'])
              st.dataframe(df)
              fig = px.bar(df, y="Total_Amount", x="District", title=f' {top_trs_ds_state}  vs District Total_Amount ',
                    color="District", hover_data=["State","Year", "Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)


def top_usr_pn():
       col1, col2, col3 = st.columns(3)
       with col1:
              top_usr_pn_state = st.selectbox('PICK A STATE : ', state)
       with col2:
              top_usr_pn_year = st.selectbox('PICK A YEAR : ', year)
       with col3:
              top_usr_pn_quater = st.selectbox('PICK A QUATER : ', quater)

       if top_usr_pn_state=='All' and top_usr_pn_year=='All' and top_usr_pn_quater=='All':
              query = "select * from top_user_pincode"
       elif top_usr_pn_state=='All' and top_usr_pn_year=='All' and top_usr_pn_quater!='All':
              query = "select * from top_user_pincode where quater = {a}".format(a=top_usr_pn_quater)
       elif top_usr_pn_state== 'All' and top_usr_pn_year != 'All' and top_usr_pn_quater != 'All':
              query = "select * from top_user_pincode where year = {a} and  quater = {b}".format(a=top_usr_pn_year,b = top_usr_pn_quater)
       elif top_usr_pn_state!= 'All' and top_usr_pn_year =='All' and top_usr_pn_quater =='All':
              query = "select * from top_user_pincode where state = \'{a}\'".format(a = top_usr_pn_state)
       elif top_usr_pn_state!= 'All' and top_usr_pn_year =='All' and top_usr_pn_quater !='All':
              query = "select * from top_user_pincode where state = \'{a}\' and quater = {b}".format(a = top_usr_pn_state,b = top_usr_pn_quater)
       elif top_usr_pn_state=='All' and top_usr_pn_year!='All' and top_usr_pn_quater=='All':
              query = "select * from top_user_pincode where year = {a}".format(a=top_usr_pn_year)
       elif top_usr_pn_state!='All' and top_usr_pn_year!='All' and top_usr_pn_quater=='All':
              query = "select * from top_user_pincode where year = {a} and state =\'{b}\'".format(a=top_usr_pn_year,b=top_usr_pn_state)
       else:
              query = "select * from top_user_pincode where state =\'{a}\' and year = {b} and quater = {c}".format(a=top_usr_pn_state,b=top_usr_pn_year,c=top_usr_pn_quater)
       nk.execute(query)
       x = nk.fetchall()
       df = pd.DataFrame(x, columns=['State', 'Year', 'Quater','Pincode_Name', 'Pincode_Registered_User'])
       st.dataframe(df)
       st.markdown("CHOOSE A REQUIRED DATA AND DOWNLOAD IT....")
       csv = df.to_csv()
       st.download_button(
              label="Download data as CSV",
              data=csv,
              file_name='TOP_USER_PINCODE.csv',
              mime='text/csv', )

def top_usr_pn1():
       col1, col2, col3 = st.columns(3)
       with col1:
              top_usr_pn_state = st.selectbox('STATE TYPE : ', state)
       with col2:
              top_usr_pn_year = st.selectbox('YEAR TYPE : ', year)
       with col3:
              top_usr_pn_quater = st.selectbox('QUATER TYPE : ', quater)

       if top_usr_pn_state == 'All' and top_usr_pn_year == 'All' and top_usr_pn_quater == 'All':
              query = "select * from top_user_pincode"
       elif top_usr_pn_state == 'All' and top_usr_pn_year == 'All' and top_usr_pn_quater != 'All':
              query = "select * from top_user_pincode where quater = {a}".format(a=top_usr_pn_quater)
       elif top_usr_pn_state == 'All' and top_usr_pn_year != 'All' and top_usr_pn_quater != 'All':
              query = "select * from top_user_pincode where year = {a} and  quater = {b}".format(
                     a=top_usr_pn_year,
                     b=top_usr_pn_quater)
       elif top_usr_pn_state != 'All' and top_usr_pn_year == 'All' and top_usr_pn_quater == 'All':
              query = "select * from top_user_pincode where state = \'{a}\'".format(a=top_usr_pn_state)
       elif top_usr_pn_state != 'All' and top_usr_pn_year == 'All' and top_usr_pn_quater != 'All':
              query = "select * from top_user_pincode where state = \'{a}\' and quater = {b}".format(
                     a=top_usr_pn_state,
                     b=top_usr_pn_quater)
       elif top_usr_pn_state == 'All' and top_usr_pn_year != 'All' and top_usr_pn_quater == 'All':
              query = "select * from top_user_pincode where year = {a}".format(a=top_usr_pn_year)
       elif top_usr_pn_state != 'All' and top_usr_pn_year != 'All' and top_usr_pn_quater == 'All':
              query = "select * from top_user_pincode where year = {a} and state =\'{b}\'".format(
                     a=top_usr_pn_year,
                     b=top_usr_pn_state)
       else:
              query = "select * from top_user_pincode where state =\'{a}\' and year = {b} and quater = {c}".format(
                     a=top_usr_pn_state, b=top_usr_pn_year, c=top_usr_pn_quater)
       nk.execute(query)
       x = nk.fetchall()
       df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'Pincode_Name', 'Pincode_Registered_User'])
       st.dataframe(df)
       fig = px.bar(df, y='Pincode_Registered_User', x="State",
                    title=f' {top_usr_pn_state}  vs Pincode Registered User ',
                    color="Pincode_Name", hover_data=["State", "Year", "Quater"])
       fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
       fig.update_layout(width=900, height=900)
       st.plotly_chart(fig)

def top_usr_district():
       col1, col2, col3 = st.columns(3)
       with col1:
              top_usr_ds_state = st.selectbox('PICK A STATE : ', state)
       with col2:
             top_usr_ds_year = st.selectbox('PICK A YEAR : ', year)
       with col3:
              top_usr_ds_quater = st.selectbox('PICK A QUATER : ', quater)

       if top_usr_ds_state=='All' and top_usr_ds_year=='All' and top_usr_ds_quater=='All':
              query = "select * from top_user_district"
       elif top_usr_ds_state=='All' and top_usr_ds_year=='All' and top_usr_ds_quater!='All':
              query = "select * from top_user_district where quater = {a}".format(a=top_usr_ds_quater)
       elif top_usr_ds_state== 'All' and top_usr_ds_year != 'All' and top_usr_ds_quater != 'All':
              query = "select * from top_user_district where year = {a} and  quater = {b}".format(a=top_usr_ds_year,b = top_usr_ds_quater)
       elif top_usr_ds_state!= 'All' and top_usr_ds_year =='All' and top_usr_ds_quater =='All':
              query = "select * from top_user_district where state = \'{a}\'".format(a = top_usr_ds_state)
       elif top_usr_ds_state!= 'All' and top_usr_ds_year =='All' and top_usr_ds_quater !='All':
              query = "select * from top_user_district where state = \'{a}\' and quater = {b}".format(a = top_usr_ds_state,b = top_usr_ds_quater)
       elif top_usr_ds_state=='All' and top_usr_ds_year!='All' and top_usr_ds_quater=='All':
              query = "select * from top_user_district where year = {a}".format(a=top_usr_ds_year)
       elif top_usr_ds_state!='All' and top_usr_ds_year!='All' and top_usr_ds_quater=='All':
              query = "select * from top_user_district where year = {a} and state =\'{b}\'".format(a=top_usr_ds_year,b=top_usr_ds_state)
       else:
              query = "select * from top_user_district where state =\'{a}\' and year = {b} and quater = {c}".format(a=top_usr_ds_state,b=top_usr_ds_year,c=top_usr_ds_quater)

       nk.execute(query)
       x = nk.fetchall()
       df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District','District_Registered_User'])
       st.dataframe(df)
       st.markdown("CHOOSE A REQUIRED DATA AND DOWNLOAD IT....")
       csv = df.to_csv()
       st.download_button(
              label="Download data as CSV",
              data=csv,
              file_name='TOP_USER_DISTRICT.csv',
              mime='text/csv', )

def top_usr_district1():
       col1, col2, col3 = st.columns(3)
       with col1:
              top_usr_ds_state = st.selectbox(' A STATE : ', state)
       with col2:
              top_usr_ds_year = st.selectbox(' A YEAR : ', year)
       with col3:
              top_usr_ds_quater = st.selectbox(' A QUATER : ', quater)

       if top_usr_ds_state == 'All' and top_usr_ds_year == 'All' and top_usr_ds_quater == 'All':
              query = "select * from top_user_district"
       elif top_usr_ds_state == 'All' and top_usr_ds_year == 'All' and top_usr_ds_quater != 'All':
              query = "select * from top_user_district where quater = {a}".format(a=top_usr_ds_quater)
       elif top_usr_ds_state == 'All' and top_usr_ds_year != 'All' and top_usr_ds_quater != 'All':
              query = "select * from top_user_district where year = {a} and  quater = {b}".format(a=top_usr_ds_year,
                                                                                                  b=top_usr_ds_quater)
       elif top_usr_ds_state != 'All' and top_usr_ds_year == 'All' and top_usr_ds_quater == 'All':
              query = "select * from top_user_district where state = \'{a}\'".format(a=top_usr_ds_state)
       elif top_usr_ds_state != 'All' and top_usr_ds_year == 'All' and top_usr_ds_quater != 'All':
              query = "select * from top_user_district where state = \'{a}\' and quater = {b}".format(
                     a=top_usr_ds_state, b=top_usr_ds_quater)
       elif top_usr_ds_state == 'All' and top_usr_ds_year != 'All' and top_usr_ds_quater == 'All':
              query = "select * from top_user_district where year = {a}".format(a=top_usr_ds_year)
       elif top_usr_ds_state != 'All' and top_usr_ds_year != 'All' and top_usr_ds_quater == 'All':
              query = "select * from top_user_district where year = {a} and state =\'{b}\'".format(a=top_usr_ds_year,
                                                                                                   b=top_usr_ds_state)
       else:
              query = "select * from top_user_district where state =\'{a}\' and year = {b} and quater = {c}".format(
                     a=top_usr_ds_state, b=top_usr_ds_year, c=top_usr_ds_quater)

       nk.execute(query)
       x = nk.fetchall()
       df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District', 'District_Registered_User'])
       st.dataframe(df)
       fig = px.bar(df, y='District_Registered_User', x="District", title=f' {top_usr_ds_state}  vs District Registered Users ',
                    color="District", hover_data=["State", "Year", "Quater"])
       fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
       fig.update_layout(width=900, height=900)
       st.plotly_chart(fig)


def top_agg_trs():
       tab1, tab2 = st.tabs(["Transaction count","Transaction Amount"])
       with tab1:
              col1, col2, col3 = st.columns(3)
              with col1:
                     agg_trs_state = st.selectbox('PICK-STATE  ', state)
              with col2:
                     agg_trs_year = st.selectbox('PICK-YEAR : ', year)
              with col3:
                     agg_trs_quater = st.selectbox('PICK-QUATER : ', quater)

              if agg_trs_state == 'All' and agg_trs_year == 'All' and agg_trs_quater == 'All':
                     query = "SELECT state,year,quater,transaction_type,transaction_count FROM aggregated_transactions ORDER BY transaction_count DESC LIMIT 10"
              elif agg_trs_state == 'All' and agg_trs_year == 'All' and agg_trs_quater != 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_count from AGGREGATED_TRANSACTIONS where quater = {a} ORDER BY transaction_count DESC LIMIT 10".format(a=agg_trs_quater)
              elif agg_trs_state == 'All' and agg_trs_year != 'All' and agg_trs_quater != 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_count from AGGREGATED_TRANSACTIONS where year = {a} and  quater = {b} ORDER BY transaction_count DESC LIMIT 10".format(
                            a=agg_trs_year, b=agg_trs_quater)
              elif agg_trs_state != 'All' and agg_trs_year == 'All' and agg_trs_quater == 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_count from AGGREGATED_TRANSACTIONS where state = \'{a}\' ORDER BY transaction_count DESC LIMIT 10".format(a=agg_trs_state)
              elif agg_trs_state != 'All' and agg_trs_year == 'All' and agg_trs_quater != 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_count from AGGREGATED_TRANSACTIONS where state = \'{a}\' and quater = {b} ORDER BY transaction_count DESC LIMIT 10".format(
                            a=agg_trs_state, b=agg_trs_quater)
              elif agg_trs_state == 'All' and agg_trs_year != 'All' and agg_trs_quater == 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_count from AGGREGATED_TRANSACTIONS where year = {a} ORDER BY transaction_count DESC LIMIT 10" .format(a=agg_trs_year)
              elif agg_trs_state != 'All' and agg_trs_year != 'All' and agg_trs_quater == 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_count from AGGREGATED_TRANSACTIONS where year = {a} and state =\'{b}\' ORDER BY transaction_count DESC LIMIT 10".format(
                            a=agg_trs_year, b=agg_trs_state)
              else:
                     query = "select State,Year,Quater,Transaction_Type,Transaction_count from AGGREGATED_TRANSACTIONS  where state =\'{a}\' and year = {b} and quater = {c} ORDER BY transaction_count DESC LIMIT 10".format(
                            a=agg_trs_state, b=agg_trs_year, c=agg_trs_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'Transaction_Type', 'Transaction_count'])
              st.write(df)
              fig = go.Figure(go.Pie(labels=df["Transaction_Type"], values=df['Transaction_count'], hole=0.5))
              fig.update_layout(width=900, height=800)
              st.plotly_chart(fig)
              fig = px.bar(df, y="Transaction_count", x="Transaction_Type", title=f'View of Transaction_Type vs Transaction_count ',
                           color="Transaction_Type", hover_data=['State', 'Year', "Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)

       with tab2:
              col1, col2, col3 = st.columns(3)
              with col1:
                     agg_trs_state = st.selectbox('PICKSTATE  ', state)
              with col2:
                     agg_trs_year = st.selectbox('PICKYEAR : ', year)
              with col3:
                     agg_trs_quater = st.selectbox('PICKQUATER : ', quater)

              if agg_trs_state == 'All' and agg_trs_year == 'All' and agg_trs_quater == 'All':
                     query = "SELECT state,year,quater,transaction_type,transaction_amount FROM aggregated_transactions ORDER BY transaction_amount DESC LIMIT 10"
              elif agg_trs_state == 'All' and agg_trs_year == 'All' and agg_trs_quater != 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_amount from AGGREGATED_TRANSACTIONS where quater = {a} ORDER BY transaction_amount DESC LIMIT 10".format(
                            a=agg_trs_quater)
              elif agg_trs_state == 'All' and agg_trs_year != 'All' and agg_trs_quater != 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_amount from AGGREGATED_TRANSACTIONS where year = {a} and  quater = {b} ORDER BY transaction_amount DESC LIMIT 10".format(
                            a=agg_trs_year, b=agg_trs_quater)
              elif agg_trs_state != 'All' and agg_trs_year == 'All' and agg_trs_quater == 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_amount from AGGREGATED_TRANSACTIONS where state = \'{a}\' ORDER BY transaction_amount DESC LIMIT 10".format(
                            a=agg_trs_state)
              elif agg_trs_state != 'All' and agg_trs_year == 'All' and agg_trs_quater != 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_amount from AGGREGATED_TRANSACTIONS where state = \'{a}\' and quater = {b} ORDER BY transaction_amount DESC LIMIT 10".format(
                            a=agg_trs_state, b=agg_trs_quater)
              elif agg_trs_state == 'All' and agg_trs_year != 'All' and agg_trs_quater == 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_amount from AGGREGATED_TRANSACTIONS where year = {a} ORDER BY transaction_amount DESC LIMIT 10".format(
                            a=agg_trs_year)
              elif agg_trs_state != 'All' and agg_trs_year != 'All' and agg_trs_quater == 'All':
                     query = "select State,Year,Quater,Transaction_Type,Transaction_amount from AGGREGATED_TRANSACTIONS where year = {a} and state =\'{b}\' ORDER BY transaction_amount DESC LIMIT 10".format(
                            a=agg_trs_year, b=agg_trs_state)
              else:
                     query = "select State,Year,Quater,Transaction_Type,Transaction_amount from AGGREGATED_TRANSACTIONS  where state =\'{a}\' and year = {b} and quater = {c} ORDER BY transaction_amount DESC LIMIT 10".format(
                            a=agg_trs_state, b=agg_trs_year, c=agg_trs_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'Transaction_Type', 'Transaction_Amount'])
              st.write(df)
              fig = go.Figure(go.Pie(labels=df["Transaction_Type"], values=df['Transaction_Amount'], hole=0.5))
              fig.update_layout(width=900, height=800)
              st.plotly_chart(fig)
              fig = px.bar(df, y="Transaction_Amount", x="Transaction_Type",
                           title=f'View of Transaction_Type vs Transaction_Amount ',
                           color="Transaction_Type", hover_data=['State', 'Year', "Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)


def top_agg_usr():
       tab1, tab2 ,tab3 = st.tabs(["Brand ", "Registered User","Appopens"])
       with tab1:
              col1, col2, col3 = st.columns(3)
              with col1:
                     agg_usr_state = st.selectbox('STATE FOR BRAND', state)
              with col2:
                     agg_usr_year = st.selectbox('YEAR FOR BRAND', year)
              with col3:
                     agg_usr_quater = st.selectbox('QUATER FOR BRAND', quater)
              if agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "SELECT * from AGGREGATED_USER_BRAND ORDER BY count DESC OFFSET 108 LIMIT 10"
              elif agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select * from AGGREGATED_USER_BRAND where quater = {a} ORDER BY COUNT DESC OFFSET 3 LIMIT 10 ".format(
                            a=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater != "All":
                     query = "select * from AGGREGATED_USER_BRAND where year = {a} and quater = {b} ORDER BY COUNT DESC OFFSET 3  LIMIT 10".format(
                            a=agg_usr_year, b=agg_usr_quater)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "select * from AGGREGATED_USER_BRAND where state = \'{a}\' ORDER BY COUNT DESC  OFFSET 3 LIMIT 10".format(
                            a=agg_usr_state)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select * from AGGREGATED_USER_BRAND where state = \'{a}\' and quater = {b} ORDER BY COUNT DESC OFFSET 3  LIMIT 10".format(
                            a=agg_usr_state, b=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select * from AGGREGATED_USER_BRAND where year = {a} ORDER BY COUNT DESC OFFSET 3 LIMIT 10".format(
                            a=agg_usr_year)
              elif agg_usr_state != "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select * from AGGREGATED_USER_BRAND where year = {a} and state =\'{b}\' ORDER BY COUNT DESC OFFSET 3 LIMIT 10".format(
                            a=agg_usr_year, b=agg_usr_state)
              else:
                     query = "select * from AGGREGATED_USER_BRAND  where state =\'{a}\' and year = {b} and quater = {c} ORDER BY COUNT DESC OFFSET 3 LIMIT 10".format(
                            a=agg_usr_state, b=agg_usr_year, c=agg_usr_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'Brand Name',"Count","Percentage"])
              st.dataframe(df)
              fig = px.bar(df, x="Brand Name", y="Count",
                           title=f'View of TOP 10 Brand Count  ',
                           color="Brand Name", hover_data=['State', 'Year', "Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)

       with tab2:
              col1, col2, col3 = st.columns(3)
              with col1:
                     agg_usr_state = st.selectbox('STATES', state)
              with col2:
                     agg_usr_year = st.selectbox('YEARS', year)
              with col3:
                     agg_usr_quater = st.selectbox('QUATERS', quater)
              if agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "select State,Year,Quater,Registered_User from AGGREGATED_USER_REGISTER ORDER BY Registered_User DESC LIMIT 10"
              elif agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select State,Year,Quater,Registered_User from AGGREGATED_USER_REGISTER where quater = {a} ORDER BY Registered_User DESC LIMIT 10 ".format(a=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater != "All":
                     query = "select State,Year,Quater,Registered_User from AGGREGATED_USER_REGISTER where year = {a} and quater = {b} ORDER BY Registered_User DESC LIMIT 10".format(a=agg_usr_year,b=agg_usr_quater)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "select State,Year,Quater,Registered_User from AGGREGATED_USER_REGISTER where state = \'{a}\' ORDER BY Registered_User DESC LIMIT 10".format(a=agg_usr_state)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select State,Year,Quater,Registered_User from AGGREGATED_USER_REGISTER where state = \'{a}\' and quater = {b} ORDER BY Registered_User DESC LIMIT 10".format(a=agg_usr_state,b=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select State,Year,Quater,Registered_User from AGGREGATED_USER_REGISTER where year = {a} ORDER BY Registered_User DESC LIMIT 10".format(a=agg_usr_year)
              elif agg_usr_state != "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select State,Year,Quater,Registered_User from AGGREGATED_USER_REGISTER where year = {a} and state =\'{b}\' ORDER BY Registered_User DESC LIMIT 10".format(a=agg_usr_year,b=agg_usr_state)
              else:
                     query = "select State,Year,Quater,Registered_User from AGGREGATED_USER_REGISTER  where state =\'{a}\' and year = {b} and quater = {c} ORDER BY Registered_User DESC LIMIT 10".format(a=agg_usr_state, b=agg_usr_year, c=agg_usr_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x,columns=['State', 'Year', 'Quater', 'Registered_User'])
              st.dataframe(df)
              fig = px.bar(df, y="Registered_User", x="State",
                           title=f'View of TOP 10 Registered_User ',
                           color="State", hover_data=['State', 'Year', "Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)
       with tab3:
              col1, col2, col3 = st.columns(3)
              with col1:
                     agg_usr_state = st.selectbox('STATE', state)
              with col2:
                     agg_usr_year = st.selectbox('YEAR', year)
              with col3:
                     agg_usr_quater = st.selectbox('QUATER', quater)
              if agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER_REGISTER ORDER BY AppOpens DESC LIMIT 10"
              elif agg_usr_state == "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER where quater = {a}".format(a=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater != "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER_REGISTER where year = {a} and quater = {b} ORDER BY AppOpens DESC LIMIT 10".format(a=agg_usr_year,b=agg_usr_quater)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater == "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER_REGISTER where state = \'{a}\' ORDER BY AppOpens DESC LIMIT 10".format(a=agg_usr_state)
              elif agg_usr_state != "All" and agg_usr_year == "All" and agg_usr_quater != "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER_REGISTER where state = \'{a}\' and quater = {b} ORDER BY AppOpens DESC LIMIT 10".format(a=agg_usr_state,b=agg_usr_quater)
              elif agg_usr_state == "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER_REGISTER where year = {a} ORDER BY AppOpens DESC LIMIT 10".format(a=agg_usr_year)
              elif agg_usr_state != "All" and agg_usr_year != "All" and agg_usr_quater == "All":
                     query = "select State, Year, Quater,AppOpens from AGGREGATED_USER_REGISTER where year = {a} and state =\'{b}\' ORDER BY AppOpens DESC LIMIT 10".format(a=agg_usr_year,b=agg_usr_state)
              else:
                     query ="select State, Year, Quater,AppOpens from AGGREGATED_USER_REGISTER  where state =\'{a}\' and year = {b} and quater = {c} ORDER BY AppOpens DESC LIMIT 10".format(a=agg_usr_state, b=agg_usr_year, c=agg_usr_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'AppOpens'])
              st.dataframe(df)
              fig = px.bar(df, y="AppOpens", x="State",
                           title=f'View of TOP 10 AppOpens ',
                           color="State", hover_data=['State', 'Year', "Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)


def top_map_usr():
       tab1, tab2 = st.tabs(["Registered User", "Appopens"])
       with tab1:
              col1, col2, col3 = st.columns(3)
              with col1:
                     map_usr_state = st.selectbox('SELECT STATE : ', state)
              with col2:
                     map_usr_year = st.selectbox('SELECT  YEAR : ', year)
              with col3:
                     map_usr_quater = st.selectbox('SELECT QUATER : ', quater)

              if map_usr_state == 'All' and map_usr_year == 'All' and map_usr_quater == 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER ORDER BY Registered_User DESC LIMIT 10"
              elif map_usr_state == 'All' and map_usr_year == 'All' and map_usr_quater != 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER where quater = {a} ORDER BY Registered_User DESC LIMIT 10".format(
                            a=map_usr_quater)
              elif map_usr_state == 'All' and map_usr_year != 'All' and map_usr_quater != 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER where year = {a} and  quater = {b} ORDER BY Registered_User DESC LIMIT 10".format(
                            a=map_usr_year,
                            b=map_usr_quater)
              elif map_usr_state != 'All' and map_usr_year == 'All' and map_usr_quater == 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER where state = \'{a}\' ORDER BY Registered_User DESC LIMIT 10".format(
                            a=map_usr_state)
              elif map_usr_state != 'All' and map_usr_year == 'All' and map_usr_quater != 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER where state = \'{a}\' and quater = {b} ORDER BY Registered_User DESC LIMIT 10".format(
                            a=map_usr_state,
                            b=map_usr_quater)
              elif map_usr_state == 'All' and map_usr_year != 'All' and map_usr_quater == 'All':
                     query = "select * from MAP_USER where year = {a} ORDER BY Registered_User DESC LIMIT 10".format(a=map_usr_year)
              elif map_usr_state != 'All' and map_usr_year != 'All' and map_usr_quater == 'All':
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER where year = {a} and state =\'{b}\' ORDER BY Registered_User DESC LIMIT 10".format(
                            a=map_usr_year,
                            b=map_usr_state)
              else:
                     query = "select State,Year,Quater, District,Registered_User from MAP_USER  where state =\'{a}\' and year = {b} and quater = {c} ORDER BY Registered_User DESC LIMIT 10".format(
                            a=map_usr_state, b=map_usr_year, c=map_usr_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District', 'Registered_User'])
              st.dataframe(df)
              fig = px.bar(df, x="District", y="Registered_User",
                           title=f'View of TOP 10 Registered user  ',
                           color="State", hover_data=['State', 'Year', "Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)
       with tab2:
              col1, col2, col3 = st.columns(3)
              with col1:
                     map_usr_state = st.selectbox('SELECTED STATE : ', state)
              with col2:
                     map_usr_year = st.selectbox('SELECTED  YEAR : ', year)
              with col3:
                     map_usr_quater = st.selectbox('SELECTED QUATER : ', quater)

              if map_usr_state == 'All' and map_usr_year == 'All' and map_usr_quater == 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER ORDER BY AppOpens DESC LIMIT 10"
              elif map_usr_state == 'All' and map_usr_year == 'All' and map_usr_quater != 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER where quater = {a} ORDER BY AppOpens DESC LIMIT 10".format(a=map_usr_quater)
              elif map_usr_state == 'All' and map_usr_year != 'All' and map_usr_quater != 'All':
                     query = "select State, Year,Quater,District,AppOpens  from MAP_USER where year = {a} and  quater = {b} ORDER BY AppOpens DESC LIMIT 10".format(a=map_usr_year,b=map_usr_quater)
              elif map_usr_state != 'All' and map_usr_year == 'All' and map_usr_quater == 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER where state = \'{a}\'ORDER BY AppOpens DESC LIMIT 10".format(a=map_usr_state)
              elif map_usr_state != 'All' and map_usr_year == 'All' and map_usr_quater != 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER where state = \'{a}\' and quater = {b} ORDER BY AppOpens DESC LIMIT 10".format(a=map_usr_state,b=map_usr_quater)
              elif map_usr_state == 'All' and map_usr_year != 'All' and map_usr_quater == 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER where year = {a} ORDER BY AppOpens DESC LIMIT 10".format(a=map_usr_year)
              elif map_usr_state != 'All' and map_usr_year != 'All' and map_usr_quater == 'All':
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER where year = {a} and state =\'{b}\' ORDER BY AppOpens DESC LIMIT 10".format(a=map_usr_year,b=map_usr_state)
              else:
                     query = "select State, Year,Quater,District,AppOpens from MAP_USER  where state =\'{a}\' and year = {b} and quater = {c} ORDER BY AppOpens DESC LIMIT 10".format(a=map_usr_state, b=map_usr_year, c=map_usr_quater)

              nk.execute(query)
              x = nk.fetchall()
              df = pd.DataFrame(x, columns=['State', 'Year', 'Quater', 'District', 'AppOpens'])
              st.dataframe(df)
              fig = px.bar(df, x="District", y="AppOpens",
                           title=f'View of TOP 10 Registered user  ',
                           color="State", hover_data=['State', 'Year', "Quater"])
              fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=20))
              fig.update_layout(width=900, height=900)
              st.plotly_chart(fig)


content = ['About','Overview','Transaction',"Users","TOP - 10","Outcomes"]
options = ["Aggregated Transaction", "Aggregated User", "Map Transaction","Map User","Top Transaction District","Top Transaction Pincode", "Top User District","Top User Pincode"]
with st.sidebar:
       opt = st.sidebar.selectbox('MENU',content)

if opt=='About':
       st.header("PHONEPAY PULSE ANALYSIS")
       st.subheader("INTRODUCTION")
       st.markdown("PhonePe Private Limited is a leading e-commerce payment platform in India.\
       The digital wallet company was founded in December 2015. This platform offers services in over 11 Indian regional languages.")
       st.markdown("PhonePe works on the Unified Payment Interface (UPI) system and all you need is to feed in your bank account details and create a UPI ID.\
       There is no need to recharge the wallet, because the money will be directly debited from your bank account at the click of a button in a safe and secure manner.")
       st.subheader("GROWTH & DEVELOPMENT")
       st.markdown("PhonePe retained its top position, processing the biggest number of UPI transactions in the month.\
       It processed 46.71% or 351.9 Cr UPI transactions in February 2023, amounting to INR 6.2 Lakh Cr during the period under review.\
       In terms of percentage, it accounted for 50.18% of the value of UPI transactions.")
       st.markdown("This year as we became India's largest digital payments platform with 46% UPI market share, we decided to demystify the what, why and how of digital payments in India.\
       This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, we thought as Indias largest digital payments platform with 46% UPI market share, we have a ring-side view of how India sends, spends, manages and grows its money.\
       So it was time to demystify and share the what, why and how of digital payments in India.")
       st.subheader("WHY WE NEED PHONEPE PULSE ")
       st.markdown("PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.")
       st.video("https://youtu.be/c_1H6vivsiA")

if opt == "Overview":
       st.header("TABLE VISUALIZATION")
       choice = st.sidebar.radio("Choose the type of the table",options)
       if choice == "Aggregated Transaction":
              agg_trs()

       elif choice == "Aggregated User":
              agg_usr()

       elif choice == "Map Transaction":
              map_trs()
       elif choice == "Map User":
              map_usr()
       elif choice == "Top Transaction District":
              top_trs_dis()

       elif choice == "Top Transaction Pincode":
              top_trs_pn()
       elif choice == "Top User District":
              top_usr_district()

       elif choice == "Top User Pincode":
              top_usr_pn()


if opt=="Transaction":
       st.header("TRANSACTIONS DETAILS")
       tab1, tab2, = st.tabs(["Aggregated Transaction", "Map Transaction"])
       with tab1:
              st.subheader("AGGREGATED_TRANSACTION")
              agg_trs1()
       with tab2:
              st.subheader("MAP_TRANSACTION")
              map_trs1()


if opt=="Users":
       st.header("USER DETAIL")
       tab1, tab2= st.tabs(["AGGREGATED_USERS", "MAP_USERS" ])
       with tab1:
              st.subheader("AGGREGATED_USERS")
              agg_usr1()
       with tab2:
              st.subheader("MAP_USERS")
              map_usr1()


if opt=="TOP - 10":
       st.header("TOP 10  ANALYSIS")
       tab1, tab2, tab3, tab4,tab5,tab6,tab7= st.tabs(["AGGREGATED TRANSACTION","AGGREGATED USER","MAP USER","TOP TRANSACTION DISTRICT","TOP TRANSACTION PINCODE","TOP_USER_DISTRICT","TOP_USER_PINCODE"])
       with tab1:
              st.subheader("TOP  10  TRANSACTION   COUNT AND  TRANSACTION  AMOUNT  BASED  ON  TRANSACTION TYPE")
              top_agg_trs()
       with tab2:
              st.subheader("TOP  10  REGISTERD  USER , APPOPENS  AND  BRAND  BASED  ON  COUNT")
              top_agg_usr()
       with tab3:
              st.subheader("TOP  10  REGISTERD USER  AND  APPOPENS  BASED  ON  DISTRICT")
              top_map_usr()
       with tab4:
              st.subheader("TOP  10  DISTRICT  COUNT  AND  DISTRICT  AMOUNT")
              top_trs_dis1()
       with tab5:
              st.subheader("TOP 10 PINCODE COUNT AND PINCODE AMOUNT")
              top_trs_pn1()
       with tab6:
              st.subheader("TOP 10 DISTRICT USERS")
              top_usr_district1()
       with tab7:
              st.subheader("TOP 10 PINCODE REGISTERED USERS")
              top_usr_pn1()

if opt=='Outcomes':
       st.subheader("KeyTakeAways")
       st.write("##### * PhonePe Pulse analysis can also be beneficial for businesses in several ways")
       st.write("##### * By analyzing transaction data, businesses can identify peak sales periods, popular products or services, and customer spending patterns. This information can help businesses make informed decisions regarding inventory management, pricing strategies, and marketing campaigns.")
       st.write("##### * PhonePe Pulse analysis can aid businesses in effectively managing their cash flow. By analyzing income and expense patterns, businesses can gain insights into their cash flow cycles, identify periods of surplus or deficit, and take appropriate measures to ensure a healthy cash flow.")
       st.write("##### * PhonePe Pulse analysis provides businesses with detailed transaction data that can be used for financial reporting and decision-making. The analysis can be used to generate reports, such as sales reports, expense reports, or profit and loss statements, which aid in assessing business performance, identifying areas of improvement, and making informed financial decisions.")




       st.write("##### * PhonePe Pulse analysis can provide businesses with valuable insights into sales, revenue, customer behavior, expenses, cash flow, and financial performance. By leveraging this analysis, businesses can make data-driven decisions, optimize their operations, and enhance their overall business approach.")






























