#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    # open our db connection
    dbconn = connect()
    # set up a cursor object
    cursor = dbconn.cursor()
    # execute our delete query
    cursor.execute("delete from matches")
    # commit the deletion
    dbconn.commit()
    # close the db connection
    dbconn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    # open our db connection
    dbconn = connect()
    # set up a cursor object
    cursor = dbconn.cursor()
    # execute our delete query
    cursor.execute("delete from players")
    # commit the deletion
    dbconn.commit()
    # close the db connection
    dbconn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    # open our db connection
    dbconn = connect()
    # set up a cursor object
    cursor = dbconn.cursor()
    # execute our query
    cursor.execute("select count(player_name) from players")
    # read our result
    result = cursor.fetchone()
    count = result[0]
    # close the db connection
    dbconn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    # open our db connection
    dbconn = connect()
    # set up a cursor object
    cursor = dbconn.cursor()
    # execute our query
    cursor.execute("insert into players (player_name) values (%s)", (name,))
    # commit the insertion
    dbconn.commit()
    # close the db connection
    dbconn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    # open our db connection
    dbconn = connect()
    # set up a cursor object
    cursor = dbconn.cursor()
    # execute our query
    cursor.execute("select * from player_standings;")
    # read our results
    playerStandings = cursor.fetchall()
    # close the db connection
    dbconn.close()
    # return the results of our player standings
    return playerStandings



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    # open our db connection
    dbconn = connect()
    # set up a cursor object
    cursor = dbconn.cursor()
    # execute our query
    cursor.execute("insert into matches (opponent_1, opponent_2, winner) values (%s, %s, %s)", (winner, loser, winner))
    # commit the insertion
    dbconn.commit()
    # close the db connection
    dbconn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """



    # open our db connection
    dbconn = connect()
    # set up a cursor object
    cursor = dbconn.cursor()
    # empty the pairings table
    cursor.execute("delete from pairings;")
    dbconn.commit()
    # determine how many records in our player_standings table
    cursor.execute("select count(*) from player_standings;")
    # log the result
    result = cursor.fetchone()
    records = result[0]
    print("Records: " + str(records))
    # grab two adjacent records at a time. they should have the same number of wins after one round.
    # then take the player info and insert it into the pairings table
    for i in xrange(0, records-1, 2):
        cursor.execute("select player_id, player_name from player_standings limit 2 offset (%s);", (i,))
        rows = cursor.fetchall()
        cursor.execute("insert into pairings (p1_id, p1_name, p2_id, p2_name) values (%s, %s, %s, %s)", (rows[0][0], rows[0][1], rows[1][0], rows[1][1]))
        # commit the insertion
        dbconn.commit()

    # grab our pairings
    cursor.execute("select * from pairings;")
    pairings = cursor.fetchall()
    # close the db connection
    dbconn.close()
    # return the results of our pairings
    return pairings
