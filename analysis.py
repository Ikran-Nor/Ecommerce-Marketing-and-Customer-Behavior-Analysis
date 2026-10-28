# Import libraries.
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", 40)

# Find the folder containing this Python script
BASE_DIR = Path(__file__).resolve().parent

# Support datasets in a data folder or the project folder
DATA_DIR = BASE_DIR / "data" if (BASE_DIR / "data").is_dir() else BASE_DIR

# Load the five datasets
customers = pd.read_csv(DATA_DIR / "customers.csv")
transactions = pd.read_csv(DATA_DIR / "transactions.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
events = pd.read_csv(DATA_DIR / "events.csv")
campaigns = pd.read_csv(DATA_DIR / "campaigns.csv")


# Keep the names and their DataFrames together in one dictionary.
for name, df in{"Customers": customers, "Transactions": transactions, "Events": events,
                "Products": products, "Campaigns": campaigns}.items():
# Repeat the same inspection for every DataFrame.
    print(f"{name}: rows={len(df):,}, columns={df.shape[1]}")

# Displaying each table's first five rows.
for name, df in {"Customers": customers, "Transactions": transactions, "Events": events,
                 "Products": products, "Campaigns": campaigns}.items():
    print(f"{name}: \n{df.head()}\n")

for name, df in{"Customers": customers, "Transactions": transactions, "Events": events,
                "Products": products, "Campaigns": campaigns}.items():
    print(f"{name}: \n{df.info()}\n")

for name, df in {"Customers": customers, "Transaction": transactions, "Events": events,
                 "Products": products, "Campaigns": campaigns}.items():
    print(f"{name}: \n{df.describe(include="all")}\n")

# checking missing values
for name, df in{"Customers": customers, "Transactions": transactions, "Events": events,
                "Products": products, "Campaigns": campaigns}.items():
    audit = pd.DataFrame({"missing_values":df.isna().sum(), "missing_rate":(df.isna().mean()*100).round(2)})
    print("\n", name.upper())
    print(audit)
    print("\n Duplicated values:", "\n", df.duplicated().sum())  

# Filling missing device type
events["device_type"]= events["device_type"].fillna("unknown")
# Compare event types with whether the product ID is missing.
product_missing_by_event = pd.crosstab(
    events["event_type"],
    events["product_id"].isna())
product_missing_by_event.columns = ["Product_ID_Available", "Product_ID_Missing"]
product_missing_by_event

# Convert the listed date columns to proper datetime values.
for df, col in [(customers, "signup_date"), (products, "launch_date"),
                (campaigns, "start_date"), (campaigns, "end_date"),
                (transactions, "timestamp"), (events, "timestamp")]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Store product IDs as nullable integers; missing IDs stay missing.
for df in [products, transactions, events]:
    df["product_id"] = df["product_id"].astype("Int64")

# Remove spaces and use consistent text types.
for col in ["country","gender","loyalty_tier","acquisition_channel"]:
    customers[col] = customers[col].astype("string").str.strip()
for col in ["event_type","device_type","traffic_source","page_category","experiment_group"]:
    events[col] = events[col].astype("string").str.strip()
events["event_type"] = events["event_type"].str.lower()
events["traffic_source"] = events["traffic_source"].str.title()
events["device_type"] = events["device_type"].str.lower()
# Translate country codes into readable country names.
customers["country"] = customers["country"].replace(
    {"US":"United States","UK":"United Kingdom","IN":"India","BR":"Brazil","CA":"Canada","DE":"Germany","AU":"Australia"})

# Campaign ID 0 means no campaign; other values indicate an attributed ID.
for df in [transactions, events]:
    df["campaign_status"] = np.where(df["campaign_id"].eq(0), "No Campaign", "Campaign Attributed")
print("Cleaned event types:", events["event_type"].value_counts().to_dict())

# Add human-readable labels for premium and non-premium products.
products["Premium_status"] = np.where(
    products["is_premium"] ==1,
    "Premium",
    "Not_premium")

# Check whether non-missing product IDs exist in the product table.
print("Unknown transaction products:", (~transactions["product_id"].dropna().isin(products["product_id"])).sum())
print("Unknown event products:", (~events["product_id"].dropna().isin(products["product_id"])).sum())
# Check whether customer IDs exist in the customer table.
print("Unknown transaction customers:", (~transactions["customer_id"].isin(customers["customer_id"])).sum())
print("Unknown event customers:", (~events["customer_id"].isin(customers["customer_id"])).sum())
# Count rows that have campaign ID zero (no campaign attribution).
print("No-campaign transaction rows:", transactions["campaign_id"].eq(0).sum())
print("No-campaign event rows:", events["campaign_id"].eq(0).sum())

# Join signup dates only for this time-quality check.
timeline_tx = transactions[["customer_id","timestamp"]].merge(customers[["customer_id","signup_date"]], on="customer_id",
                                                              validate="many_to_one")
timeline_ev = events[["customer_id","timestamp"]].merge(customers[["customer_id","signup_date"]], on="customer_id", 
                                                        validate="many_to_one")
# Count records that happened before the recorded signup date.
print("Transactions before signup:", (timeline_tx["timestamp"] < timeline_tx["signup_date"]).sum())
print("Events before signup:", (timeline_ev["timestamp"] < timeline_ev["signup_date"]).sum())
del timeline_tx, timeline_ev 
# Compare website traffic source with campaign attribution status.
Events_campaign_attributed_unattributed_traffic_source = pd.crosstab(
    events["traffic_source"],
    events["campaign_id"] == 0)
Events_campaign_attributed_unattributed_traffic_source.columns =["Has_campaign", "Has_no_campaign"]
Events_campaign_attributed_unattributed_traffic_source

# Merge product information to each transaction.
sales_analysis = transactions.merge(products[["product_id","category","brand","base_price","is_premium", "Premium_status"]], 
                                   on="product_id", how="left", validate="many_to_one")
# Calculate revenue before discount.
sales_analysis["revenue_before_discount"] = sales_analysis["quantity"] * sales_analysis["base_price"]
# Calculate discount amount.
sales_analysis["discount_amount"] = sales_analysis["revenue_before_discount"] * sales_analysis["discount_applied"]
sales_analysis["signed_revenue"] = np.where(sales_analysis["refund_flag"].eq(1), -1, 1) * (
    sales_analysis["revenue_before_discount"] - sales_analysis["discount_amount"])
# Compare only rows with both a recorded and calculated revenue amount.
complete = sales_analysis["gross_revenue"].notna() & sales_analysis["signed_revenue"].notna()
print("Complete revenue rows:", complete.sum())
print("Matches validated formula (%):", round(np.isclose(sales_analysis.loc[complete,"gross_revenue"],sales_analysis.loc[
                                                         complete,"signed_revenue"],atol=.01).mean()*100,2))
# Count rows whose product ID and recorded revenue are both missing.
print("Rows missing both product and revenue:", (sales_analysis["product_id"].isna()
                                                 & sales_analysis["gross_revenue"].isna()).sum())
# Count rows whose product ID and recorded revenue are both missing.
print("Refund rows with missing revenue:", (sales_analysis["refund_flag"].eq(1)
                                            & sales_analysis["gross_revenue"].isna()).sum()) 

# Use the refund flag to give refunded units a negative sign.
sales_analysis["signed_units_by_refund_flag"] = np.where(sales_analysis["refund_flag"].eq(1), 
                                                -sales_analysis["quantity"], sales_analysis["quantity"])
# Use the sign of known revenue for an alternative units measure.
sales_analysis["known_revenue_signed_units"] = sales_analysis["quantity"] * np.sign(sales_analysis["gross_revenue"])

sales_analysis["known_revenue_signed_units"] = (
    pd.to_numeric(sales_analysis["known_revenue_signed_units"], errors="coerce").round().astype("Int64"))

# create customers age group column
customers["age_group"] = pd.cut(customers["age"], bins=[17, 24, 34, 44, 54, 64, np.inf], 
                                labels=["18-24", "25-34", "35-44", "45-54", "55-64", "65+"])
# Extract year, month, quarter and weekday from dates.
for df in [sales_analysis, events]:
    df["year"] = df["timestamp"].dt.year
    df["year_month"] = df["timestamp"].dt.to_period("M")
    df["quarter"] = "Q" + df["timestamp"].dt.quarter.astype("string")
    df["days_of_week"] = df["timestamp"].dt.day_name()
# Add one so both the start date and end date count as campaign days.
campaigns["campaign_duration_days"] = (campaigns["end_date"] - campaigns["start_date"]).dt.days + 1
print(campaigns["campaign_duration_days"].describe())

# Filter completed sales
completed_sales = sales_analysis.loc[sales_analysis["refund_flag"].eq(0) & sales_analysis["gross_revenue"].notna()].copy()

# Put every KPI name and its calculation into a dictionary.
kpi_dict = {
    "Total Transactions": sales_analysis["transaction_id"].nunique(),
    "Registered Customers": customers["customer_id"].nunique(),
    "Customers With Transactions": sales_analysis["customer_id"].nunique(),
    "Non-Refunded Units": sales_analysis.loc[sales_analysis["refund_flag"].eq(0), "quantity"].sum(),
    "Net Units From Refund Flags": sales_analysis["signed_units_by_refund_flag"].sum(),
    "Net Units With Known Revenue": sales_analysis["known_revenue_signed_units"].sum(),
    "Recorded Net Revenue": sales_analysis["gross_revenue"].sum(),
    "Refunded Transactions": sales_analysis["refund_flag"].sum(),
    "Known Refund Amount": -sales_analysis.loc[sales_analysis["gross_revenue"].lt(0), "gross_revenue"].sum(),
    "Average Completed Transaction Value": completed_sales["gross_revenue"].mean(),
    "Original Discount Amount, Known Products": sales_analysis.loc[sales_analysis["refund_flag"].eq(0), "discount_amount"]
    .sum(),
    # Add the refund rate right into the dictionary
    "Refund Rate (%)": round(sales_analysis["refund_flag"].mean() * 100, 2)
}
# Convert the dictionary into a two-column table.
kpi_table = pd.DataFrame(list(kpi_dict.items()), columns=["Metric", "Value"])

# Format results for display without changing the underlying calculations.
kpi_table["Value"] = kpi_table["Value"].apply(lambda x: f"{x:,.2f}" if x % 1 != 0 else f"{int(x):,}")

# Display the table cleanly
print(kpi_table.to_string(index=False))

customer_analysis = sales_analysis.merge(customers[["customer_id","country","age_group","gender",
                                           "loyalty_tier","acquisition_channel"]], 
                             on="customer_id", how="left", validate="many_to_one")
# Which loyalty tiers contribute the most recorded revenue?
loyalty_tier_performance =(
    customer_analysis.groupby("loyalty_tier")
    .agg(
        Customers=("customer_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("Recorded_revenue", ascending=False))

loyalty_tier_performance["Revenue_per_customer"] =(round(
    loyalty_tier_performance["Recorded_revenue"] / loyalty_tier_performance["Customers"],2))

loyalty_tier_performance["Average_Transaction_Value"] = (round(
    loyalty_tier_performance["Recorded_revenue"] / loyalty_tier_performance["Transactions"],2))

loyalty_tier_performance

# Which countries generate the most customers, transactions and revenue?
country_performance = (
    customer_analysis.groupby("country")
    .agg(
        Customers=("customer_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("Recorded_revenue", ascending=False))

country_performance["Revenue_per_Customer"] = (round(country_performance["Recorded_revenue"] /
                                                     country_performance["Customers"],2))
country_performance["Average_Transaction_Value"] = (round(country_performance["Recorded_revenue"] /
                                                          country_performance["Transactions"],2))
country_performance

# How does purchasing behavior differ across age groups?
age_performance = (
    customer_analysis.groupby("age_group", observed=True)
    .agg(
        Customers=("customer_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("Recorded_revenue", ascending=False))

age_performance["revenue_per_customer"] =(round(age_performance["Recorded_revenue"] / age_performance["Customers"],2))

age_performance["Average_Transaction_Value"] =(round(age_performance["Recorded_revenue"] / age_performance["Transactions"],2))

age_performance

# How do recorded transactions and revenue differ by gender?
gender_performance = (
    customer_analysis.groupby("gender")
    .agg(
        Customers=("customer_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("Recorded_revenue", ascending=False))

gender_performance["revenue_per_customer"] =(round(gender_performance["Recorded_revenue"] / gender_performance["Customers"],2))

gender_performance["Average_Transaction_Value"] =(round(
    gender_performance["Recorded_revenue"] / gender_performance["Transactions"],2))

gender_performance

# Which customer acquisition channels bring customers who later generate the strongest purchase activity?
acquisition_channel_performance = (
    customer_analysis.groupby("acquisition_channel")
    .agg(
        Customers=("customer_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("Recorded_revenue", ascending=False))
acquisition_channel_performance["revenue_per_customer"] =(round(
    acquisition_channel_performance["Recorded_revenue"] / acquisition_channel_performance["Customers"],2))

acquisition_channel_performance

# Which categories generate the most revenue and have the highest percentage of refunded transactions?
category_performance = (
    sales_analysis.groupby("category")
    .agg(
        Customers=("customer_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("Recorded_revenue", ascending=False))
category_performance["Average_Transaction_value"] =(round(
    category_performance["Recorded_revenue"] / category_performance["Transactions"],2))
category_performance["Refund_rate"] =(round(
    category_performance["Refunds"] / category_performance["Transactions"]*100, 2))
category_performance 

# Which brands have the highest recorded revenue?
brand_ranking = (
    sales_analysis
    .groupby("brand")["gross_revenue"]
    .sum()
    .reset_index(name="Revenue"))
brand_ranking["Dense_Rank"] = (brand_ranking["Revenue"]
    .rank(method="dense", ascending=False).astype(int))
top_brands = brand_ranking[brand_ranking["Dense_Rank"] <= 5].sort_values("Dense_Rank")              
top_brands

# How does recorded revenue differ between premium and non-premium products?
premium_performance =(
    sales_analysis.groupby("Premium_status")
    .agg(
        Customers=("customer_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("Recorded_revenue", ascending=False))
premium_performance["Average_transaction_value"] = (round(
    premium_performance["Recorded_revenue"]/premium_performance["Transactions"],2))
premium_performance

# What share of recorded transactions and revenue is linked to a campaign ID?
campaign_analysis = sales_analysis.merge(campaigns, on="campaign_id", how="left", validate="many_to_one")
campaign_status_performance = (
    campaign_analysis
    .groupby("campaign_status")
    .agg(
        Customers=("customer_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("Recorded_revenue", ascending=False))
campaign_status_performance["Transaction_Share_%"] = (round(campaign_status_performance["Transactions"] /
    campaign_analysis["transaction_id"].nunique()* 100,2))

campaign_status_performance["Revenue_Share_%"] = (round(campaign_status_performance["Recorded_revenue"] /
    campaign_status_performance["Recorded_revenue"].sum() * 100, 2))
campaign_status_performance

# Which recorded campaign channels have the highest associated revenue?
channel_performance = (
    campaign_analysis
    .groupby("channel")
    .agg(
        Customers=("customer_id", "nunique"),
        Campaigns=("campaign_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("Recorded_revenue", ascending=False))
channel_performance["Average_transaction_value"] =(round(
    channel_performance["Recorded_revenue"] / channel_performance["Transactions"],2))
channel_performance

# How much recorded revenue is associated with campaigns whose objective is acquisition, retention, cross-sell or reactivation?
objective_performance = (
    campaign_analysis
    .groupby("objective")
    .agg(
        Customers=("customer_id", "nunique"),
        Campaigns=("campaign_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("Recorded_revenue", ascending=False))
objective_performance["Average_transaction_value"] =(round(
    objective_performance["Recorded_revenue"] / objective_performance["Transactions"],2))
objective_performance

# How much recorded revenue is linked to campaigns targeting each segment?
target_segment_performance = (
    campaign_analysis
    .groupby("target_segment")
    .agg(
        Customers=("customer_id", "nunique"),
        Campaigns=("campaign_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("Recorded_revenue", ascending=False))
target_segment_performance["Average_transaction_value"] =(round(
    target_segment_performance["Recorded_revenue"] / target_segment_performance["Transactions"],2))
target_segment_performance

# Number of events
print("Total Events:",events["event_id"].nunique())
# Customers with digital activity
print("Active Customers:", events["customer_id"].nunique())
# Number of sessions
print("Total Sessions:", events["session_id"].nunique())
# Count how many times each event type occurs.
event_distribution = ( events["event_type"].value_counts().reset_index())
event_distribution.columns = ["Event_Type", "Total_Events"]
# Calculate each event type's percentage of all recorded event rows.
event_distribution["Percentage_%"] = (round(event_distribution["Total_Events"] /
                                            event_distribution["Total_Events"].sum()* 100, 2))
event_distribution

# Select completed, non-refunded transactions with a discount value.
discount_analysis = sales_analysis[
    (sales_analysis["refund_flag"] == 0) &
    (sales_analysis["gross_revenue"].notna()) &
    (sales_analysis["discount_applied"].notna())
].copy()
# How do transaction values differ across discount levels?
discount_stats = (
    discount_analysis
    .groupby("discount_applied")
    .agg(
        Transactions=("transaction_id", "nunique"),
        Average_Revenue=("gross_revenue", "mean"),
        Median_Revenue=("gross_revenue", "median"),
        Total_Revenue=("gross_revenue", "sum"))
    .reset_index())
# Convert 0.05 into 5%.
discount_stats["Discount_%"] = ( discount_stats["discount_applied"] * 100)
discount_stats

# Did recorded revenue increase or decrease from one month to the next?
sales_analysis["year_month"] = sales_analysis["timestamp"].dt.to_period("M")
monthly_performance = (
    sales_analysis
    .groupby("year_month")
    .agg(
        Customers=("customer_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("year_month"))
monthly_performance["MOM_Revenue_Change ($)"] = (
    monthly_performance["Recorded_revenue"] - monthly_performance["Recorded_revenue"].shift(1))
monthly_performance["MOM_Revenue_Growth (%)"] = (monthly_performance["Recorded_revenue"].pct_change(1) * 100).round(2)
monthly_performance.head()

# How did annual recorded revenue change compared with the previous year?
sales_analysis["year"] = sales_analysis["timestamp"].dt.to_period("Y")
yearly_performance = (
    sales_analysis
    .groupby("year")
    .agg(
        Customers=("customer_id", "nunique"),
        Transactions=("transaction_id", "nunique"),
        Refunds=("refund_flag","sum"),
        Signed_units_sold=("known_revenue_signed_units", "sum"),
        Recorded_revenue=("gross_revenue", "sum"))
    .reset_index()
    .sort_values("year"))
yearly_performance["YoY_Revenue_Change ($)"] = (
    yearly_performance["Recorded_revenue"] - yearly_performance["Recorded_revenue"].shift(1))
yearly_performance["YoY_Revenue_Growth (%)"] = (yearly_performance["Recorded_revenue"].pct_change(1) * 100).round(2)
yearly_performance

# Prepare a simple two-column table for the chart.
Monthly_revenue = (sales_analysis.groupby("year_month")["gross_revenue"].sum().reset_index(name="Revenue"))
# Convert the month column into dates.
Monthly_revenue["year_month"] = (Monthly_revenue["year_month"].dt.to_timestamp())
# Sort the months in chronological order.
Monthly_revenue = Monthly_revenue.sort_values("year_month")
# Create a folder called graphs.
FIG = Path("graphs")
FIG.mkdir(exist_ok=True)
# Create the figure
plt.figure(figsize=(13, 5))
# Create a line chart
plt.plot(Monthly_revenue["year_month"], Monthly_revenue["Revenue"],
     marker="o",
    linewidth=2)
# Add title and labels
plt.title("Monthly Recorded Revenue")
plt.xlabel("Month")
plt.ylabel("Recorded Revenue")
# Improve spacing
plt.xticks(rotation=45)
# Save the graph inside the graphs folder.
plt.savefig(FIG / "01_monthly_revenue.png", dpi=160)
# Display the graph
plt.show()

# Sort categories from lowest to highest revenue
category_plot = category_performance.sort_values("Recorded_revenue")
# Create the figure
plt.figure(figsize=(8, 4))
# Create a horizontal bar chart
plt.barh(
    category_plot["category"],
    category_plot["Recorded_revenue"])
# Add title and labels
plt.title("Revenue by Product Category")
plt.xlabel("Recorded Revenue")
plt.ylabel("Product Category")
# Improve spacing
plt.tight_layout()
# Save the graph inside the graphs folder.
plt.savefig(FIG / "02_category_revenue.png", dpi=160)
# Display the graph
plt.show()

# Create the figure
plt.figure(figsize=(4, 4))
# Create a donut chart
plt.pie(
    campaign_status_performance["Recorded_revenue"],
    labels=campaign_status_performance["campaign_status"],
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"width": 0.4})
# Add title
plt.title("Revenue Share by Campaign Status")
# Improve spacing
plt.tight_layout()
# Save the graph inside the graphs folder.
plt.savefig(FIG / "03_campaign_donut.png", dpi=160)
# Display the graph
plt.show()

# Create the figure
plt.figure(figsize=(8, 4))
# Create a histogram
plt.hist(
    completed_sales["gross_revenue"],
    bins=30)
# Add title and labels
plt.title("Transaction Revenue Distribution")
plt.xlabel("Transaction Revenue")
plt.ylabel("Number of Transactions")
# Improve spacing
plt.tight_layout()
# Save the graph inside the graphs folder.
plt.savefig(FIG / "04_revenue_histogram.png", dpi=160)
# Display the graph
plt.show()

stat_sales = customer_analysis[(customer_analysis["refund_flag"] == 0) &(customer_analysis["gross_revenue"].notna())].copy()
plt.figure(figsize=(9, 5))
stat_sales.boxplot(
    column="gross_revenue",
    by="loyalty_tier")
plt.title("Transaction Value by Loyalty Tier")
plt.suptitle("")
plt.xlabel("Loyalty Tier")
plt.ylabel("Transaction Revenue (€)")
# Save the graph inside the graphs folder.
plt.savefig(FIG / "05_loyalty_boxplot.png", dpi=160)
plt.show()

# Calculate the percentage of each event type within each traffic source
event_heat = pd.crosstab(events["traffic_source"],events["event_type"],normalize="index") * 100
# Display the table
event_heat
# Create the figure
plt.figure(figsize=(7, 4))
# Create a heatmap
sns.heatmap(
    event_heat,
    annot=True,
    fmt=".1f",
    cmap="Blues")
# Add title and labels
plt.title("Event Distribution by Traffic Source")
plt.xlabel("Event Type")
plt.ylabel("Traffic Source")
# Improve spacing
plt.tight_layout()
# Save the graph inside the graphs folder.
plt.savefig(FIG / "06_traffic_heatmap.png", dpi=160)
# Display the graph
plt.show()

# Sort categories by refund rate
refund_plot = category_performance.sort_values("Refund_rate", ascending=False)
# Create the figure
plt.figure(figsize=(8, 4))
# Create a bar chart
plt.bar(
    refund_plot["category"],
    refund_plot["Refund_rate"])
# Add title and labels
plt.title("Refund Rate by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Refund Rate (%)")
# Rotate the category names
plt.xticks(rotation=45)
# Improve spacing
plt.tight_layout()
# Save the graph inside the graphs folder.
plt.savefig(FIG / "08_category_refunds.png", dpi=160)
# Display the graph
plt.show()

# Count events for each traffic source
source_counts = events["traffic_source"].value_counts()
# Display the result
source_counts
# Create the figure
plt.figure(figsize=(8, 4))
# Create a bar chart
plt.bar(
    source_counts.index,
    source_counts.values)
# Add title and labels
plt.title("Events by Traffic Source")
plt.xlabel("Traffic Source")
plt.ylabel("Number of Events")
# Rotate traffic-source names
plt.xticks(rotation=45)
# Improve spacing
plt.tight_layout()
# Save the graph inside the graphs folder.
plt.savefig(FIG / "09_source_event_counts.png", dpi=160)
# Display the graph
plt.show()

# Select non-refunded transactions with known values
scatter_data = sales_analysis[
    (sales_analysis["refund_flag"] == 0) &
    (sales_analysis["revenue_before_discount"].notna())]
# Select 5% of transactions to avoid too many dots
scatter_plot = scatter_data.sample(frac=0.05, random_state=42)
# Create the figure
plt.figure(figsize=(8, 5))

# Create a scatter plot
plt.scatter(
    scatter_plot["discount_applied"] * 100,
    scatter_plot["revenue_before_discount"],
    alpha=0.3)
# Add title and labels
plt.title("Discount vs Transaction Value")
plt.xlabel("Discount (%)")
plt.ylabel("Revenue Before Discount")
# Improve spacing
plt.tight_layout()
# Save the graph inside the graphs folder.
plt.savefig(FIG / "10_Discount vs Transaction Value", dpi=160)
# Display the graph
plt.show()

Annual_revenue = (sales_analysis
    .groupby("year")["gross_revenue"]
    .sum()
    .reset_index(name="Revenue"))
# Sort years from oldest to newest
annual_plot = Annual_revenue.sort_values("year")
# Create the figure
plt.figure(figsize=(7, 4))
# Create a bar chart
plt.bar(
    annual_plot["year"].astype(str),
    annual_plot["Revenue"])
# Add title and labels
plt.title("Annual Revenue")
plt.xlabel("Year")
plt.ylabel("Recorded Revenue")
# Improve spacing
plt.tight_layout()
# Save the graph inside the graphs folder.
plt.savefig(FIG / "11_Annual Revenue", dpi=160)
# Display the graph
plt.show()
