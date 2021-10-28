DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS college;

-- https://www.mysqltutorial.org/mysql-enum/
-- Porting to other RDBMS could be an issue because ENUM is not SQL-standard and not many database systems support it.

CREATE TABLE college (
  code VARCHAR(5) PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

CREATE TABLE course (
  code VARCHAR(10) PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  college VARCHAR(5),
  FOREIGN KEY (college) REFERENCES college (code) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE student (
  id CHAR(9) PRIMARY KEY,
  firstname VARCHAR(50) NOT NULL,
  lastname VARCHAR(50) NOT NULL,
  course VARCHAR(10),
  year INT UNSIGNED NOT NULL,
  gender ENUM ('Other', 'Male', 'Female'),
  avatar VARCHAR(300),
  FOREIGN KEY (course) REFERENCES course (code) ON UPDATE CASCADE ON DELETE SET NULL
);