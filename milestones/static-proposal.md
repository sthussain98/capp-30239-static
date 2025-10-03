# Sarah Hussain

## Description

Through this project I will explore and illustrate key indicators of financial inclusion using the World Bank’s Global Findex dataset. The analysis will cover account ownership, payments, savings, credit, and financial resilience—areas that matter for policymakers in low-income countries where many people lack access to formal and digital financial services. While the Global Findex covers the demand side, I will also examine supply-side infrastructure (bank branches, ATMs, agent networks, and debit/credit cards in circulation) using the IMF’s Financial Access Survey (FAS). I plan to focus on South Asia while comparing trends to higher-income countries.By focusing on both consumer-facing (demand-side) data and supply-side infrastructure, I aim to build a narrative that links the availability of financial infrastructure with individuals’ behaviors and attitudes toward using those services

The Global Findex contains roughly 300 indicators; I will narrow these to 6–8 targeted indicators that best communicate the story. Data are available from 2011–2024 and are disaggregated by gender, income, age, urban/rural residence, labor-force status, and education. I will choose the most useful disaggregation hierarchies aligned with the narrative I want to present rather than using every breakdown by default.

Data from the FAS contains roughly 70 indicators normalized by adult population size, land area, and GDP. The dataset spans from 2004 to 2024. Similar to my approach to the Global Findex data, I will narrow these indicators down to the most compelling ones. Additionally, I hope to use indicators at the country-level (e.g. number of ATMs in Pakistan). 


## Data Sources

### Data Source 1: World Bank’s Global Findex 

URL: https://www.worldbank.org/en/publication/globalfindex/download-data

Size: 8564 rows, 437 columns

The data are in wide format — each row corresponds to a country, a year, and a specific disaggregation (gender, income, age, urban/rural residence, labor-force status, or education). The data can be easily downloaded as a csv and comes with a data dictionary. 
### Data Source 2: IMF’s Financial Access Survey (FAS)

URL: https://data.imf.org/en/datasets/IMF.STA:FAS

Size: 24,957 rows, 70 columns

The data are in wide format: each row is unique to a country and a specific financial indicator. If an indicator is disaggregated (for example, by gender or income), rows are further distinguished by those categories. Indicator values are stored in columns for each year. The data can also be easily downloaded as csv. 
