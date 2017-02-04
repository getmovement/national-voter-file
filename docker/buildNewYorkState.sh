#!/bin/sh

###################
## Populate the date dimension with 20 years worth
## of days
docker-compose run etl /opt/pentaho/data-integration/pan.sh -file /national-voter-file/src/main/pdi/populateDateDimension.ktr

################################
##### Load Electoral Jurisdiction Dimensions
################################
docker-compose run etl /opt/pentaho/data-integration/pan.sh -file /national-voter-file/src/main/pdi/LoadCensus.ktr -param:censusFile=/national-voter-file/dimensionaldata/census.csv -param:filterState=NY -param:lookupFile=/national-voter-file/dimensionaldata/countyLookup.csv


##################
## Python script to clean up and enrich the New York Voter File
docker-compose run etl python3 /national-voter-file/src/main/python/transformers/newyork_prepare.py

##################
## Transform to extract voting precincts directly from the source voter file
docker-compose run etl /opt/pentaho/data-integration/pan.sh  -file /national-voter-file/src/main/pdi/newyork/SaveNewYorkPrecincts.ktr -param:reportDate=2016-08-31 -param:reportFile=/national-voter-file/data/NewYork/AllNYSVoters20160831SAMPLE.txt

###################
## Run job to process sample voter file
docker-compose run etl /opt/pentaho/data-integration/kitchen.sh -file /national-voter-file/src/main/pdi/ProcessPreparedVoterFile.kjb -param:reportDate=2016-08-31 -param:reportFile=/national-voter-file/data/NewYork/AllNYSVoters20160831SAMPLE_OUT.csv -param:reporterKey=3
