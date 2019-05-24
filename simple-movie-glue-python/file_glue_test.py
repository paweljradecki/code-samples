#!/usr/bin/python2 -tt

from nose.tools import *
from file_glue import *

# Given no files
# When executed
# Then do nothing
# And say files copied and merged
def no_files_test():
  fg = FileGlue([])
  fg.copy_and_merge()
  assert_true( fg.are_copied_and_merged() )

# Given one non-empty file
# When executed
# Then do nothing
# And say files copied and merged
def one_file_test():
  fg = FileGlue(['File.txt'])
  fg.copy_and_merge()
  assert_true( fg.are_copied_and_merged() )

# Given seven empty files
# When executed
# Then copy and merge them into a new empty file
# And say files copied and merged
def seven_empty_files_test():
  filename_list = ['File1', 'File2', 'File3', 'File4', 
                   'File5', 'File6', 'File7']
  for filename in filename_list:
    write_binary(filename, '')
  fg = FileGlue(filename_list, 'File7.out')
  fg.copy_and_merge()
  
  f = open('File7.out', 'rb')
  c = f.read()
  f.close

  assert c == ''
  assert_true( fg.are_copied_and_merged() )

  remove_files(filename_list + ['File7.out'])

# Given five small binary files
# When executed
# Then make a new file being a merged version of 
# given five files
def five_small_binary_files_test():
  write_binary('File111', '111')
  write_binary('File22222', '22222')
  write_binary('File33', '33')
  write_binary('File4444', '4444')
  write_binary('File55', '55')

  filename_list = ['File111', 'File22222', 'File33', 'File4444','File55']

  fg = FileGlue(filename_list)
  fg.copy_and_merge()

  f = open('File55.out', 'rb')
  c = f.read()
  f.close()
  assert c == '1112222233444455'

  remove_files(filename_list + ['File55.out'])

# TODO: Output file exists
# TODO: What if at least one file doesn't exist?
# Given six large binary files
# When executed
# Then make a new file being a merged version of 
# given six files
def six_large_binary_files_test():
  #FILESIZE = 400000000 # 400 mln
  FILESIZE = 4000000 # 4 mln
  write_binary('FileL1', '1'*FILESIZE)
  write_binary('FileL2', '2'*FILESIZE)
  write_binary('FileL3', '3'*FILESIZE)
  write_binary('FileL4', '4'*FILESIZE)
  write_binary('FileL5', '5'*FILESIZE)
  write_binary('FileL6', '6'*FILESIZE)


  filename_list = ['FileL1', 'FileL2', 'FileL3', 'FileL4','FileL5', 'FileL6']
  fg = FileGlue(filename_list)
  fg.copy_and_merge()
  print 'Took: ' +str(fg.copy_and_merge_time())+' seconds'

  f = open('FileL6.out', 'rb')
  c = f.read()
  f.close()
  expected_c = '1'*FILESIZE + '2'*FILESIZE + '3'*FILESIZE + '4'*FILESIZE + '5'*FILESIZE + '6' * FILESIZE
  assert c == expected_c

  remove_files(filename_list+['FileL6.out'])

# 
# Test utilities
# 

def write_binary(filename, content):
  f = open(filename, 'wb')
  f.write(content)
  f.close()

def remove_files(filenames):
  for filename in filenames:
    os.remove(filename)
