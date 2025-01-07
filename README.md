# E-Commerce Dashboard

## Overview
The **E-Commerce Dashboard** is a comprehensive data visualization platform designed to provide valuable insights into e-commerce performance metrics. This project leverages Python and Streamlit to create an interactive and user-friendly dashboard for monitoring key business indicators such as sales, customer behavior, product performance, and more.

## Features
- **Interactive Data Visualization**: Utilize tools like Plotly for dynamic and visually appealing charts.
- **Customer Analysis**: Perform RFM (Recency, Frequency, Monetary) segmentation to better understand customer behavior.
- **Performance Metrics**: Analyze sales, order trends, and product performance.
- **User-Friendly Interface**: A clean and responsive dashboard powered by Streamlit.
- **Customizable**: Built with modular code for easy modification and scalability.

## Technology Stack
- **Programming Language**: Python
- **Framework**: Streamlit
- **Libraries**:
  - Pandas (Data manipulation)
  - Plotly (Data visualization)
  - Streamlit (Dashboard creation)

## Installation
Follow the steps below to set up the project on your local machine:

### Prerequisites
1. Python 3.8 or higher installed.
2. `pip` for Python package management.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ecommerce-dashboard.git
   cd ecommerce-dashboard
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard:
   ```bash
   streamlit run dashboard/dashboard.py
   ```

4. Open your browser and navigate to the local URL provided by Streamlit (e.g., `http://localhost:8501`).

## Data Sources
The dashboard uses the following datasets:
- `order_items_dataset.csv`: Contains details of individual order items.
- `orders_dataset.csv`: Provides data on customer orders.
- `customers_dataset.csv`: Includes customer demographic and behavior data.
- `order_payments_dataset.csv`: Tracks payment details for orders.
- `order_reviews_dataset.csv`: Contains reviews and feedback for orders.
- `products_dataset.csv`: Provides product catalog details.
- `product_category_name_translation.csv`: Maps product categories to their translated names.

Ensure these datasets are placed in the `data/` directory of the project.

## Folder Structure
```
.
├── dashboard/
│   ├── dashboard.py         # Main Streamlit app
│   ├── rfm.py               # RFM analysis module
├── data/
│   ├── order_items_dataset.csv
│   ├── orders_dataset.csv
│   ├── customers_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── products_dataset.csv
│   ├── product_category_name_translation.csv
├── LICENSE                  # License file (Apache 2.0)
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation (this file)
```

## Usage
1. Open the dashboard in your browser.
2. Select the metrics you want to explore using the sidebar filters.
3. Interact with the visualizations to gain insights.

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.

## Contribution
Contributions are welcome! If you have suggestions or improvements, feel free to:
1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request.

## Contact
If you have any questions or feedback, please feel free to contact:
- **Name**: Alfito Putra Fajar Pratama
- **Email**: alfito.pfp@gmail.com
- **LinkedIn**: [Your LinkedIn Profile](https://linkedin.com/in/alfitoptr)

---
Thank you for using the E-Commerce Dashboard! We hope it adds value to your e-commerce business analysis.
