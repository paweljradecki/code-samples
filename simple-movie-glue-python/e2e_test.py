#/usr/bin/env python2
# vim: set fileencoding=utf-8 

import subprocess
import os
from nose.tools import *

# helpers

def call_helper(execution_line):
    p = subprocess.Popen(execution_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return [p.stdout.readlines(), p.wait()]

def remove_files(filenames):
  for filename in filenames:
    os.remove(filename)

# tests

def technisat_e2e_test():
    """
    Tests whether appropriate new files are created.
    For one movie tests whether the first and the last 
    three bytes of the source files match equivalent bytes in a result file.
    Checks whether result code is zero, success.
    """

    expected_output_filenames = [u'./technisat-test-data/ZażółćGęśląJaźń.ts', 
                                 u'./technisat-test-data/Śmierć lorda Edgware\'a.ts', 
                                 u'./technisat-test-data/Kobieta, która___.ts']

    [stdout, return_code] = call_helper("cd technisat-test-data; ../simple_movie_glue.py --non-interactive")

    f = open(u'./technisat-test-data/20.000.Kobieta, która___.ts', 'rb')
    f.seek(0)
    source_first_bytes = f.read(3)
    f.close

    f = open(u'./technisat-test-data/20.004.Kobieta, która___.ts', 'rb')
    f.seek(-3, 2)
    source_last_bytes = f.read(3)
    f.close
    
    f = open(u'./technisat-test-data/Kobieta, która___.ts', 'rb')
    f.seek(0)
    destination_first_bytes = f.read(3)
    f.seek(-3, 2)
    destination_last_bytes = f.read(3)
    f.close

    for filename in expected_output_filenames:
      try:
           with open(filename) as f: pass
      except IOError as e:
           assert False

    assert source_first_bytes == destination_first_bytes
    assert source_last_bytes == destination_last_bytes
    assert return_code == 0

    # clean-up
    remove_files(expected_output_filenames)
