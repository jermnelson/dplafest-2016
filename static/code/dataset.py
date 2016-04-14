"""Module `dataset` used to create JSON dataset for DPLA testing of Linked Data Fragments
Server project"""
__author__ = "Jeremy Nelson"

import click
import datetime
import ijson
import json
import os
import random
import sys


def generate_recs(filepath, max_value, output):
    if os.path.exists(output):
        test_recs = json.load(open(output, encoding='utf8', errors='ignore'))
    else:
        test_recs = []
    random_pos = []
    start = datetime.datetime.utcnow()
    print("Starting {} at {}".format(filepath, start))
    #print("...Generating Random positions")
    #while 1:
    #    if len(random_pos) >= 20000: # This initial test go from 0-50k
    #        break
    #    rand_counter = random.randint(0, int(max_value))
    #    if not rand_counter in random_pos:
    #        random_pos.append(rand_counter)
    source_resources = ijson.items(
        open(filepath, encoding='utf8', errors='ignore'),
        "item._source.sourceResource")
    rec_counter = 0
    print("...Starting extracting records")
    for resource in source_resources:
        #if rec_counter in random_pos:
        test_recs.append(resource)
        rec_counter += 1
        if not rec_counter%100 and rec_counter > 0:
            #sys.stdout.write(".")
            print(".", end="")
        if not rec_counter%1000:
            #sys.stdout.write(" {} ".format(rec_counter))
            print(" {} ".format(rec_counter), end="")
    end = datetime.datetime.utcnow()
    with open(output, "w+", encoding="utf8", errors="ignore") as output_file:
        json.dump(test_recs, output_file, indent=2, sort_keys=True)
    print("Finished at {} total time {} mins, total records processed={}".format(
        end,
        (end-start).seconds / 60.0,
        rec_counter))
    
     
            
        
        

@click.command()
@click.option('--filepath', help='Full file path to DPLA JSON file', default=None)
@click.option('--max_value', help='Maximum value', default=None)
@click.option('--output', 
    help="Output filepath for JSON", 
    default=os.path.join("..", "json", "test-recs.js"))
def create_dataset(filepath, max_value, output):
    if not os.path.exists(filepath):
        raise ValueError("{} does not exist".format(filepath))
    generate_recs(filepath, max_value, output)

    

if __name__ == '__main__':
    create_dataset()
