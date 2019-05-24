SIMPLE MOVIE GLUE
=================

September, 2012
version 0.1

USER GUIDE
----------

### WHAT IS THIS TOOL FOR?

(D)evice (V)ideo (R)ecorder is a device that allows to record digitally transmitted movie.
The movie can be recorded and then saved to the internal or an external storage.
It is possible to plug in an external hard drive and save a bunch of recorded movies there.
Possible but often not very convenient. Some DVRs support only FAT-formatted hard drives which limit file size to 4 GB-1. This means big movie files saved to a FAT-based external storage are split into pieces.
This tool was created to glue these pieces together to have just one file per movie.
Having one file per movie is more convenient to maintain and easier for other devices to play.
simple_movie_glue tries to be very simple and easy to use. It works in a batch mode. Given many split movies it glues them all one by one in a single run.

### WHY ANOTHER FILE MERGING TOOL?

simple_movie_glue's foremost feature is merging ts movie files in a batch mode. This means convenience: copy split movies to the directory with simple_movie_glue, run the tool, go for a longer walk and once you're back the movies will be copied.

### HOW TO INSTALL IT?

Download and install [Python2](http://www.python.org/download/).

Download simple_movie_glue zip package from github and unzip it to the directory with movies.

Ensure that:

1.  The directory resides on hard drive with a filesystem supporting large files ex.: NTFS, EXT3. FAT32-formatted drive can't be used because of a file size limit.
2.  There is a lot of free space on this drive.

Verify installation by executing simple_movie_glue either by double-clicking on it (Windows) or running it through command line.

### WHERE WILL RESULTS APPEAR?

Glued movies will appear in the same directory where split movies are and the simple_movie_glue itself.

### WHAT DEVICES DOES IT SUPPORT?

Currently, it supports only [Technisat](http://www.technisat.com/en_XX/).

### WHAT KNOWN ISSUES DOES IT HAVE?

It does not display filenames with magic characters (other than Latin) correctly under Windows.

TECHNICAL DOCUMENTATION
-----------------------

simple_movie_glue is implemented in Python2. It reads all filenames from the current folder, applies regular-expression mask to filter out all non-movie files and then builds a movie dictionary. This dictionary has movie titles as its keys and movie filenames as values. It allows to iterate over movies easily. During an iteration files of a movie are copied. Copies lie sequentially and they form the glued result.

How to run end to end tests?  nosetests \*e2e_test\*.py

How to run all tests?  nosetests \*test\*.py

FEEDBACK
--------

Use github issues tab to submit bugs, feature requests, comments, complains.
All of them are more than welcome.
