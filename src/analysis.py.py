import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/crime_data.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# ------ BASIC INSIGHTS ------
print("\n🔍 Top 10 Crime Locations:\n")
print(df['Location'].value_counts().head(10))

print("\n🔍 Crime Type Frequency:\n")
print(df['Crime_Type'].value_counts())

# ------ VISUALIZATION ------
plt.figure(figsize=(10,5))
sns.countplot(x='Crime_Type', data=df)
plt.xticks(rotation=45)
plt.title("Crime Type Frequency in the City")
plt.show()

# ------ MONTHLY TRENDS ------
df['Month'] = df['Date'].dt.month
monthly_trend = df.groupby('Month')['Crime_Type'].count()

plt.figure(figsize=(10,5))
monthly_trend.plot(kind='line', marker='o')
plt.title("Monthly Crime Trend")
plt.xlabel("Month")
plt.ylabel("Number of Crimes")
plt.show()

print("\n📌 Crime Trend by Month (For Report):\n")
print(monthly_trend)
