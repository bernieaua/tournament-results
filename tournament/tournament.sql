-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create the tournament database; if a tournament db already exists, drop it
DROP DATABASE IF EXISTS tournament;

-- Create our tournament database
CREATE DATABASE tournament;

-- connect to the database
\c tournament;

-- create our table that will hold player ids and names
CREATE TABLE players (
player_id serial not null,
player_name varchar(50) not null,
PRIMARY KEY(player_id)
);

-- create our table that will hold the match results
CREATE TABLE matches (
opponent_1 int not null references players(player_id),
opponent_2 int not null references players(player_id),
winner int not null references players(player_id)
);

-- create our table that will hold match pairings
CREATE TABLE pairings (
p1_id int not null,
p1_name varchar(50) not null,
p2_id int not null,
p2_name varchar(50) not null
);

-- create a view that will show each player's wins
-- we'll use an aggregate function and group by to tabulate results
create view matches_won as
select p.player_id, p.player_name, count(m.winner) as wins from players p left join matches m on p.player_id=m.winner group by p.player_id order by wins desc, p.player_id;

-- create a view that will show the numbers of matches played by each player
-- we'll use an aggregate function and group by to tabulate results
create view matches_played as
select p.player_id, p.player_name, count(m.opponent_1) as matches from players p left join matches m on (p.player_id=m.opponent_1 or p.player_id=m.opponent_2) group by p.player_id order by p.player_id;

-- create a view that will show the player standings
-- this view will use the previous two views
create view player_standings as
select mw.player_id, mw.player_name, mw.wins, mp.matches from matches_won mw join matches_played mp on mw.player_id=mp.player_id order by mw.wins desc;
