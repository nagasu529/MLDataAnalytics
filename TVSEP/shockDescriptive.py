# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_selection import f_oneway
import statsmodels.api as sm
import numpy as np
import statsmodels.formula.api as smf # Use smf for formula API
from statsmodels.stats.anova import anova_lm #Import anova_lm correctly
import statsmodels.stats.multicomp as mc

#%%
# Load the dataset
shocks = pd.read_csv("E:/ExportFiles/shocks.csv")     
shocks_detail = pd.read_csv("E:/ExportFiles/shocks_detail.csv")      
shocks.head()
print(len(shocks))
# %%
# Count occurrences of each type of shock

shock_counts = shocks['typeshock'].value_counts()
shocks_id = shocks_detail['shocks__id'].value_counts()
print(shocks_id)
print(shock_counts)
print(sum(shock_counts))
print(sum(shocks_id))

#csv export for shocks_id and shocks_checking
shock_counts.to_csv("E:/ExportFiles/shock_counts.csv")
shocks_id.to_csv("E:/ExportFiles/shocks_id.csv")



# %%
a = [11,21,10,1,22,63,55,2,24,6,5,62,77,2,46,18,90,8,70]
b = ['Drought','Strong decrease of prices for Output','Flooding of agricultural land','Strong increase of prices for Input',
             'Illness of household member','Pests and Livestock diseases','Storm','Death of household member','Accident','House damage',
             'Had to spent money because of ceremony','Job loss','Flooding on the house/homestead','Household member left the household',
             'being cheated at work/business','Collapse of business','Other, specify','Conflict with neighbours in the village',
             'victim of crime (theft, robbery, etc.)']
shock_index = list(zip(a,b))
shock_dict = dict(shock_index)
print(shock_index)

#%%
#adding the new data from dict to shoch_detail dataframe.
shocks_detail['shock_id_description'] = shocks_detail['shocks__id'].map(shock_dict)
shocks_detail.head()


# %%

#shock_index basd on the catagories group.
def categorize_shock(shock):
    if shock in ['Drought','Flooding of agricultural land','Pests and Livestock diseases','Storm']:
        return "agricultural"
    elif shock in ['Illness of household member','Death of household member','Accident',
             'Household member left the household']:
        return "demographic"
    elif shock in ['House damage','Job loss','Flooding on the house/homestead','being cheated at work/business'
             ,'Collapse of business','Strong increase of prices for Input','Strong decrease of prices for Output',
             'Had to spent money because of ceremony','Collapse of business']:
        return "economics"
    elif shock in ['Conflict with neighbours in the village',
          'victim of crime (theft, robbery, etc.)']:
        return "social"
    else:
        return "others"

# Apply the custom function
shocks_detail["shocks_Group"] = shocks_detail["shock_id_description"].apply(categorize_shock)

#%%
#doing the crosstab and descriptive statistics thinks.
# Multi-index crosstab
indexDetail = shocks_detail.columns.tolist()
print(indexDetail)
ct = pd.crosstab(shocks_detail['shock_id_description'], shocks_detail['shocks_Group'])

# Visualize the crosstab using a heatmap (Seaborn)
plt.figure(figsize=(8, 6))  # Adjust figure size as needed
sns.heatmap(ct, annot=True, fmt="d", cmap="YlGnBu", cbar_kws={'label': 'Frequency'}) # fmt="d" for integer values
plt.title('Crosstab: Shock Experience vs. vXXX')
plt.xlabel('vXXX')
plt.ylabel('Shock Experience (v31102d)')
plt.show()


#Alternative visualization:  Bar chart (Matplotlib)

ct.plot(kind='bar', stacked=True, figsize=(10, 6)) # stacked=True stacks bars for each category
plt.title('Crosstab: Shock Experience vs. vXXX')
plt.xlabel('Shock Experience (v31102d)')
plt.ylabel('Frequency')
plt.legend(title='vXXX')
plt.show()

#%%
shocks_detail['shockmoneyloss'].describe()

#making the intervals value on shockmoneyloss and make a graph

# 1. Log Transformation:
shocks_detail['shockmoneyloss_log'] = np.log1p(shocks_detail['shockmoneyloss']) #log1p handles zeros

# 2. Class Intervals:
bin_edges = [0, 1000, 5000, 10000, 50000, 100000, float('inf')] # Example bins - adjust as needed
labels = ['0-1000', '1001-5000', '5001-10000', '10001-50000', '50001-100000', '100000+']
shocks_detail['shockmoneyloss_category'] = pd.cut(shocks_detail['shockmoneyloss'], bins=bin_edges, labels=labels, right=False)


# 3. Visualization:

