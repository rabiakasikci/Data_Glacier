# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 09:21:39 2024

@author: Rabia KAŞIKCI
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

Cab_Data = pd.read_csv("Cab_Data.csv")
City = pd.read_csv("City.csv")
Customer_ID = pd.read_csv("Customer_ID.csv")
Transaction_ID = pd.read_csv("Transaction_ID.csv")


print("Cab Data:")
print(Cab_Data.head())

print("\nCustomer Data:")
print(Customer_ID.head())

print("\nTransaction Data:")
print(Transaction_ID.head())

print("\nCity Data:")
print(City.head())




print("Null value:")
print(Cab_Data.isnull().sum())

print("\nNull value:")
print(Customer_ID.isnull().sum())

print("\nNull value:")
print(Transaction_ID.isnull().sum())

print("\nNull value:")
print(City.isnull().sum())



print("satitical value:")
print(Cab_Data.describe())

print("\satitical value:")
print(Customer_ID.describe())

print("\satitical value:")
print(Transaction_ID.describe())

print("\satitical value:")
print(City.describe())



result = pd.merge(Cab_Data, Transaction_ID, on='Transaction ID', how='inner')  # 'ID' sütununa göre iç birleştirme
data =   pd.merge(result, Customer_ID, on='Customer ID', how='inner')  # 'ID' sütununa göre iç birleştirme


total_customer_pink  = data[data["Company"]== "Pink Cab" ]["Customer ID"].unique().sum()
total_customer_yellow = data[data["Company"]== "Yellow Cab" ]["Customer ID"].unique().sum()

companies = ['Pink Cab', 'Yellow Cab']
total_customers = [total_customer_pink, total_customer_yellow]


plt.figure(figsize=(12, 6))
plt.bar(companies, total_customers, width=0.5, color="#f05131", label="Müşteri Sayısı")
plt.ylabel("Number of customer")
plt.xlabel("Company")
plt.legend()

plt.show()




total_cost = data.groupby('Company')['Cost of Trip'].sum().reset_index()

plt.figure(figsize=(8, 5))
plt.bar(total_cost['Company'], total_cost['Cost of Trip'], color=['blue', 'orange'])
plt.title('Total Cost of Trip by Company')
plt.xlabel('Company')
plt.ylabel('Total Cost of Trip')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()




# Pink Cab
unique_customers_pink_cab = data[data["Company"] == "Pink Cab"]["Customer ID"].unique()
male_customers_pink_cab = data[(data["Customer ID"].isin(unique_customers_pink_cab)) & (data["Gender"] == "Male")].shape[0]
female_customers_pink_cab = data[(data["Customer ID"].isin(unique_customers_pink_cab)) & (data["Gender"] == "Female")].shape[0]
customers_age_pink_cab = data[data["Customer ID"].isin(unique_customers_pink_cab)]["Age"]

# Yellow Cab
unique_customers_yellow_cab = data[data["Company"] == "Yellow Cab"]["Customer ID"].unique()
male_customers_yellow_cab = data[(data["Customer ID"].isin(unique_customers_yellow_cab)) & (data["Gender"] == "Male")].shape[0]
female_customers_yellow_cab = data[(data["Customer ID"].isin(unique_customers_yellow_cab)) & (data["Gender"] == "Female")].shape[0]
customers_age_yellow_cab = data[data["Customer ID"].isin(unique_customers_yellow_cab)]["Age"]

# Print results
print("Pink Cab - Male Customers:", male_customers_pink_cab)
print("Pink Cab - Female Customers:", female_customers_pink_cab)
print("Pink Cab - Average Age:", customers_age_pink_cab.mean())

print("Yellow Cab - Male Customers:", male_customers_yellow_cab)
print("Yellow Cab - Female Customers:", female_customers_yellow_cab)
print("Yellow Cab - Average Age:", customers_age_yellow_cab.mean())

# Combine data for both companies
labels = ['Male Pink Cab', 'Female Pink Cab', 'Male Yellow Cab', 'Female Yellow Cab']
sizes = [male_customers_pink_cab, female_customers_pink_cab, male_customers_yellow_cab, female_customers_yellow_cab]
colors = ['#f05131', '#f0d031', '#31f0f0', '#d1f031']  # Colors for each category
explode = (0.1, 0, 0.1, 0)  # Explode the Male slices for both companies

# Create a pie chart for the combined data
plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, 
        autopct='%1.1f%%', startangle=90)

# Title
plt.title('Customer Gender Distribution - Pink Cab vs Yellow Cab')

# Equal aspect ratio ensures the pie chart is circular
plt.axis('equal')

# Show the plot
plt.show()




#AGE HİSTOGRAM

age_counts_pink = customers_age_pink_cab.value_counts().sort_index()

age_counts_yellow = customers_age_yellow_cab.value_counts().sort_index()







# Histogramı oluşturmak için
plt.figure(figsize=(10, 6))  # Figure boyutunu ayarla

# Pink Cab için histogram çizimi
plt.hist(customers_age_pink_cab, bins=10, edgecolor='black', alpha=0.7, label='Pink Cab', color='red')

# Yellow Cab için histogram çizimi
plt.hist(customers_age_yellow_cab, bins=10, edgecolor='black', alpha=0.7, label='Yellow Cab', color='yellow')

# Grafik ayarları
plt.title('Pink Cab vs Yellow Cab Yaş Dağılımı')
plt.xlabel('Yaş')
plt.ylabel('Kişi Sayısı')
plt.grid(True)
plt.legend()  # Lengend ekleyelim
plt.tight_layout()

