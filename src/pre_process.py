
import polars as pl


# relevant variables
rel_vars= ['countrynewwb','codewb', 'year', 'pop_adult', 'regionwb24_hi', 'incomegroupwb24', 
           'group', 'group2','account_t_d', 'fiaccount_t_d', 'mobileaccount_t_d', 'fin11a',
                  'fin11b', 'fin11c', 'fin11f', 'fin11d', 'fin11e', 'fin14a', 
                  'fin14b', 'fin14c', 'fin14d', 'fin26a', 'fin26b', 'fin27a', 
                  'g20_made', 'fin17f', 'fin17a_17a1_d', 'fin17a', 'fin17b', 'fin17c', 'fin24aSD_ND']

# variables that need to be int type
int_cols = ['account_t_d', 'fiaccount_t_d', 'mobileaccount_t_d', 'fin11a',
                  'fin11b', 'fin11c', 'fin11f', 'fin11d', 'fin11e', 'fin14a', 
                  'fin14b', 'fin14c', 'fin14d', 'fin26a', 'fin26b', 'fin27a', 
                  'g20_made', 'fin17f', 'fin17a_17a1_d', 'fin17a', 'fin17b', 'fin17c', 'fin24aSD_ND']

south_asia_countries = ['South Asia', 'India', 'Bangladesh', 'Pakistan']

def process_data(): 
    """
    Pre-processes the data by selecting the relevanr variables
    and converting them to int type. 
    
    Returns:pl.DataFrame: A DataFrame.
    """
    
    global_findex = pl.read_csv('../data/GlobalFindexDatabase2025.csv', infer_schema_length=10000)
    global_findex_clean = global_findex.select(rel_vars)
    global_findex_int = global_findex_clean.with_columns(
    [pl.col(col).replace('NA', None).cast(pl.Float64) for col in int_cols]
)
    global_findex_per = global_findex_int.with_columns(
        [pl.col(col)*100 for col in int_cols]
    )
    return global_findex_per

def filter_regions(df):
    """
    Filter the dataframe to only include regions and cleans the region names. 

    Input: pl.DataFrame: A DataFrame
    Return: pl.DataFrame: A DataFrame
    """
    regions = ['East Asia & Pacific (excluding high income)', 
           'Europe & Central Asia (excluding high income)', 
           'Middle East & North Africa (excluding high income)',
           'Sub-Saharan Africa (excluding high income)',
           'Latin America & Caribbean (excluding high income)', 
           'South Asia']
    
    findex_region = df.filter((pl.col('countrynewwb').is_in(regions)) & (pl.col('group2') == 'all'))
    clean_region_name = findex_region.with_columns(
    pl.when(pl.col('countrynewwb') == 'East Asia & Pacific (excluding high income)').then(pl.lit('East Asia & Pacific'))
    .when(pl.col('countrynewwb') == 'Europe & Central Asia (excluding high income)').then(pl.lit('Europe & Central Asia'))
    .when(pl.col('countrynewwb') == 'Middle East & North Africa (excluding high income)').then(pl.lit('Middle East & North Africa'))
    .when(pl.col('countrynewwb') == 'Latin America & Caribbean (excluding high income)').then(pl.lit('Latin America & Caribbean'))
    .when(pl.col('countrynewwb') == 'Sub-Saharan Africa (excluding high income)').then(pl.lit('Sub-Saharan Africa'))
    .otherwise(pl.col('countrynewwb'))  # keep original value if no match
    .alias('clean_region_name')        # name of the new column
)
    
    return clean_region_name


def filter_south_asia(df, group = True): 

    """
    Filter the dataframe to only include South Asia, India, Pakistan, 
    and Bangladesh. 

    Input: 
        - df(pl.DataFrame): A DataFrame
        - group(boolean): if True, then keep the observations disaggregated by 
            income, gender or age. 
    Return: pl.DataFrame: A DataFrame
    """

    global_findex_south_asia = df.filter((pl.col('countrynewwb').is_in(south_asia_countries))) 
    if group: 
        return global_findex_south_asia.filter(pl.col('group2') != 'all')
    else: 
        return global_findex_south_asia.filter(pl.col('group2') == 'all')
    

def long_acc_ownership_df(df):
    """
    Tranform the dataframe from wide to long where each observation 
    corresponds to a specific type of financial account

    Input:  df(pl.DataFrame): A DataFrame
    
    Return: pl.DataFrame: A DataFrame
    """
    account_df = df.select(pl.col(['countrynewwb', 'year', 'fiaccount_t_d','mobileaccount_t_d']))

    long_accounts = account_df.unpivot(
        index =['countrynewwb', 'year'],
        on = ['fiaccount_t_d', 'mobileaccount_t_d'],
        variable_name = 'account_type',
        value_name = 'account_per')

    long_accounts = long_accounts.with_columns(
        pl.when(pl.col('account_type') == 'fiaccount_t_d').then(pl.lit('Bank or similar inst.'))
            .when(pl.col('account_type') == 'mobileaccount_t_d').then(pl.lit('Mobile Money'))
            .otherwise(pl.col('account_type'))
            .alias('account_type'))

    return long_accounts


def savings_behavior_df(df):
    """
    Tranform the dataframe from wide to long where each observation 
    corresponds to a specific type of saving method

    Input:  df(pl.DataFrame): A DataFrame
    
    Return: pl.DataFrame: A DataFrame
    """
    long_savings = df.unpivot(
        index =['countrynewwb', 'year', 'group', 'group2'], 
        on = ['fin17a_17a1_d', 'fin17c'], 
        variable_name = 'savings_method', 
        value_name = 'savings_per')
    
    long_savings = long_savings.with_columns(
    pl.when(pl.col('savings_method') == 'fin17a_17a1_d').then(pl.lit('Saved Formally'))
    .when(pl.col('savings_method') == 'fin17c').then(pl.lit('Saved Informally'))
    .otherwise(pl.col('savings_method'))
    .alias('savings_method'))

#     clean_region_name = long_savings.with_columns(
#     pl.when(pl.col('countrynewwb') == 'East Asia & Pacific (excluding high income)').then(pl.lit('East Asia & Pacific'))
#     .when(pl.col('countrynewwb') == 'Europe & Central Asia (excluding high income)').then(pl.lit('Europe & Central Asia'))
#     .when(pl.col('countrynewwb') == 'Middle East & North Africa (excluding high income)').then(pl.lit('Middle East & North Africa'))
#     .when(pl.col('countrynewwb') == 'Latin America & Caribbean (excluding high income)').then(pl.lit('Latin America & Caribbean'))
#     .when(pl.col('countrynewwb') == 'Sub-Saharan Africa (excluding high income)').then(pl.lit('Sub-Saharan Africa'))
#     .otherwise(pl.col('countrynewwb'))  # keep original value if no match
#     .alias('clean_region_name')        # name of the new column
# )

    long_savings = long_savings.filter(pl.col('year') != 2011)
    return long_savings