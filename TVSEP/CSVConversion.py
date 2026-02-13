# %%
import pandas as pd
import matplotlib.pyplot as plt

# Read the .dta file (BSRU PC, MSI Claw, Home PC)
#file_path = "C:/Users/kitti/TVSepData/shocks.dta"
#file_path = "C:/Users/kitti/TVSepData/shocks_detail.dta"
#file_path = "C:/Users/kitti/TVSepData/ShockData/TVSEP2022SurveyV1.dta"

# Read the .dta file (HP Notebook)
#file_path = "C:/Users/Admin/TVSepData/ShockData/shocks.dta"
#file_path = "C:/Users/Admin/TVSepData/ShockData/shocks_detail.dta"
#file_path = "C:/Users/Admin/TVSepData/ShockData/TVSEP2022SurveyV1.dta"

# Read the .dta file (BSRU PC)
#file_path = "E:/ExportFiles/stataFiles/shocks.dta"
#file_path = "E:/ExportFiles/stataFiles/shocks_detail.dta"
file_path = "E:/ExportFiles/stataFiles/TVSEP2022SurveyV1.dta"
data = pd.read_stata(file_path)

# Display the first few rows
print("First 5 rows of data:")
print(data.head())

# Display basic information about the dataset
print("\nDataset Info:")
print(data.info())

# Display summary statistics
print("\nDescriptive Statistics:")
print(data.describe())

# Check for missing values
print("\nMissing Values Per Column:")
print(data.isnull().sum())

# %%
# Replace 'column_name' with the name of the column you want to visualize
column_names = list(data.columns)
print(column_names)



# %%
#Export data to .csv files.
#data.to_csv("C:/Full_2007_TH.csv")
data.to_csv("E:/ExportFiles/TVSEP2022SurveyV1.csv")

# %%


# %%
#Descriptive the comlumns overview on seaborn.

"""
data['typeshock'].hist(bins=20)
plt.title("Histogram of head_ethnicity")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()
"""



# %%
