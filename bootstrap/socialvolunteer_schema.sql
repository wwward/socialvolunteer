-- For SQLite3
-- www3 - Mar 26, 0:20
CREATE DATABASE IF NOT EXISTS volunteerdb;
CREATE TABLE Volunteer(id VARCHAR(30), name VARCHAR(60), phone
VARCHAR(15), location VARCHAR(60), friends VARCHAR(30), total_score
SMALLINT, reputation SMALLINT, username VARCHAR(30));
CREATE TABLE Organization(id VARCHAR(30), name VARCHAR(60), phone VARCHAR(15), location VARCHAR(60), reputation SMALLINT, description VARCHAR(100));
CREATE TABLE Job(id VARCHAR(30), organization_id VARCHAR(30), event_date
DATE, event_time SMALLINT, event_day_of_week SMALLINT, score_value SMALLINT, committed VARCHAR(30), completed
VARCHAR(30), description VARCHAR(255), category VARCHAR(255));
CREATE TABLE Keyword(keyword VARCHAR(30), reference_id VARCHAR(30));
-- Two simple indexes to shorten lookup times
CREATE INDEX Idx_volunteer ON Volunteer (location);
CREATE INDEX Idx_organization ON Organization (location);
CREATE INDEX Idx_keyword ON Keyword (keyword);

