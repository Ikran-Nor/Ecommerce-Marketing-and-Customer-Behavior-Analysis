# Ecommerce-Marketing-and-Customer-Behavior-Analysis Using Python
## 1. Project overview

This project explores an e-commerce dataset to understand customers, sales, products, website activity, and marketing campaigns. I used Python to clean and connect five datasets, calculate business metrics, and create charts that help explain the results.

The goal is to turn raw data into useful information that an e-commerce business can use to make better decisions.

## 2. Business problem

An online business collects a lot of information about purchases, customers, products, website visits, and marketing campaigns. However, it can be difficult to understand what this information means when it is stored in separate files.

The business needs to understand:

- Which customers and products contribute the most to sales?
- How do customers interact with the website?
- Which marketing channels are linked to purchases and revenue?
- How do refunds, discounts, and data-quality problems affect the results?

**Main business question:** How can customer, product, transaction, website, and campaign data help the business understand sales performance and identify opportunities for improvement?

## 3. Project objectives

1. Prepare the datasets for reliable analysis.
2. Measure sales, revenue, refunds, and customer activity.
3. Compare purchasing behavior by customer group.
4. Find the product categories and brands with the highest recorded revenue.
5. Explore website events and traffic sources.
6. Compare revenue associated with different marketing campaigns.
7. Show changes in recorded revenue over time.
8. Present findings and practical recommendations, while explaining data limitations.

## 4. Datasets

The project uses five CSV files.

| Dataset | Rows | What it contains |
|---|---:|---|
| `customers.csv` | 100,000 | Customer age, country, gender, loyalty tier, signup date, and acquisition channel |
| `transactions.csv` | 103,127 | Purchases, product IDs, quantities, discounts, recorded revenue, and refunds |
| `events.csv` | 2,000,000 | Website views, clicks, carts, purchases, traffic sources, devices, and sessions |
| `products.csv` | 2,000 | Product category, brand, base price, launch date, and premium status |
| `campaigns.csv` | 50 | Marketing channel, objective, dates, target segment, and expected uplift |

`transactions` is the main table for sales analysis. `events` is the main table for website activity. I used customer, product, and campaign information to add context to the transactions.

## 5. Questions explored

### Customer analysis

- Who are the customers by age, country, and gender?
- Which loyalty tiers contribute the most recorded revenue?
- Which loyalty tier has higher revenue per purchasing customer?
- Which customer acquisition channels are associated with the most revenue?

### Product and purchasing analysis

- Which product categories generate the most recorded revenue?
- Which categories sell the most known-revenue units?
- How do premium and non-premium products compare?
- Which categories have the highest refund rates?
- How do transaction values differ by discount level?

### Digital behavior analysis

- Which website events happen most often?
- Which traffic sources have the most recorded events?
- How does the mix of events differ by traffic source?
- What can website activity tell us about customer behavior?

### Marketing analysis

- How much recorded revenue is linked to a campaign ID?
- Which campaign channels, objectives, and target segments are associated with the most transactions and revenue?
- How does monthly and yearly recorded revenue change?

## 6. My analysis process

### Step 1: Understand the business and data

I defined the business questions and reviewed the five datasets to understand how they relate to each other.

### Step 2: Load the datasets

I used `pd.read_csv()` to load each CSV file into a Pandas DataFrame.

### Step 3: Inspect the datasets

I checked the number of rows and columns, viewed sample records, and reviewed column types and summary statistics using `shape`, `head()`, `info()`, and `describe()`.

### Step 4: Check and prepare data quality

I checked for:

- Missing values and duplicate records.
- Incorrect data types and inconsistent text categories.
- Missing or unknown product IDs and campaign IDs.
- Negative revenue values and refund flags.
- Events or transactions dated before the recorded customer signup date.

I converted date columns to datetime values, made category names consistent, and kept missing device information as **`unknown`** instead of guessing a device. I did not automatically delete records with missing revenue or product IDs.

