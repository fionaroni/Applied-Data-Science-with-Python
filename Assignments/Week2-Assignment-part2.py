census_df = pd.read_csv('census.csv')

def answer_five():
    only_sumlev50 = census_df[census_df['SUMLEV'] == 50] #only observations with sumlev of 50
    count_counties = only_sumlev50.groupby('STNAME')['CTYNAME'].nunique() # series with number of unique counties per state
    max_counties = count_counties.max() # get highest number of counties in any state
    return count_counties[count_counties == max_counties].index[0] # boolean mask and index

answer_five()

def answer_six():
    only_sumlev50 = census_df[census_df['SUMLEV'] == 50] # only rows with sumlev of 50
    populous_counties = only_sumlev50.groupby('STNAME')['CENSUS2010POP'].nlargest(3) # finds the 3 counties with largest pops in each state; groupby also quietly turns df into series and sets index to the group 'STNAME' 
    populous_counties = populous_counties.reset_index() # must reset index after groupby, in order to promote 'STNAME' back to a column, in order to access its values
    state_pops = populous_counties.groupby('STNAME')['CENSUS2010POP'].sum() # quietly turns into a series, and 'STNAME' becomes index
    state_list = state_pops.nlargest(3) # finds the 3 states with the greatest populations, quietly turns into a series
    return state_list.index.tolist() # returns index (state names) in the form of a list

answer_six()

def answer_seven():
    only_sumlev50 = census_df[census_df['SUMLEV'] == 50] # only rows with sumlev of 50  
    cols_to_keep = ['CTYNAME','POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015'] #filter cols - only cols of interest
    county_pops = only_sumlev50[cols_to_keep] # new df - all rows, but only cols of interest 
    county_pops = county_pops.set_index('CTYNAME') # set index to county name
    
    county_pops['minimum'] = county_pops.min(axis=1) # axis=1, so that compute across cols (within one row)
    county_pops['maximum'] = county_pops.max(axis=1)
    county_pops['absolute change'] = county_pops['maximum']-county_pops['minimum']

    max_change = county_pops['absolute change'].max() # boolean mask and index
    
    return county_pops[county_pops['absolute change'] == max_change].index[0]
    
answer_seven()

def answer_eight():
    #only_counties = census_df[census_df['SUMLEV'] == 50]
    #regions1or2 = only_counties[(only_counties['REGION'] == 1) | (only_counties['REGION'] == 2)]
    #pop15greater = regions1or2[regions1or2['POPESTIMATE2015'] > regions1or2['POPESTIMATE2014']]
    #has_washington = pop15greater[pop15greater['CTYNAME'].str[:10] == 'Washington']
    #return has_washington[['STNAME','CTYNAME']]
    
    df_from_one_query = census_df[(census_df['SUMLEV'] == 50) & ((census_df['REGION'] == 1) | (census_df['REGION'] == 2)) & (census_df['POPESTIMATE2015'] > census_df['POPESTIMATE2014']) & (census_df['CTYNAME'].str[:10] == 'Washington')]
    return df_from_one_query[['STNAME','CTYNAME']]

answer_eight()