Tournament - Bernie Aua
April 2015


INSTRUCTIONS


SET UP THE DATABASE

From within psql, execute the following command:

\i tournament.sql

This will create the tables and views necessary for this application.


TEST THE APPLICATION

From within the vagrant shell, execute the following:

python tournament_test.py


Note: a second testPairings() function was added to test the pairing of eight players.
