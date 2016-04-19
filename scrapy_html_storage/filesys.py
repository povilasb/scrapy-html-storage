"""File system related facilities.
"""

import os
import gzip


def ensure_dir_exists(dir_path):
    """Create the specified directory if it does not exist.

    Creates all intermediate subdirectories needed for the leaf directory.

    Args:
        dir_path (str): directory to be created.
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def write_to_file(fname, html_body):
    """Writes text to file.

    Args:
        fname (str): save text to this file.
        html_body (str): results page HTML content.
    """
    dir_path = os.path.dirname(fname)
    ensure_dir_exists(dir_path)

    with open(fname, 'w') as html_file:
        html_file.write(html_body)


def write_to_gzip(fname, html_body):
    """Writes text to compressed file.

    Args:
        fname (str): save compressed text to this file.
        html_body (str): results page HTML content.
    """
    dir_path = os.path.dirname(fname)
    ensure_dir_exists(dir_path)

    with gzip.open(fname, 'wb') as html_file:
        html_file.write(html_body)
