import pandas as pd


def data_prep(dataframe):
    """
    This function formats the dataframe into the appropriate structure before creating the RFM.

    Parameters
    ----------
    dataframe : pandas.DataFrame

    Returns
    -------
    dataframe : pandas.DataFrame


    """
    dataframe["total_order_num"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe[
        "customer_value_total_ever_online"]
    date_cols = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_cols] = dataframe[date_cols].apply(pd.to_datetime)

    return dataframe


def create_rfm(dataframe, csv=True, days=3):
    """
    Creates Recency-Frequency-Monetary (RFM) scores and segments based on the provided DataFrame.

    Parameters
    ----------
    dataframe: pandas.DataFrame
        Input DataFrame containing relevant customer data, including columns such as 'last_order_date',
        'total_order_num', 'customer_value_total', 'master_id'.
    csv :  bool, optional
        If True, the resulting RFM DataFrame will be saved to a CSV file named 'rfm_flo.csv' in the current directory.
        Default is True.
    days : int, optional
        Number of days to add to the maximum order date for recency calculation. Default is 3.

    Returns
    -------
    rfm: pandas.DataFrame
        DataFrame containing customer IDs, RFM values, and corresponding RFM scores and segments.

    """
    dataframe = data_prep(dataframe)

    max_order_date = dataframe["last_order_date"].max()
    analysis_date = max_order_date + pd.Timedelta(days=days)

    rfm = pd.DataFrame()
    rfm["customer_id"] = dataframe["master_id"]
    rfm["recency"] = (analysis_date - dataframe["last_order_date"]).dt.days
    rfm["frequency"] = dataframe["total_order_num"]
    rfm["monetary"] = dataframe["customer_value_total"]

    rfm["recency_score"] = pd.qcut(rfm["recency"], 5, [5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, [1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, [1, 2, 3, 4, 5])

    rfm["rf_score"] = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)
    rfm["rf_score"] = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)
    rfm["rfm_score"] = rfm["rf_score"].astype(str) + rfm["monetary_score"].astype(str)

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

    if csv:
        rfm.to_csv("rfm_flo.csv")

    return rfm


df_original = pd.read_csv("dataset/flo_data_20k.csv")
df = df_original.copy()

create_rfm(df)
