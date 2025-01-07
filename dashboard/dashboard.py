import streamlit as st
import pandas as pd
import plotly.express as px
from rfm import rfm_analysis

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("E-Commerce Dashboard")

@st.cache_data
def load_data():
    order_items_df = pd.read_csv("E:/Data Kerja Fito/Dicoding/Proyek Analisis Data/data/order_items_dataset.csv")
    orders_df = pd.read_csv("E:/Data Kerja Fito/Dicoding/Proyek Analisis Data/data/orders_dataset.csv")
    customer_df = pd.read_csv("E:/Data Kerja Fito/Dicoding/Proyek Analisis Data/data/customers_dataset.csv")
    order_payments_df = pd.read_csv("E:/Data Kerja Fito/Dicoding/Proyek Analisis Data/data/order_payments_dataset.csv")
    order_reviews_df = pd.read_csv("E:/Data Kerja Fito/Dicoding/Proyek Analisis Data/data/order_reviews_dataset.csv")
    products_df = pd.read_csv("E:/Data Kerja Fito/Dicoding/Proyek Analisis Data/data/products_dataset.csv")
    category_translation_df = pd.read_csv("E:/Data Kerja Fito/Dicoding/Proyek Analisis Data/data/product_category_name_translation.csv")
    return order_items_df, orders_df, customer_df, order_reviews_df, order_payments_df, products_df, category_translation_df

def create_sidebar_filters(orders_df):
    # Sidebar Filters
    st.sidebar.title("Filters")
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    
    ## Date Range Filter
    date_range = st.sidebar.date_input("Select Date Range:", 
                                       [orders_df['order_purchase_timestamp'].min(),
                                        orders_df['order_purchase_timestamp'].max()])
    ## Trend Interval Filter
    trend_interval = st.sidebar.selectbox("Select Trend Interval:", ["Daily", "Weekly", "Monthly"])

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_orders = orders_df[(orders_df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) & 
                                    (orders_df['order_purchase_timestamp'] <= pd.Timestamp(end_date))]
        return filtered_orders, trend_interval
    return orders_df, trend_interval

def display_key_metrics(orders_df, revenue_trend):
    # Key Metrics Section
    st.subheader("Key Performance Metrics")
    total_customers = orders_df["customer_id"].nunique()
    total_orders = orders_df.shape[0]
    total_revenue = revenue_trend["price"].sum()
    avg_order_value = total_revenue / total_orders

    col1, col2 = st.columns(2)
    col1.metric("Total Customers", total_customers)
    col2.metric("Total Orders", total_orders)
    col3, col4 = st.columns(2)
    col3.metric("Total Revenue", f"${total_revenue:,.2f}")
    col4.metric("Avg. Order Value", f"${avg_order_value:,.2f}")

def display_revenue_trend(order_items_with_timestamp, trend_interval):
    # Revenue Trend Visualization Section
    st.subheader(f"Revenue Trend - {trend_interval}")
    
    if trend_interval == "Daily":
        time_group = order_items_with_timestamp['order_purchase_timestamp'].dt.to_period("D")
    elif trend_interval == "Weekly":
        time_group = order_items_with_timestamp['order_purchase_timestamp'].dt.to_period("W")
    elif trend_interval == "Monthly":
        time_group = order_items_with_timestamp['order_purchase_timestamp'].dt.to_period("M")
    revenue_trend = order_items_with_timestamp.groupby(time_group)["price"].sum().reset_index()
    revenue_trend["order_purchase_timestamp"] = revenue_trend["order_purchase_timestamp"].astype(str)

    # Plot the trend
    fig_revenue = px.line(revenue_trend, x="order_purchase_timestamp", y="price",
                          title=f"Revenue Trend ({trend_interval})",
                          labels={"price": "Revenue ($)", "order_purchase_timestamp": trend_interval},
                          markers=True)
    fig_revenue.update_traces(line=dict(color="#636EFA", width=3))
    fig_revenue.update_layout(template="plotly_white")
    st.plotly_chart(fig_revenue)

