DROP TABLE artist;
DROP TABLE artist_details;
DROP TABLE song;

CREATE TABLE artist
(
    artist_full_id int PRIMARY KEY,
    artist_id VARCHAR(20),
    artist_7digitalid int(11),
    artist_playmeid int(11),
    artist_mbid text
);

CREATE TABLE artist_details(artist_full_id int primary key auto_increment, artist_name VARCHAR
(255), artist_hotttnesss double, artist_familiarity double, artist_location text, artist_longitude double);

CREATE TABLE song(track_id VARCHAR(40) PRIMARY KEY, artist_full_id int, danceability DOUBLE, song_id text, release_attr text, title text, end_of_fade_in double, time_signature int
(11), mode int
(11), loudness double, mode_confidence double, song_hotttnesss double, time_signature_confidence double, key_attr int
(11), analysis_sample_rate int
(11), year int
(11), key_confidence double, audio_md5 text, track_7digitalid int
(11), energy double, duration double, release_7digitalid int
(11), tempo double, start_of_fade_out double, artist_latitude double);

INSERT INTO artist_details
    (artist_name, artist_hotttnesss, artist_familiarity, artist_location, artist_longitude)
SELECT
    artist_name, artist_hotttnesss, artist_familiarity, artist_location, artist_longitude
FROM megarelation
GROUP BY artist_id, artist_name, artist_hotttnesss, artist_familiarity, artist_location, artist_longitude;

INSERT INTO song
SELECT track_id, artist_full_id, danceability, song_id, release_attr, title, end_of_fade_in, time_signature, mode, loudness, mode_confidence, song_hotttnesss, time_signature_confidence, key_attr, analysis_sample_rate, year, key_confidence, audio_md5, track_7digitalid, energy, duration, release_7digitalid, tempo, start_of_fade_out, artist_latitude
FROM artist_details JOIN megarelation USING(artist_name, artist_hotttnesss, artist_familiarity, artist_location, artist_longitude);

INSERT INTO artist
SELECT
    artist_full_id, artist_id, artist_7digitalid, artist_playmeid, artist_mbid
FROM artist_details JOIN megarelation USING(artist_name, artist_hotttnesss, artist_familiarity, artist_location, artist_longitude)
GROUP BY DROP TABLE artist;
DROP TABLE artist_details;
DROP TABLE song;

CREATE TABLE artist
(
    artist_full_id int PRIMARY KEY,
    artist_id VARCHAR(20),
    artist_7digitalid int(11),
    artist_playmeid int(11),
    artist_mbid text
);

CREATE TABLE artist_details(artist_full_id int primary key auto_increment, artist_name VARCHAR
(255), artist_hotttnesss double, artist_familiarity double, artist_location text, artist_longitude double);

CREATE TABLE song(track_id VARCHAR(40) PRIMARY KEY, artist_full_id int, danceability DOUBLE, song_id text, release_attr text, title text, end_of_fade_in double, time_signature int
(11), mode int
(11), loudness double, mode_confidence double, song_hotttnesss double, time_signature_confidence double, key_attr int
(11), analysis_sample_rate int
(11), year int
(11), key_confidence double, audio_md5 text, track_7digitalid int
(11), energy double, duration double, release_7digitalid int
(11), tempo double, start_of_fade_out double, artist_latitude double);

INSERT INTO artist_details
    (artist_name, artist_hotttnesss, artist_familiarity, artist_location, artist_longitude)
SELECT
    artist_name, artist_hotttnesss, artist_familiarity, artist_location, artist_longitude
FROM megarelation
GROUP BY artist_id, artist_name, artist_hotttnesss, artist_familiarity, artist_location, artist_longitude;

INSERT INTO song
SELECT track_id, artist_full_id, danceability, song_id, release_attr, title, end_of_fade_in, time_signature, mode, loudness, mode_confidence, song_hotttnesss, time_signature_confidence, key_attr, analysis_sample_rate, year, key_confidence, audio_md5, track_7digitalid, energy, duration, release_7digitalid, tempo, start_of_fade_out, artist_latitude
FROM artist_details JOIN megarelation USING(artist_name, artist_hotttnesss, artist_familiarity, artist_location, artist_longitude);

INSERT INTO artist
SELECT
    artist_full_id, artist_id, artist_7digitalid, artist_playmeid, artist_mbid
FROM artist_details JOIN megarelation USING(artist_name, artist_hotttnesss, artist_familiarity, artist_location, artist_longitude)
GROUP BY artist_full_id, artist_id, artist_7digitalid, artist_playmeid, artist_mbid;