"""Module `dataset` used to create JSON dataset for DPLA testing of Linked Data Fragments
Server project"""
__author__ = "Jeremy Nelson"

import click
import ijson
import json
import os
import random

@click.command()
@click.option('--filepath', help='Full file path to DPLA JSON file', default=None)
@click.option('--max_value', help='Maximum value', default=None)
@click.option('--output', 
    help="Output filepath for JSON", 
    default=os.path.join("..", "json", "test-recs.js"))
def create_dataset(filepath, max_value, output):
    if not os.path.exists(filepath):
        raise ValueError("{} does not exist".format(filepath))
    parser = ijson.parse(open(output, encoding='utf8', errors='ignore'))
    if os.path.exists(output):
        test_recs = json.load(open(output, encoding='utf8', errors='ignore'))
    else:
        test_recs = []
    




