# Copyright 2025 [Your Name or Organization Name]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime as dt
import pandas as pd

def rfm_analysis(orders_df, order_items_df):
    """
    Melakukan analisis RFM (Recency, Frequency, Monetary) berdasarkan data pesanan dan item pesanan.
    
    Parameters:
        orders_df (DataFrame): Data pesanan pelanggan.
        order_items_df (DataFrame): Data item pesanan.
    
    Returns:
        DataFrame: Data pelanggan dengan skor RFM dan kategori.
    """
    # Set tanggal analisis (current_date)
    current_date = dt.datetime(2018, 10, 17)
    
    # Gabungkan orders_df dengan order_items_df berdasarkan order_id
    rfm_df = orders_df.merge(order_items_df, on='order_id')
    rfm_df['order_purchase_timestamp'] = pd.to_datetime(rfm_df['order_purchase_timestamp'])
    rfm_df = rfm_df.drop_duplicates(subset='order_id')  # Hapus duplikasi order_id

    # Hitung Recency, Frequency, dan Monetary untuk setiap customer_id
    rfm = rfm_df.groupby('customer_id').agg({
        'order_purchase_timestamp': lambda x: (current_date - x.max()).days,  # Recency
        'order_id': 'count',  # Frequency
        'price': 'sum'  # Monetary
    }).reset_index()
    
    # Ganti nama kolom
    rfm.columns = ['customer_id', 'Recency', 'Frequency', 'Monetary']

    # Segmentasi R, F, M menggunakan binning
    rfm['R_Segment'] = pd.qcut(rfm['Recency'], q=4, labels=[4, 3, 2, 1])  # Recency: Semakin rendah, semakin baik
    bins = [0, 3, 6, 10, float('inf')]  # Frequency: Tentukan bin manual
    labels = [1, 2, 3, 4]  # Semakin tinggi, semakin sering
    rfm['F_Segment'] = pd.cut(rfm['Frequency'], bins=bins, labels=labels, right=True)
    rfm['M_Segment'] = pd.qcut(rfm['Monetary'], q=4, labels=[1, 2, 3, 4])  # Monetary: Semakin tinggi, semakin baik
    
    # Hitung skor RFM total
    rfm['RFM_Score'] = rfm[['R_Segment', 'F_Segment', 'M_Segment']].sum(axis=1)

    # Fungsi untuk mengkategorikan pelanggan berdasarkan RFM
    def categorize_rfm(row):
        recency = int(row['R_Segment'])
        frequency = int(row['F_Segment'])
        monetary = int(row['M_Segment'])

        if recency == 4 and frequency == 4 and monetary == 4:
            return 'Champions'
        elif recency >= 3 and frequency >= 3:
            return 'Loyal Customers'
        elif recency >= 3 and frequency >= 2:
            return 'Potential Loyalists'
        elif recency == 4 and frequency <= 2:
            return 'New Customers'
        elif recency >= 3 and frequency == 1:
            return 'Promising'
        elif recency == 2 and frequency >= 2:
            return 'Need Attention'
        elif recency == 2 and frequency == 1:
            return 'About to Sleep'
        elif recency == 1 and (frequency >= 3 or monetary >= 3):
            return 'Can\'t Lose'
        elif recency == 1 and frequency >= 2:
            return 'At Risk'
        else:
            return 'Hibernating'

    # Fungsi untuk kategori Recency
    def categorize_recency(row):
        recency = row['R_Segment']
        if recency == 1:
            return 'Low'
        elif recency == 2:
            return 'Medium'
        elif recency == 3:
            return 'High'
        else:
            return 'Very High'

    # Fungsi untuk kategori Frequency
    def categorize_frequency(row):
        frequency = row['F_Segment']
        if frequency == 1:
            return 'Low'
        elif frequency == 2:
            return 'Medium'
        elif frequency == 3:
            return 'High'
        else:
            return 'Very High'

    # Fungsi untuk kategori Monetary
    def categorize_monetary(row):
        monetary = row['M_Segment']
        if monetary == 1:
            return 'Low'
        elif monetary == 2:
            return 'Medium'
        elif monetary == 3:
            return 'High'
        else:
            return 'Very High'

    # Tambahkan kolom kategori ke DataFrame
    rfm['Recency_Category'] = rfm.apply(categorize_recency, axis=1)
    rfm['Frequency_Category'] = rfm.apply(categorize_frequency, axis=1)
    rfm['Monetary_Category'] = rfm.apply(categorize_monetary, axis=1)
    rfm['Customer_Category'] = rfm.apply(categorize_rfm, axis=1)

    return rfm
