import pandas as pd
import streamlit as st
import plotly.express as px

# 1. Page Setup
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

st.title("📊 E-Commerce Sales Dashboard")
st.markdown("##")

# 2. Load Data
@st.cache_data
def get_data():
    df = pd.read_csv("ecommerce_raw_data")
    # specific cleanup if needed
    df["Total_Sales"] = df["Unit_Price"] * df["Quantity"]
    return df

df = get_data()

# 3. Sidebar (Filters)
st.sidebar.header("Filter Options:")
city = st.sidebar.multiselect(
    "Select City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

category = st.sidebar.multiselect(
    "Select Category:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Filter the dataframe based on selection
df_selection = df.query(
    "City == @city & Category == @category"
)

# 4. KPI Cards (Top Row)
total_sales = int(df_selection["Total_Sales"].sum())
average_sale = round(df_selection["Total_Sales"].mean(), 2)
total_orders = len(df_selection)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales")
    st.subheader(f"₹ {total_sales:,}")
with middle_column:
    st.subheader("Avg Transaction")
    st.subheader(f"₹ {average_sale}")
with right_column:
    st.subheader("Total Orders")
    st.subheader(f"{total_orders}")

st.markdown("""---""")

# 5. Charts
# Sales by Product Line (Bar Chart)
sales_by_product = (
    df_selection.groupby(by=["Product"]).sum()[["Total_Sales"]].sort_values(by="Total_Sales")
)
fig_product_sales = px.bar(
    sales_by_product,
    x="Total_Sales",
    y=sales_by_product.index,
    orientation="h",
    title="<b>Sales by Product</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product),
    template="plotly_white",
)

# Sales by Date (Line Chart)
# Ensure date is sorted
df_selection = df_selection.sort_values(by="Date")
fig_daily_sales = px.line(
    df_selection,
    x="Date",
    y="Total_Sales",
    title="<b>Daily Sales Trend</b>",
    template="plotly_white",
)

# Display Charts Side-by-Side
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_daily_sales, use_container_width=True)

# 6. Raw Data (Optional view)
if st.checkbox("Show Raw Data"):
    st.dataframe(df_selection)
