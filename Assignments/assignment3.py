
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[6]:

import pandas as pd
import numpy as np

def energy():
    # load energy data (excel file), drop unnamed columns, rename columns, set index to Country
    energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skipfooter=38)    .drop(['Unnamed: 0', 'Unnamed: 2'], axis=1)    .rename(columns={'Unnamed: 1':'Country',                     'Petajoules':'Energy Supply',                     'Gigajoules':'Energy Supply per Capita',                     '%':'% Renewable'})
    
    # convert 'Energy Supply' column to gigajoules values
    energy['Energy Supply'] *= 1000000
    
    # replace missing values (data with string '...') with np.NaN 
    energy['Energy Supply'] = energy['Energy Supply'].apply(pd.to_numeric, errors='coerce')
    energy['Energy Supply per Capita'] = energy['Energy Supply per Capita'].apply(pd.to_numeric, errors='coerce')

    # rename countries that have parantheses
    for i in energy['Country']:
        if i[-1:] == ')':
            new_name = i.split(' (')[0]
            energy['Country'].replace(i, new_name, inplace=True)

    # rename certain countries
    dic = {"Republic of Korea": "South Korea",           "United States of America": "United States",           "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",           "China, Hong Kong Special Administrative Region": "Hong Kong"}
    energy['Country'].replace(dic, inplace=True)
    
    return energy

def gdp():
    # load GDP data (csv)
    gdp = pd.read_csv('world_bank.csv', skiprows=4)    .rename(columns={'Country Name': 'Country'})
    
    # rename certain countries
    gdp_dic = {'Korea, Rep.': 'South Korea',               'Iran, Islamic Rep.': 'Iran',               'Hong Kong SAR, China': 'Hong Kong'}
    gdp['Country'].replace(gdp_dic, inplace=True)
        
    # drop needless columns
    gdp.drop(['Country Code', 'Indicator Name', 'Indicator Code', '1960',
              '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969',
              '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978',
              '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987',
              '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996',
              '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005'], axis=1, inplace=True)
    return gdp

def scimen():
    # load journal-contributions data
    scimen = pd.read_excel('scimagojr-3.xlsx')
    return scimen

def answer_one():
    inner_energygdp = pd.merge(Energy, GDP, on='Country')
    final = pd.merge(inner_energygdp, ScimEn, on='Country')
    final = final.set_index('Country')
    return final[final['Rank'] <= 15]

Energy, GDP, ScimEn = energy(), gdp(), scimen()

answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[7]:

get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[8]:

def answer_two():
    "calculates (length of outer join) minus (length of inner join) equals (# of entries lost)"  
    outer_energygdp = pd.merge(Energy, GDP, how='outer', on='Country')
    outer = pd.merge(outer_energygdp, ScimEn, how='outer', on='Country')
    
    inner_energygdp = pd.merge(Energy, GDP, on='Country')
    inner = pd.merge(inner_energygdp, ScimEn, on='Country')
    
    difference = len(outer) - len(inner)
    #return len(outer) #318
    #return len(inner) #162
    return difference

answer_two()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[9]:

def answer_three():
    Top15 = answer_one()
    # calculate average GDP from 2006-2015 GDP for each country, excluding NaN values; 15 rows, 10 cols
    cols_to_keep = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    # assign these values to a Series, with 'Country' as index
    avgGDP = Top15[cols_to_keep].apply(np.mean, axis=1)
    # sort GDP in descending order (sort method default args: inplace=True, ascending=True)
    avgGDP.sort(ascending=False)
    return avgGDP

answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[14]:

def answer_four():
    Top15 = answer_one()
    # find country with 6th largest average GDP, store inside a variable as a string
    sixth_largest_avgGDP = answer_three().index[5]
    # create new series from which we can query
    United_Kingdom = Top15.loc[sixth_largest_avgGDP]
    # find that country's GDP in 2006; 2.4e+12
    start = United_Kingdom['2006']
    # find that country's GDP in 2015; 2.6e+12
    finish = United_Kingdom['2015']
    # calculate change
    change = finish - start # 2.2e+11
    return change

answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[221]:

def answer_five():
    Top15 = answer_one()
    mean_ES = Top15['Energy Supply per Capita'].mean()
    return mean_ES

answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[36]:

def answer_six_alternative(): # uses sort()
    Top15 = answer_one()
    # make a copy of '% Renewable' col and sort values in descending order, assign to variable "descending"
    descending = Top15['% Renewable'].copy()
    descending.sort(ascending=False)
    # assign variables for name of country & for percentage 
    country, percentage = descending.index[0], descending[0]
    # put values into a tuple, initiated with ()
    as_tuple = (country, percentage)
    #return as_tuple
    return as_tuple

def answer_six(): # uses sort_values
    Top15 = answer_one()
    # get country with highest '% Renewable' value
    maxRenew = Top15.sort_values(by='% Renewable', ascending=False).iloc[0]
    # return country name & '% Renewable' value as tuple
    return (maxRenew.name, maxRenew['% Renewable'])

answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[45]:

