import os
import shutil

import requests
import sys
from pygithub3 import Github
import click


def get_latest_commit_sha(client):
    ref = client.git_data.references.get('heads/master')
    return ref.object['sha']


def find_gitignore_url(client, commit, lang):
    tree = client.git_data.trees.get(commit, recursive=True)
    for item in tree.tree:
        if item['type'] == 'blob':
            filename, ext = os.path.splitext(os.path.basename(item['path']))
            if lang.lower() in filename.lower():
                return 'https://raw.githubusercontent.com/github/gitignore/master/{}'.format(item['path'])

    return None


@click.command()
@click.argument('language', required=True)
def main(language):
    gh = Github(user='github', repo='gitignore')
    latest_sha = get_latest_commit_sha(gh)
    gitignore_url = find_gitignore_url(gh, latest_sha, language)
    if not gitignore_url:
        print('Unable to find gitignore file for the provided language: {}'.format(language))
        return 1

    resp = requests.get(gitignore_url)
    with open('.gitignore', 'a') as f:
        f.write(resp.content)

    return 0


if __name__ == '__main__':
    sys.exit(main())





