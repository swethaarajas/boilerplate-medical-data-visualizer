import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
bmi = df['weight'] / ((df['height'] / 100) ** 2)
over = []
for i in bmi:
    if i > 25:
        over.append(1)
    if i <= 25:
        over.append(0)
df['overweight'] = over


# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df["cholesterol"] = df["cholesterol"].apply(lambda x:0 if x == 1 else 1)
df["gluc"] = df["gluc"].apply(lambda x:0 if x == 1 else 1)

# Draw Categorical Plot
def draw_cat_plot():
  
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars= 'cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
# Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat["total"] = 1
    df_cat = df_cat.groupby(["cardio", "variable", "value"],as_index = False).count()
    

    # Draw the catplot with 'sns.catplot()'



    # Get the figure for the output
    fig = sns.catplot( x = 'variable', y ="total", data = df_cat, hue = 'value', col = 'cardio', kind = "bar").fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    df_heat = df[
    (df['ap_lo'] <= df['ap_hi'] ) &
    (df['height'] >= df['height'].quantile(0.025)) &
    (df['height'] <= df['height'].quantile(0.975)) &
    (df['weight'] >= df['weight'].quantile(0.025)) &
    (df['weight'] <= df['weight'].quantile(0.975))]

    #df_heat.drop('BMI',axis=1)
    
    # Calculate the correlation matrix
    corr = df_heat.corr(method = "pearson")
    #corr.drop('BMI', axis=1)
    # Generate a mask for the upper triangle
    mask = np.triu(corr)
  
    # Set up the matplotlib figure
    fig, axes = plt.subplots(figsize=(12,12))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask = mask, linewidths = 1, annot = True, fmt = ".1f", square = True, center = 0.08, cbar_kws = {"shrink":0.5})


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
