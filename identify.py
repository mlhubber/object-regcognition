# -*- coding: utf-8 -*-

# Copyright (c) Graham.Williams@Togaware. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# A command line script to identify the main object of an image.
#
# ml identify objects [<path>]

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

from objreg_utils import (
    img_url_to_json,
    plot_single_prediction,
    get_model_api,
    tab_complete_path,
    validateURL,
)

import json
import os
import sys
import readline
import urllib
from mlhub import utils as mlutils
import socket

# The working dir of the command which invokes this script.

CMD_CWD = mlutils.get_cmd_cwd()

# Utilities


def _score_for_one_img(img, label='image'):
    """Score for a single image in url.

    Args:
        img (str): a url to an image, or a path to an image.
    """

    try:
        jsonimg = img_url_to_json(img, label=label)
    except (urllib.error.URLError, socket.gaierror, FileNotFoundError, OSError):
        print("URL or file invalid:\n  {}".format(url))
        return

    json_lod = json.loads(jsonimg)
    output = predict_for(json_lod)
    # Want --plot from CLI
    if False: plot_single_prediction(img, output)
    return output


def _score_for(url):
    """Score for the images in url.

    Args:
        url (str): a url to an image, or a path to an image, or a dir for images.
    """

    if validateURL(url):
        _score_for_one_img(url, label=url)
    else:
        # Change to the dir of command which invokes this script
        if CMD_CWD != '':
            oldwd = os.getcwd()
            os.chdir(CMD_CWD)

        url = os.path.abspath(os.path.expanduser(url))

        if CMD_CWD != '':
            os.chdir(oldwd)

        if os.path.isdir(url):
            for img in os.listdir(url):
                img_file = os.path.join(url, '', img)
                _score_for_one_img(img_file, label=img_file)
        else:
            _score_for_one_img(url, label=url)


# Load model

predict_for = get_model_api()


# Setup input path completion

readline.set_completer_delims('\t')
readline.parse_and_bind("tab: complete")
readline.set_completer(tab_complete_path)

# Scoring

if len(sys.argv) < 2:
    try:
        url = input("\nPath or URL of images to recognize (Quit by Ctrl-d):\n(You could try images in '~/.mlhub/objects/cache/images/')\n> ")
    except EOFError:
        print()
        sys.exit(0)

    while url != '':
        _score_for(url)

        try:
            url = input('\nPath or URL of images to recognize (Quit by Ctrl-d):\n> ')
        except EOFError:
            print()
            sys.exit(0)
else:
    for url in sys.argv[1:]:
        _score_for(url)