def answer_seven_alternative(): # uses sort()
    Top15 = answer_one()
    # calculate ratio of self-citations to total citations, assign values to new col
    Top15['self_to_total'] = Top15['Self-citations'] / Top15['Citations']
    # create copy of 'self_to_total' col and sort values in descending order, assign to var "ratio"
    ratio = Top15['self_to_total'].copy()
    ratio.sort(ascending=False)
    # assign variables for name of country & for highest ratio
    country, highest_value = ratio.index[0], ratio[0]
    # put values into a tuple, initiated with ()
    as_tuple = (country, highest_value)
    return as_tuple

def answer_seven(): # uses sort_values()
    Top15 = answer_one()
    # create new column with ratio of self-citations to total citations
    Top15['Self to Total'] = Top15['Self-citations'] / Top15['Citations']
    # get country with highest 'Self to Total' value
    country = Top15.sort_values(by='Self to Total', ascending=False).iloc[0]
    # return country name & 'Self to Total' value as a tuple
    return (country.name, country['Self to Total'])

answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[60]:

def answer_eight_alternative(): # uses sort()
    Top15 = answer_one()
    # create new col with estimated populations in each country
    Top15['est_population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    # create copy of 'est_population' col, sort values in descending order, assing to var "pop"
    pop = Top15['est_population'].copy()
    pop.sort(ascending=False)
    # assign variable for third most populous country
    third_mostpop = pop.index[2]
    return third_mostpop

def answer_eight(): # uses sort_values()
    Top15 = answer_one()
    # create new col with estimated populations in each country
    Top15['est_population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    # find the third most populous country by sorting, querying (iloc), and storing series in 'most_pop'
    ThirdMostPop = Top15.sort_values(by='est_population', ascending=False).iloc[2]
    return ThirdMostPop.name

answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[61]:

def answer_nine():
    Top15 = answer_one()
    # calculate estimated populations in each country, assign to variable "est_population"
    Top15['est_population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    # calculate estimated citable docs per person, store values in a col
    Top15['citabledocs_per_cap'] = Top15['Citable documents'] / Top15['est_population']
    return Top15['citabledocs_per_cap'].corr(Top15['Energy Supply per Capita'])

answer_nine()


# In[62]:

def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    # calculate estimated population
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    # calculate citable docs per capita
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    # scatterplot to visualize relationship between Citable docs per Capita and Energy Supply per Capita
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])
    
plot9()


# In[63]:

#plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[79]:

def answer_ten():
    Top15 = answer_one()
    # calculate median of % Renewable values
    median = Top15['% Renewable'].median() # 17.020280
    # True if at or above median, False if below median - broadcast values to new col 'HighRenew'
    Top15['HighRenew'] = Top15['% Renewable'] >= median
    # 1 if True, 0 if False - apply lambda function
    Top15['HighRenew'] = Top15['HighRenew'].apply(lambda x: 1 if x else 0)
    # set index of series to country name -- already accomplished in answer_one() function
    # sort countries by Rank in ascending order
    Top15.sort_values(by='Rank', inplace=True) # either set inplace to True, or assign series to a new var
    return Top15['HighRenew']

answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[96]:


def answer_eleven():
    Top15 = answer_one()
    # create dictionary mapping each country to its continent
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    # create df with columns names (no values under cols)
    groups = pd.DataFrame(columns = ['size', 'sum', 'mean', 'std'])
    # compute estimated population for each country
    Top15['Estimate Population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    
    # 'group' (continent) 
    # frame' (each frame is a df of all countries in a continent, with all cols)
    # Top15.groupby(ContinentDict) is a DataFrameGroupBy object
    # Top15.gropuby(ContinentDict) ensures metrics of CONTINENTS, rather than countries, are worked on
    for group, frame in Top15.groupby(ContinentDict):
        # create new entry/row (hence, usage of loc) for each continent
        # number of countries per continent under 'size', sum of populations of all countries under 'sum', mean of pops of all countries under 'mean', std of pops of all countries under 'std''
        groups.loc[group] = [len(frame), frame['Estimate Population'].sum(),frame['Estimate Population'].mean(),frame['Estimate Population'].std()]
    
    return groups

answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[109]:

def answer_twelve():
    Top15 = answer_one()
    # create dictionary mapping each country to its continent
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    # reset index of df
    Top15 = Top15.reset_index()
    # create new col 'Continent' that specifies the continent of the country (using dict)
    # ContinentDict[country] = dict[key]; the key is the country, the value is the continent
    Top15['Continent'] = [ContinentDict[country] for country in Top15['Country']]
    # cut '% Renewable' into 5 bins, so that each country's '% Renewable' value falls into a bin/range
    Top15['bins'] = pd.cut(Top15['% Renewable'], 5)
    # return df with multiindex of Continent & of 'bins'
    return Top15.groupby(['Continent','bins']).size()

answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[131]:

def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15['Energy Supply'] / Top15['Energy Supply per Capita']).astype(float)
    # convert scientific notation in series to string with thousands seperators (commas)
    return Top15['PopEst'].apply(lambda x: '{0:,}'.format(x))
    
    # we can perform this formatting on a number as well, converts the num to a string
    #test_num = 1000000.5067
    #return '{0:,}'.format(test_num)

answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[133]:

def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")
    
plot_optional()


# In[ ]:

#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!

