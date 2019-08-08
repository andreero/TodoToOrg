"""Convert todo.txt formatted files to Emacs Org mode format

Arguments:
    list of .txt files

Returns:
    None
"""

import re
import os
import argparse
from datetime import datetime
from collections import defaultdict


def parse_date(date_text):
    """ Parse datetime object from string, return None on failure """
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return None


def date_to_string(date):
    """ Convert input to date string, return empty string on failure """
    try:
        return datetime.strftime(date, "%Y-%m-%d")
    except (TypeError, ValueError):
        return ""


def parse_project(text, project_regex):
    """ Parse @project_name string from text, return empty string on failure """
    try:
        return project_regex.search(text).group(1)
    except AttributeError:
        return ""


def parse_key_values(text, key_value_regex):
    """ Parse dict of key:values from text, return empty dict on failure """
    key_values = {}
    for match in key_value_regex.findall(text):
        if len(match.split(':')) == 2:
            key_values[match.split(':')[0]] = match.split(':')[1]
    return key_values


def remove_tags(text, project_regex, context_regex, key_value_regex):
    """ Remove any @project_names, +contexts, key:values from input string """
    text = re.sub(project_regex, '', text)
    text = re.sub(context_regex, '', text)
    text = re.sub(key_value_regex, '', text)
    return text


def process_notes(key_values, completion_date, creation_date):
    """ Convert completion, creation and deadline dates to Org mode format """
    components = []
    if completion_date:
        components.append(f'CLOSED: [{date_to_string(completion_date)}]')
    if creation_date:
        components.append(f'[{date_to_string(creation_date)}]')
    for key, value in key_values.items():
        if key == 'due':
            components.append(f'DEADLINE: <{date_to_string(parse_date(value))}>')
    return '\n'.join(list(filter(None, components)))


def convert_to_org(lines):
    """ Convert list of strings in todo.txt format to Emacs Org mode formatted string """
    projects = defaultdict(list)
    priority_regex = re.compile(r'\(([A-Z])\)')
    project_regex = re.compile(r"(?:^|\s)\+([^\s]+)")
    context_regex = re.compile(r'(?:^|\s)@([^\s]+)')
    key_value_regex = re.compile(r'(?:^|\s)([^\s:]+:[^s:]+)')

    for line in lines:
        completed = False
        priority = ""
        completion_date = None
        creation_date = None

        components = line.split()

        try:
            # completion
            if components[0] == 'x':
                completed = True
                components.pop(0)

            # priority
            if priority_regex.match(components[0]):
                priority = priority_regex.match(components[0]).group(1)
                components.pop(0)

            # dates
            date1 = parse_date(components[0])
            date2 = parse_date(components[1])
            if date1 and date2:
                completion_date = date1
                creation_date = date2
                components.pop(0)
                components.pop(0)
            elif date1:
                if completed:
                    completion_date = date1
                else:
                    creation_date = date1
                components.pop(0)
        except IndexError:
            pass

        line = ' '.join(components)
        project = parse_project(line, project_regex)
        if not project:
            project = 'Tasks'
        contexts = context_regex.findall(line)
        key_values = parse_key_values(line, key_value_regex)
        cleaned_line = remove_tags(line, project_regex, context_regex, key_value_regex)

        org_status = 'DONE' if completed else 'TODO'
        org_priority = f'[#{priority}]' if priority else ''
        org_tags = f':{":".join(contexts)}:' if contexts else ''
        org_heading = ' '.join(list(filter(None, [org_status, org_priority, cleaned_line, org_tags])))
        org_notes = process_notes(key_values, completion_date, creation_date)

        node = '\n'.join(list(filter(None, [f'** {org_heading}', org_notes])))
        projects[project].append(node)

    output_lines = []
    for key, value in projects.items():
        joined_values = '\n'.join(value)
        output_lines.append(f'* {key}\n{joined_values}')

    return '\n'.join(output_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Todo.txt to Org mode converter',
        usage="todo2org.py file1.txt file2.txt ..")
    parser.add_argument('input_files', type=argparse.FileType('r', encoding='utf-8'), nargs='+', help='list of input files')
    options = parser.parse_args()

    for input_file in options.input_files:
        file_name, extension = os.path.splitext(input_file.name)
        with input_file, open(file_name+'.org', 'w', newline='\n', encoding='utf-8') as output_file:
            converted_lines = convert_to_org(input_file.readlines())
            output_file.writelines(converted_lines)


if __name__ == "__main__":
    main()
