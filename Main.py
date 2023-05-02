import pandas as pd

# ---------------------------------------------
# Function definitions
# ---------------------------------------------

# Function to multiply dataframe across states
def state_multiplier(target_df, date_col, state_col):
    # List of states
    states_list = ['nsw', 'qld', 'sa', 'vic', 'wa', 'nt', 'act', 'tas']

    # Empty DataFrame to hold results
    dates_states_df = pd.DataFrame(columns=[date_col, state_col])

    # Adding copy of date range table for every state and concatenating together
    for state in states_list:
        target_df[state_col] = state.upper()
        # print(date_range)
        dates_states_df = pd.concat([dates_states_df, target_df])

    return dates_states_df

# -------
# Set up
# -------

# Setting print options for dataframe QA outputs
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

# Setting csv encoding type
encoding_type = 'utf-8'

# Preparing school data
school_dates = r"AU School Hols - Data - 2010-2026 - dayrows.csv"
school_df = pd.read_csv(school_dates, encoding=encoding_type)
school_df = school_df.rename({"Calendar_Year": "Year", "School_Period_Name": "School_Hol_Desc"}, axis=1)
school_df = school_df.drop(["School_Period_Type", "Year"], axis=1)
school_df["has_school_hol"] = True
try:
    school_df['Date'] = pd.to_datetime(school_df['Date'], format='%Y-%m-%d')
except ValueError:
    school_df['Date'] = pd.to_datetime(school_df['Date'], format='%d/%m/%Y')
school_df.columns = map(str.upper, school_df.columns)
school_df = school_df.drop_duplicates()
print("School Dates data df 'school_df' prepared in format:"
      " ")
print(school_df.head())
# Concatenating values where multiple schools descriptions are on one date
school_df['SCHOOL_HOL_DESC'] = school_df[['DATE', 'HAS_SCHOOL_HOL', 'SCHOOL_HOL_DESC', 'STATE']] \
    .groupby(['DATE', 'HAS_SCHOOL_HOL', 'STATE'])['SCHOOL_HOL_DESC'] \
    .transform(lambda x: '|'.join(x))
school_df = school_df[['DATE', 'HAS_SCHOOL_HOL', 'SCHOOL_HOL_DESC', 'STATE']].drop_duplicates()

# Preparing public holiday data
public_dates = r"AU Pub Hols Data 2010-2026 - db_friendly.csv"
public_df = pd.read_csv(public_dates, encoding=encoding_type)
public_df = public_df.rename({"CAL_DATE": "Date",
                              "REGION": "State", },
                             axis=1)
public_df = public_df.drop(["IS_PUBLIC_HOLIDAY", "IS_SCHOOL_HOLIDAY", "SPCL_EVNT_DESC"], axis=1)
public_df["has_pub_hol"] = True
try:
    public_df['Date'] = pd.to_datetime(public_df['Date'], format='%Y-%m-%d')
except ValueError:
    public_df['Date'] = pd.to_datetime(public_df['Date'], format='%d/%m/%Y')
public_df.columns = map(str.upper, public_df.columns)
public_df = public_df.drop_duplicates()
# Concatenating values where multiple public hol descriptions are on one date
public_df['PUBLIC_HOLIDAY_DESC'] = public_df[['DATE', 'HAS_PUB_HOL', 'PUBLIC_HOLIDAY_DESC', 'STATE']] \
    .groupby(['DATE', 'HAS_PUB_HOL', 'STATE'])['PUBLIC_HOLIDAY_DESC'] \
    .transform(lambda x: '|'.join(x))
public_df = public_df[['DATE', 'HAS_PUB_HOL', 'PUBLIC_HOLIDAY_DESC', 'STATE']].drop_duplicates()
print("-----------------------------")
print("Public Dates data df 'public_df' prepared in format:"
      " ")
print(public_df.head())

# Preparing special dates data
special_dates = r"Special Days.csv"
special_df = pd.read_csv(special_dates, encoding=encoding_type)
special_df = special_df.rename({"Name": "Special_Day_Desc"}, axis=1)
special_df["has_special_day"] = True
try:
    special_df['Date'] = pd.to_datetime(special_df['Date'], format='%Y-%m-%d')
except ValueError:
    special_df['Date'] = pd.to_datetime(special_df['Date'], format='%d/%m/%Y')
special_df.columns = map(str.upper, special_df.columns)
# Concatenating values where multiple special descriptions are on one date
special_df['SPECIAL_DAY_DESC'] = special_df[['DATE', 'HAS_SPECIAL_DAY', 'SPECIAL_DAY_DESC']] \
    .groupby(['DATE', 'HAS_SPECIAL_DAY'])['SPECIAL_DAY_DESC'] \
    .transform(lambda x: '|'.join(x))
special_df = special_df[['DATE', 'HAS_SPECIAL_DAY', 'SPECIAL_DAY_DESC']].drop_duplicates()
special_df = special_df.drop_duplicates()

# Multiplying dataframe across states
special_df = state_multiplier(special_df, 'DATE', 'STATE')
print("-----------------------------")
print("Special_Days data df 'special_df' prepared in format:"
      " ")
print(special_df.head())

# --------------------------------------------
# Creating date range data as basis for joins
# --------------------------------------------

# Create date range df across a range of dates

start_date = pd.to_datetime('2010-01-01', format='%Y-%m-%d')
end_date = pd.to_datetime('2026-12-31', format='%Y-%m-%d')

# Getting a dataframe containing all dates in the date range

date_range = pd.date_range(start=start_date, end=end_date, freq='D').to_frame(index=False, name='Date')

# Multiplying date states dataframe by states
dates_states = state_multiplier(date_range, 'Date', 'State')

# Setting column names to upper case
dates_states.columns = map(str.upper, dates_states.columns)

print("-----------------------------")
print("Date range data df 'dates_states' prepared in format:"
      " ")
print(dates_states.head())

# --------------------
# Joining data sources
# --------------------

# Merging data
combo_df = dates_states \
    .merge(school_df, how='left', on=["DATE", "STATE"]) \
    .merge(public_df, how='left', on=["DATE", "STATE"]) \
    .merge(special_df, how='left', on=["DATE", "STATE"])

# Fill na values for bool 'has' columns
combo_df["HAS_SCHOOL_HOL"] = combo_df["HAS_SCHOOL_HOL"].fillna(False)
combo_df["HAS_PUB_HOL"] = combo_df["HAS_PUB_HOL"].fillna(False)
combo_df["HAS_SPECIAL_DAY"] = combo_df["HAS_SPECIAL_DAY"].fillna(False)

# Re-order columns
combo_df = combo_df[['DATE',
                     'STATE',
                     'HAS_PUB_HOL',
                     'PUBLIC_HOLIDAY_DESC',
                     'HAS_SCHOOL_HOL',
                     'SCHOOL_HOL_DESC',
                     'HAS_SPECIAL_DAY',
                     'SPECIAL_DAY_DESC']]

# Sorting Dataframe
combo_df = combo_df.sort_values(["STATE", "DATE"])

# Printing information on the final output
print("-----------------------------")
print("End result of data df 'combo_df' prepared in format:")
print(combo_df.head())
print("-----------------------------")
print("Data types for 'combo_df' are:")
print(combo_df.dtypes)

# --------------------------------
# Outputting the end result to csv
# --------------------------------

# Getting range as string
start_str = start_date.strftime("%Y")
end_str = end_date.strftime("%Y")

# Outputting to a csv
combo_df.to_csv(f"Combined Date Reference Data {start_str}-{end_str}.csv", index=False)
