#!/usr/bin/python2 -tt
#vim: set fileencoding=utf-8

from nose.tools import *
from movie_dictionary_builder import *
from recording_device import *

goldenstar_movie_builder = MovieDictionaryBuilder(goldenstar_pattern(), goldenstar_title_group_no())

star = 'Star Wars'
goldenstar_movies = [
                      [ star+'.ts',  star ],
                      [ star+'.001', star ],
                      [ star+'.999', star ],
                      [ star+'.ts',  star ],
                    ]

non_goldenstar_movies = [
                        'Some Movie.ts_',
                        'Some other movie._ts',
                        'Something weird.1a1',
                        'Movie filename without extention',
                    ]

def goldenstar_regex_test():
  for m in goldenstar_movies:
    assert goldenstar_movie_builder.matches_pattern(m[0]) == m[1]

def goldenstar_regex_negative_test():
  for m in non_goldenstar_movies:
    assert goldenstar_movie_builder.matches_pattern(m[0]) == None

technisat_movie_builder = MovieDictionaryBuilder(technisat_pattern(), technisat_title_group_no())
rock = 'Rock and Roll Hall of Fame - koncert na 25-lecie'
droga = u'Droga życia'
kobieta = u'Kobieta, która___'
smierc = u'Śmierć lorda Edgware\'a'
gra = u'Śmiertelna gra'
technisat_movies = [
                     ['18.000.'+rock+'.ts',rock],
                     ['18.001.'+rock+'.ts',rock],
                     ['18.002.'+rock+'.ts',rock],
                     ['18.003.'+rock+'.ts',rock],
                     ['18.004.'+rock+'.ts',rock],
                     ['18.005.'+rock+'.ts',rock],
                     ['12.000.'+droga+'.ts', droga],
                     ['12.001.'+droga+'.ts',droga],
                     ['12.002.'+droga+'.ts',droga],
                     ['12.003.'+droga+'.ts',droga],
                     ['12.004.'+droga+'.ts',droga],
                     ['20.000.'+kobieta+'.ts',kobieta],
                     ['20.001.'+kobieta+'.ts',kobieta],
                     ['20.002.'+kobieta+'.ts',kobieta],
                     ['20.003.'+kobieta+'.ts',kobieta],
                     ['20.004.'+kobieta+'.ts',kobieta],
                     ['24.000.'+smierc+'.ts',smierc],
                     ['24.001.'+smierc+'.ts',smierc],
                     ['24.002.'+smierc+'.ts',smierc],
                     ['24.003.'+smierc+'.ts',smierc],
                     ['24.004.'+smierc+'.ts',smierc],
                     ['24.005.'+smierc+'.ts',smierc],
                     ['8.000.'+gra+'.ts',gra],
                     ['8.001.'+gra+'.ts',gra],
                     ['8.002.'+gra+'.ts',gra],
                     ['8.003.'+gra+'.ts',gra],
                  ]

def technisat_test():
  for m in technisat_movies:
    assert technisat_movie_builder.matches_pattern(m[0]) == m[1]

non_technisat_movies = [
                        '13',
                        '19',
                        '2000',
                        '2001',
                        '21',
                        '25',
                        '9',
                    ]

def technisat_regex_negative_test():
  for m in non_technisat_movies:
    assert goldenstar_movie_builder.matches_pattern(m[0]) == None
