#!/usr/bin/python2 -tt
# vim: set fileencoding=utf-8 

from file_glue import *
from movie_dictionary_builder import *
from encoding_utils import *
from recording_device import *

import os
from sys import stdout, argv

def print_usage():
  print
  print "  USAGE:"
  print "  simple_movie_glue.py [--non-interactive|-h|--help]"
  print
  print "  DESCRIPTION:"
  print "  Glues all TS files together in the current folder according"
  print "  to the Technisat pattern."
  print
  print "  By default, it works in an interactive way: it asks before gluing,"
  print "  waits for an interaction when processing is finished."
  print
  print "  OPTIONS:"
  print "  -h --help              prints usage"
  print "  --non-interactive      does not ask questions at work"
  print 

def pretty_print_filenames_to_be_glued(movie_items):
  group_no = 1
  for title, filenames in movie_items:
    print group_no, 
    pretty_print_unicode_array(filenames)
    group_no += 1
    print

def glue(movie_items):

  glued = False
  list = []

  for title, filenames in movie_items:
    print 'Gluing', encode_unicode_string(title+'.ts'+'...'),
    stdout.flush()
    fg = FileGlue(filenames, title+'.ts')
    try:
      fg.copy_and_merge()
      glued = True
    except KeyboardInterrupt:
      print 'INTERRUPTED!'
      stdout.flush()
      exit(1)
    print 'glued in '+ str(fg.copy_and_merge_time()) + ' seconds.'
    stdout.flush()

  if glued != True:
    print 'Nothing was glued!'
    stdout.flush()

  return


def prompt(msg):
  print msg, 
  something = raw_input()

#
# MAIN EXECUTION
#

if __name__=='__main__':

  import os
  interactive = True
  END_MESSAGE = "FINISHED!" 

  pattern = technisat_pattern()
  title_group_no = technisat_title_group_no()

  if len(sys.argv) > 2:
    print
    print "Too many parameters!"
    print_usage()
    exit(0)

  if len(sys.argv) == 2:
    if sys.argv[1] == '--non-interactive':
      interactive = False
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
      print_usage()
      exit(0)
    else:
      print
      print "Invalid parameter name:", sys.argv[1]
      print_usage()
      exit(1)
  
  print
  print "Scanning source folder:", os.getcwd()
  print "with a Technisat pattern."
  print

  all_filenames = os.listdir(u'.')
  movie_dictionary = MovieDictionaryBuilder(pattern, title_group_no, all_filenames).dictionary()
  movie_items = sorted(movie_dictionary.items())

  if movie_items:
    print "Found movie files to be glued:"
    pretty_print_filenames_to_be_glued(movie_items)
  else:
    print "No movie files found to be glued."
    if interactive:
      prompt(END_MESSAGE+" Press ENTER to exit.")
    else:
      print END_MESSAGE
    exit(0)

  print 
  if interactive:
    print "Proceed with gluing? [Y/n]",
    answer = raw_input()  

    if (answer!='Y' and answer!='y' and answer!=''):
      exit(0)

  print
  glue(movie_items)
  print
  if interactive:
    prompt(END_MESSAGE+" Press ENTER to exit.")
  else:
    print END_MESSAGE
  exit(0)
