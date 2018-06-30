DELETE FROM subscribers;
DELETE FROM incident_reports;
DELETE FROM incidents;

// Ievgen number
INSERT INTO subscribers (phone_number, phone_number_confirmed, phone_number_confirmation_code, access_token, subscribed_verified_alerts, subscribed_unverified_alerts, area_lat, area_lon, radius)
VALUES ('+17188830959', true, '12345', 'abc1', true, true, 40.6933600, -73.9853900, 3);

// free number https://www.receivesms.co/us-phone-number/2641/
INSERT INTO subscribers (phone_number, phone_number_confirmed, phone_number_confirmation_code, access_token, subscribed_verified_alerts, subscribed_unverified_alerts, area_lat, area_lon, radius)
VALUES ('+16234695657', true, '12346', 'abc2', true, true, 40.6933600, -73.9853900, 2);