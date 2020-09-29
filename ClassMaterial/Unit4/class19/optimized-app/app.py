# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 15:53:06 2020

@author: Jonathan
"""

import streamlit as st
import pandas as pd
import pickle
import seaborn as sns
from matplotlib.pyplot import style
style.use('ggplot')

# list of columns to use for app
cols = ['MSSubClass', 'MSZoning', 'Neighborhood', 'OverallQual', 'OverallCond', 'YearBuilt', 'FullBath', 'HalfBath', 'GarageType']

num_cols = ['OverallQual', 'OverallCond', 'GrLivArea', 'SalePrice', 'LotArea', 'SalePrice']

st.title('Iowa Housing Data Application')

# loads in the grouping file to be used for bar/line charts
# notice the use of @st.cache -- save processing time
@st.cache
def load_grouping_file(x_col, y_col):
    filepath = f"https://raw.githubusercontent.com/JonathanBechtel/optimized-app/master/groupbys/{x_col}_{y_col}.csv"
    print(filepath)
    df = pd.read_csv(filepath, index_col=x_col)
    return df

# loads in the seaborn boxplot
# this function is NOT cached due to irregularities with how streamlit works
def load_boxplots(x_col, y_col):
    pickled_boxplot = f"boxplots/{x_col}_{y_col}.pkl"
    with open(pickled_boxplot, 'rb') as boxplot_dict:
        chart = pickle.load(boxplot_dict)
    return chart

def load_model_results(learning_rate, tree_depth, n_estimators, random_state, val_size):
    mod_results_path = f"https://raw.githubusercontent.com/JonathanBechtel/optimized-app/master/models/{learning_rate}_{tree_depth}_{n_estimators}_{random_state}_{round(val_size, 2)}.csv"
    print(mod_results_path)
    mod_results = pd.read_csv(mod_results_path)
    val_results_path = f"https://raw.githubusercontent.com/JonathanBechtel/optimized-app/master/models/val_{learning_rate}_{tree_depth}_{n_estimators}_{random_state}_{round(val_size, 2)}.csv"
    val_results = pd.read_csv(val_results_path)
    return mod_results, val_results

section = st.sidebar.radio('Choose Application Section', ['Data Explorer', 'Model Explorer', 'Causal Impact'])

if section == 'Data Explorer':
    
    st.subheader("Build Charts From Sidebar Choices")
    
    x_axis = st.sidebar.selectbox('Choose Column For X-Axis', cols)
    y_axis = st.sidebar.selectbox('Choose Column For Y-Axis', num_cols)
    
    chart_type = st.sidebar.selectbox('Choose Chart Type', ['bar', 'line', 'box'])
    
    if chart_type == 'bar':
        try:
            file = load_grouping_file(x_axis, y_axis)
            st.bar_chart(file)
        except:
            st.text("Could not find data for specified column combinations")    
        
    elif chart_type == 'line':
        try:
            file = load_grouping_file(x_axis, y_axis)
            st.line_chart(file)
        except:
            st.text("Could not find data for specified column combinations")
            
    elif chart_type == 'box':
        try:
            chart = load_boxplots(x_axis, y_axis)
            print(type(chart))
            st.pyplot(chart)
        except:
            st.text("Could not find seaborn chart figure for specified columns")
            
if section == 'Model Explorer':
    
    st.subheader("Explore Model Parameters")
    
    num_rounds    = st.sidebar.number_input('Number of Boosting Rounds',
                                 min_value=100, max_value=1000, step=100)
    
    tree_depth    = st.sidebar.number_input('Tree Depth',
                                 min_value=3, max_value=8, step=1, value=3)
    
    learning_rate = st.sidebar.selectbox('Learning Rate',
                                    [.01, .05, .1, .3, .5, 1], index=2)
    
    val_size      = st.sidebar.number_input('Validation Size',
                                      min_value=.2, max_value=.5, step=.1, value=0.2)
    
    random_state  = st.sidebar.number_input('Random State', min_value=1950, max_value=1959, step=1)

    # the function gets called with the input values as parameters whenever something is changed
    
    # make these empty sections, and then add in the appropriate content depending on whether or not the file
    # returned exists or not
    st.subheader("Model Results")
    results_section = st.empty()
    st.subheader("Predicted vs Actual Validation Values")
    preds_section   = st.empty()
    
    try:
        mod_results, val_results = load_model_results(learning_rate, tree_depth, num_rounds, random_state, val_size)
        results_section.table(mod_results)
        preds_section.pyplot(sns.regplot(x='Preds', y='Values', data=val_results).figure)
    except:
        results_section.text("Could not find the data with the listed parameters")
        preds_section.text("Could not find the data with the listed parameters")

    