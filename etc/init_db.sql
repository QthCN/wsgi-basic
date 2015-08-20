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

CREATE TABLE POLICIES(
  id  INT NOT NULL AUTO_INCREMENT,
  action VARCHAR(128) NOT NULL,
  role VARCHAR(1024) DEFAULT "",
  owner INT DEFAULT 0,
  PRIMARY KEY (id),
  KEY (action)
);

-- Test users
INSERT INTO USERS(name, role, password) VALUES("tianhuan", "admin", PASSWORD("111111"));
INSERT INTO USERS(name, role, password) VALUES("userA", "user", PASSWORD("111111"));

-- Default policies
INSERT INTO POLICIES(action, role, owner) VALUES("wsgi_basic:validate_token", "admin", 1);
INSERT INTO POLICIES(action, role, owner) VALUES("wsgi_basic:delete_token", "admin", 1);