import re
import string

class MovieDictionaryBuilder:
  """
  Builds dictionary:
   { movie_title : list_of_movie_filenames }
  which is used later as an iterator
  """

  def __init__(self, pattern, title_group_no, filenames=[]):
    """
    Creates internal structures.
    """
    self.pattern = pattern
    self.title_group_no = title_group_no

    self.movie_dictionary = self.build_movie_dictionary(filenames)

  def dictionary(self):
    return self.movie_dictionary

  #
  # Utility methods
  #

  def matches_pattern(self, movie_filename):
    """
    Checks whether the movie_filename matches 
    the regular expression self.pattern.
    If so it returns the title which is selected
    by self.title_group_no, regular expression group number.

    Ex.: 
        if 

        self.pattern = r'(\d\d\d)\.(.*)\.ts'
        self.title_group_no = 2
        movie_filename = "002.Sherlock Holmes.ts"

        then it will return

        "Sherlock Holmes"
    """
    match = re.search(self.pattern, movie_filename)
    if match:
      return match.group(self.title_group_no)
    else:
      return None

  def build_movie_dictionary(self, filenames):
    d = {}
    sorted_filenames = sorted(filenames)
    for f in sorted_filenames:
      title = self.matches_pattern(f)
      if title:
        if not d.has_key(title):
          d[title] = []
        d[title].append(f)
    return d
