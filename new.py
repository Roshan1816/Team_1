import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
from datetime import datetime, date

st.set_page_config(
    layout="wide",  # "centered" or "wide"
    initial_sidebar_state="expanded"  # "expanded" or "collapsed"
)
st.title('Daily Expenses Dashboard')
st.write(" ")

# Create a sidebar for user input
#st.sidebar.header('User Input')
#start_date = st.sidebar.date_input('Start Date')
#end_date = st.sidebar.date_input('End Date')

def load_data():
    data = pd.read_csv("expense_data_1.csv")
    data['Date'] = pd.to_datetime(data['Date'], format="%m/%d/%Y %H:%M")
    return data


data = load_data()

st.sidebar.title("Filter Options")

#start_date=pd.to_datetime(data["Date"]).min()
#end_date=pd.to_datetime(data["Date"]).max()

#date1=pd.to_datetime(st.sidebar.date_input("Start Date",start_date))
#date2=pd.to_datetime(st.sidebar.date_input("End Date",end_date))

start_date = st.sidebar.date_input("Start Date", format="YYYY/MM/DD")
end_date = st.sidebar.date_input("End Date", format="YYYY/MM/DD")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.sidebar.write("  ")

def inran(start,end):
   if start>=date(2022,1,1) and start<=date(2022,3,31):
      return True
   elif end>=date(2021,11,1) and end<=date(2021,12,31):
      return True
   else:
      return False

st.write('<center><style>div.row-widget.stButton > button {background-color: #35fcf6; color: black; font-size: 16px; padding: 6px 25px;}</style></center>', unsafe_allow_html=True)
if st.sidebar.button("submit"):
   if inran(start_date,end_date):
        filtered_data = data[(data['Date'].dt.date >= start_date) & (data['Date'].dt.date <= end_date)]
        # Display filtered data
        #    st.write("Filtered Data:")
        # st.write(filtered_data)
        plotdata=filtered_data[['Category','Amount']]
        x=filtered_data['Category']
        y=filtered_data['Amount']
        #    st.bar_chart(plotdata)
        #    st.line_chart(plotdata)
        
        #fig, ax = px.subplots()
        
        #plt.figure(figsize=(8, 6),facecolor='black')
        grouped_data = filtered_data.groupby('Category')['Amount'].sum().reset_index()
        #pie=px.pie(grouped_data['Amount'],labels=grouped_data['Category'],names="Category")
        #px.axis('equal')  
        #px.set_title('Expenses by Category')
        #for text in pie[1]:
         #   text.set_color('#05c7fc')
        #fig.patch.set_facecolor('black')
        # plt.figure(figsize=(1,3))
        #st.write(pie)
        C1, C2 = st.columns([2.8,1.5])

        #  left column
        with C1:
                #px.figure(figsize=(5,5))
                fig=px.pie(grouped_data, values="Amount", names="Category")
                #plt.pie(grouped_data['Amount'], labels=grouped_data['Category'], autopct='%1.1f%%', startangle=90)
                #plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                st.plotly_chart(fig,use_container_width=True)
                #st.write(fig)
                
        st.write("   ")
        
            #  right column
        with C2:
                # st.write("This is some content displayed on the right side.")
                # st.line_chart(plotdata)
                cd=data.groupby('Category')['Amount'].sum()
                st.write(cd)
                c=cd.max()
                d=cd.min()
                #st.sidebar.metric("higest spent on",f)
                #st.sidebar.metric("least spent on",d)
            

        st.write("")
        st.write("#### Filtered Data:" )
        st.write(filtered_data)
        st.write("  ")
        st.write("  ")
        
        df=pd.DataFrame(filtered_data)
        st.write("#### Spent on vs Amount")
        chart=alt.Chart(df).mark_bar().encode(x='Note',y='Amount').properties(width=975, height=650).configure_axis(
             titleFontSize=18)
        st.write("  ")
        st.write(chart)   
        wt=filtered_data.groupby('Income/Expense')['Amount'].sum()
        a=wt['Income']
        b=wt['Expense']
        st.sidebar.metric("Income",a)
        st.sidebar.metric("Expense", b)
   else:
      st.write('<span style="color:red">*** Data is not present in dataset in the given range plese enter valid range ***</span>', unsafe_allow_html=True)

   
else:
   expenses_data = pd.read_csv("expense_data_1.csv")
   expenses_df = pd.DataFrame(expenses_data)
   grouped_data = expenses_data.groupby('Category')['Amount'].sum().reset_index()
   
   c1,c2=st.columns([2,2])
   with c1:
      st.write(" ")
      st.write("### Expenses on different products")
      #px.figure(figsize=(10, 8),facecolor='black')
      fig=px.pie(grouped_data, values="Amount", names="Category")
      #pie=plt.pie(grouped_data['Amount'],labels=grouped_data['Category'], autopct='%1.1f%%', startangle=140,textprops={'fontsize': 12})
      #plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
      #px.title('Expenses by Category')
      #for text in pie[1]:
      #   text.set_color('#05c7fc')
      st.plotly_chart(fig,use_container_width=True)
      st.write(" ")
   
   st.write(" ")
    
   with c2:
      st.write(" ")
      data['Date'] = pd.to_datetime(data['Date'])

    # Extract month from 'Date' column
      data['Month'] = data['Date'].dt.month

    # Group data by month and sum the expenses
      monthly_expenses = data.groupby('Month')['Amount'].sum()
    #st.write(monthly_expenses)
    
      st.write("### Monthly Expenses")
      #px.figure(figsize=(8, 6),facecolor='#5b8da6')
      #fig=px.bar(df,x="Date", y="Amount")
      #fig=px.bar(monthly_expenses,x="Month", y="Amount")
      fig=px.bar(x=monthly_expenses.index, y=monthly_expenses.values)
      #px.xlabel('Month')
      #px.ylabel('Total Expenses')
      #px.title('Monthly Expenses')
      st.plotly_chart(fig,use_container_width=True)
      st.write(" ")
   st.write(" ")  
   st.write("#### Data: ")
   st.write(expenses_data)
#x=expenses_data['Date']
   st.write(" ")
   st.write("### Daily expenses in the year 2021-22")
   y = expenses_data.groupby('Date')['Amount'].sum().reset_index()
   
   st.set_option('deprecation.showPyplotGlobalUse', False)
   #px.figure(figsize=(8, 6),facecolor='#5b8da6')
   px.bar(x=['Date'], y=['Amount'])
   #px.xlabel('Date')
   #px.ylabel('Expenses ($)')
   #px.title('Expenses by date')
   st.plotly_chart(fig,use_container_width=True)
    
   a=monthly_expenses.max()
   b=monthly_expenses.min()
   rt=data.groupby('Income/Expense')['Amount'].sum()
   c=rt['Income']
   d=rt['Expense']
    
   st.write(" ")   
   st.sidebar.metric("Highest spent in the month", a)
   st.sidebar.metric("lowest spent in a month", b)
   st.sidebar.metric("Income", c)
   st.sidebar.metric("Expense", d)