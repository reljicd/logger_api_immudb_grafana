COPY users(username, api_key)
FROM '/data/users.csv'
DELIMITER ','
CSV HEADER;
