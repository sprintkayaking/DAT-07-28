# configs for twitter homework.

import requests
from requests_oauthlib import OAuth1
import pandas as pd

#replace with your own personal twitter API keys
auth = OAuth1('NOZHm1aLT1AVmchGbCmiZOAga', 'nPyaYCt8L7ymqGZtU8EqC0a2ypI9aSJgVNIhtoZ0wGsaf3BJw9',
                '1079981876864008192-AlhO4yOa06oW2sXZpLpWPwnOxEERYS', 'o3E0AsKJfDoTBk77UQYExzOG7E46jPYvpWNGAKsD6lUBY')

#API endpoint and search string for functions find_user, get_followers
user_base_url = 'https://api.twitter.com/1.1/users/lookup.json'
user_search = '?screen_name='

#user is a string field relating to twitter usernames, keys are none by default but can be set to extract specific fields
#for example ['name', 'followers_count']

def find_user(user, keys=None):
    results = requests.get(user_base_url + user_search + user.replace('@', ''), auth=auth).json()[0]

    if keys != None:
        reduced_results = {}
        for key in keys:
            reduced_results[key] = results[key]
        return reduced_results

    else:
        return results

#test prompts for find_user function to be used for testing
# find_user('@GA', keys=['name', 'screen_name', 'followers_count', 'friends_count'])
# find_user('@GA')

#screen_name is a string field relating to twitter usernames, as above keys are defaulted to None, to_df is also
#set to False by default, toggling to True will return results in a pd DataFrame.

def get_followers(screen_name, keys=None, to_df=False):
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

# function friends_of_friends : goal is to find mutual friends between two users.
# I got stuck at trying to return numerous names or ids when those keys are passed through. When they are not
# passed through, I get the entire dictionary, do you know what's causing this?

friends_base_url = 'https://api.twitter.com/1.1/friends/list.json'
user_search = '?screen_name='


def friends_of_friends(name1, name2, keys=None, to_df=False):
    names = [name1, name2]
    name_list = [name.replace('@', '') for name in names]

    results = [requests.get(friends_base_url + user_search + name, auth=auth).json() for name in name_list]

    followers = [i['users'] for i in results]

    flat_list = []
    for sublist in followers:
        results = [sublist for sublist in sublist]

        if keys != None:

            reduced_list = []
            for user in results:
                user_dict = {}
                for key in keys:
                    user_dict[key] = user[key]
                    reduced_list.append(user_dict)

                    if to_df != False:
                        return pd.DataFrame(reduced_list)

                    else:
                        return reduced_list

        elif to_df != False:
            return pd.DataFrame(results)

        else:
            return results

#test prompts for friends_of_friends
# friends_of_friends('Beyonce', 'MariahCarey')
# friends_of_friends('Beyonce', 'MariahCarey', keys=['name'], to_df=True)
# friends_of_friends('Beyonce', 'MariahCarey', to_df=True)

#find_hashtag function, work in progress

# base_url = 'https://api.twitter.com/1.1/search/tweets.json'
#
# def find_hashtag(hashtag, count=None, result_type=None):
#     # creating a tweet variable from the hashtag input, replacing hash with ''
#     clean_hashtag = hashtag.replace('#', '')
#     tweets = '?qtext=%23' + f"{clean_hashtag}"
#
#     # creating a count variable for count input
#     if count != None:
#         count = '&count=' + f"{count}"
#
#     # creating a result_type variable
#     if result_type != None:
#         result_type = 'result_type=' + f"{result_type}"
#
#     # results from API endpoint, currently not configured for count and result_type
#     search_results = requests.get(base_url + tweets, auth=auth).json()
#     return search_results
#
# #     if keys != None:
# #         reduced_results_list = []
# #         for result in search_results:
# #             new_user_dict = {}
# #             for key in keys:
# #                 new_user_dict[key] = result[key]
# #                 reduced_results_list.append(new_user_dict)
#
# find_hashtag('#DataScience')