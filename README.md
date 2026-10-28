# E-Commerce Marketing & Customer Behavior Analysis Using Python

## Project Overview

This project analyzes e-commerce sales, customer behavior, product performance, website activity, and marketing campaigns using Python.

I worked with five related datasets containing 100,000 customers, 103,127 transactions, and 2 million website events.

The objective was to transform raw data into meaningful business insights that support customer retention, marketing decisions, and sales performance improvement.

**Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn

**Analysis techniques:** Data cleaning, exploratory data analysis (EDA), data merging, feature engineering, KPI calculations, and data visualization.

[View Python Analysis](analysis.py) | [View Project Report]([Ecommerce%20marketing%20analysis.pdf)

---

## Business Problem

An e-commerce business collects information about its customers, purchases, products, website activity, and marketing campaigns.

However, this information is stored across separate datasets, making it difficult to understand overall business performance.

This project investigates four main questions:

1. Which customers and products generate the most recorded revenue?
2. How do purchasing patterns differ across customer segments?
3. Which marketing channels are associated with sales performance?
4. What opportunities exist to improve customer retention, revenue, and data quality?

## Dataset Overview

The analysis combines five datasets.

| Dataset | Records | Description |
|---|---:|---|
| customers.csv | 100,000 | Customer demographics, loyalty tiers, and acquisition channels |
| transactions.csv | 103,127 | Purchases, discounts, revenue, and refunds |
| products.csv | 2,000 | Product categories, brands, and pricing |
| events.csv | 2,000,000 | Website events, traffic sources, and sessions |
| campaigns.csv | 50 | Marketing channels, campaign objectives, and target segments |

### Dataset Availability

Four datasets are included in this repository: `customers.csv`, `transactions.csv`, `products.csv`, and `campaigns.csv`.

The full `events.csv` dataset was used during the analysis but is not uploaded because of its large size.

GitHub may also be unable to display large CSV files as interactive tables. The files can still be downloaded using GitHub's raw-file download option.

**Reproducibility note:** Running the complete Python analysis requires access to all five datasets, including the full `events.csv` file.

## Data Analysis Process

### 1. Data Inspection

- Examined dataset structures, column names, and data types.
- Identified missing values and duplicate records.
- Reviewed categorical and numerical variables.
- Checked relationships between customer, transaction, product, and campaign IDs.

### 2. Data Cleaning

- Converted date columns into datetime formats.
- Standardized categorical values.
- Investigated missing product IDs and revenue.
- Checked refunds and negative revenue values.
- Identified inconsistencies between transaction dates and customer signup dates.
- Preserved missing values when their correct replacements could not be established.

### 3. Data Transformation

- Created customer age groups.
- Extracted months, quarters, years, and weekdays.
- Calculated discount amounts and signed transaction quantities.
- Classified premium and non-premium products.
- Added campaign attribution indicators.
- Merged related datasets using Pandas.

### 4. Exploratory Data Analysis

Analyzed:

- Customer demographics and loyalty tiers
- Product and category performance
- Revenue and refund trends
- Customer acquisition channels
- Website events and traffic sources
- Marketing campaign associations
- Monthly and yearly sales performance

### 5. Data Visualization

Used Matplotlib and Seaborn to create:

- Revenue trend charts
- Product category comparisons
- Campaign revenue distribution charts
- Transaction value histograms
- Customer loyalty boxplots
- Website event heatmaps
- Refund rate comparisons
- Discount analysis scatter plots

## Key Performance Indicators

| KPI | Result |
|---|---:|
| Total transactions | 103,127 |
| Registered customers | 100,000 |
| Customers with transactions | 64,035 |
| Recorded net revenue | 8,373,966.36 |
| Refunded transactions | 3,029 |
| Refund rate | 2.94% |
| Average completed transaction value (known revenue) | 95.92 |

Revenue is expressed in dataset units because the source does not specify a currency. Transactions with missing revenue are excluded from recorded revenue totals.

## Key Business Findings

### Customer Behavior

- Bronze loyalty customers generated approximately 4.48 million in recorded revenue, the highest total among loyalty tiers.
- Gold customers had the highest recorded revenue per purchasing customer, approximately 146.48.
- Customers aged 35–44 contributed the most recorded revenue.
- Organic acquisition was associated with approximately 2.57 million in recorded revenue.

**Business insight:** Total revenue and revenue per customer provide different perspectives on customer value. Both should be considered when designing retention strategies.

### Product Performance

- Electronics generated approximately 3.45 million in recorded revenue, the highest among product categories.
- Home followed with approximately 2.00 million.
- Sports had the highest recorded category refund rate at 3.24%.
- Premium products generated more recorded revenue than non-premium products.

**Business insight:** The company should monitor high-revenue categories while investigating product returns and customer satisfaction.

### Website Behavior

- The dataset contains 2 million website events across 633,462 distinct sessions.
- Views represented approximately 52.18% of recorded events.
- Clicks represented approximately 18.95%.
- Add-to-cart events represented approximately 14.22%.

**Business insight:** Website activity provides useful engagement information, but event percentages cannot be interpreted as conversion rates without appropriate session-level analysis.

### Marketing Campaigns

- Approximately 79.68% of transactions were associated with a campaign ID.
- Campaign-associated transactions represented approximately 6.68 million in recorded revenue.
- Affiliate was associated with the highest recorded campaign-channel revenue, approximately 1.61 million.
- Reactivation campaigns were associated with the highest recorded revenue among campaign objectives.

**Business insight:** These results identify important campaign associations, but they do not establish that campaigns caused additional sales.

### Revenue Trends

| Year | Recorded Revenue | Year-over-Year Change |
|---|---:|---:|
| 2021 | 2,817,199.32 | N/A |
| 2022 | 2,785,927.47 | -1.11% |
| 2023 | 2,770,839.57 | -0.54% |

Recorded revenue declined slightly during the analyzed period.

## Data Quality and Limitations

The analysis identified several important data-quality concerns:

- 10,449 transactions were missing both product IDs and recorded revenue.
- 200,371 website events had missing product IDs.
- 40,300 website events had missing device information.
- Some transactions and website events were dated before their associated customers' signup dates.
- Missing revenue limits the completeness of financial totals.
- Campaign association does not establish causal marketing impact.

These findings highlight the importance of validating data and clearly communicating analytical limitations.

## Business Recommendations

Based on the analysis, I recommend:

1. **Improve data quality:** Investigate missing revenue and product information to strengthen reporting reliability.
2. **Strengthen customer retention:** Develop targeted loyalty strategies informed by customer value and purchasing behavior.
3. **Monitor product performance:** Support high-revenue categories while investigating refund patterns.
4. **Evaluate marketing effectiveness:** Examine campaign costs and use appropriate comparison methods before assessing campaign impact.
5. **Investigate revenue trends:** Review product mix, discounts, purchasing patterns, and refunds to understand declining recorded revenue.
6. **Improve website measurement:** Develop reliable session-level metrics to better understand the customer purchasing journey.

## Skills Demonstrated

- Python programming for data analysis
- Pandas DataFrames and data manipulation
- Data cleaning and validation
- Merging multiple datasets
- Exploratory data analysis
- Feature engineering
- Descriptive statistics
- Business KPI calculations
- Time-series comparisons
- Matplotlib and Seaborn visualizations
- Business insight generation
- Data storytelling and reporting

## Conclusion

This project demonstrates my ability to use Python to investigate business problems, prepare and analyze multiple datasets, calculate performance metrics, and communicate findings.

The analysis identified important patterns in customer behavior, product performance, marketing associations, and revenue trends.

It also demonstrated why reliable data quality and careful interpretation are essential for making informed business decisions.

**Author:** Ikran Nor Ali

**Focus:** Data Analytics | Python | SQL | Power BI