### Step 5: Create useful new columns

I created fields to support the analysis, including:

- Customer age groups.
- Year, month, quarter, and weekday.
- Campaign duration.
- Product premium status and campaign attribution status.
- Revenue before discount and discount amount.
- Signed units to account for refunded items.

### Step 6: Join related datasets

I used Pandas `merge()` to connect transactions with product, customer, and campaign details. This allowed me to compare sales across customer groups, product categories, and marketing campaigns.

### Step 7: Calculate business metrics

I used `groupby()` and `agg()` to calculate transactions, distinct customers, recorded revenue, unit totals, refunds, refund rates, and average transaction values.

I also calculated month-over-month (MoM) and year-over-year (YoY) revenue changes using `shift()` and `pct_change()` after sorting dates in order.

### Step 8: Explore and visualize the data

I created line charts, bar charts, a donut chart, histogram, boxplot, heatmap, and scatter plot to communicate the results.

## 7. Key findings

### Overall sales performance

| Metric | Result |
|---|---:|
| Transactions | 103,127 |
| Registered customers | 100,000 |
| Customers with transactions | 64,035 |
| Recorded net revenue | 8,373,966.36 |
| Refunded transactions | 3,029 |
| Refund rate | 2.94% |
| Average value of completed, non-refunded transactions with known revenue | 95.92 |

About **64%** of registered customers appear in the transaction data. The remaining customers have no recorded transaction in this dataset. Revenue amounts are shown in **dataset units** because the source does not confirm a currency.

**Important:** Recorded revenue does not include transactions with missing revenue, so it is not the complete revenue total for every transaction.

### Customer findings

- **Bronze** customers generated the most total recorded revenue (about **4.48 million**), mainly because this tier includes more purchasing customers.
- **Gold** customers had the highest recorded revenue per purchasing customer in the loyalty comparison (about **146.48**). This shows why average customer value is useful alongside total revenue.
- The **United States** contributed the most recorded revenue by customer country (about **2.95 million**), followed by India (about **1.68 million**).
- Customers aged **35-44** contributed the most recorded revenue (about **2.97 million**), closely followed by customers aged **25-34** (about **2.79 million**).
- **Organic** acquisition was linked to the highest recorded revenue (about **2.57 million**), followed by **Paid Search** (about **2.50 million**).

### Product findings

- **Electronics** was the largest category by recorded revenue (about **3.45 million**), followed by **Home** (about **2.00 million**).
- **Sports** had the highest recorded category refund rate (**3.24%**), followed by **Beauty** (**3.10%**).
- **Premium products** were linked to about **6.45 million** in recorded revenue, compared with about **1.92 million** for non-premium products. Their average transaction value was also higher, but that does not mean premium status itself caused higher spending.
- The average recorded transaction value was lower at higher discount levels in this dataset (about **99.62** with no discount versus **79.34** with a 20% discount). This comparison alone does not prove that discounts caused the difference.

### Digital behavior findings

- The dataset contains **2 million website event records** and **633,462 distinct session IDs**.
- **Views** were the most common event (about **52.18%** of all events), followed by **clicks** (about **18.95%**) and **add-to-cart events** (about **14.22%**).
- **Purchase events** accounted for about **5.16%** of event records. This is **not a website conversion rate**, because one session can contain several events.
- The event analysis describes website activity but does not establish a reliable step-by-step conversion funnel.

### Campaign findings

- **82,172 transactions (79.68%)** had an associated campaign ID.
- These campaign-associated transactions represented about **6.68 million** in recorded revenue, approximately **79.82%** of total recorded revenue.
- The **Affiliate** campaign channel was associated with the most recorded revenue (about **1.61 million**), followed by **Paid Search** (about **1.53 million**).
- **Reactivation** was the campaign objective associated with the most recorded revenue (about **1.96 million**).
- Campaigns targeting **New Customers** had the highest total associated revenue among the recorded target segments (about **1.70 million**).

