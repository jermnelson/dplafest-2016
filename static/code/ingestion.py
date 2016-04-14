"""ingestion.py - DPLA Test

This script is licensed under the GNU Affero version 3. 
Copyrighted 2015 by Jeremy Nelson <jermnelson@gmail.com>
"""
__author__ = "Jeremy Nelson"

import click
import datetime 
import json
import logging
import os 
import rdflib 
import redis

ldfs_cache = redis.StrictRedis()
LUA_LOCATION = os.path.join("..", "linked-data-fragments/lib/")
LUA_SCRIPTS = dict()

logging.basicConfig(filename='ingestion.log',level=logging.DEBUG)

def setup():
    for name in ["add_get_triple",
                 "triple_pattern_search",
                 "get_triple"]:
        filepath = os.path.join(
            LUA_LOCATION, "{}.lua".format(name))
        print(filepath, os.path.exists(filepath))
        with open(filepath) as fo:
            lua_script = fo.read()
        sha1 = ldfs_cache.script_load(lua_script)
        LUA_SCRIPTS[name] = sha1

def process_source(source, backend):
    triples_processed = 0
    keys = 3
    rec_graph = rdflib.Graph()
    rec_graph.parse(data=json.dumps(source), format='json-ld')
    for s,p,o in rec_graph:
        triples_processed += 1
        if backend:
             ldfs_cache.evalsha(LUA_SCRIPTS["add_get_triple"], 4, str(s), str(p), str(o), backend)
        else:
             ldfs_cache.evalsha(LUA_SCRIPTS["add_get_triple"], 3, str(s), str(p), str(o))
    return triples_processed

@click.command()
@click.option('--filepath', help='Full file path to DPLA JSON file')
@click.option('--backend', help="Select hash, set, or string", default=None)
def process_dpla_json(filepath, backend):
    dpla_json = json.load(open(filepath, errors='ignore'))
    start = datetime.datetime.utcnow()
    total_triples = 0
    logging.info("Started processing {} records at {}".format(len(dpla_json), start.isoformat()))
    for i,row in enumerate(dpla_json):
        total_triples += process_source(row, backend)
        #if not i%100 and i>0:
        #    print(".", end="")
        #if not i%1000:
        #    print(i, end="")
        #if not i%5000 and i > 0:
        #    print(" triples={} ".format(total_triples))
    end = datetime.datetime.utcnow()
    logging.info("Finished processing at {}, total time {} mins. Records {} Triples {}\n".format(
        end.isoformat(),
        (end-start).seconds / 60.0,
        len(dpla_json),
        total_triples))

if __name__ == '__main__':
    setup()
    process_dpla_json()
