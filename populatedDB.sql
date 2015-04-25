-- MySQL dump 10.13  Distrib 5.6.23, for Win32 (x86)
--
-- Host: localhost    Database: cs4400
-- ------------------------------------------------------
-- Server version	5.6.24-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book` (
  `ISBN` varchar(50) NOT NULL,
  `SubjectName` varchar(50) NOT NULL,
  `ShelfNumber` int(2) NOT NULL,
  `Title` varchar(50) NOT NULL,
  `Cost` int(10) NOT NULL,
  `IsBookOnReserve` char(1) NOT NULL,
  `Edition` int(3) NOT NULL,
  `Publisher` varchar(50) NOT NULL,
  `PublicationPlace` varchar(50) NOT NULL,
  `CopyrightYear` year(4) NOT NULL,
  PRIMARY KEY (`ISBN`),
  KEY `SubjectName` (`SubjectName`),
  KEY `ShelfNumber` (`ShelfNumber`),
  CONSTRAINT `Book_ibfk_1` FOREIGN KEY (`SubjectName`) REFERENCES `subject` (`Name`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Book_ibfk_2` FOREIGN KEY (`ShelfNumber`) REFERENCES `shelf` (`ShelfNumber`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES ('0-122-12364-3','Science',2,'Modern Physics',60,'0',9,'Pearson','Austin',2006),('0-123-36956-6','Fiction',6,'Eragon',30,'0',7,'Bloomsbury','Cincinnati',1990),('0-216-45265-4','Nonfiction',5,'Thomas Edision',60,'0',3,'Atlantic','Los Angeles',2010),('0-219-13698-3','Economics',3,'Basic Economics',70,'1',3,'Holt','Cambridge',2007),('0-221-15423-8','Math',1,'Advanced Trigonometry',80,'0',2,'McGraw','Atlanta',2004),('0-235-56482-4','Economics',3,'The Principles of Economics',50,'0',4,'Prentice','San Jose',2003),('0-321-12226-7','Math',1,'Intro to Calculus',70,'0',4,'McGraw','Atlanta',2005),('0-432-72214-7','Fiction',6,'Harry Potter',20,'0',10,'Pearson','New York',2005),('0-563-42039-3','Science',2,'Theory of Evolution',30,'0',6,'Amazon','New York',2009),('0-620-23467-2','Science',2,'Modern Biology',90,'0',1,'Holt','Cambridge',2000),('0-724-37125-2','Nonfiction',5,'The Life of Rosa Parks',50,'0',2,'Crescent','Marietta',2001),('0-872-93012-2','Fiction',6,'Theory of LoL',10,'0',1,'Chen Books','New Hampshire',2014),('0-992-32673-1','History',4,'America History',75,'1',6,'Prentice','Dallas',2003),('0-992-32673-5','History',4,'The Principles of Economics',100,'0',8,'BookHub','Phoenix',2012);
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_authors`
--

DROP TABLE IF EXISTS `book_authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book_authors` (
  `ISBN` varchar(50) NOT NULL,
  `Author` varchar(50) NOT NULL,
  PRIMARY KEY (`ISBN`,`Author`),
  CONSTRAINT `Book_Authors_ibfk_1` FOREIGN KEY (`ISBN`) REFERENCES `book` (`ISBN`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_authors`
--

LOCK TABLES `book_authors` WRITE;
/*!40000 ALTER TABLE `book_authors` DISABLE KEYS */;
INSERT INTO `book_authors` VALUES ('0-122-12364-3','Michael'),('0-123-36956-6','Chris'),('0-216-45265-4','Daniel'),('0-219-13698-3','Kevin'),('0-219-13698-3','Mark'),('0-221-15423-8','George'),('0-235-56482-4','Gabe'),('0-321-12226-7','Robert'),('0-432-72214-7','Rowling'),('0-563-42039-3','Darwin'),('0-620-23467-2','David'),('0-724-37125-2','Jacob'),('0-872-93012-2','Allen'),('0-992-32673-1','Bob'),('0-992-32673-1','Paul'),('0-992-32673-5','Anthony');
/*!40000 ALTER TABLE `book_authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_copy`
--

DROP TABLE IF EXISTS `book_copy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book_copy` (
  `ISBN` varchar(50) NOT NULL,
  `CopyNumber` int(2) NOT NULL,
  `IsOnHold` char(1) NOT NULL,
  `IsCheckedOut` char(1) NOT NULL,
  `IsDamaged` char(1) NOT NULL,
  `FutureRequester` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CopyNumber`,`ISBN`),
  KEY `ISBN` (`ISBN`),
  CONSTRAINT `Book_Copy_ibfk_1` FOREIGN KEY (`ISBN`) REFERENCES `book` (`ISBN`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_copy`
--

LOCK TABLES `book_copy` WRITE;
/*!40000 ALTER TABLE `book_copy` DISABLE KEYS */;
INSERT INTO `book_copy` VALUES ('0-122-12364-3',1,'1','0','0','kevin'),('0-123-36956-6',1,'0','0','1','devin'),('0-216-45265-4',1,'0','0','0',NULL),('0-219-13698-3',1,'0','0','0','bob'),('0-221-15423-8',1,'0','0','1',NULL),('0-235-56482-4',1,'0','0','1',NULL),('0-321-12226-7',1,'0','0','0','eric'),('0-432-72214-7',1,'0','0','1',NULL),('0-563-42039-3',1,'0','0','1',NULL),('0-620-23467-2',1,'0','0','1',NULL),('0-724-37125-2',1,'0','0','1',NULL),('0-872-93012-2',1,'0','0','1',NULL),('0-992-32673-1',1,'0','0','0',NULL),('0-992-32673-5',1,'0','0','1',NULL),('0-122-12364-3',2,'0','0','0','shauna'),('0-123-36956-6',2,'1','0','0',NULL),('0-216-45265-4',2,'0','0','0',NULL),('0-219-13698-3',2,'0','0','0',NULL),('0-221-15423-8',2,'0','0','0',NULL),('0-235-56482-4',2,'0','0','0',NULL),('0-321-12226-7',2,'0','0','0',NULL),('0-432-72214-7',2,'0','0','1',NULL),('0-563-42039-3',2,'0','0','1',NULL),('0-724-37125-2',2,'1','0','0',NULL),('0-872-93012-2',2,'0','0','1',NULL),('0-992-32673-1',2,'0','0','0',NULL),('0-122-12364-3',3,'0','0','0',NULL),('0-123-36956-6',3,'0','0','0',NULL),('0-216-45265-4',3,'0','0','0',NULL),('0-219-13698-3',3,'0','0','0',NULL),('0-221-15423-8',3,'0','0','0',NULL),('0-235-56482-4',3,'0','1','0',NULL),('0-563-42039-3',3,'1','0','0',NULL),('0-724-37125-2',3,'0','1','0',NULL),('0-872-93012-2',3,'0','1','0',NULL),('0-219-13698-3',4,'0','0','0',NULL),('0-221-15423-8',4,'0','0','0',NULL),('0-235-56482-4',4,'0','0','0',NULL),('0-563-42039-3',4,'0','1','0',NULL),('0-724-37125-2',4,'0','0','0',NULL),('0-872-93012-2',4,'0','0','0',NULL),('0-219-13698-3',5,'0','0','0',NULL),('0-221-15423-8',5,'1','0','0','devin'),('0-235-56482-4',5,'0','0','1',NULL),('0-563-42039-3',5,'0','0','0',NULL),('0-872-93012-2',5,'0','0','0',NULL),('0-219-13698-3',6,'0','0','0',NULL),('0-221-15423-8',6,'0','1','0','rsun39'),('0-235-56482-4',6,'0','0','0',NULL),('0-219-13698-3',7,'0','0','0',NULL),('0-221-15423-8',7,'0','0','0','rsun39'),('0-235-56482-4',7,'0','0','0',NULL);
/*!40000 ALTER TABLE `book_copy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `floor`
--

DROP TABLE IF EXISTS `floor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `floor` (
  `FloorNumber` int(1) NOT NULL,
  `NumStudentAssistant` int(3) NOT NULL,
  `NumCopier` int(2) NOT NULL,
  PRIMARY KEY (`FloorNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `floor`
--

LOCK TABLES `floor` WRITE;
/*!40000 ALTER TABLE `floor` DISABLE KEYS */;
INSERT INTO `floor` VALUES (1,5,5),(2,3,2),(3,1,1);
/*!40000 ALTER TABLE `floor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issue`
--

DROP TABLE IF EXISTS `issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `issue` (
  `Username` varchar(25) NOT NULL,
  `IssueID` int(10) NOT NULL AUTO_INCREMENT,
  `ISBN` varchar(50) NOT NULL,
  `CopyNumber` int(2) NOT NULL,
  `IssueDate` datetime NOT NULL,
  `ExtensionDate` datetime NOT NULL,
  `ReturnDate` datetime NOT NULL,
  `ExtensionCount` int(5) DEFAULT '0',
  PRIMARY KEY (`IssueID`),
  KEY `Username` (`Username`),
  KEY `ISBN` (`ISBN`),
  KEY `CopyNumber` (`CopyNumber`),
  CONSTRAINT `issue_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `student_faculty` (`Username`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `issue_ibfk_2` FOREIGN KEY (`ISBN`) REFERENCES `book_copy` (`ISBN`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `issue_ibfk_3` FOREIGN KEY (`CopyNumber`) REFERENCES `book_copy` (`CopyNumber`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issue`
--

LOCK TABLES `issue` WRITE;
/*!40000 ALTER TABLE `issue` DISABLE KEYS */;
INSERT INTO `issue` VALUES ('rsun39',1,'0-122-12364-3',1,'2015-01-05 00:00:00','2015-01-05 00:00:00','2015-01-19 10:18:08',0),('rsun39',2,'0-123-36956-6',1,'2015-01-05 00:00:00','2015-01-05 00:00:00','2015-01-19 10:18:09',0),('rsun39',3,'0-216-45265-4',1,'2015-01-05 00:00:00','2015-01-05 00:00:00','2015-01-19 10:18:12',0),('rsun39',4,'0-221-15423-8',1,'2015-01-05 00:00:00','2015-01-05 00:00:00','2015-01-19 10:18:13',0),('rsun39',5,'0-235-56482-4',1,'2015-01-05 00:00:00','2015-01-05 00:00:00','2015-01-19 10:18:15',0),('rsun39',6,'0-321-12226-7',1,'2015-01-05 00:00:00','2015-01-05 00:00:00','2015-01-19 10:18:16',0),('rsun39',7,'0-432-72214-7',1,'2015-01-05 00:00:00','2015-01-05 00:00:00','2015-01-19 10:18:18',0),('rsun39',8,'0-563-42039-3',2,'2015-01-05 00:00:00','2015-01-05 00:00:00','2015-01-19 10:18:19',0),('rsun39',9,'0-620-23467-2',1,'2015-01-05 00:00:00','2015-01-05 00:00:00','2015-01-19 10:18:21',0),('rsun39',10,'0-724-37125-2',1,'2015-01-05 00:00:00','2015-01-05 00:00:00','2015-01-19 10:18:24',0),('rsun39',11,'0-872-93012-2',1,'2015-01-05 00:00:00','2015-01-05 00:00:00','2015-01-19 10:18:26',0),('shauna',12,'0-221-15423-8',2,'2015-01-05 00:00:00','2015-01-05 10:21:02','2015-01-19 10:21:02',2),('denise',13,'0-221-15423-8',3,'2015-01-05 00:00:00','2015-01-05 10:21:15','2015-01-19 10:21:15',1),('ji',14,'0-235-56482-4',2,'2015-01-05 00:00:00','2015-01-05 10:21:28','2015-01-19 10:21:28',1),('morley',15,'0-235-56482-4',4,'2015-01-05 00:00:00','2015-02-01 10:25:30','2015-02-15 10:25:30',3),('kevin',16,'0-221-15423-8',4,'2015-01-05 00:00:00','2015-01-19 10:24:35','2015-02-02 00:00:00',1),('devin',17,'0-122-12364-3',1,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:26:55',0),('devin',18,'0-123-36956-6',1,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:26:57',0),('devin',19,'0-216-45265-4',1,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:27:00',0),('devin',20,'0-221-15423-8',5,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:27:02',0),('devin',21,'0-235-56482-4',5,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:27:03',0),('devin',22,'0-321-12226-7',1,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:27:05',0),('devin',23,'0-432-72214-7',2,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:27:07',0),('devin',24,'0-563-42039-3',2,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:27:09',0),('devin',25,'0-620-23467-2',1,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:27:10',0),('devin',26,'0-724-37125-2',1,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:27:13',0),('devin',27,'0-872-93012-2',2,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:27:14',0),('devin',28,'0-992-32673-5',1,'2015-02-01 00:00:00','2015-02-01 00:00:00','2015-02-15 10:27:19',0),('kelly',29,'0-122-12364-3',1,'2015-04-23 00:00:00','2015-04-23 00:00:00','2015-05-10 00:00:00',0),('kelly',30,'0-123-36956-6',2,'2015-04-23 00:00:00','2015-04-23 00:00:00','2015-05-10 00:00:00',0),('kelly',31,'0-221-15423-8',5,'2015-04-23 00:00:00','2015-04-23 00:00:00','2015-05-10 00:00:00',0),('kelly',32,'0-563-42039-3',3,'2015-04-23 00:00:00','2015-04-23 00:00:00','2015-05-10 00:00:00',0),('kelly',33,'0-724-37125-2',2,'2015-04-23 00:00:00','2015-04-23 00:00:00','2015-05-10 00:00:00',0),('george',34,'0-216-45265-4',1,'2015-04-23 00:00:00','2015-04-23 00:00:00','2015-05-07 10:33:14',0),('george',35,'0-221-15423-8',6,'2015-04-23 00:00:00','2015-04-23 00:00:00','2015-05-07 10:33:16',0),('george',36,'0-872-93012-2',3,'2015-04-23 00:00:00','2015-04-23 00:00:00','2015-05-07 10:33:18',0),('george',37,'0-724-37125-2',3,'2015-04-23 00:00:00','2015-04-23 00:00:00','2015-05-07 10:33:20',0),('george',38,'0-563-42039-3',4,'2015-04-23 00:00:00','2015-04-23 00:00:00','2015-05-07 10:33:21',0);
/*!40000 ALTER TABLE `issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shelf`
--

DROP TABLE IF EXISTS `shelf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shelf` (
  `ShelfNumber` int(2) NOT NULL,
  `FloorNumber` int(2) NOT NULL,
  `AisleNumber` int(2) NOT NULL,
  PRIMARY KEY (`ShelfNumber`),
  KEY `FloorNumber` (`FloorNumber`),
  CONSTRAINT `Shelf_ibfk_1` FOREIGN KEY (`FloorNumber`) REFERENCES `floor` (`FloorNumber`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shelf`
--

LOCK TABLES `shelf` WRITE;
/*!40000 ALTER TABLE `shelf` DISABLE KEYS */;
INSERT INTO `shelf` VALUES (1,1,1),(2,1,2),(3,2,1),(4,2,2),(5,3,1),(6,3,2);
/*!40000 ALTER TABLE `shelf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff` (
  `Username` varchar(25) NOT NULL,
  PRIMARY KEY (`Username`),
  CONSTRAINT `Staff_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `user` (`Username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES ('admin'),('staff');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_faculty`
--

DROP TABLE IF EXISTS `student_faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student_faculty` (
  `Username` varchar(25) NOT NULL,
  `Name` varchar(25) NOT NULL,
  `DOB` datetime NOT NULL,
  `Gender` char(1) NOT NULL,
  `IsDebarred` char(1) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Address` varchar(50) NOT NULL,
  `IsFaculty` char(1) NOT NULL DEFAULT 'N',
  `Penalty` float(10,2) NOT NULL DEFAULT '0.00',
  `Dept` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Username`),
  CONSTRAINT `Student_Faculty_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `user` (`Username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_faculty`
--

LOCK TABLES `student_faculty` WRITE;
/*!40000 ALTER TABLE `student_faculty` DISABLE KEYS */;
INSERT INTO `student_faculty` VALUES ('allen','Allen Chen','1995-03-10 00:00:00','M','1','allenchen@gmail.com','North Ave 192','0',124.00,'NULL'),('bob','Bob Waters','1952-05-20 00:00:00','M','0','bob.waters91029@gmail.com','Klaus 1213','1',0.00,'CS'),('burdell','George P. Burdell','1940-02-05 00:00:00','M','1','georgepburdell@gmail.com','Ol Georgia Tech 420','0',420.00,'NULL'),('denise','Denise Quan','1994-09-03 00:00:00','F','0','denisequan@gmail.com','Folk Residence Hall','0',47.00,'NULL'),('devin','Devin Gao','1997-04-05 00:00:00','M','0','devingao@gmail.com','Glenn Residence Hall','0',0.00,'NULL'),('donna','Donna Eric','1996-12-04 00:00:00','F','0','donnaeric@gmail.com','Towers Residence Hall','0',0.00,'NULL'),('eric','Eric Leahy','1964-09-03 00:00:00','M','0','ericleahy@gmail.com','Klaus 2443','1',0.00,'CS'),('george','George Smith','1994-06-24 00:00:00','M','0','georgesmith@gmail.com','Georgia Town','0',0.00,'NULL'),('hana','Hana Li','1995-06-22 00:00:00','F','0','hanali@gmail.com','555 8th St Nw','0',0.00,'NULL'),('huggy','Huggy Chan','1996-03-02 00:00:00','M','0','huggychan@gmail.com','Montag Residence Hall','0',0.00,'NULL'),('jacka','Jack Gao','1994-03-18 00:00:00','M','0','jackgao@gmail.com','8th Street West','0',0.00,'NULL'),('ji','Ji Moon','1994-01-20 00:00:00','M','0','jimoon@gmail.com','8th Street South','0',47.00,'NULL'),('karen','Karen Liu','1980-09-03 00:00:00','F','0','karenliu@gmail.com','Klaus 2042','1',0.00,'PHYS'),('kelly','Kelly In','1994-05-24 00:00:00','F','0','kellyin@gmail.com','Crecine Apartments','0',0.00,'NULL'),('kevin','Kevin Xu','1994-03-10 00:00:00','M','0','kevinxu@gmail.com','555 8th St NW','0',40.00,'NULL'),('mark','Mark Cho','1994-04-20 00:00:00','M','0','markcho@gmail.com','Center Street Apartments','0',0.00,'NULL'),('meimei','Elizabeth Sun','1994-06-14 00:00:00','F','0','elizabethsun@gmail.com','Homepark','0',0.00,'NULL'),('morley','Morley Morley','1952-09-03 00:00:00','M','0','morley@gmail.com','Math Town','1',33.50,'MATH'),('pedro','Pedro Rangelf','1985-09-03 00:00:00','M','0','pedro@gmail.com','Combo 95','1',0.00,'RUSS'),('rsun39','Robert Sun','1994-10-03 00:00:00','M','1','sunwrobert@gmail.com','555 8th St NW','0',47.00,'NULL'),('shauna','Shauna Nime','1994-06-14 00:00:00','F','0','shaunanime@gmail.com','Shokugan No 5','0',47.00,'NULL');
/*!40000 ALTER TABLE `student_faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subject` (
  `Name` varchar(50) NOT NULL,
  `FloorNumber` int(1) NOT NULL,
  `NumJournals` int(10) DEFAULT NULL,
  PRIMARY KEY (`Name`),
  KEY `FloorNumber` (`FloorNumber`),
  CONSTRAINT `Subject_ibfk_1` FOREIGN KEY (`FloorNumber`) REFERENCES `floor` (`FloorNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES ('Economics',2,10),('Fiction',3,2),('History',2,4),('Math',1,5),('Nonfiction',3,5),('Science',1,3);
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject_keywords`
--

DROP TABLE IF EXISTS `subject_keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subject_keywords` (
  `Name` varchar(50) NOT NULL,
  `Keyword` varchar(50) NOT NULL,
  PRIMARY KEY (`Name`,`Keyword`),
  CONSTRAINT `Subject_keywords_ibfk_1` FOREIGN KEY (`Name`) REFERENCES `subject` (`Name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject_keywords`
--

LOCK TABLES `subject_keywords` WRITE;
/*!40000 ALTER TABLE `subject_keywords` DISABLE KEYS */;
INSERT INTO `subject_keywords` VALUES ('Economics','Market'),('Economics','Supply and Demand'),('Fiction','Anime'),('Fiction','Fairy tales'),('Fiction','Fantasy'),('History','China'),('History','Europe'),('History','USA'),('Math','Algebra'),('Math','Calculus'),('Math','Trigonometry'),('Nonfiction','Autobiography'),('Nonfiction','Biography'),('Nonfiction','Research'),('Science','Biology'),('Science','Chemistry'),('Science','Physics');
/*!40000 ALTER TABLE `subject_keywords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `Username` varchar(25) NOT NULL,
  `Password` varchar(25) NOT NULL,
  PRIMARY KEY (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('admin','admin'),('allen','abc'),('bob','abc'),('burdell','abc'),('denise','abc'),('devin','abc'),('donna','abc'),('eric','abc'),('george','abc'),('hana','abc'),('huggy','abc'),('jacka','abc'),('ji','abc'),('karen','abc'),('kelly','abc'),('kevin','abc'),('mark','abc'),('meimei','abc'),('morley','abc'),('pedro','abc'),('rsun39','abc'),('shauna','abc'),('staff','staff');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-04-23 10:35:55
