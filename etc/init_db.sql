CREATE DATABASE IF NOT EXISTS wsgi_basic DEFAULT CHARACTER SET utf8;
USE wsgi_basic;

CREATE TABLE USERS(
  id INT NOT NULL AUTO_INCREMENT,
  name     VARCHAR(128)  NOT NULL UNIQUE,
  role VARCHAR(128) NOT NULL,
  password VARCHAR(1024) NOT NULL,
  PRIMARY KEY (id),
  KEY (name)
);

CREATE TABLE TOKENS(
  token_id VARCHAR(128) NOT NULL,
  username VARCHAR(128)  NOT NULL,
  create_time DATETIME NOT NULL,
  expire_time DATETIME NOT NULL,
  PRIMARY KEY (token_id)
);


INSERT INTO USERS(name, role, password) VALUES("tianhuan", "admin", PASSWORD("111111"));
INSERT INTO USERS(name, role, password) VALUES("userA", "user", PASSWORD("111111"));