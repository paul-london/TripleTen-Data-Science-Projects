# Module import
import streamlit as st
import pandas as pd
import plotly.express as px

# Read CSV
data = pd.read_csv('vehicles_us.csv')

# Data cleanup
# There are 51525 rows of information, and some columns have missing values: model_year, cylinders, odometer, paint_color, and is_4wd
# We should also convert model_year and cylinders to integer type, and is_4wd to bool type
# Missing model years can be filled in with the median model year of each car model, since many people don't list the model year
median_model_year = data.groupby('model')['model_year'].median()
data['model_year'] = data['model_year'].fillna(median_model_year)
#data['model_year'] = data['model_year'].astype(int) # this doesn't work, not sure why

# Electric cars have 0 cylinders, we can make that substitution prior to replacing missing values
# Other missing values can be filled in with the median cylinders for each model
data.loc[data['fuel'] == 'electric', 'cylinders'] = 0.0
median_cylinders = data.groupby('model')['cylinders'].median()
data['cylinders'] = data['cylinders'].fillna(median_cylinders)
#data['model_year'] = data['model_year'].astype(int) # this doesn't work, not sure why

# If odometer information wasn't included, we should use the mean odometer for each model year, to reflect average driving amount.
mean_odometer = data.groupby('model_year')['odometer'].mean()
data['odometer'] = data['odometer'].fillna(mean_odometer)

# If the color wasn't included in the listing, we can just replace these with 'Unknown'
data['paint_color'] = data['paint_color'].fillna('Unknown')

# If the 4WD information wasn't included in the listing, we can just replace these with 'Unknown'
data['is_4wd'] = data['is_4wd'].fillna('Unknown')
data['is_4wd'] = data['is_4wd'].astype(bool) 

# Header and brief introduction
st.header('Analysis of Car Sales Advertisements')
st.text('We are working with a dataset of used car advertisements. \nAs part of this project, we will take a look at the data itself, make sure it is complete and correct, and gather insights using plots and analysis. \nPlease take a moment to explore the various visualizations and analyses.')

# Histogram of Model Years of the cars - outliers removed (model year > 1989)
data_filtered_hist = data[data['model_year'] > 1989]
hist = px.histogram(data_filtered_hist, x='model_year', title='Model Year Frequency', nbins=100, labels={'x':'Model Year', 'y':'Count'})
hist.update_layout(bargap=0.1)
st.plotly_chart(hist)

# Making checkbox to alter behavior of scatter plot between sorting by fuel type to sorting by vehicle condition
checked = st.checkbox('If checked: Change scatterplot to sort by Vehicle Condition')
if checked:
    st.write('Scatterplot will sort by Vehicle Condition')
    # Scatter plot of price vs. odometer reading
    color_map_cond = {'salvage': 'red', 'like new': 'blue', 'good': 'green', 'fair': 'orange', 'excellent': 'black', 'new': 'yellow'}
    data_filtered_scatter = data[(data['odometer'] < 400000) & (data['price'] < 100000)]
    scatter_price_odo = px.scatter(data_filtered_scatter, title='Sale Price vs. Odometer Reading (by Vehicle Condition)', x='odometer', y='price', hover_data=['odometer', 'price'], color='condition', color_discrete_map=color_map_cond)
    st.plotly_chart(scatter_price_odo)
else:
    st.write('Scatterplot will sort by Fuel Type')
    color_map = {'gas': 'red', 'hybrid': 'blue', 'electric': 'green', 'diesel': 'orange', 'other': 'black'}
    data_filtered_scatter = data[(data['odometer'] < 400000) & (data['price'] < 100000)]
    scatter_price_odo = px.scatter(data_filtered_scatter, title='Sale Price vs. Odometer Reading (by Fuel Type)', x='odometer', y='price', hover_data=['odometer', 'price'], color='fuel', color_discrete_map=color_map)
    st.plotly_chart(scatter_price_odo)