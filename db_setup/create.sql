DROP TABLE IF EXISTS subscribers;
DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS incident_reports;

CREATE TABLE incidents(
   id SERIAL PRIMARY KEY NOT NULL,
   created_at timestamp NOT NULL DEFAULT now() ,
   updated_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE incident_reports(
   id SERIAL PRIMARY KEY NOT NULL,
   incident_id INT NOT NULL,
   address VARCHAR(256) NOT NULL,
   description TEXT NOT NULL,
   img_name VARCHAR(256) DEFAULT NULL,
   incident_lat float NOT NULL,
   incident_lon float  NOT NULL,
   created_at timestamp DEFAULT now() NOT NULL,
   updated_at timestamp DEFAULT now() NOT NULL
);

CREATE TABLE subscribers(
   id SERIAL PRIMARY KEY NOT NULL,
   phone_number VARCHAR(32) NOT NULL,
   phone_number_signup_confirmed BOOLEAN DEFAULT FALSE NOT NULL,
   phone_number_signup_confirmation_code VARCHAR(16) NOT NULL,
   access_token VARCHAR(256) DEFAULT NULL,
   subscribed_verified_alerts BOOLEAN DEFAULT FALSE NOT NULL,
   subscribed_unverified_alerts BOOLEAN DEFAULT FALSE NOT NULL,
   area_lat float NOT NULL,
   area_lon float  NOT NULL,
   created_at timestamp DEFAULT now() NOT NULL,
   updated_at timestamp DEFAULT now() NOT NULL
);

// calculates distance in miles between 2 points https://stackoverflow.com/questions/10034636/postgresql-latitude-longitude-query
CREATE OR REPLACE FUNCTION distance(lat1 FLOAT, lon1 FLOAT, lat2 FLOAT, lon2 FLOAT) RETURNS FLOAT AS $$
DECLARE                                                   
    x float = 69.1 * (lat2 - lat1);                           
    y float = 69.1 * (lon2 - lon1) * cos(lat1 / 57.3);        
BEGIN                                                     
    RETURN sqrt(x * x + y * y);                               
END  
$$ LANGUAGE plpgsql;