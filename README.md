# Sparkify :: Cloud-Based Data Warehouse Project

## Introduction

Sparkify, an innovative music streaming startup, is embarking on a transformative journey to harness the power of cloud technologies. As the company experiences rapid growth in both its user base and song catalog, the need for scalable and efficient data management becomes paramount.

## Project Overview
This project centers on the development of a sophisticated ETL (Extract, Transform, Load) pipeline designed to:

Extract data from Sparkify's S3 storage
Transform the data to optimize it for analytical purposes
Load the processed data into AWS Redshift

### Key Objectives

Seamlessly migrate data from S3 to Redshift
Structure the data into a set of dimensional tables
Enable advanced analytics capabilities
Enhance data accessibility for business intelligence teams

By leveraging AWS cloud services, particularly Redshift, Sparkify aims to:

Scale operations efficiently
Improve query performance
Gain deeper insights into user behavior and music trends

This project lays the foundation for Sparkify's data-driven future, empowering the company to make informed decisions and maintain its competitive edge in the dynamic music streaming industry.

## Sparkify ETL Process

The Extract, Transform, Load (ETL) process for Sparkify's data pipeline consists of three main stages:
### 1. Extract
Data is extracted from two primary sources in Amazon S3:

**Song Data**
Content: Metadata about songs and artists
Format: JSON files
Source: Subset of the Million Song Dataset

**Log Data**
Content: User activity logs detailing app interactions
Generation: Created by an event simulator
Basis: Simulated app activity based on the songs in the song dataset
Nature: Represents logs from an imaginary music streaming app

###  2. Stage
Extracted data is initially staged in two separate tables in **Amazon Redshift:**
  1. staging_events
  2. staging_songs

### 3. Transform, Load
Data undergoes transformation and is loaded into a set of dimensional tables:

Process: Utilizes SQL queries
Source: Staging tables (Songs and Events)
Destination: Dimensional tables optimized for analytics

This ETL process ensures that Sparkify's raw data is efficiently extracted, properly staged, and effectively transformed into a structure that facilitates complex queries and deep analytics.

## Data Model

### Fact Table
Songplays is the fact table - contains all historical songs log

**Songplays**
songplay_id - INTEGER, PRIMARY KEY, IDENTITY *Auto-incrementing unique identifier for each song play event*
start_time  - TIMESTAMP *Exact timestamp of when the song play event was initiated*
user_id     - INTEGER *Foreign key referencing the user who initiated the song play*
level       - VARCHAR *User's current subscription tier (e.g., 'free' or 'paid') at the time of play*
song_id     - VARCHAR *Foreign key referencing the specific song that was played*
artist_id   - VARCHAR *Foreign key referencing the artist of the played song*
session_id  - INTEGER *Identifier for the user's listening session*
location    - VARCHAR *Geographic location of the user at the time of play, typically city and state*
user_agent  - VARCHAR- *String identifying the user's device or software application used to play the song*


### Sparkify Dimension Tables Schema

These dimension tables in the Sparkify data warehouse provide detailed attributes for users, songs, artists, and time periods. They are designed to be referenced by the fact table (songplays) for comprehensive data analysis and reporting on user listening patterns and music trends.

**Users**
user_id    - INTEGER, PRIMARY KEY *Unique identifier for each user in the application*
first_name - VARCHAR *User's first name, used for personalization and demographics*
last_name  - VARCHAR *User's last name, used for personalization and demographics*
gender     - VARCHAR *User's self-reported gender, used for demographic analysisv
level      - VARCHAR *Current subscription tier of the user (e.g., 'free' or 'paid')*

**Songs**
song_id  - VARCHAR, PRIMARY KEY *Unique identifier for each song in the music database*
title    - VARCHAR *Full title of the song as it appears in the database*
artist_id - VARCHAR *Foreign key referencing the artists table, linking each song to its performer*
year     - INTEGER *Year of the song's official release*
duration - FLOAT *Length of the song in seconds, precise to milliseconds*

**Artists**
artist_id - VARCHAR, PRIMARY KEY *Unique identifier for each artist in the music database*
name      - VARCHAR *Full name or stage name of the artist*
location  - VARCHAR *Primary geographic location associated with the artist, typically city and country*
latitude  - DECIMAL *Latitude coordinate of the artist's associated location*
longitude - DECIMAL *Longitude coordinate of the artist's associated location*

**Time**
start_time - TIMESTAMP, PRIMARY KEY *Base timestamp from which all other time fields are derived*
hour       - INTEGER *Hour component extracted from start_time, range 0-23*
day        - INTEGER *Day of month extracted from start_time, range 1-31*
week       - INTEGER *Week number within the year extracted from start_time, range 1-53*
month      - INTEGER *Month number extracted from start_time, range 1-12*
year       - INTEGER *Four-digit year extracted from start_time*
weekday    - VARCHAR *day of the week extracted from start_time *


### Distribution styles

** DISTSTYLE EVEN ** is used for fact table - as this is big table, as this table needs to have joins with multiple dimension tables - this would help in parallel processing
** DISTSTYLE ALL**  is used for all Dimension tables - as these are small tables and loading all data on nodes will be particularly useful in faster and effecient query processing.


## Project Components

**dwh.cfg**- * contains Config information *
**create_tables.py** - script that utlizes sql_queries.py to drops and creates all tables
**etl.py** - etl process
**setup.ipynb** - utlizes all above scripts to start of all above scripts

## How to Run this process

**ensure config file is properly updated**

Run the notebook **setup.ipynb** cell by cell



"# AWS_DE" 