**Campaign attribution is not the same as campaign impact.** These results show which transactions are linked to campaigns, not how many extra purchases the campaigns caused. The dataset does not support a confirmed return-on-ad-spend or causal uplift calculation.

### Revenue trends

| Year | Recorded revenue | Change from previous year |
|---|---:|---:|
| 2021 | 2,817,199.32 | Not available |
| 2022 | 2,785,927.47 | -1.11% |
| 2023 | 2,770,839.57 | -0.54% |

Recorded revenue decreased slightly across the three years in the dataset. This trend should be monitored, but missing revenue and data-quality issues should be considered before drawing strong conclusions.

## 8. Data quality findings and limitations

Data quality was an important part of this project.

- **10,449 transactions (10.13%)** are missing both product ID and recorded revenue. Among them, **10,124** are not flagged as refunds and **325** are flagged as refunds.
- **200,371 website events (10.02%)** have no product ID. Many are bounce events, where a product ID may not be needed.
- **40,300 events (2.015%)** have no device type. I labelled these as `unknown` to keep the records without making assumptions.
- **2,704 transactions** have negative recorded revenue, and all are flagged as refunds. This is consistent with the dataset's refund convention.
- Many transaction and event timestamps appear before the corresponding customer signup dates. This may be a data-generation or recording issue and needs further investigation.
- Event counts cannot be treated as unique visitor counts or conversion rates.
- Marketing campaign association cannot be treated as proof of additional revenue caused by marketing.

These limitations mean the findings are best used for **descriptive analysis** and for identifying questions that need further investigation.

## 9. Recommendations

Based on these results, I would recommend that an e-commerce business:

1. **Improve sales data quality.** Investigate why product IDs and revenue are missing from some transactions before using the data for financial reporting.
2. **Support valuable customer groups.** Review retention and loyalty offers for customers who spend more per person, while also supporting the larger customer groups that generate strong total revenue.
3. **Monitor important product categories.** Keep track of Electronics and Home because they contribute the most recorded revenue. Review customer feedback and return reasons for Sports and Beauty, which have higher refund rates.
4. **Review digital marketing performance.** Study Affiliate, Paid Search, and Reactivation campaigns in more detail. Use campaign cost information and a suitable comparison group before claiming that campaigns increased sales.
5. **Investigate the revenue decline.** Review monthly patterns, product mix, discounts, and refunds to understand why recorded revenue decreased slightly from 2021 to 2023.
6. **Improve website measurement.** Track visitors and sessions consistently so the business can calculate proper conversion rates and understand where customers leave the purchasing journey.
7. **Investigate signup-date problems.** Check why many events and transactions appear before customer signup dates, instead of changing or removing them without evidence.

## 10. Conclusion

This project helped me turn five separate e-commerce datasets into a clearer picture of customers, products, sales, digital behavior, and marketing activities.

I found that Electronics contributed the most recorded revenue among product categories, Bronze customers contributed the most total revenue among loyalty tiers, and Gold customers showed the highest revenue per purchasing customer. I also found that many transactions were linked to marketing campaigns and that recorded annual revenue decreased slightly during the period studied.

The analysis also showed why **data quality matters**. Missing revenue, incomplete product IDs, and unusual signup dates limit what the business can conclude. My main lesson from this project is that good data analysis requires not only calculations and charts, but also checking the data and explaining what the results can and cannot tell us.

## 11. Skills demonstrated

- Loading and inspecting CSV datasets with Pandas.
- Cleaning missing values and standardizing data types and categories.
- Joining datasets and creating new analytical columns.
- Using `groupby()`, `agg()`, `nunique()`, `shift()`, and `pct_change()`.
- Calculating business KPIs and comparing customer and product groups.
- Making beginner-friendly visualizations with Matplotlib and Seaborn.
- Presenting findings, limitations, and recommendations in simple business language.
