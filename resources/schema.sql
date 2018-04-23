DROP TABLE IF EXISTS students;
CREATE TABLE students (
  studentID      INT NOT NULL AUTO_INCREMENT,
  firstName    VARCHAR(30) NOT NULL, 
  lastName     VARCHAR(30) NOT NULL,
  pictureURL   VARCHAR(60),
  birthday     VARCHAR(10),
  iceName      VARCHAR(50),
  icePhone     VARCHAR(20),
  signOutInfo  VARCHAR(120),
  PRIMARY KEY (studentID)
);

DROP TABLE IF EXISTS classes;
CREATE TABLE classes (
  classID   INT NOT NULL AUTO_INCREMENT,
  className VARCHAR(30) NOT NULL,
  startDate DATETIME NOT NULL, 
  endDate   DATETIME NOT NULL,
  startTime DATETIME NOT NULL,
  endTIme   DATETIME NOT NULL,
  sun       bool NOT NULL,
  mon       bool NOT NULL,
  tue       bool NOT NULL,
  wed       bool NOT NULL,
  thu       bool NOT NULL,
  fri       bool NOT NULL,
  sat       bool NOT NULL,
  PRIMARY KEY (classID)
);

DROP TABLE IF EXISTS class_membership;
CREATE TABLE class_membership (
  classID   INT NOT NULL AUTO_INCREMENT,
  studentID INT NOT NULL,
  firstName   VARCHAR (30) NOT NULL,
  lastName   VARCHAR (30) NOT NULL,
  PRIMARY KEY (classID, studentID)
);


DROP TABLE IF EXISTS attendance;
CREATE TABLE attendance (
  classID     INT NOT NULL,
  inTime     DATETIME NOT NULL,
  outTime    DATETIME,
  studentID   INT NOT NULL,
  PRIMARY KEY (classID, studentID)
);

DROP TABLE IF EXISTS tutors;