# Histogramı göster
plt.show()



city_counts = data.groupby("City")["Transaction ID"].count()

plt.figure(figsize=(12,6))
plt.bar(city_counts.index, city_counts.values,width=0.5,
        color="#f05131")
plt.ylabel("Number of Uses")
plt.xlabel("City")
plt.legend()
plt.title("Use of taxi")
plt.xticks(rotation=90)  # Rotate labels to be vertical

plt.show()


pink_ny = data[(data["City"] == "NEW YORK NY") & (data["Company"] == "Pink Cab") ].shape[0]
yellow_ny = data[(data["City"] == "NEW YORK NY") & (data["Company"] == "Yellow Cab") ].shape[0]

print(pink_ny ,yellow_ny )


data.groupby(["City", "Company"])["Customer ID"].count()


grouped_data = data.groupby(["City", "Company"])["Customer ID"].count().unstack()

# Plotting
grouped_data.plot(kind='bar', figsize=(10, 6))
plt.title('Customer Count by City and Company')
plt.xlabel('City')
plt.ylabel('Customer Count')
plt.xticks(rotation=45)
plt.legend(title='Company')
plt.tight_layout()
plt.show()


volume_by_method = data.groupby('Payment_Mode')['Transaction ID'].sum().reset_index()

print(volume_by_method)

data['Date of Travel'] = pd.to_datetime(data['Date of Travel'] - 25569, unit='D')



data_year = data[data['Date of Travel'].dt.year == 2018]

# Yıllara göre toplam cost hesapla (2016 için)
annual_cost_year = data_year.groupby(['Company', 'Date of Travel'])['Cost of Trip'].sum().reset_index()

# Grafiği oluştur
plt.figure(figsize=(10, 6))

for company in annual_cost_2016['Company'].unique():
    company_data = annual_cost_2016[annual_cost_year['Company'] == company]
    plt.plot(company_data['Date of Travel'], company_data['Cost of Trip'], marker='o', label=company)

plt.title('Change of Cost of Trip according yo year -2018')
plt.xlabel('Date')
plt.ylabel('Sum Cost of Trip')
plt.xticks(rotation=45)  # Tarihleri daha iyi görmek için döndür
plt.legend(title='Company')
plt.grid()
plt.tight_layout()  # Grafiğin daha iyi görünmesi için
plt.show()




data["income_category"] = data["Income (USD/Month)"].apply(
    lambda x: "Low Income" if x < 3000 else ("Middle Income" if x < 7000 else "High Income")
)



grouped_data = data.groupby(["income_category", "Company"]).agg({

    "Transaction ID": "count"     # İşlem sayısı
}).reset_index()







from IPython.display import display

# Tablonun görüntülenmesi
display(grouped_data)

# Grafik oluşturma
plt.figure(figsize=(10, 6))
sns.barplot(data=grouped_data, x='income_category', y='Transaction ID', hue='Company', palette='viridis')

# Grafik başlıkları ve etiketleri
plt.title('Transaction Count by Income Category and Company', fontsize=16)
plt.xlabel('Income Category', fontsize=14)
plt.ylabel('Transaction Count', fontsize=14)
plt.legend(title='Company')
plt.grid(axis='y')

# Grafiği göster
plt.tight_layout()
plt.show()



####################################################################################################
#                     
#                              FORECASTING
#
####################################################################################################


from statsmodels.tsa.holtwinters import ExponentialSmoothing

monthly_customers = data[data['Company'].isin(['Pink Cab', 'Yellow Cab'])].groupby(['Company', data['Date of Travel'].dt.to_period('M')]).nunique()['Customer ID']

# Şirket verilerini ayırma
pink_monthly_customers = monthly_customers['Pink Cab']
yellow_monthly_customers = monthly_customers['Yellow Cab']

# Model oluşturma ve eğitme
forecast_results = {}

for company_data, company_name in zip([pink_monthly_customers, yellow_monthly_customers], ['Pink Cab', 'Yellow Cab']):
    model = ExponentialSmoothing(company_data, trend='mul', seasonal=None)
    model_fit = model.fit()

    # 12 aylık tahmin yapma
    forecast = model_fit.forecast(steps=12)
    forecast_results[company_name] = forecast
    print(f"{company_name} için tahmin:\n{forecast}\n")

# Grafiği oluştur
plt.figure(figsize=(10, 6))
plt.plot(pink_monthly_customers.index.to_timestamp(), pink_monthly_customers.values, label='Pink Cab', color='blue')
plt.plot(yellow_monthly_customers.index.to_timestamp(), yellow_monthly_customers.values, label='Yellow Cab', color='red')

# Tahmin verisini çiz
forecast_index = pd.date_range(start=pink_monthly_customers.index[-1].to_timestamp(), periods=13, freq='M')[1:]
plt.plot(forecast_index, forecast_results['Pink Cab'], label='Pink Cab Tahmin', color='cyan', linestyle='--')
plt.plot(forecast_index, forecast_results['Yellow Cab'], label='Yellow Cab Tahmin', color='orange', linestyle='--')

# Başlık ve etiketler
plt.title('Aylık Müşteri Sayıları ve Tahminler')
plt.xlabel('Tarih')
plt.ylabel('Müşteri Sayısı')

# Legend ekle
plt.legend()

# Grafiği göster
plt.show()