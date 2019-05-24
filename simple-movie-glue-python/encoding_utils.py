def encode_unicode_string(string):
  output = ''
  try:
    output += string.encode('utf-8')
  except UnicodeEncodeError:
    output += string.encode('ascii', 'replace')
  return output

def pretty_print_unicode_array(array):
  output = '['
  i = 0 
  for e in array:
    output += encode_unicode_string(e)

    # if it is not the last one
    if i!=len(array)-1:
      output += ', '
    i+=1
  print output + ']',
