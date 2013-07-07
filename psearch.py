#!/usr/bin/env python

import sys
import json, urllib
import requests

GOOGLE_API = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'

BING_API = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Composite?Sources=%27web%27&Query=%27"%2b"'
MY_AZURE_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
'''
Please get yoursef one, following the steps below:
first go to https://datamarket.azure.com/dataset/bing/search# and register
to get a free Bing Search API Subscription - it's free for up to 5000 requests
per month, then go on https://datamarket.azure.com/account/keys and add another
key to the default one (I have failed to understand why the default one cannot
be used), give it a name (doesn't matter what), copy-paste to MY_AZURE_KEY above.
'''

def alert_and_exit(alert_message):
    print alert_message
    sys.exit(1)

def google_phrase_search(phrase):
    """
    (str) -> (int)

    Return a number of occurrences of a phrase in Google search
    """
    google_query = GOOGLE_API + urllib.urlencode({'q': phrase})

    try:
        google_response = urllib.urlopen(google_query)
    except IOError:
        alert_and_exit("Was unable to establish connection to search providers.")

    google_search_results = google_response.read().decode("utf8")
    google_results = json.loads(google_search_results)
    google_data = google_results['responseData']

    try:
        return int(google_data['cursor']['estimatedResultCount'])
    except:
        return 0 #exception for "no results"

def bing_phrase_search(phrase):
    """
    (str) -> (int)

    Return a number of occurrences of a phrase in Bing search
    """
    bing_query = BING_API + phrase + '%27&$format=json&$top=1'

    try:
        bing_response = requests.get(bing_query, auth=(MY_AZURE_KEY, MY_AZURE_KEY), verify=False).json()
    except IOError:
        alert_and_exit("Was unable to establish connection to search providers.")
        
    try:
        return int(bing_response['d']['results'][0]['WebTotal'])
    except:
        return 0 #exception for "no results"

def main():
    """Takes string argument and return the number of occurances of the given
    string in Google and Bing phrase search (example "Winter is coming")
    """
    phrase = ""

    if len(sys.argv) == 1:
        alert_and_exit("No arguments for a search were given. Type '--help' argument for help")

    if sys.argv[1] == "--help":
        alert_and_exit("Returns a number of occurrences of an entire phrase\n" + \
                       "using Google and Bing search engines\n" + \
                       "Example: psearch winter is coming")
                  
    for arg in sys.argv[1:]:
        phrase = phrase + " " + arg

    phrase = '"' + phrase[1:] + '"' #get rid of extra space, add quotes for phrase search

    phrase_occurrences_google = google_phrase_search(phrase)
    phrase_occurrences_bing = bing_phrase_search(phrase)

    print "Estimated number of occurrences of:", phrase
    print "{:,}".format(phrase_occurrences_google), "- Google search engine."
    print "{:,}".format(phrase_occurrences_bing), "- Bing search engine."

    return phrase_occurrences_google, phrase_occurrences_bing
    
if __name__ == '__main__':
    main()
