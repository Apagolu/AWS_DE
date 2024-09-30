import configparser

# get config details
config = configparser.ConfigParser()
config.read('dwh.cfg')

DWH_ROLE_ARN = config.get("IAM","IAM_ROLE_NAME")
LOG_DATA = config.get("S3","LOG_DATA")
LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")

# drop staging tables if they exist
drop_staging_events = "DROP TABLE IF EXISTS staging_events"
drop_staging_songs = "DROP TABLE IF EXISTS staging_songs"
# drop fact and dim tables if they exist
drop_songplays = "DROP TABLE IF EXISTS songplays"
drop_users= "DROP TABLE IF EXISTS users"
drop_songs = "DROP TABLE IF EXISTS songs"
drop_artists = "DROP TABLE IF EXISTS artists"
drop_time = "DROP TABLE IF EXISTS time"



# CREATE TABLES
create_staging_events= ("""
    CREATE TABLE IF NOT EXISTS staging_events (
    artist          VARCHAR,
    auth            VARCHAR,
    firstName       VARCHAR,
    gender          VARCHAR,
    itemInSession   INTEGER,
    lastName        VARCHAR,
    length          FLOAT,
    level           VARCHAR,
    location        VARCHAR,
    method          VARCHAR,
    page            VARCHAR,
    registration    FLOAT,
    sessionId       INTEGER,
    song            VARCHAR,
    status          INTEGER,
    ts              TIMESTAMP,
    userAgent       VARCHAR,
    userId          INTEGER);
""")

create_staging_songs = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs        INTEGER,
    artist_id        VARCHAR,
    artist_latitude  DECIMAL(9,6),
    artist_longitude DECIMAL(9,6),
    artist_location  VARCHAR(MAX),
    artist_name      VARCHAR(MAX),
    song_id          VARCHAR,
    title            VARCHAR(MAX),
    duration         FLOAT,
    year             INTEGER
)
""")

create_songplays = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id     INTEGER IDENTITY(0,1) PRIMARY KEY,
    start_time      TIMESTAMP,
    user_id         INTEGER,
    level           VARCHAR,
    song_id         VARCHAR,
    artist_id       VARCHAR,
    session_id      INTEGER,
    location        VARCHAR(MAX),
    user_agent      VARCHAR(MAX)
)
DISTSTYLE EVEN;
""")

create_users = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    first_name  VARCHAR,
    last_name   VARCHAR,
    gender      VARCHAR,
    level       VARCHAR
)
DISTSTYLE ALL;
""")

create_songs = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id     VARCHAR PRIMARY KEY,
    title       VARCHAR,
    artist_id   VARCHAR,
    year        INTEGER,
    duration    FLOAT
)
DISTSTYLE ALL;
""")

create_artists = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id   VARCHAR PRIMARY KEY,
    name        VARCHAR,
    location    VARCHAR,
    latitude    DECIMAL(9,6),
    longitude   DECIMAL(9,6)
)
DISTSTYLE ALL;
""")

create_time_table = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time  TIMESTAMP PRIMARY KEY,
    hour        INTEGER,
    day         INTEGER,
    week        INTEGER,
    month       INTEGER,
    year        INTEGER,
    weekday     VARCHAR
)
DISTSTYLE ALL;
""")


# Loading Staging tables
load_staging_events = ("""
COPY staging_events FROM {}
CREDENTIALS 'aws_iam_role={}'
JSON {}
REGION 'us-west-2'
TIMEFORMAT as 'epochmillisecs';
""").format(LOG_DATA, DWH_ROLE_ARN, LOG_JSONPATH)

load_staging_songs = ("""
COPY staging_songs FROM {}
CREDENTIALS 'aws_iam_role={}'
JSON 'auto'
REGION 'us-west-2';
""").format(SONG_DATA, DWH_ROLE_ARN)

# Load Fact and Dim TABLES

songplay_load = ("""
INSERT INTO songplays (
                        start_time,
                        user_id,
                        level,
                        song_id,
                        artist_id,
                        session_id,
                        location,
                        user_agent
                       )
SELECT DISTINCT(stgevnts.ts)        AS start_time,
       stgevnts.userId              AS user_id,
       stgevnts.level               AS level,
       stgsongs.song_id             AS song_id,
       stgsongs.artist_id           AS artist_id,
       stgevnts.sessionId           AS session_id,
       stgevnts.location            AS location,
       stgevnts.userAgent           AS user_agent
FROM staging_events as stgevnts
JOIN staging_songs as stgsongs ON 
                         (stgevnts.artist = stgsongs.artist_name 
                         AND stgevnts.song = stgsongs.title)
WHERE stgevnts.page = 'NextSong';
""")

users_load = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT
    DISTINCT(userId) AS user_id, 
    firstName        AS first_name, 
    lastName         AS last_name, 
    gender, 
    level
FROM staging_events
WHERE user_id IS NOT NULL;
""")

songs_load = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT
    DISTINCT(song_id), 
    title, 
    artist_id, 
    year, 
    duration
FROM staging_songs
WHERE song_id IS NOT NULL;
""")

load_artists = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT  
    DISTINCT(artist_id), 
    artist_name            AS name, 
    artist_location        AS location, 
    artist_latitude        AS latitude, 
    artist_longitude       AS longitude
FROM staging_songs
WHERE artist_id IS NOT NULL;
""")

load_time = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT 
    DISTINCT(ts)               AS start_time, 
    EXTRACT(hour FROM ts)      AS hour, 
    EXTRACT(day FROM ts)       AS day,
    EXTRACT(week FROM ts)      AS week, 
    EXTRACT(month FROM ts)     AS month,
    EXTRACT(year FROM ts)      AS year, 
    EXTRACT(weekday FROM ts)   AS weekday
FROM staging_events;
""")

# QUERY LISTS

create_all = [create_staging_events,create_staging_songs,create_songplays,create_users,create_songs,create_artists,create_time_table]
drop_all = [drop_staging_events,drop_staging_songs,drop_songplays,drop_users,drop_songs,drop_artists,drop_time]
staging_copy = [load_staging_events, load_staging_songs]
Load_main_tables = [songplay_load, users_load, songs_load, load_artists, load_time]
