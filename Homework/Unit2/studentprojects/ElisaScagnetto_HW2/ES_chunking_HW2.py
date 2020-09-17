#!/usr/bin/env python
# coding: utf-8

# In[4]:


file_path='https://dat-data.s3.amazonaws.com/taxi.csv'


# In[5]:


def probe_df(file_path,chunksize=1000):
    import pandas as pd
    import numpy as np
    from pandas.api.types import is_numeric_dtype
    cols=[]
    dict1={}
 
    for df in pd.read_csv(file_path, chunksize=chunksize):
        cols=df.columns
        for coln in cols:
            var1=df[coln].isnull().sum()
            var2=np.dtype(df[coln])
            if is_numeric_dtype(df[coln]):
                var3=df[coln].sum()
                var4=df[coln].notnull().sum()
                          
                
            else:
                var3=0
            if coln not in dict1:
                dict1[coln]={'null values': [var1],
                         'dtype' : [str(var2)],
                         'sums': [var3],
                         'nums' : [var4] }
            else:
                dict1[coln]['null values'].append(var1)
                dict1[coln]['sums'].append(var3)
                dict1[coln]['nums'].append(var4)
                
    for k in dict1:
        dict1[k]['null values']=sum(dict1[k]['null values'])
                    
        if dict1[k]['dtype'] != ['object'] and dict1[k]['dtype'] != ['bool']:
            dict1[k]['Avg_values']=sum(dict1[k]['sums'])/sum(dict1[k]['nums'])
 
        else: 
            dict1[k]['Avg_values']='N/A'
            
        dict1[k].pop('sums', None)
        dict1[k].pop('nums', None)

    return dict1


# In[6]:


dict1=probe_df(file_path, 250)


# In[8]:


dict2={}
for k in dict1:
    if dict1[k]['null values'] != 0:
        if k not in dict2:
            dict2[k]=dict1[k]['Avg_values']


# In[9]:


dict2


# In[10]:


filepathread=r'C:\Users\Jonat\Downloads\taxi (1).csv'
filepathwrite=r'C:\Users\Jonat\Downloads\taxi_new.csv'


# In[11]:


def write_df(file_path_read, file_path_write, chunk_size=1000, missing_vals=None):
    import pandas as pd
    import numpy as np
    n=0
    for df in pd.read_csv(file_path_read, chunksize=chunk_size):
        if missing_vals != None:
            df=df.fillna(missing_vals)
        if n==0:
            df.to_csv(path_or_buf= file_path_write,mode='w', index=False)
        else:
            df.to_csv(path_or_buf= file_path_write,mode='a', header=False, index=False)
        n+=1


# In[12]:


write_df(filepathread, filepathwrite, chunk_size=250, missing_vals=dict2)

