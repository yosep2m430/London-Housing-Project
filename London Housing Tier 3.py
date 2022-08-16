#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib as plt


# In[3]:


url_LondonHousePrices= "https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls"
properties=pd.read_excel(url_LondonHousePrices, sheet_name='Average price', index_col=None)


# In[4]:


properties.head()


# In[5]:


properties.info()


# In[6]:


properties.drop(labels=['Unnamed: 34','Unnamed: 37','Unnamed: 47'], axis=1, inplace=True)


# In[7]:


properties_T=properties.T
properties_T.index


# In[8]:


properties_T= properties_T.reset_index()
properties_T.index


# In[9]:


properties_T.columns=properties_T.iloc[0]


# In[10]:


properties_T.head()


# In[11]:


properties_T.index


# In[12]:


properties_T.drop(0,inplace=True)


# In[13]:


properties_T=properties_T.reset_index(drop=True)


# In[14]:


properties_T.head()


# In[15]:


properties_T.rename(columns={'Unnamed: 0': 'Boroughs', pd.NaT:'ID'}, inplace=True)


# In[16]:


clean_properties=pd.melt(properties_T, id_vars=['Boroughs','ID'], var_name=['Date'], value_name='Average_price')
clean_properties.head()


# In[17]:


clean_properties.dtypes


# In[18]:


clean_properties['Average_price']=clean_properties['Average_price'].astype(float)


# In[19]:


clean_properties.dtypes


# In[20]:


clean_properties.isna().any()


# In[21]:


clean_properties['Boroughs'].unique()


# In[22]:


NotB=['Inner London', 'Outer London', 
               'NORTH EAST', 'NORTH WEST', 'YORKS & THE HUMBER', 
               'EAST MIDLANDS', 'WEST MIDLANDS',
              'EAST OF ENGLAND', 'LONDON', 'SOUTH EAST', 
              'SOUTH WEST', 'England']


# In[23]:


clean_properties= clean_properties[~clean_properties.Boroughs.isin(NotB)]


# In[24]:


clean_properties.head()


# In[25]:


df=clean_properties


# In[26]:


LondonP= df[df['Boroughs']=='City of London']


# In[28]:


LP= LondonP.plot(kind='line',x='Date', y= 'Average_price')


# In[29]:


LP.set_ylabel('Price')


# In[30]:


df['Year']=df['Date'].apply(lambda t: t.year)


# In[32]:


df.tail()


# In[33]:


dfg=df.groupby(by=['Boroughs','Year']).mean()


# In[34]:


dfg=dfg.reset_index()
dfg.head()


# In[35]:


def create_price_ratio(x):
    y1998= float(x['Average_price'][x['Year']==1998])
    y2018=float(x['Average_price'][x['Year']==2018])
    ratio=[y1998/y2018]
    return ratio


# In[37]:


final={}
for x in dfg['Boroughs'].unique():
    borough= dfg[dfg['Boroughs']==x]
    final[x]=create_price_ratio(borough)
print(final)


# In[38]:


df_ratio= pd.DataFrame(final)


# In[39]:


df_ratios_T= df_ratio.T
df_ratios= df_ratios_T.reset_index()
df_ratios.head()


# In[40]:


df_ratios.rename(columns={'index':'Borough', 0:'2018'}, inplace=True)
df_ratios.head()


# In[41]:


top15=df_ratios.sort_values(by='2018', ascending=False).head(15)
print(top15)


# In[42]:


ax=top15[['Borough','2018']].plot(kind='bar')
ax.set_xticklabels(top15.Borough)


# In[ ]:




