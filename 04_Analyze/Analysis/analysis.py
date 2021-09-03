import pandas as pd

df = pd.read_csv('C:/Users/kimba/VSCode Projects/Room_Temperature_Project/03_Process/cleaned_data.csv')

print(df.groupby(['time']).describe().loc[:, ['inside_temperature', 'outside_temperature']])