def display_top_products(order_items_df, products_df):
    # Top Products Visualization Section
    st.subheader("Top 10 Products and Categories by Revenue")
    product_revenue = order_items_df.groupby("product_id")["price"].sum().reset_index()
    product_revenue = product_revenue.merge(products_df, on="product_id")
    top_products = product_revenue.nlargest(10, "price")
    fig_top_products = px.bar(top_products, x="product_id", y="price", title="Top 10 Products by Revenue",
                              text="price", color="price", labels={"price": "Revenue ($)", "product_id": "Product ID"})
    fig_top_products.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    fig_top_products.update_layout(template="plotly_white", showlegend=False)
    st.plotly_chart(fig_top_products)

def display_top_categories(order_items_df, products_df):
    # Top Categories Visualization Section
    category_revenue = order_items_df.merge(products_df, on="product_id").groupby("product_category_name_english")["price"].sum().reset_index()
    top_categories = category_revenue.nlargest(10, "price")
    fig = px.bar(top_categories, y="product_category_name_english", x="price", title="Top Categories by Revenue",
                 text="price", orientation="h", color="price", 
                 labels={"product_category_name_english": "Product Category", "price": "Revenue ($)"})
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig)

def display_customer_insights(orders_df, customer_df):
    # Customer Insights Section
    st.subheader("Customer Insights")
    repeat_customers = orders_df["customer_id"].value_counts()
    repeat_rate = (repeat_customers > 1).mean() * 100
    repeat_count = (repeat_customers > 1).sum()

    col1, col2 = st.columns(2)
    col1.metric("Repeat Customers (%)", f"{repeat_rate:.2f}%")
    col2.metric("Repeat Customers Count", repeat_count)

    # Customer State Distribution
    customer_state_counts = customer_df['customer_state'].value_counts().reset_index()
    customer_state_counts.columns = ['customer_state', 'count']  # Menamai kolom
    fig = px.bar(customer_state_counts, y='customer_state', x='count', title='Customer State Distribution',
                 labels={'customer_state': 'Customer State', 'count': 'Count'},
                 color='customer_state', color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(barmode='stack', yaxis_title='Customer State', xaxis_title='Count')
    st.plotly_chart(fig)

def display_orders_insight(orders_df, order_payments_df):
    # Order Insights Section
    st.header("Order and Payment Insights")
    orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])
    orders_df['order_estimated_delivery_date'] = pd.to_datetime(orders_df['order_estimated_delivery_date'])
    orders_df['delivery_late'] = (orders_df['order_delivered_customer_date'] > orders_df['order_estimated_delivery_date']).astype(int)

    orders_df['day_of_week'] = orders_df['order_purchase_timestamp'].dt.dayofweek
    orders_df_grouped = orders_df.groupby('day_of_week').size().reset_index(name='order_quantity')
    orders_df_grouped['day_of_week_name'] = orders_df_grouped['day_of_week'].map(
        {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    )

    fig = px.bar(
        orders_df_grouped,
        x='day_of_week_name',
        y='order_quantity',
        text='order_quantity',
        color='day_of_week_name',
        title='Order Quantity by Day of the Week',
        labels={'day_of_week_name': 'Day of the Week', 'order_quantity': 'Order Quantity'},
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis=dict(categoryorder='array', categoryarray=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        template='plotly_white'
    )

    st.plotly_chart(fig)

    
    late_deliveries = orders_df['delivery_late'].value_counts().reset_index()
    late_deliveries.columns = ['Late Delivery (1 = Yes, 0 = No)', 'Count']
    fig = px.bar(late_deliveries, x='Late Delivery (1 = Yes, 0 = No)', y='Count', title='Late Deliveries Analysis',
                 labels={'Late Delivery (1 = Yes, 0 = No)': 'Late Delivery (1 = Yes, 0 = No)', 'Count': 'Count'},
                 color='Late Delivery (1 = Yes, 0 = No)', color_discrete_map={0: 'green', 1: 'red'}, text='Count')
    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    st.plotly_chart(fig)

    # Revenue by Payment Type
    revenue_by_payment = order_payments_df.groupby("payment_type")["payment_value"].sum().reset_index()
    fig = px.pie(revenue_by_payment, names="payment_type", values="payment_value", title="Revenue by Payment Type")
    st.plotly_chart(fig)

def display_customer_feedback(order_reviews_df):
    # Customer Feedback Section
    st.subheader("Customer Feedback Analysis")
    # Review Score Distribution
    review_scores = order_reviews_df["review_score"].value_counts().reset_index()
    review_scores.columns = ["Review Score", "Count"]
    fig_reviews = px.bar(review_scores, x="Review Score", y="Count", title="Review Score Distribution",
                         labels={"Count": "Number of Reviews"},
                         color="Count", text="Count")
    fig_reviews.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig_reviews.update_layout(template="plotly_white")
    st.plotly_chart(fig_reviews)

    # Negative Reviews
    st.subheader("Negative Reviews")
    negative_reviews = order_reviews_df[order_reviews_df["review_score"] <= 2]
    st.dataframe(negative_reviews[["review_id", "review_comment_title", "review_comment_message"]])

def display_rfm(orders_df, order_items_df):
    st.text("RFM Analysis")
    rfm = rfm_analysis(orders_df, order_items_df)

    fig_recency = px.histogram(rfm, x="Recency", title="Recency Distribution", nbins=20, 
                           labels={"Recency": "Recency (Days)"}, color_discrete_sequence=["#636EFA"])
    fig_recency.update_layout(template="plotly_white")
    st.plotly_chart(fig_recency)

    fig_monetary_bins = px.pie(rfm, names="Monetary_Category", title="Customer Distribution by Monetary Bins",
                           color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_monetary_bins)

    customer_category_counts = rfm['Customer_Category'].value_counts().reset_index()
    customer_category_counts.columns = ['Customer_Category', 'Count']  # Ganti nama kolom

    fig_customer_category = px.bar(customer_category_counts,
                                    x='Customer_Category', y='Count',
                                    title="Customer Segmentation Based on RFM",
                                    labels={'Customer_Category': 'Customer Category', 'Count': 'Count'},
                                    color='Customer_Category', 
                                    color_discrete_sequence=px.colors.qualitative.Set2,text='Count')
    fig_customer_category.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    fig_customer_category.update_layout(template="plotly_white", 
                                        xaxis_title="Customer Category", 
                                        yaxis_title="Count")
    st.plotly_chart(fig_customer_category)

def main():
    # Load data
    order_items_df, orders_df, customer_df, order_reviews_df, order_payments_df, products_df, category_translation_df = load_data()
    filtered_orders, trend_interval = create_sidebar_filters(orders_df)

    # Merge and clean data for revenue calculation
    order_items_with_timestamp = order_items_df.merge(filtered_orders[['order_id', 'order_purchase_timestamp']], on='order_id', how='left').dropna(subset=['order_purchase_timestamp'])
    order_items_with_timestamp['order_purchase_timestamp'] = pd.to_datetime(order_items_with_timestamp['order_purchase_timestamp'])
    
    # Category translation
    products_df = pd.merge(products_df, category_translation_df, on='product_category_name')

    # Dashboard display
    display_key_metrics(filtered_orders, order_items_with_timestamp)
    display_revenue_trend(order_items_with_timestamp, trend_interval)
    display_top_products(order_items_with_timestamp, products_df)
    display_top_categories(order_items_with_timestamp, products_df)
    display_customer_insights(filtered_orders, customer_df)
    display_rfm(filtered_orders, order_items_df)
    display_orders_insight(filtered_orders, order_payments_df)
    display_customer_feedback(order_reviews_df)


if __name__ == "__main__":
    main()
