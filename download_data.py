#!/usr/bin/env python3

'''
This script downloads all data for a GitHub user and saves it as a file with the current timestamp.
Among other data, the number of stars, forks and followers is saved.
'''


import requests
import json
import time
import os
import argparse

SAVE_DIR = 'saved_data'

GITHUB_AUTH_TOKEN = os.environ.get('GITHUB_AUTH_TOKEN')
GITHUB_BASE_URL = 'https://api.github.com'
if GITHUB_AUTH_TOKEN:
    HEADERS = {'Authorization': 'token {}'.format(GITHUB_AUTH_TOKEN)}
else:
    HEADERS = None

def get_data_user(user):
    '''
    Get data from GitHub API.
    '''
    url = '{}/users/{}'.format(GITHUB_BASE_URL, user)
    response = requests.get(url, headers=HEADERS)
    data = json.loads(response.text)
    return data


def get_data_repos(user):
    '''
    Get data about repositories from GitHub API.
    '''
    url = '{}/users/{}/repos'.format(GITHUB_BASE_URL, user)
    return_dict = {}
    while True:
        response = requests.get(url, headers=HEADERS)
        data = json.loads(response.text)
        for repo in data:
            return_dict[repo['name']] = repo
        if 'next' not in response.links.keys():
            break
        else:
            url = response.links['next']['url']
    return return_dict


    return data


def save_data(data, user):
    '''
    Save data in a file with the current timestamp.
    '''
    timestamp = time.strftime('%Y%m%d%H%M%S')
    file_name = '{}_{}.json'.format(user, timestamp)
    save_path = os.path.join(SAVE_DIR, file_name)
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(save_path, 'w') as file_:
        json.dump(data, file_, sort_keys=True, indent=4)


def main():
    '''
    Main function.
    '''
    parser = argparse.ArgumentParser(description='Download GitHub user data.')
    parser.add_argument('user', help='GitHub user name')
    # Intervall minutes 
    parser.add_argument('intervall', help='Intervall in minutes between two downloads')
    args = parser.parse_args()
    user = args.user
    intervall = args.intervall
    while True:
        download_data(user)
        time.sleep(int(intervall)*60)


def download_data(user):
    '''
    Download data for a GitHub user.
    '''
    data_all = {}
    data = get_data_user(user)
    data_all['data_from_user_data_request'] = data
    data_repos = get_data_repos(user)
    data_all['data_from_user_repos_request'] = data_repos
    save_data(data_all, user)
    print('Data saved.')






if __name__ == '__main__':
    main()

