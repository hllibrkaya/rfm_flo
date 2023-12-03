import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
sns.set(rc={'figure.figsize': (15, 6)})

dataframe = pd.read_csv("dataset/flo_data_20k.csv")
df = dataframe.copy()


def dataset_summary(dataframe):
    """
    This function visually prints basic summary statistics of a given pandas DataFrame.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        The DataFrame  to examine.
    Returns
    -------
    None
        The function only prints the outputs to the console and doesn't return any value.
    """
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### HEAD #####################")
    print(dataframe.head())
    print("##################### Info #####################")
    print(dataframe.info())
    print("##################### NULL VALUES #####################")
    print(dataframe.isnull().sum())
    print("##################### Describe #####################")
    print(dataframe.describe().T)

def category_frequency(dataset, cat_col, plot=False):
    """
    This function finds the frequency of each unique category in a specified column of a pandas DataFrame.

    Parameters
    ----------
    dataset : pandas.DataFrame
        The DataFrame containing the data.
    cat_col : str
        The name of the categorical column for which you want to calculate the frequency.
    plot : bool, optional
        Whether to plot the frequency using seaborn. Default is False.

    Returns
    -------
        None
            The function only prints/plots the frequency table and the count of unique elements to the console.
    """
    print(f"There are {dataset[cat_col].nunique()} unique elements in this column.")
    frequency_table = pd.DataFrame({"FREQUENCY": dataset[cat_col].value_counts()})
    print(frequency_table)

    if plot:
        colors = sns.color_palette('pastel')
        sns.countplot(data=dataset, x= cat_col, order=frequency_table.index, palette=colors)
        plt.ylabel("FREQUENCY")
        plt.show()


dataset_summary(df)

df["omnichannel_total_order_num"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["omnichannel_customer_value_total"] = df["customer_value_total_ever_offline"] + df[
    "customer_value_total_ever_online"]

date_cols = df.columns[df.columns.str.contains("date")]
df[date_cols] = df[date_cols].apply(pd.to_datetime)

df.groupby("order_channel").agg({"master_id": "count",
                                 "omnichannel_total_order_num": "sum",
                                 "omnichannel_customer_value_total": "sum"})

df.sort_values(by="omnichannel_customer_value_total", ascending=False)[:10]

df.sort_values(by="omnichannel_total_order_num", ascending=False)[:10]

max_order_date = df["last_order_date"].max()

analysis_date = max_order_date + pd.Timedelta(days=3)  # 3 days after the last order

rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).dt.days
rfm["frequency"] = df["omnichannel_total_order_num"]
rfm["monetary"] = df["omnichannel_customer_value_total"]

rfm["recency_score"] = pd.qcut(rfm["recency"], 5, [5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, [1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, [1, 2, 3, 4, 5])

rfm["rf_score"] = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm["segment"] = rfm["rf_score"].replace(seg_map, regex=True)

rfm.groupby("segment").agg({"recency": ["mean", "count"],
                            "frequency": ["mean", "count"],
                            "monetary": ["mean", "count"]
                            })

category_frequency(rfm, "segment", plot=True)

# TASKS
######################################################################

# FLO is incorporating a new women's shoe brand into its portfolio.
# The product prices of the newly included brand surpass the general customer preferences.
# Therefore, there is a desire to establish special communication with customers of the targeted profile
# for the promotion and sales of the brand. It is planned that these customers will be loyal individuals who
# make purchases from the women's category. Save the customer IDs in a CSV file as "new_brand_target_customer_ids.csv."

target = rfm[rfm["segment"].isin(["champions", "loyal_customers"])]["customer_id"]
customers = df[(df["master_id"].isin(target)) & (df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
customers.to_csv("target_customer_ids.csv", index=False)

######################################################################

# A discount of nearly 40% is planned for Men's and Children's products.
# The aim is to specifically target past loyal customers who have shown interest in categories related to this discount
# but haven't made purchases for an extended period, as well as new customers.
# Save the IDs of customers with the appropriate profile in a CSV file as "discount_target_customer_ids.csv."

target = rfm[rfm["segment"].isin(["hibernating", "at_risk", "cant_loose", "new_customers", "promising"])]["customer_id"]

customers = df[
    (df["master_id"].isin(target)) & (
            df["interested_in_categories_12"].str.contains("ERKEK") |
            df["interested_in_categories_12"].str.contains("COCUK")
    )
    ]["master_id"]

customers.to_csv("offer_target_customer_ids.csv", index=False)
