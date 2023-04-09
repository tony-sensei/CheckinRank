CREATE TABLE IF NOT EXISTS businessInfo(
	id		    VARCHAR(25)	    PRIMARY KEY,
    name		VARCHAR(100)	NOT NULL,
    address 	VARCHAR	        DEFAULT NULL,
    city		VARCHAR(100)	DEFAULT NULL,
    zipcode	    VARCHAR(10)	    NOT NULL,
    latitude	NUMERIC 	    NOT NULL,
    longitude	NUMERIC 	    NOT NULL
);

CREATE TABLE IF NOT EXISTS category(
	id 			SERIAL		    PRIMARY KEY,
    name 		VARCHAR(100)	NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS category_in_business(
	business_id 	VARCHAR(25)	REFERENCES businessInfo(id),
    category_id     INTEGER 	REFERENCES category(id),
    PRIMARY KEY (business_id, category_id)
);

CREATE TABLE IF NOT EXISTS checkin(
    business_id VARCHAR(25) REFERENCES businessInfo(id),
    date_hour TIMESTAMP NOT NULL,
    checkin_count INTEGER NOT NULL,
    PRIMARY KEY (business_id, date_hour)
);

CREATE TABLE IF NOT EXISTS review(
    review_id       VARCHAR(25) PRIMARY KEY,
	business_id 	VARCHAR(25)	REFERENCES businessInfo(id),
	text            TEXT        NOT NULL,
    date 	        TIMESTAMP	NOT NULL
);

CREATE TABLE IF NOT EXISTS population(
	zipcode 	VARCHAR(10)	PRIMARY KEY,
    population 	INTEGER	    NOT NULL
);
