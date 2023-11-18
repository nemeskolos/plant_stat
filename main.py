import pandas as pd
import streamlit as st
from Scripts.data_loading import data_preprocessing, data_read
from Scripts.stat import stats, calculate_t_tests
from Scripts.plots import reshape_for_plotting, create_line_chart, create_custom_plot

# Call the data processing functions from data_load.py
data_22, data_28 = data_read()
data = data_preprocessing(data_22, data_28)

# Calling the statistic functions from stat.py
mean_values, std_values, se_values = stats(data)
t_test_result_df = calculate_t_tests(data)

# Visualization part
mean_melted = reshape_for_plotting(mean_values, 'Mean')
std_melted = reshape_for_plotting(std_values, 'Std')
se_melted = reshape_for_plotting(se_values, 'SE')

stat_type = st.sidebar.selectbox(":green[Select a ] :red[Statistic]", options=["Mean", "Std", "SE"],
                        index=0, key='stat_type')

# Choose the statistic
if stat_type == "Mean":
    plot_data = mean_melted
elif stat_type == "Std":
    plot_data = std_melted
else:
    plot_data = se_melted

# Select the measurement type
mes_type = st.sidebar.selectbox(":green[Select a ] :red[Measurement Type]", options=plot_data["Measurement"].unique(),
                        index=0, key='mes_type')

# Select the group for comparison
group_to_compare = st.sidebar.selectbox(":green[Select a ] :red[Group for Comparison]", options=t_test_result_df.index.unique(),
                                index=0, key='group_to_compare')
# Select a date
selected_date = st.selectbox("Select a Date", options=plot_data["Date"].unique(),
                             index=0, key='selected_date')

# Creat a line chart
create_line_chart(plot_data, mes_type, group_to_compare)

# Create a boxplot
create_custom_plot(plot_data, selected_date, mes_type)
