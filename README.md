# FLO - Customer Segmentation with RFM Analysis

## Overview

FLO, an online shoe store, aims to divide its customers into segments and determine marketing strategies based on these
segments. To achieve this, customer behaviors will be identified, and groups will be formed based on clustering patterns
in these behaviors.

## Project Structure

- **rfm.py**: Python script containing functions for preparing rfm dataset.
- **rfm_research.xlsx**: Python script containing obs./researchs from raw dataset .
- **rfm_flo.csv**: Excel file containing the rfm scores and segments.
- **target_customer_ids.csv**: CSV file for first task.
- **offer_target_customer_ids.csv**: CSV file for second task.
- **dataset/flo_data_20k.csv**: Excel file containing the dataset.

## Requirements

Make sure to install the required packages before running the script:

```bash
pip install -r requirements.txt
```

The required packages are:

- pandas==2.1.1
- matplotlib==3.8.2
- seaborn==0.12.2

## Functionality

### `dataset_summary(dataframe)`

Provides a basic summary of the dataset, including its shape, head, info, null values, and descriptive statistics.

### `category_frequency(dataset, cat_col, plot=False)`

Calculates and displays the frequency of each unique category in a specified column. Optionally, it can plot the results
using seaborn.

### `data_prep(dataframe)`

Formats the given dataframe into the appropriate structure before creating the RFM.

### `create_rfm(dataframe, csv=True, days=3)`

Creates Recency-Frequency-Monetary (RFM) scores and segments based on the provided DataFrame. Optionally saves the
resulting RFM DataFrame to a CSV file named rfm_flo.csv

## Additional Analysis

1. New Women's Shoe Brand Promotion:
    - Identifies and saves target customer IDs for a new women's shoe brand promotion.
    - The target customers are in the 'champions' and 'loyal_customers' segments, who have shown interest in the women's
      category."
2. Discount on Men's and Children's Products:
    - Identifies and saves customer IDs for a discount on Men's and Children's products.
    - The target customers are in segments such as "hibernating," "at_risk," "cant_loose," "new_customers," and "
      promising" who have shown interest in the relevant categories.

These tasks demonstrate the practical application of RFM analysis for targeted marketing strategies.
