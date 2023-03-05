create TABLE users (
  id SERIAL,
  username VARCHAR(50) unique,
  api_key VARCHAR(50) unique,
  PRIMARY KEY (id)
);
