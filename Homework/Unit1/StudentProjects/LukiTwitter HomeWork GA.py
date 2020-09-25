#!/usr/bin/env python
# coding: utf-8

# In[7]:


# configs for twitter homework.

import requests
from requests_oauthlib import OAuth1
import pandas as pd

#replace with your own personal twitter API keys
auth = OAuth1('yRFD3WsOMN80LbeY3ugWxpduM', 'cuxQuVFpfFhIBcwNN9KPk3Qz3bOxH48ZRJJNFOTD91jeiyfX6W', '1288869541515350017-57MZSQRwrCSQ3XcZsbwKe1pGWg0Vcq', '8qnWLDyFTnn7oyUJ7Xo8NvuGKFRoM8waoLeg9bRKI3zso')

#API endpoint and search string for functions find_user, get_followers


#user is a string field relating to twitter usernames, keys are none by default but can be set to extract specific fields
#for example ['name', 'followers_count']

def find_user(user, keys=None):
    user_base_url = 'https://api.twitter.com/1.1/users/lookup.json'
    user_search = '?screen_name='
    results = requests.get(user_base_url + user_search + user.replace('@', ''), auth=auth).json()[0]

    if keys != None:
        reduced_results = {}
        for key in keys:
            reduced_results[key] = results[key]
        return reduced_results

    else:
        return results

#test prompts for get_followers function to be used for testing
# find_user('@GA', keys=['name', 'screen_name', 'followers_count', 'friends_count'])
# find_user('@GA')

#screen_name is a string field relating to twitter usernames, as above keys are defaulted to None, to_df is also
#set to False by default, toggling to True will return results in a pd DataFrame.


# In[10]:


find_user('GA', keys=['name', 'screen_name', 'followers_count', 'friends_count'])


# In[17]:


import requests
from requests_oauthlib import OAuth1

auth = OAuth1('yRFD3WsOMN80LbeY3ugWxpduM', 'cuxQuVFpfFhIBcwNN9KPk3Qz3bOxH48ZRJJNFOTD91jeiyfX6W', '1288869541515350017-57MZSQRwrCSQ3XcZsbwKe1pGWg0Vcq', '8qnWLDyFTnn7oyUJ7Xo8NvuGKFRoM8waoLeg9bRKI3zso')

def find_hashtag(hashtag, count=None, search_type=None):
    
    base_url = 'https://api.twitter.com/1.1/search/tweets.json'
    tweets = '?qtext=' + text
    count = '&count='+ str(count)
    search_type = '&result_type=' + result_type

    search_results = requests.get(base_url + tweets + count + result_type + tweets.replace('#',''), auth=auth).json()
find_hashtag('DataScience', count='100', result_type ='mixed')
    


# In[20]:


import requests
from requests_oauthlib import OAuth1
base_url = 'https://api.twitter.com/1.1/search/tweets.json'
# tweets = '?qtext='
# count = '&count='
# result_type = '&result_type='
auth = OAuth1('yRFD3WsOMN80LbeY3ugWxpduM', 'cuxQuVFpfFhIBcwNN9KPk3Qz3bOxH48ZRJJNFOTD91jeiyfX6W', '1288869541515350017-57MZSQRwrCSQ3XcZsbwKe1pGWg0Vcq', '8qnWLDyFTnn7oyUJ7Xo8NvuGKFRoM8waoLeg9bRKI3zso')
def find_hashtag(hashtag, count=None, result_type=None):
    #creating a tweet variable from the hashtag input, replacing hash with ''
    clean_hashtag = hashtag.replace('#','')
    tweets = '?qtext=%23' + f"{clean_hashtag}"
    #creating a count variable for count input and converting to a stringt
    if count !=None:
        count = '&count=' + str(f"{count}")
    #creating a result_type variable        
    if result_type !=None:
        result_type = 'result_type=' + f"{result_type}"
    #results from API endpoint, currently not configured for count and result_type
    search_results = requests.get(base_url + tweets, auth=auth).json()
    return search_results    
#     if keys != None:
#         reduced_results_list = []
#         for result in search_results:
#             new_user_dict = {}
#             for key in keys:
#                 new_user_dict[key] = result[key]
#                 reduced_results_list.append(new_user_dict)
find_hashtag('#DataScience')


# In[8]:


#
def get_followers(screen_name, keys=None, to_df=False):
    base_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    user_base_url = 'https://api.twitter.com/1.1/users/lookup.json'
    user_search = '?screen_name='
    results = requests.get(user_base_url + user_search + screen_name.replace('@', ''), auth=auth).json()[0]

    if keys != None:
        reduced_results = {}
        for key in keys:
            reduced_results[key] = results[key]
        if to_df == True:
            df = pd.DataFrame(reduced_results, index=[0])  # setting index as 0 as pandas is enforcing an index
            return df
        else:
            return reduced_results

    else:
        if to_df == True:
            df = pd.DataFrame(results, index=[0])  # setting index as 0 as pandas is enforcing an index
            return df
        else:
            return results

#test prompts for get_followers function to be used for testing
# get_followers('@GA', keys=['name', 'screen_name', 'followers_count', 'friends_count'], to_df=True)
# get_followers('@GA')
# get_followers('GA')
# get_followers('GA', keys=['name', 'followers_count'])
# get_followers('GA', keys=['name', 'followers_count'], to_df=True)
# get_followers('GA', to_df=True)


# In[6]:


get_followers('GA')


# In[ ]:




