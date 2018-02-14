import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

# rename columns to reflect Gold, Silver, Bronze, rather than 01 !, 02 !, 03!, respectively
for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

# split each index value at the first paranthesis
names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()
df.shape
df

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 

def answer_one():
    most_gold = df['Gold'].max()
    return df[df['Gold'] == most_gold].index[0]

answer_one()

def answer_two():
    df['difference'] = abs(df['Gold']-df['Gold.1'])
    biggest_diff = df['difference'].max()
    return df[df['difference'] == biggest_diff].index[0]

answer_two()

def answer_three():
    min1gold_SW = df[(df['Gold'] > 0) & (df['Gold.1'] > 0)] # new df - only countries w/ at least 1 gold in both summer and winter
    min1gold_SW['difference'] = abs(min1gold_SW['Gold']-min1gold_SW['Gold.1'])/min1gold_SW['Gold.2']
    biggest_diff = min1gold_SW['difference'].min()
    return min1gold_SW[min1gold_SW['difference'] == biggest_diff].index[0]

answer_three()

def answer_four():
    df['Points'] = df['Gold.2']*3 + df['Silver.2']*2 + df['Bronze.2']
    return df['Points']

answer_four()

