import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
def load_and_process(url_or_path_to_csv_file):

    # Method Chain 1 (Load data and deal with missing data)

    df1 = (
          pd.read_csv(url_or_path_to_csv_file)
          .rename(columns={"neighbourhood_group": "nbg","neighbourhood":"nb", "calculated_host_listings_count":"hostlistcount"})
          .dropna()
          # etc...
      )

    # Method Chain 2 (Create new columns, drop others, and group the data by neighborhood group and room type)

    df2 = (
          df1.assign(minimum_cost=lambda x: x['minimum_nights']*x['price'])
            .drop(['last_review', 'id', 'host_id','latitude','longitude'], axis=1).loc[lambda x: x['availability_365']>0]
      )
    return df2

sns.set_theme(style="darkgrid")
# Averafe price and popularity of different room type, visualized by barplots and countplots
def price_by_room_type(data):#summary pivot table
    df = data.groupby('room_type')['price'].describe()
    return df
def popularity_by_room_type_countplot(data):#countplot of different room type, showing the popularity of each room type
    ax = sns.countplot(x="room_type", data=data)
def price_by_room_barplot(data):#barplot of average price of different room type
    name=['Entire home/apt','Private room','Shared room']
    mean=[]
    for i in range(len(data['mean'])):
        mean.append(data['mean'][i])
    ax = sns.barplot(x=name, y=mean)
    ax.set(xlabel='room_type', ylabel='average price')
df1 = price_by_room_type(df_cleaned)
popularity_by_room_type_countplot(df_cleaned)
price_by_room_barplot(df1)

# Averafe price and popularity of different neighbourhood group, visualized by barplots and countplots
def price_by_nbg(data):
    df = data.groupby('nbg')['price'].describe()#summary pivot table
    return df
def popularity_by_nbg_countplot(data):#countplot of different neighourhood group, showing the popularity of each room type
    ax = sns.countplot(x='nbg',data=data)
def price_by_nbg_barplot(data):#barplot of average price of different neighbourhood group
    name=["Bronx","Brooklyn",'Manhattan','Queens','Staten Island']
    mean=[]
    for i in range(len(data['mean'])):
        mean.append(data['mean'][i])
    ax = sns.barplot(x=name, y=mean)
    ax.set(xlabel='neighbourhood_group', ylabel='average price')
df2 = price_by_nbg(df_cleaned)
df2
price_by_nbg_barplot(df2)
popularity_by_nbg_countplot(df_cleaned)

#Before plotting correlation matrix, we can convert the categorical variable 'room_type' and 'neighbourhood_group' to numeric variable.
def convert(data):#first convert room_type, then convert neighbourhood group
    df1 = (
      data.assign(room_type_num=lambda x: np.where(x['room_type']=='Entire home/apt', 3, (np.where(x['room_type']=='Private room',2,(np.where(x['room_type']=='Shared room',1,0))))))
        .assign(nbg_num=lambda x: np.where(x['nbg']=='Manhattan', 5, (np.where(x['nbg']=='Brooklyn',4,(np.where(x['nbg']=='Queens',3,np.where(x['nbg']=='Staten Island',2,1)))))))
  )
    return df1
df_cleaned_converted=convert(df_cleaned)

def correlation_matrix(data):
    # Explore correlation between the variables.
    corr = data.corr()# plot the heatmap
    sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, annot=True, cmap=sns.diverging_palette(220, 20, as_cmap=True))
correlation_matrix(df_cleaned)

# Scatterplot
def scatterplot1(data):
    data.plot(kind='scatter', y='reviews_per_month', x='minimum_nights')
scatterplot1(df_cleaned_converted)
def scatterplot2(data):
    data.plot(kind='scatter', y='price', x='nbg_num')
scatterplot2(df_cleaned_converted)
def scatterplot3(data):
    data.plot(kind='scatter', y='price', x='room_type_num')
scatterplot3(df_cleaned_converted)

#Histogram
def histogram(data):
    df_cleaned_converted['price'].plot(kind='hist', bins=200, figsize=(12,6), facecolor='grey',edgecolor='black')

