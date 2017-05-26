#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_sublime_snippet_documenter
----------------------------------

Tests for `sublime_snippet_documenter` module.
"""

from sublime_snippet_documenter import sublime_snippet_documenter


def reset_test_readme():
    """Reset the readme used for testing to its original state."""
    output = "# Test Readme\n\n## Usage\n\nTesting\n\n## Contributions\n\nTest"

    with open('./tests/test_files/README.md', 'w') as f:
        f.write(output)


def test_find_xml_children():
    """Find the children in the snippet."""
    snippets = sublime_snippet_documenter.find_sublime_snippets(
        './tests/test_files/')

    # make sure we found the (one) testing snippet
    assert len(snippets) == 1

    for snippet in snippets:
        snippet_data = sublime_snippet_documenter.get_snippet_data(snippet)

        # ensure the tabTrigger is correct
        assert snippet_data['tabTrigger'] == 'dictcount'

        # ensure the scope is correct
        assert snippet_data['scope'] == 'source.python'

        # ensure the description is correct
        assert snippet_data['description'] == 'Test description'

        print("Snippet data: {}".format(snippet_data))

        # make sure the documentation was created correctly
        snippet_docs = sublime_snippet_documenter.create_snippet_documentation(
            snippet_data)
        print("Snippet docs: {}".format(snippet_docs))
        assert snippet_docs == "- `dictcount`: Test description\n"

        complete_snippet_documentation = "\n\n## Available Snippets\n\n"
        complete_snippet_documentation += snippet_docs

        # write the snippet documentation to the output file
        sublime_snippet_documenter.add_documentation(
            complete_snippet_documentation, './tests/test_files/README.md')

    # rest the readme used for testing
    reset_test_readme()
