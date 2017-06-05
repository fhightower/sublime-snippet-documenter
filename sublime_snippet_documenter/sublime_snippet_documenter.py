#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import xml.etree.ElementTree as ET

SNIPPET_DOCS_MARKDOWN_TEMPLATE = "- `{}`: {}\n"


def parse_arguments():
    parser = argparse.ArgumentParser(description='Create documentation for ' +
                                                 'sublime text snippets.')
    parser.add_argument('input_directory', help='input directory')
    parser.add_argument('output_file', help='output file')

    args = parser.parse_args()
    return args


def create_snippet_documentation(snippet_data):
    """create function."""
    return SNIPPET_DOCS_MARKDOWN_TEMPLATE.format(snippet_data['tabTrigger'],
                                                 snippet_data['description'])


def add_documentation(snippet_documentation, output_file):
    """Add the complete documentation to the end of the output file."""
    snippet_docs_heading = "\n\n## Available Snippets\n"

    # split the snippets up
    sorted_snippets = snippet_documentation.split("\n")
    # sort the documentation alphabetically
    sorted_snippets.sort()

    # recreate the documentation with a heading and sorted snippet docs
    snippet_documentation = snippet_docs_heading + "\n".join(sorted_snippets)

    # add a newline at the end of the snippet docs section
    snippet_documentation += "\n"

    # append the documentation to the output file
    with open(output_file, 'a') as f:
        f.write(snippet_documentation)


def find_sublime_snippets(directory):
    """Find sublime snippet files in given directory and parse as XML."""
    parsed_sublime_snippets = list()

    # walk through the given directory
    for root, dirs, files in os.walk(directory):
        # iterate through the files in that directory
        for file_name in files:
            # if the file is a sublime snippet...
            if file_name.endswith(".sublime-snippet"):
                # read the contents of the snippet
                with open(os.path.join(root, file_name), 'r') as f:
                    # parse the snippet's text as XML
                    parsed_snippet = ET.fromstring(f.read())
                    # append the parsed snippet to be returned
                    parsed_sublime_snippets.append(parsed_snippet)

    # return the list of parsed, sublime snippets
    return parsed_sublime_snippets


def get_snippet_data(parsed_snippet):
    """Record the essential values from a snippet."""
    snippet_data = {
        'tabTrigger': None,
        'scope': None,
        'description': None,
    }

    for child in parsed_snippet:
        # if the current child is one we are looking for, record its value
        if child.tag in snippet_data:
            snippet_data[child.tag] = child.text

    # return the important values from the current snippet
    return snippet_data


def main():
    """Document sublime text snippets."""
    args = parse_arguments()
    complete_snipppet_documentation = str()

    # find all sublime snippets in the input directory
    sublime_snippets = find_sublime_snippets(args.input_directory)

    for sublime_snippet in sublime_snippets:
        # get the data from the snippet
        snippet_data = get_snippet_data(sublime_snippet)

        # create documentation from the given data
        snippet_documentation = create_snippet_documentation(snippet_data)

        complete_snipppet_documentation += snippet_documentation

    add_documentation(complete_snipppet_documentation, args.output_file)


if __name__ == '__main__':
    main()
