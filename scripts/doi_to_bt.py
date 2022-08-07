import requests

def doi_to_bt(doi):
    url = "http://dx.doi.org/" + doi
    headers = {"accept": "application/x-bibtex"}
    bt = requests.get(url, headers=headers)
    return(bt.text)

