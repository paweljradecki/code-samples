# Wholesale articles importer

## Requirements

Import data from `data/*.dat` files, normalise it and save it to JSON.

## Prerequisites

- OpenJDK12+ from AdoptOpenJDK
- Maven with `JAVA_HOME` set pointing at JDK12
- `dimensions.dat` file split into a file per dimension, eg. with:
```
grep "DA" dimensions.dat > dimensions_da.dat
grep "DP" dimensions.dat > dimensions_dp.dat
grep "DU" dimensions.dat > dimensions_du.dat
grep "DC" dimensions.dat > dimensions_dc.dat
```
- Executable jar file must be run on a path with existing folders: `data`, `article.json` and `final-json-output`.

## Installation and running

### Compile and package

```
mvn clean install
```

### Run

```
rm -Rf ./article.json/*
rm -Rf ./final-json-output/*
java -jar target/wholesale-articles-importer.jar
``` 

## Open issues
- Scalability 
    - Parsing `articles.dat` could be simultaneously run by multiple threads possibly by splitting file into smaller ones.
    - Processes of parsing `dimensions.dat`, `prices.dat`, `texts.dat` could be done in parallel. Each of these parings could also employ many threads.
    - Map-reduce (eg. with Hadoop implementation) feels like a very good and scalable but expensive solution for quickly growing amount of data.
- Reliability
    - Nagios alarm could be employed to check if process is alive and if logs produce ERRORs.
- Robustness
    - Integration test with tricky data should be written to verify edge cases are properly handled.
    
