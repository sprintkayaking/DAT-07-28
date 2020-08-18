#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import requests and set up tokens for OAuth1 authentication. Check it's working(should return 'Respose [200]')
import requests
from requests_oauthlib import OAuth1

token1='DeWbsfI9l3XhzARsLTo1kHYFL'
token2='m6JkY76aQv7zgJaApxz9IitfgfnlKCRo1cIkaqK3zqbQanDKk4'
token3='1291070701408002050-ft6VvAOaqSvW77CEr5kWN6NzyHavPy'
token4='hXS9DBpTuFXnXwODPfgoPnjNSXcRKmWVqFG72uPXjthlu'
auth = OAuth1(token1, token2, token3, token4)

url ='https://api.twitter.com/1.1/account/verify_credentials.json'
requests.get(url,auth=auth)


# FUNCTION 1 - FIND USER

# In[3]:


#Function queries Twitter data and returns dictionary with user objects.
def find_user(user, keys=None):
    user=user.strip('@')    #If input user begins with '@', the character will be removed
    url =f'https://api.twitter.com/1.1/users/show.json?screen_name={user}' # variable user passed into the url using 'f'
    userdata=requests.get(url,auth=auth).json() #Returns the request in json format
    
    if keys != None:       #keys are optional. If used a dictionary is generated with only the specified keys
        userdata_keys = {}
        for key in keys:
            userdata_keys[key] = userdata[key] #build the dictionary 'userdate_keys' with keys and values from the userdata
        return userdata_keys
    else:                                     #No keys specified so the whole dictionary is returned
        return userdata


# FUNCTION 2 - FIND HASHTAG

# In[13]:


#Function returns a list of data objects with information about the input tweet. Count and search type are optional.
def find_hashtag(hashtag, count=None, search_type=None):
   
    if not hashtag.startswith('#'):   #checks if the tweet name doesnt begin with '#' and adds %23 in front (the '#' in the url is encoded to '%23')
        hashtag='%23'+hashtag         
    else:
        hashtag='%23' + hashtag.strip('#') #if the tweet name begins with '#', this is replaced by %23.

    if search_type != None:     #search type is specified
        searchtype=search_type.replace('/', ',') #if more than one type is used, replaces '/' with ',' 
        url =f'https://api.twitter.com/1.1/search/tweets.json?q={hashtag}&count={count}&result_type={searchtype}' #variables from input argument and keys passed into the url 
        hashtag_search=requests.get(url,auth=auth).json()
    else:
        url =f'https://api.twitter.com/1.1/search/tweets.json?q={hashtag}&count={count}'
    return requests.get(url,auth=auth).json()


# FUNCTION 3 - Get Followers

# In[89]:


#Function returns a list of data objects for each of the users followers. Keys are required. Can be turned into a table if to_df set to True
def get_followers(screen_name, keys=['name', 'followers_count', 'friends_count', 'screen_name'], to_df=False):
   
    screen_name=screen_name.strip('@') #removes the intial '@' if entered
    url =f'https://api.twitter.com/1.1/followers/list.json?screen_name={screen_name}' #passes the user variable into the url path
    results=requests.get(url,auth=auth).json()['users'] #outputs the request into json format
      
    dict_users={}   # create a dictionary using the keys
    for i in keys:
        dict_users[i] = [user[i] for user in results]
    

    if to_df:    # if to_df is set to True the dictionary is turned into a table using pandas DataFrame function
        import pandas as pd
        usersdf = pd.DataFrame(dict_users)
        return usersdf
    
    return results


# FUNCTION 4 - FRIENDS OF FRIENDS

# In[132]:


#Function searches friends of two Twitter users and returns list of data objects for the friends in common
def friends_of_friends(names, keys=None, to_df=False):

    for item in names:  #loop through the names in the input list and create a list with the request outputs
        url =f'https://api.twitter.com/1.1/friends/list.json?screen_name={item}&count=200'
        list_users.append(requests.get(url,auth=auth).json()['users'])
        
#split the list into two lists, one for each user
    results1=list_users[0]
    results2=list_users[1]

#check the items in the two lists that have the same 'id' and append to a new list
    listfriends=[]
    listfriends=[item for item in results1 if item['id'] in [n['id'] for n in results2]]
    print(len(listfriends))

#create dictionary using keys if passed in the function arguments or all the keys available if not used as input
    results_dict={}
    if keys !=None:
        for i in keys:
            results_dict[i] = [user[i] for user in listfriends]
    else:
        for k,v in [(key,d[key]) for d in listfriends for key in d]:
            if k not in results_dict: 
                results_dict[k]=[v]
            else: 
                results_dict[k].append(v)
#build a table (pandas data frame from the dictionary) if to_df is True
    if to_df:
        import pandas as pd
        friendsdf = pd.DataFrame(results_dict)
        return friendsdf
    else:
        return results1


# In[ ]:




