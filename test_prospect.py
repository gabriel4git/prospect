#!/usr/bin/env python

import click
from click.testing import CliRunner
from prospect import places_near

def test_places_near():
    runner = CliRunner()
    
    res = runner.invoke(places_near, ['--keyword=retirement_home'], input='')
    res_clean = runner.invoke(places_near, ['--clean', '--keyword=retirement_home'], input='') 
    
    assert not res_clean.exception
    assert not res.exception

if __name__ == '__main__':
    test_places_near()