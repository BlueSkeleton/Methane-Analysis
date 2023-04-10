import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

df_meth = pd.read_csv("methane.csv")
df_coal = pd.read_excel("iae_coal.xlsx")
#df_coal.columns
df_coal.drop(columns ='source')
df_coal.dropna()
df_og =  pd.read_excel("iae_og.xlsx")
#df_og.columns
df_og.drop(columns= 'source')
#df_abat.head()
#print(df_abat)
#df_meth.head()
#df_meth.describe()
#df_meth.columns
df_meth.drop(columns='notes')
df_abat = pd.concat([df_og, df_coal])
df = pd.concat([df_abat, df_meth])
#print(df)
df.dropna()
#print(df)
df_meth.drop(columns='source')
sorted_data = df_meth.sort_values(by='emissions', ascending=False)
#print(sorted_data)
#sorted_data.head(20)
sorted_data.dropna()
df_meth.drop(columns='source')
df_meth.drop(columns='reason')

grouped_data = df_meth.groupby(['country', 'source', 'type']).agg({'emissions': 'sum'}).reset_index()
top_countries_data = grouped_data.groupby('country').agg({'emissions': 'sum'}).sort_values(by='emissions', ascending=False).head(10).reset_index()
top_countries = top_countries_data['country'].tolist()
top_grouped_data = grouped_data[grouped_data['country'].isin(top_countries)]
fig, ax = plt.subplots(figsize=(12, 6))
top_grouped_data.pivot_table(values='emissions', index='country', columns='source', aggfunc='sum').loc[top_countries].plot(kind='bar', ax=ax)
plt.title('Top 10 Countries by Methane Emissions - Source-wise')
plt.xlabel('Country')
plt.ylabel('Emissions')
plt.legend(title='Source', bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)
plt.show()

fig, ax = plt.subplots(figsize=(12, 6))
top_grouped_data.pivot_table(values='emissions', index=['country', 'source'], columns='type', aggfunc='sum').loc[[(country, source) for country in top_countries for source in top_grouped_data['source'].unique()]].plot(kind='bar', ax=ax)
plt.title('Top 10 Countries by Methane Emissions - Sub-source-wise')
plt.xlabel('Country, Source')
plt.ylabel('Emissions')
plt.legend(title='Type', bbox_to_anchor=(1, 1))
plt.xticks(rotation=75)
plt.show()
df_meth.drop(columns='notes')

# Assuming your dataset is stored in a DataFrame named 'data'

# Group the data by country, source, and type
grouped_data = df.groupby(['country', 'source', 'type']).agg({'emissions': 'sum'}).reset_index()

# Sort the grouped data by emissions in descending order and select the top 10 countries
top_countries_data = grouped_data.groupby('country').agg({'emissions': 'sum'}).sort_values(by='emissions', ascending=False).head(10).reset_index()
top_countries = top_countries_data['country'].tolist()
top_grouped_data = grouped_data[grouped_data['country'].isin(top_countries)]

# Sort the data by source in descending order
top_grouped_data = top_grouped_data.sort_values(by='source', ascending=False)

# Create a bar chart for the top 10 countries, broken down by source
fig, ax = plt.subplots(figsize=(12, 6))
top_grouped_data.pivot_table(values='emissions', index='country', columns='source', aggfunc='sum').loc[top_countries].plot(kind='bar', ax=ax)
plt.title('Top 10 Countries by Methane Emissions - Source-wise')
plt.xlabel('Country')
plt.ylabel('Emissions')
plt.legend(title='Source', bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)

plt.show()

# Create a bar chart for the top 10 countries, broken down by source and type
fig, ax = plt.subplots(figsize=(12, 6))
top_grouped_data.pivot_table(values='emissions', index=['country', 'source'], columns='type', aggfunc='sum').loc[[(country, source) for country in top_countries for source in top_grouped_data['source'].unique()]].plot(kind='bar', ax=ax)
plt.title('Top 10 Countries by Methane Emissions - Sub-source-wise')
plt.xlabel('Country, Source')
plt.ylabel('Emissions')
plt.legend(title='Type', bbox_to_anchor=(1, 1))
plt.xticks(rotation=75)

plt.show()