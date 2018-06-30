DROP TABLE IF EXISTS subscribers;
DROP TABLE IF EXISTS incidents;

CREATE TABLE incidents(
   id SERIAL PRIMARY KEY NOT NULL,
   address VARCHAR(256) NOT NULL,
   description TEXT NOT NULL,
   img_name VARCHAR(256) DEFAULT NULL,
   incident_lat float NOT NULL,
   incident_lon float  NOT NULL,
   created_at timestamp NOT NULL DEFAULT now(),
   updated_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE subscribers(
   id SERIAL PRIMARY KEY NOT NULL,
   phone_number VARCHAR(32) NOT NULL,
   phone_number_confirmed BOOLEAN DEFAULT FALSE NOT NULL,
   phone_number_confirmation_code VARCHAR(16) NOT NULL,
   access_token VARCHAR(256) DEFAULT NULL,
   subscribed_verified_alerts BOOLEAN DEFAULT FALSE NOT NULL,
   subscribed_unverified_alerts BOOLEAN DEFAULT FALSE NOT NULL,
   area_lat float NOT NULL,
   area_lon float  NOT NULL,
   radius float NOT NULL DEFAULT 1,
   created_at timestamp DEFAULT now() NOT NULL,
   updated_at timestamp DEFAULT now() NOT NULL
);

