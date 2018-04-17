DROP TABLE IF EXISTS students;
CREATE TABLE students (
  studentID      INT NOT NULL AUTO_INCREMENT,
  firstName    VARCHAR(30) NOT NULL, 
  lastName     VARCHAR(30) NOT NULL,
  pictureURL   VARCHAR(60),
  birthday     VARCHAR(10) NOT NULL,
  iceName      VARCHAR(50) NOT NULL,
  icePhone     VARCHAR(20) NOT NULL,
  signOutInfo  VARCHAR(120),
  PRIMARY KEY (studentID)
);

DROP TABLE IF EXISTS tutors;
CREATE TABLE tutors (
  tutorID      INT NOT NULL AUTO_INCREMENT,
  firstName    VARCHAR(30) NOT NULL,
  lastName     VARCHAR(30) NOT NULL,
  pictureURL   VARCHAR(60),
  phoneNumber  VARCHAR(20),
  email        VARCHAR(20) NOT NULL,
  days         VARCHAR(20),
  studentID    INT,
  PRIMARY KEY (tutorID)
);


DROP TABLE IF EXISTS classes;
CREATE TABLE classes (
  classID   INT NOT NULL AUTO_INCREMENT,
  className VARCHAR(30) NOT NULL,
  startDate DATETIME NOT NULL, 
  endDate   DATETIME NOT NULL, 
  days      VARCHAR(20) NOT NULL,
  startTime DATETIME NOT NULL,
  endTIme   DATETIME NOT NULL, 
  studentID INT NOT NULL, 
  PRIMARY KEY (classID)
);

DROP TABLE IF EXISTS attendance;
CREATE TABLE attendance (
  classID     INT NOT NULL, 
  date        DATETIME NOT NULL, 
  studentID   INT NOT NULL, 
  totalNumber INT NOT NULL, 
  day         VARCHAR(20) NOT NULL, 
  tutorID     INT, 
  timestamp   TIMESTAMP NOT NULL,
  PRIMARY KEY (classID)

);

