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
# Create a stacked bar chart for the top 10 countries, broken down by type
def emissions_type_wise():
    fig, ax = plt.subplots(figsize=(12, 6))
    top_grouped_data.pivot_table(values='emissions', index='country', columns='type', aggfunc='sum').loc[top_countries].plot(kind='bar', stacked=True, ax=ax)
    plt.title('Top 10 Countries by Methane Emissions - Type-wise', color= "green")
    plt.xlabel('Country')
    plt.ylabel('Emissions')
    plt.legend(title='Type', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45)
    
df_oil_gas =  pd.read_csv("oil_gas.csv")
df_coal = pd.read_csv("coal.csv")
df_abat = pd.concat([df_oil_gas, df_coal])
def emissions_source():
    fig, ax = plt.subplots(figsize=(12, 6))
    top_grouped_data.pivot_table(values='emissions', index='country', columns='type', aggfunc='sum').loc[top_countries].plot(kind='bar', ax=ax)
    plt.title('Top 10 Countries by Methane Emissions - Source-wise')
    plt.xlabel('Country')
    plt.ylabel('Emissions')
    plt.legend(title='Source', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45)
def abatement_cost():
    fig, ax = plt.subplots(figsize=(12, 6))
    sorted_data.plot(x='type', y='savings_to_cost_ratio', kind='bar', ax=ax, legend=None, color= "green")
    plt.xlabel('Abatement Type')
    plt.ylabel('Savings-to-Cost Ratio')
    plt.title('Cost Efficiency of Methane Abatement Methods by Source')
    plt.xticks(rotation=75)
# creating dashboard
st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown('''<h1 style='text-align: center; color: #028A0F;'>Methane Emissions</h1><style>
span[data-baseweb="tag"] {
  background-color: purple !important;
}
</style>''', unsafe_allow_html=True)   #<----- title)
options = ['emissions type wise', 'emissions source', 'abatement cost', 'proportion total emissions', 'average abatement cost']
st.sidebar.header("Choose your KPI")
selecto = st.sidebar.radio("KPI List", options)
def proportion_total_emissions():
    top_grouped_data_sum = top_grouped_data.groupby('type').agg({'emissions': 'sum'}).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(top_grouped_data_sum['emissions'], labels=top_grouped_data_sum['type'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('Proportion of Total Emissions by Type for Top 10 Countries')
    # plt.show()
    
 
def average_abatement_cost():
    fig, ax = plt.subplots(figsize=(10, 6))
    sorted_data.plot(x='type', y='cost', kind='barh', ax=ax, legend=None, color= "green")
    plt.xlabel('Average Cost')
    plt.ylabel('Abatement Type')
    plt.title('Average Cost of Methane Abatement Methods by Type')
    # plt.show()
    
    
if selecto == 'emissions type wise':
    emissions_type_wise()
    st.pyplot()
    
elif selecto == 'emissions source':
    emissions_source()
    st.pyplot()
elif selecto == 'abatement cost':
    abatement_cost()
    st.pyplot()
elif selecto == 'proportion total emissions':
    proportion_total_emissions()
    st.pyplot()
else: #'average_abatement_cost'
    average_abatement_cost()
    st.pyplot()