# Histogram with log scale
plt.figure(figsize=(10, 6))
plt.hist(shocks_detail['shockmoneyloss_log'], bins=20)  # Adjust number of bins as needed
plt.title('Histogram of Shock Money Loss (Log Scale)')
plt.xlabel('Money Loss Amount (Log Transformed)')
plt.ylabel('Frequency')
plt.show()

# Box plot
plt.figure(figsize=(10, 6))
sns.boxplot(x=shocks_detail['shockmoneyloss_category'])
plt.title('Box Plot of Shock Money Loss Categories')
plt.xlabel('Money Loss Category')
plt.ylabel('Money Loss Amount')
plt.xticks(rotation=45, ha='right')
plt.show()

#Violin Plot
plt.figure(figsize=(10, 6))
sns.violinplot(x=shocks_detail['shockmoneyloss_category'])
plt.title('Violin Plot of Shock Money Loss Categories')
plt.xlabel('Money Loss Category')
plt.ylabel('Money Loss Amount')
plt.xticks(rotation=45, ha='right')
plt.show()


#Frequency Table
frequency_table = shocks_detail['shockmoneyloss_category'].value_counts().sort_index()
print("\nFrequency Table of shockmoneyloss Categories:\n", frequency_table)

#%%
#shock_index basd on the catagories group.
def shockValueLos_interval(shockValue):
    if shockValue < 1000:
        return "under 1,000"
    elif shockValue <= 5000:
        return "1,001-5,000"
    elif shockValue <= 10000:
        return "5,001 - 10,000"
    elif shockValue <= 50000:
        return "10,001 - 50,000"
    elif shockValue <= 100000:
        return "50,001 - 100,000"
    else:
        return "over 100,000"

# Apply the custom function
shocks_detail["shockValueLos_interval"] = shocks_detail["shockmoneyloss"].apply(shockValueLos_interval)

#doing the crosstab and descriptive statistics thinks.
# Multi-index crosstab
ct = pd.crosstab(shocks_detail['shockValueLos_interval'], shocks_detail['shocks_Group'])

# Visualize the crosstab using a heatmap (Seaborn)
plt.figure(figsize=(8, 6))  # Adjust figure size as needed
sns.heatmap(ct, annot=True, fmt="d", cmap="YlGnBu", cbar_kws={'label': 'Frequency'}) # fmt="d" for integer values
plt.title('Crosstab: shock value lost vs. group of shock')
plt.xlabel('group of shock')
plt.ylabel('shock value lost')
plt.show()


#Alternative visualization:  Bar chart (Matplotlib)

ct.plot(kind='bar', stacked=True, figsize=(10, 6)) # stacked=True stacks bars for each category
plt.title('Crosstab: shock value lost vs. group of shock')
plt.xlabel('group of shock')
plt.ylabel('shock value lost')
plt.legend(title='vXXX')
plt.show()

#%%
frequency_data = shocks['v31102b'].value_counts()
frequency_df = frequency_data.reset_index()
frequency_df.columns = ['Number of Shock', 'Frequency']

# Style the DataFrame for better visual appearance
styled_df = frequency_df.style.set_table_styles([
    {'selector': 'th', 'props': [('text-align', 'left'), ('font-weight', 'bold')]},  # Left-align headers, bold
    {'selector': 'td', 'props': [('text-align', 'right')]},  # Right-align data
    {'selector': '', 'props': [('border', '1px solid black'), ('border-collapse', 'collapse')]}, # Add borders
    {'selector': 'th, td', 'props': [('padding', '8px')]}, # Add padding for better spacing
    {'selector': '.row_heading', 'props': [('display', 'none')]} #Hide index
]).format({'Frequency': '{:d}'}) #Format frequency as integer


# Display the styled DataFrame
styled_df

#%%
#One-way anova

# Ensure 'shockmoneyloss' is numeric (handle potential non-numeric values)
shocks_detail['shockmoneyloss'] = pd.to_numeric(shocks_detail['shockmoneyloss'], errors='coerce')

# Group the data by 'shocks_Group'
groups = shocks_detail.groupby('shocks_Group')['shockmoneyloss']

# Extract the monetary loss values for each group
group_values = [group for name, group in groups]

# Perform one-way ANOVA
f_stat, p_value = f_oneway(*group_values)

# Print the results
print("F-statistic:", f_stat)
print("p-value:", p_value)

# Interpretation
if p_value < 0.05:
    print("There is a significant difference between the group means.")
else:
    print("There is no significant difference between the group means.")
#%%
shocks_detail.head()
#shocks_detail.to_csv('D:/ExportFiles/shocks_detail_merge.csv')

# %%
