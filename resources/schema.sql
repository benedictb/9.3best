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
  startDate DATE NOT NULL,
  endDate   DATE NOT NULL,
  startTime TIME NOT NULL,
  endTime   TIME NOT NULL,
  sun       bool NOT NULL DEFAULT 0,
  mon       bool NOT NULL DEFAULT 0,
  tue       bool NOT NULL DEFAULT 0,
  wed       bool NOT NULL DEFAULT 0,
  thu       bool NOT NULL DEFAULT 0,
  fri       bool NOT NULL DEFAULT 0,
  sat       bool NOT NULL DEFAULT 0,
  PRIMARY KEY (classID)
);

DROP TABLE IF EXISTS enrollment;
CREATE TABLE enrollment (
  classID   INT NOT NULL,
  studentID INT NOT NULL,
  firstName   VARCHAR (30) NOT NULL,
  lastName   VARCHAR (30) NOT NULL,
  PRIMARY KEY (classID, studentID)
);


DROP TABLE IF EXISTS attendance;
CREATE TABLE attendance (
  classID     INT NOT NULL,
  inTime      DATETIME NOT NULL,
  outTime     DATETIME,
  studentID   INT NOT NULL,
  inDate      DATE,
  dayOfWeek   VARCHAR(3),
  PRIMARY KEY (classID, studentID, inDate)
);

-- clean up previous table names
DROP TABLE IF EXISTS tutors;
DROP TABLE IF EXISTS class_membership