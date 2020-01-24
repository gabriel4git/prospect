#!/usr/bin/env python

import googlemaps
import json
import csv
import click
import config
from datetime import datetime

@click.command()
@click.option("--keyword", help="search term _ separated", required=True)
@click.option("--clean/--dirty", default="False", help="generates csv with only 'name','formatted_address', 'permanently_closed', 'url', 'formatted_phone_number', 'website', 'opening hours'")
@click.option("--full/--trunc", default="False", help="full or truncated, three for testing, results")
@click.option("--near", help="lat, lon pair, e.g. 34.0451801,-118.2602186", default=config.home, required=True, prompt="lat-lon pair")

def places_near(keyword, near, clean, full):
    """Create a csv from detailed places 
    (https://developers.google.com/places/web-service/details)
    information in a given radius
    """

    client=googlemaps.Client(config.maps_key)

    results = client.places_nearby(keyword=keyword.replace('_', ' '), location=(near),
    radius=config.radius, language=config.language, type=keyword)    

    with open(keyword + '.csv', 'w') as f: 
        place_info = dict()
        limit = len(results['results'])
        headers = []
        field_set = []

        if full == False:
            limit = 3
        if clean == True:
            field_set = ['name','formatted_address', 'permanently_closed', 'url', 'formatted_phone_number', 'website', 'opening_hours']
        for res in results['results'][0:limit]: 
            pi = client.place(res['place_id'], language=config.language, fields=field_set)['result']
            place_info[res['place_id']] = pi
            if len(headers) < len(pi.keys()):
                headers = pi.keys()

        sort_pi = sorted(place_info.items(), key=lambda item: len(item[1].keys()))
        place_info = dict(sort_pi)
        w = csv.DictWriter(f, headers, extrasaction='ignore')
        w.writeheader()
        for k, v in place_info.items():
            w.writerow(v) 

if __name__ == '__main__':
    places_near()