CREATE TABLE IF NOT EXISTS businessInfo(
	id		    VARCHAR(25)	    PRIMARY KEY,
    name		VARCHAR(100)	not null,
    address 	VARCHAR	        default null,
    city		VARCHAR(10)	    default null,
    zipcode	    VARCHAR(5)	    not null,
    latitude	numeric 	    not null,
    longitude	numeric 	    not null
);

CREATE TABLE IF NOT EXISTS category(
	id 			SERIAL		    PRIMARY KEY,
    name 		VARCHAR(100)	NOT NULL
);

CREATE TABLE IF NOT EXISTS category_in_business(
	business_id 	VARCHAR(25)	REFERENCES businessInfo(id),
    category_id     INTEGER 	REFERENCES category(id),
    PRIMARY KEY (business_id, category_id)
);

CREATE TABLE IF NOT EXISTS checkin(
	business_id 	VARCHAR(25)	REFERENCES businessInfo(id),
    date 	        TIMESTAMP	NOT NULL,
    PRIMARY KEY (business_id, date)
);

CREATE TABLE IF NOT EXISTS review(
    review_id       VARCHAR(25) PRIMARY KEY,
	business_id 	VARCHAR(25)	REFERENCES businessInfo(id),
	text            TEXT        NOT NULL,
    date 	        TIMESTAMP	NOT NULL
);

CREATE TABLE IF NOT EXISTS population(
	zipcode 	VARCHAR(5)	primary key,
    population 	INTEGER	    NOT NULL
);

