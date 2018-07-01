
DELETE FROM subscribers;
DELETE FROM incidents;

/* Ievgen number - 3 miles*/
INSERT INTO subscribers (phone_number, phone_number_confirmed, phone_number_confirmation_code, access_token, subscribed_verified_alerts, subscribed_unverified_alerts, area_lat, area_lon, radius)
VALUES ('+17188830959', true, '12345', 'abc1', true, true, 40.6933600, -73.9853900, 3);

/* Erika's number - 30 miles*/
INSERT INTO subscribers (phone_number, phone_number_confirmed, phone_number_confirmation_code, access_token, subscribed_verified_alerts, subscribed_unverified_alerts, area_lat, area_lon, radius)
VALUES ('+15165102043', true, '12347', 'abc3', true, true, 40.6933600, -73.9853900, 30);

/* Joe's number - 300 miles*/
INSERT INTO subscribers (phone_number, phone_number_confirmed, phone_number_confirmation_code, access_token, subscribed_verified_alerts, subscribed_unverified_alerts, area_lat, area_lon, radius)
VALUES ('+19178600476', true, '12348', 'abc5', true, true, 40.6933600, -73.9853900, 300);

/* Frank's number - 3000 miles*/
INSERT INTO subscribers (phone_number, phone_number_confirmed, phone_number_confirmation_code, access_token, subscribed_verified_alerts, subscribed_unverified_alerts, area_lat, area_lon, radius)
VALUES ('+19178152736', true, '12349', 'abc6', true, true, 40.6933600, -73.9853900, 3000);

/* free number https://smsreceivefree.com/info/15344295472/ - 3 miles, need to log in */
INSERT INTO subscribers (phone_number, phone_number_confirmed, phone_number_confirmation_code, access_token, subscribed_verified_alerts, subscribed_unverified_alerts, area_lat, area_lon, radius)
VALUES ('+15344295472', true, '12346', 'abc2', true, true, 40.6933600, -73.9853900, 3);
