import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import warnings
st.set_page_config(
    page_icon=":smiley:",
    layout="wide",
)
#warnings.filterwarnings("ignore")
df_meth = pd.read_csv("methane.csv")
df_meth.drop(columns='source')
#df_meth.shape
df_oil_gas =  pd.read_csv("oil_gas.csv")
df_coal = pd.read_csv("coal.csv")
df_abat = pd.concat([df_oil_gas, df_coal])
df2=df_abat.drop(["source"], axis=1)
#Data by country and type
grouped_data = df_meth.groupby(['country', 'type']).agg({'emissions': 'sum'}).reset_index()
# Sort the grouped data by emissions in descending order to get the top 10 countries
top_countries_data = grouped_data.groupby('country').agg({'emissions': 'sum'}).sort_values(by='emissions', ascending=False).head(10).reset_index()
top_countries = top_countries_data['country'].tolist()
top_grouped_data = grouped_data[grouped_data['country'].isin(top_countries)]
# Grouping data by type to get the mean savings and cost
abatement_grouped = df2.groupby('type').agg({'savings': 'mean', 'cost': 'mean'}).reset_index()
# savings-to-cost ratio
abatement_grouped['savings_to_cost_ratio'] = abatement_grouped['savings'] / abatement_grouped['cost']
# savings-to-cost ratio in descending order
sorted_data = abatement_grouped.sort_values(by='savings_to_cost_ratio', ascending=False)
# print(sorted_data)
# Create a stacked bar chart for the top 10 countries, broken down by type
def draw0():
    fig, ax = plt.subplots(figsize=(12, 6))
    top_grouped_data.pivot_table(values='emissions', index='country', columns='type', aggfunc='sum').loc[top_countries].plot(kind='bar', stacked=True, ax=ax)
    plt.title('Top 10 Countries by Methane Emissions - Type-wise')
    plt.xlabel('Country')
    plt.ylabel('Emissions')
    plt.legend(title='Type', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45)
    # plt.show()
df_oil_gas =  pd.read_csv("oil_gas.csv")
df_coal = pd.read_csv("coal.csv")
df_abat = pd.concat([df_oil_gas, df_coal])
#df_abat.shape
def draw1():
    fig, ax = plt.subplots(figsize=(12, 6))
    top_grouped_data.pivot_table(values='emissions', index='country', columns='type', aggfunc='sum').loc[top_countries].plot(kind='bar', ax=ax)
    plt.title('Top 10 Countries by Methane Emissions - Source-wise')
    plt.xlabel('Country')
    plt.ylabel('Emissions')
    plt.legend(title='Source', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45)
    # plt.show()
def draw2():
    fig, ax = plt.subplots(figsize=(12, 6))
    sorted_data.plot(x='type', y='savings_to_cost_ratio', kind='bar', ax=ax, legend=None)
    plt.xlabel('Abatement Type')
    plt.ylabel('Savings-to-Cost Ratio')
    plt.title('Cost Efficiency of Methane Abatement Methods by Source')
    plt.xticks(rotation=75)
    # plt.show()
##### Dashboard Stuff #####
st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown('''<h1 style='text-align: center; color: #7a0099;'>Methane in the Brain</h1><style>
span[data-baseweb="tag"] {
  background-color: purple !important;
}
</style>''', unsafe_allow_html=True)   #<----- title)
options = ['draw0','draw1', 'draw2', 'draw3', 'draw4', 'draw_pie_chart']
st.sidebar.header("Choose your KPI")
selecto = st.sidebar.radio("KPI List", options)
def draw3():
    top_grouped_data_sum = top_grouped_data.groupby('type').agg({'emissions': 'sum'}).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(top_grouped_data_sum['emissions'], labels=top_grouped_data_sum['type'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('Proportion of Total Emissions by Type for Top 10 Countries')
    # plt.show()
    
 
def draw4():
    fig, ax = plt.subplots(figsize=(10, 6))
    sorted_data.plot(x='type', y='cost', kind='barh', ax=ax, legend=None)
    plt.xlabel('Average Cost')
    plt.ylabel('Abatement Type')
    plt.title('Average Cost of Methane Abatement Methods by Type')
    # plt.show()
    
def draw_pie_chart():
    # Group data by type and sum the emissions for each type
    type_emissions = df_meth.groupby("type")["emissions"].sum().reset_index()
    # Create the pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(type_emissions["emissions"], labels=type_emissions["type"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Share of Methane Emissions by Type (All Countries)")
    # plt.show()
    
# def draw_pie_chart():
#     all_countries_grouped = df_meth.groupby('type').agg({'emissions': 'sum'}).reset_index()
#     fig, ax = plt.subplots(figsize=(8, 8))
#     ax.pie(all_countries_grouped['emissions'], labels=all_countries_grouped['type'], autopct='%1.1f%%', startangle=90)
#     ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
#     plt.title('Methane Emissions by Type for All Countries')
#     # plt.show()
    
if selecto == 'draw0':
    draw0()
    st.pyplot()
    
elif selecto == 'draw1':
    draw1()
    st.pyplot()
elif selecto == 'draw2':
    draw2()
    st.pyplot()
elif selecto == 'draw3':
    draw3()
    st.pyplot()
else: # 'draw4'
    draw4()
    st.pyplot()