-- For SQLite3
-- www3 - Mar 26, 0:20
CREATE TABLE Volunteer(id VARCHAR(30), name VARCHAR(60), phone
VARCHAR(15), location VARCHAR(60), friends VARCHAR(30), total_score
SMALLINT, reputation SMALLINT);
CREATE TABLE Organization(id VARCHAR(30), name VARCHAR(60), phone
VARCHAR(15), location VARCHAR(60), reputation SMALLINT);
CREATE TABLE Job(id VARCHAR(30), organization_id VARCHAR(30), event_date
DATE, score_value SMALLINT, committed VARCHAR(30), completed
VARCHAR(30));
-- Two simple indexes to shorten lookup times
CREATE INDEX Idx_volunteer ON Volunteer (location);
CREATE INDEX Idx_organization ON Organization (location);

