import shutil
import time
import signal
import sys
import os

from time import sleep

# NOTE: Performance on Linux. When running this program on Linux it seems to be a bit too greedy. It takes too much resources causing the operating system to lose usual interactivity. Some applications running in parallel with it like music player tend to hang for a short while; can't listen to music smoothely. Not sure if this is still valid.
# TODO: What if FileGlue gets killed during gluing by other process. Is there a way to ensure the partial result file is never written in this case?
# TODO: Maybe command line interface dependencies (eg. KeyboardInterrupt) should not be here...?

class FileGlue:
  """
  Merges files together.
  
  So far the only one strategy has been implemented: copy_and_merge.
  Basically, it copies input files. These copies reside sequentially on hard-disk, one after the other and make a single file, an output file.

  Output filename can be specified in the constructor. Otherwise output filename is a concatenation of the last input filename and '.out' string. 
  Overwritting is set by default. To disable it use a flag in constructor.
  """
  pass

  def __init__(self, input_filenames, output_filename=None, overwrite=True):
    """
    Constructs FileGlue object. Sets input filename list. Specifies output filename. Sets overwrite flag.
    """
    # Buffer used upon copying 
    self.buffer_size = 256000

    self.filename_list = input_filenames
    self.copied_and_merged = False
    self.overwrite = overwrite

    if output_filename is None and len(input_filenames) != 0:
      last_filename = input_filenames[-1]
      self.output_filename = last_filename + '.out'
    else:
      self.output_filename = output_filename

  def is_allowed_to_copy_and_merge(self):
    """
    Prevents from erasing previous results.
    """
    if self.overwrite:
      return True
    elif os.path.isfile(self.output_filename):
      return False
    else:
      return True

  def copy_and_merge(self):
    """
    Glues files together. Measures time of the operation. Listens for the process interruption signals.
    """
    self.start_time = time.time()

    def signal_handler(signal, frame):
      raise KeyboardInterrupt

    signal.signal(signal.SIGINT, signal_handler)

    if len(self.filename_list) > 1:
      try:
        destination = open(self.output_filename,'wb')
        for filename in self.filename_list:
          source = open(filename,'rb')
          shutil.copyfileobj(source, destination, self.buffer_size)
          source.close()
        destination.close()
      except KeyboardInterrupt:
        try: 
          destination.close()
        except NameError:
          None
        else:
          os.remove(self.output_filename)
        try:
          source.close()
        except NameError:
          None
        raise KeyboardInterrupt

    self.copied_and_merged = True
    self.end_time = time.time()
    return

  def are_copied_and_merged(self):
    """
    Tells if all input files are copied.
    """
    return self.copied_and_merged

  def copy_and_merge_time(self):
    """
    Tells how long the operation has taken in seconds.
    """
    return round(self.end_time-self.start_time, 1)
