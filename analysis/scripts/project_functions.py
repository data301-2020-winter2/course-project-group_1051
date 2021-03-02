import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
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
def summary(data):
    # Summarizes the count, mean, standard deviation, min, and max for neighborhood group and room type.
    df3 = data.groupby('nbg')['price'].describe()
    df4 = data.groupby('room_type')['price'].describe()
    return df3, df4
def correlation_matrix(data):
    # Correlation Matrix
    corr = data.corr()# plot the heatmap
    sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, annot=True, cmap=sns.diverging_palette(220, 20, as_cmap=True))
def scatterplot(data):
    # Scatterplot
    data.plot(kind='scatter', y='reviews_per_month', x='minimum_nights')
def pairplot(data):
    # Pair plot
    sns.pairplot(data)
def histogram(data):
    #Histogram
    data['price'].plot(kind='hist', bins=200, figsize=(10,5), facecolor='grey',edgecolor='black')
def categorical_variabele_EDA(data):
    #Categorical variable EDA
    df_cat1 = data.select_dtypes(include = 'object').copy()
    df_cat2 = data.select_dtypes(include = 'object').copy()
    df_cat1.room_type.value_counts()
    df_cat2.nbg.value_counts()
    sns.countplot(data = df_cat1, x = 'room_type')
    sns.countplot(data = df_cat2, x = 'nbg')

load_and_process("/Users/yiraozhang/Desktop/course-project-group_1051/data/raw/AB_NYC_2019.csv")

