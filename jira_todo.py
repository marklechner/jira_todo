#!/usr/bin/env python3

import getpass
import yaml
import datetime
from jira import JIRA


def load_config():
    with open("config.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def generate_ticket(conf, u):
    todos = conf['todo_list']
    task_template = "{{task}}{}{{task}}"
    current_date = datetime.date.today()
    year, woy, doy = current_date.isocalendar()
    ticket = {
        'project': {'key': "PROJECTKEY"},
        'summary': 'ToDo List week {} - {}'\
            .format(woy, year),
        'description': 'ToDo list for week {} of {}\n'\
            .format(woy, year),
        'issuetype': {'name': 'Task'},
        'labels': ['todos'],
        'assignee': {'name': u}
        }
    for i in todos:
        ticket['description'] = ticket['description']\
            + task_template.format(i)
    return ticket


def get_creds(config):
    u = config.get('default_user') if config.get('default_user') \
        else input("Username: ")
    p = getpass.getpass()
    return u, p


def main():
    conf = load_config()
    u, p = get_creds(conf)
    jira_server = {"server": conf['jira_server']}
    jira = JIRA(options=jira_server, basic_auth=(u, p))
    ticket = generate_ticket(conf, u)
    todo_list_ticket = jira.create_issue(fields=ticket)
    print("Created - {}".format(todo_list_ticket))


if __name__ == "__main__":
    main()
