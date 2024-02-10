import requests

r = requests.get('https://gitlab.com/api/v4/users/ilemona/projects')

my_projects = r.json()

for project in my_projects:
    print(project['name'])
    print(project['description'])
    print(project['web_url'])
    print("\n")
