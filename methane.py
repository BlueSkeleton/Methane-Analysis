import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import warnings
from bs4 import BeautifulSoup
import requests

st.set_page_config(
    page_icon=":smiley:",
    layout="wide",
)


def cleaner(a):
    return a.get_text()

def converter(b):
    b = b.replace(",", "").strip()
    if b == '':
        return None
    if 'bn t' in b:
        return float(b.replace('bn t','')) * 1000000000
    elif 'm t' in b:
        return float(b.replace('m t', '')) * 1000000
    elif 't' in b:
        return float(b.replace('t', ''))
    else:
        return None

url = "https://www.worlddata.info/greenhouse-gas-by-country.php"
meat = requests.get(url)
soup = BeautifulSoup(meat.content, "lxml")
table = soup.find_all("td")
cleantable = list(map(cleaner,table))
#print(cleantable) #10
rowlen = len(cleantable) / 10
#print("we're gonna have "+str(rowlen)+" rows")
primet = pd.DataFrame(np.array(cleantable).reshape(rowlen,10))     #we wanna keep 0 5 and 6, met co2 equivalent total and per capita
primet = primet.drop([1,2,3,4,7,8,9],axis = 1)
emissions = primet.drop(0,axis=0)
emissions = emissions.rename(columns={0: "Country",5: "Methane CO2 Equivalent(Tons)",6:"CO2 Equivalent per capita(tons)"})

emissions["Methane CO2 Equivalent(Tons)"] = emissions["Methane CO2 Equivalent(Tons)"].apply(converter)


#warnings.filterwarnings("ignore")


df_meth = pd.read_csv("methane.csv")
df_meth.drop(columns='source')
#df_meth.shape

df_oil_gas =  pd.read_csv("iae_og.csv")
df_coal = pd.read_csv("iae_coal.csv")
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
print(sorted_data)



# Create a stacked bar chart for the top 10 countries, broken down by type
def draw0():
    fig, ax = plt.subplots(figsize=(12, 6))
    top_grouped_data.pivot_table(values='emissions', index='country', columns='type', aggfunc='sum').loc[top_countries].plot(kind='bar', stacked=True, ax=ax)
    plt.title('Top 10 Countries by Methane Emissions - Type-wise')
    plt.xlabel('Country')
    plt.ylabel('Emissions')
    plt.legend(title='Type', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45)
    plt.show()

def draw1():
    fig, ax = plt.subplots(figsize=(12, 6))
    top_grouped_data.pivot_table(values='emissions', index='country', columns='type', aggfunc='sum').loc[top_countries].plot(kind='bar', ax=ax)
    plt.title('Top 10 Countries by Methane Emissions - Source-wise')
    plt.xlabel('Country')
    plt.ylabel('Emissions')
    plt.legend(title='Source', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45)
    plt.show()

def draw2():
    fig, ax = plt.subplots(figsize=(12, 6))
    sorted_data.plot(x='type', y='savings_to_cost_ratio', kind='bar', ax=ax, legend=None)
    plt.xlabel('Abatement Type')
    plt.ylabel('Savings-to-Cost Ratio')
    plt.title('Cost Efficiency of Methane Abatement Methods by Source')
    plt.xticks(rotation=75)
    plt.show()



##### Dashboard Stuff #####



st.set_option('deprecation.showPyplotGlobalUse', False)


st.markdown('''<h1 style='text-align: center; color: #7a0099;'>Methane in the Brain</h1><style>
span[data-baseweb="tag"] {
  background-color: purple !important;
}
</style>''', unsafe_allow_html=True)   #<----- title)


options = ['draw0','draw1', 'draw2', 'draw3', 'draw4']
st.sidebar.header("Choose your KPI")
selecto = st.sidebar.radio("KPI List", options)

if selecto == 'draw0':
    fig_0 = draw0()
    st.pyplot(fig_0)
elif selecto == 'draw1':
    fig_1 = draw1()
    st.pyplot(fig_1)
elif selecto == 'draw2':
    fig_2 = draw2()
    st.pyplot(fig_2)
elif selecto == 'draw3':
    fig_3 = draw3()
    st.pyplot(fig_3)
else:
    fig_4 = draw4()
    st.pyplot(fig_4)