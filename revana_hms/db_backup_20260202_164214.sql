-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: reevanahms
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.24.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_doctorprofile`
--

DROP TABLE IF EXISTS `accounts_doctorprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_doctorprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `gender` varchar(10) NOT NULL,
  `date_of_birth` date NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `medical_certificate` varchar(100) NOT NULL,
  `qualification` varchar(255) NOT NULL,
  `specialization` varchar(255) NOT NULL,
  `year_of_experience` int NOT NULL,
  `registration_certificate` varchar(100) NOT NULL,
  `degree_certificates` varchar(100) NOT NULL,
  `aadhaar` varchar(20) NOT NULL,
  `passport_photo` varchar(100) NOT NULL,
  `experience_certificate` varchar(100) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_doctorprofile_user_id_c6e100bb_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_doctorprofile`
--

LOCK TABLES `accounts_doctorprofile` WRITE;
/*!40000 ALTER TABLE `accounts_doctorprofile` DISABLE KEYS */;
INSERT INTO `accounts_doctorprofile` VALUES (18,'Male','2026-01-07','','','','','Orthopedics',0,'','','','','',85),(19,'Female','2026-01-07','+919879647227','625 Arno Wells','','','Neurology',0,'','','','','',83),(70,'Female','1985-01-01','1389480866','H.No. 17\nGandhi Street, Adoni 373850','doctors/275/certificates/med_cert.pdf','MBBS, MD','Neurology',20,'doctors/275/certificates/reg_cert.pdf','doctors/275/certificates/deg_cert.pdf','431885997947','doctors/275/photos/photo.jpg','',275),(71,'Female','1985-01-01','02528973669','28/22, Jain Path\nVasai-Virar-247267','doctors/276/certificates/med_cert.pdf','MBBS, MD','Neurology',8,'doctors/276/certificates/reg_cert.pdf','doctors/276/certificates/deg_cert.pdf','928324772476','doctors/276/photos/photo.jpg','',276),(72,'Male','1985-01-01','+910678676979','47\nBhavsar Path\nKurnool 641222','doctors/277/certificates/med_cert.pdf','MBBS, MD','Cardiology',6,'doctors/277/certificates/reg_cert.pdf','doctors/277/certificates/deg_cert.pdf','664312798633','doctors/277/photos/photo.jpg','',277),(73,'Male','1985-01-01','+917730149607','834, Raju Street, Udaipur 618447','doctors/278/certificates/med_cert.pdf','MBBS, MD','Orthopedics',12,'doctors/278/certificates/reg_cert.pdf','doctors/278/certificates/deg_cert.pdf','534143238648','doctors/278/photos/photo.jpg','',278),(74,'Male','1985-01-01','4744489914','H.No. 55, Devi Path, Secunderabad-790820','doctors/279/certificates/med_cert.pdf','MBBS, MD','Cardiology',12,'doctors/279/certificates/reg_cert.pdf','doctors/279/certificates/deg_cert.pdf','584139190832','doctors/279/photos/photo.jpg','',279),(75,'Male','1985-01-01','+913668412112','H.No. 594\nPeri Circle\nKishanganj 997318','doctors/280/certificates/med_cert.pdf','MBBS, MD','Oncology',19,'doctors/280/certificates/reg_cert.pdf','doctors/280/certificates/deg_cert.pdf','385470280319','doctors/280/photos/photo.jpg','',280),(76,'Female','1985-01-01','09154268507','459, Varkey Zila\nVadodara-444603','doctors/281/certificates/med_cert.pdf','MBBS, MD','Orthopedics',9,'doctors/281/certificates/reg_cert.pdf','doctors/281/certificates/deg_cert.pdf','958331321785','doctors/281/photos/photo.jpg','',281),(77,'Female','1985-01-01','7212542497','H.No. 981, Mall Chowk, Ozhukarai 234771','doctors/282/certificates/med_cert.pdf','MBBS, MD','Pediatrics',12,'doctors/282/certificates/reg_cert.pdf','doctors/282/certificates/deg_cert.pdf','452475554096','doctors/282/photos/photo.jpg','',282),(78,'Male','1985-01-01','4765199338','827, Basak Ganj, Deoghar 291185','doctors/283/certificates/med_cert.pdf','MBBS, MD','Oncology',10,'doctors/283/certificates/reg_cert.pdf','doctors/283/certificates/deg_cert.pdf','753498855851','doctors/283/photos/photo.jpg','',283),(79,'Male','1985-01-01','05461117160','H.No. 10\nDugal\nBhiwani-012152','doctors/284/certificates/med_cert.pdf','MBBS, MD','Dermatology',10,'doctors/284/certificates/reg_cert.pdf','doctors/284/certificates/deg_cert.pdf','213192702453','doctors/284/photos/photo.jpg','',284),(80,'Male','1985-01-01','09493758409','75, Nagar Nagar\nHowrah-522538','doctors/285/certificates/med_cert.pdf','MBBS, MD','Cardiology',17,'doctors/285/certificates/reg_cert.pdf','doctors/285/certificates/deg_cert.pdf','241841310568','doctors/285/photos/photo.jpg','',285),(81,'Male','1985-01-01','09309053894','H.No. 666\nBhasin Marg, Tadipatri 107120','doctors/286/certificates/med_cert.pdf','MBBS, MD','Neurology',5,'doctors/286/certificates/reg_cert.pdf','doctors/286/certificates/deg_cert.pdf','537305967912','doctors/286/photos/photo.jpg','',286),(82,'Female','1985-01-01','01772864694','H.No. 09\nMallick Road\nBihar Sharif 078386','doctors/287/certificates/med_cert.pdf','MBBS, MD','Cardiology',11,'doctors/287/certificates/reg_cert.pdf','doctors/287/certificates/deg_cert.pdf','510073767517','doctors/287/photos/photo.jpg','',287),(83,'Female','1985-01-01','+919717750563','30/261, Walla Chowk, Naihati 689126','doctors/288/certificates/med_cert.pdf','MBBS, MD','Orthopedics',16,'doctors/288/certificates/reg_cert.pdf','doctors/288/certificates/deg_cert.pdf','230213197497','doctors/288/photos/photo.jpg','',288),(84,'Male','1985-01-01','2368163322','H.No. 381\nLoyal Zila\nAnantapuram-611077','doctors/289/certificates/med_cert.pdf','MBBS, MD','Dermatology',12,'doctors/289/certificates/reg_cert.pdf','doctors/289/certificates/deg_cert.pdf','719010325707','doctors/289/photos/photo.jpg','',289),(85,'Female','1985-01-01','+910917519146','201\nNaik Road\nPimpri-Chinchwad 261585','doctors/290/certificates/med_cert.pdf','MBBS, MD','Pediatrics',7,'doctors/290/certificates/reg_cert.pdf','doctors/290/certificates/deg_cert.pdf','929830289682','doctors/290/photos/photo.jpg','',290),(86,'Female','1985-01-01','05601313698','H.No. 214\nMannan Circle\nMeerut 754326','doctors/291/certificates/med_cert.pdf','MBBS, MD','Cardiology',9,'doctors/291/certificates/reg_cert.pdf','doctors/291/certificates/deg_cert.pdf','868354716300','doctors/291/photos/photo.jpg','',291),(87,'Male','1985-01-01','1937141338','H.No. 42, Lal Street\nAjmer-599056','doctors/292/certificates/med_cert.pdf','MBBS, MD','Oncology',12,'doctors/292/certificates/reg_cert.pdf','doctors/292/certificates/deg_cert.pdf','574996269944','doctors/292/photos/photo.jpg','',292),(88,'Female','1985-01-01','+914338367955','H.No. 21, Borra Zila, Rewa-435630','doctors/293/certificates/med_cert.pdf','MBBS, MD','Orthopedics',14,'doctors/293/certificates/reg_cert.pdf','doctors/293/certificates/deg_cert.pdf','364188176549','doctors/293/photos/photo.jpg','',293),(89,'Male','1985-01-01','+910570091716','35/71\nVarghese Nagar, Raiganj-256045','doctors/294/certificates/med_cert.pdf','MBBS, MD','Neurology',9,'doctors/294/certificates/reg_cert.pdf','doctors/294/certificates/deg_cert.pdf','349152890860','doctors/294/photos/photo.jpg','',294),(90,'Female','1985-01-01','5505280055','76, Hari Nagar, Alwar 795732','doctors/295/certificates/med_cert.pdf','MBBS, MD','Oncology',11,'doctors/295/certificates/reg_cert.pdf','doctors/295/certificates/deg_cert.pdf','473373125664','doctors/295/photos/photo.jpg','',295),(91,'Female','1985-01-01','6342474047','44/41\nTalwar Street\nKota 184983','doctors/296/certificates/med_cert.pdf','MBBS, MD','Dermatology',8,'doctors/296/certificates/reg_cert.pdf','doctors/296/certificates/deg_cert.pdf','517836347024','doctors/296/photos/photo.jpg','',296),(92,'Male','1985-01-01','5470001930','936\nKadakia Circle, Pali-839339','doctors/297/certificates/med_cert.pdf','MBBS, MD','Neurology',6,'doctors/297/certificates/reg_cert.pdf','doctors/297/certificates/deg_cert.pdf','339986146530','doctors/297/photos/photo.jpg','',297),(93,'Female','1985-01-01','1472352524','12, Varty Road\nGopalpur 240913','doctors/298/certificates/med_cert.pdf','MBBS, MD','Pediatrics',7,'doctors/298/certificates/reg_cert.pdf','doctors/298/certificates/deg_cert.pdf','447571474736','doctors/298/photos/photo.jpg','',298),(94,'Male','1985-01-01','09709303697','90/01, Ravi Circle\nBidhannagar-221299','doctors/299/certificates/med_cert.pdf','MBBS, MD','Orthopedics',20,'doctors/299/certificates/reg_cert.pdf','doctors/299/certificates/deg_cert.pdf','443790262960','doctors/299/photos/photo.jpg','',299),(95,'Male','1985-01-01','8404498062','H.No. 62, Baria Zila\nGwalior 132137','doctors/300/certificates/med_cert.pdf','MBBS, MD','Cardiology',13,'doctors/300/certificates/reg_cert.pdf','doctors/300/certificates/deg_cert.pdf','974467380248','doctors/300/photos/photo.jpg','',300),(96,'Female','1985-01-01','7070136084','H.No. 82\nJayaraman Road, Unnao-464770','doctors/301/certificates/med_cert.pdf','MBBS, MD','Oncology',15,'doctors/301/certificates/reg_cert.pdf','doctors/301/certificates/deg_cert.pdf','441786014254','doctors/301/photos/photo.jpg','',301),(97,'Female','1985-01-01','+917980330457','34, Mand Street, Parbhani-709291','doctors/302/certificates/med_cert.pdf','MBBS, MD','Cardiology',18,'doctors/302/certificates/reg_cert.pdf','doctors/302/certificates/deg_cert.pdf','902711640356','doctors/302/photos/photo.jpg','',302),(98,'Male','1985-01-01','09825683253','64/176\nDin Nagar, Naihati-567224','doctors/303/certificates/med_cert.pdf','MBBS, MD','Orthopedics',9,'doctors/303/certificates/reg_cert.pdf','doctors/303/certificates/deg_cert.pdf','718622361373','doctors/303/photos/photo.jpg','',303),(99,'Male','1985-01-01','09655410426','10/08, Mander Zila, Chennai 778698','doctors/304/certificates/med_cert.pdf','MBBS, MD','Neurology',6,'doctors/304/certificates/reg_cert.pdf','doctors/304/certificates/deg_cert.pdf','856291500994','doctors/304/photos/photo.jpg','',304),(100,'Male','1985-01-01','08442998577','47/35\nBains Nagar\nJunagadh 658508','doctors/305/certificates/med_cert.pdf','MBBS, MD','Neurology',14,'doctors/305/certificates/reg_cert.pdf','doctors/305/certificates/deg_cert.pdf','997286786964','doctors/305/photos/photo.jpg','',305),(101,'Male','1985-01-01','03254850048','98, Muni\nNaihati 266186','doctors/306/certificates/med_cert.pdf','MBBS, MD','Pediatrics',15,'doctors/306/certificates/reg_cert.pdf','doctors/306/certificates/deg_cert.pdf','512192553455','doctors/306/photos/photo.jpg','',306),(102,'Female','1985-01-01','02273971499','06/57\nMukhopadhyay Path, Etawah 023767','doctors/307/certificates/med_cert.pdf','MBBS, MD','Dermatology',9,'doctors/307/certificates/reg_cert.pdf','doctors/307/certificates/deg_cert.pdf','783913133410','doctors/307/photos/photo.jpg','',307);
/*!40000 ALTER TABLE `accounts_doctorprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_hospitaladminprofile`
--

DROP TABLE IF EXISTS `accounts_hospitaladminprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_hospitaladminprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `hospital_type` varchar(100) NOT NULL,
  `hours` varchar(100) NOT NULL,
  `doctor_id` varchar(100) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_hospitaladm_user_id_4cffa820_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_hospitaladminprofile`
--

LOCK TABLES `accounts_hospitaladminprofile` WRITE;
/*!40000 ALTER TABLE `accounts_hospitaladminprofile` DISABLE KEYS */;
INSERT INTO `accounts_hospitaladminprofile` VALUES (21,'Surat Admin','8985446352','79/27\nBhargava\nSonipat-115721','General','09:00 - 18:00','ADMIN-8096',261),(22,'Ahmedabad Admin','0491630719','696\nWable Zila\nKharagpur 248590','General','09:00 - 18:00','ADMIN-2102',262),(23,'Vadodara Admin','+917501054222','H.No. 03\nBuch Zila\nFarrukhabad 129801','General','09:00 - 18:00','ADMIN-1133',263),(24,'Rajkot Admin','1863221477','92, Roy Zila\nTirupati-550554','General','09:00 - 18:00','ADMIN-9069',264),(25,'Gandhinagar Admin','1390522599','25, Doctor Circle\nPali 497158','General','09:00 - 18:00','ADMIN-2055',265),(26,'Admin delaru hospital','4450968095','01\nGoda Circle\nBilaspur-831127','General','09:00 - 18:00','ADMIN-3623',266),(27,'Admin Seshadri Hospital Surat','06868497059','469, Borde Nagar\nDehri 294706','General','09:00 - 18:00','ADMIN-4418',267),(28,'Admin Date Hospital Surat','3971112903','H.No. 83, Nath Path\nDhanbad 309364','General','09:00 - 18:00','ADMIN-5303',268),(29,'Admin Shroff Hospital Ahmedabad','+917996570655','H.No. 53\nHanda Zila, Bihar Sharif 338652','General','09:00 - 18:00','ADMIN-2446',269),(30,'Admin Singh Hospital Ahmedabad','0091851386','H.No. 34, Kata Zila, Bongaigaon 063710','General','09:00 - 18:00','ADMIN-1407',270),(31,'Admin Madan Hospital Vadodara','02302828698','84/132, Mander Nagar\nHowrah-291673','General','09:00 - 18:00','ADMIN-3361',271),(32,'Admin Khare Hospital Vadodara','04070605186','81/48\nChander Nagar\nMango 713327','General','09:00 - 18:00','ADMIN-3852',272),(33,'Admin Kashyap Hospital Gandhinagar','00417991346','917\nBarad Path, Davanagere 426161','General','09:00 - 18:00','ADMIN-8624',273),(34,'Admin Jaggi Hospital Rajkot','+911670156971','09\nKapadia Nagar\nKharagpur-691840','General','09:00 - 18:00','ADMIN-4486',274);
/*!40000 ALTER TABLE `accounts_hospitaladminprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `role` varchar(50) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_email_b2644a56_uniq` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=368 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (40,'pbkdf2_sha256$1000000$sBuJjrSS0YlOwpZZYBiPJl$wI6Ot+c/z2HA++gL3KJx011bKwqog5nGCxVro9kiwXQ=','2026-01-30 10:45:53.483614',1,'blueglobalcloud@gmail.com',1,1,'',NULL,'2025-11-27 10:32:28.777677'),(81,'pbkdf2_sha256$1000000$SirV4VESpeCSSPLMRM0gt4$n4K3OUalOQSFjLOaiFEwXNaNZkuBMl8y5RYTG+5GxII=','2025-12-16 13:59:26.739444',0,'bhavanbadhe@gmail.com',0,1,'hospital_admin','09879647227','2025-12-16 11:01:01.177671'),(83,'pbkdf2_sha256$1000000$BOMC85JIdlwOE1yvdnmUkO$pedS3creetMChVjy4bxWUjVvhYsOusiT3nLlxUVR648=','2026-01-29 12:52:18.848520',0,'doctor1@test.com',0,1,'doctor','+919879647227','2025-12-17 08:41:15.586973'),(84,'pbkdf2_sha256$1000000$cHfqigUD6f7LXNeoZTuUBa$ksiui+hpurofXozmJr7YzOCOrQa+hmrTmEc11IgAmtw=','2026-01-17 05:41:22.832249',0,'doctor2@test.com',0,1,'doctor','1234567890','2025-12-17 08:41:16.143946'),(85,'pbkdf2_sha256$1000000$13dQR1kLnrlcAWd0ARM3XD$KBkVsOCx96+dy/WdoHv9xAj42AGZxY2yTxkXuQ8l8oY=','2026-01-07 05:15:51.286154',0,'doctor3@test.com',0,1,'doctor','1234567890','2025-12-17 08:41:16.678047'),(86,'pbkdf2_sha256$1000000$R5qGmd9utC9l9h6aipiDTl$CKkYmwXDUQJAnFno1QdbdwIQCjjFYACEdP8+nARmS20=',NULL,0,'doctor4@test.com',0,1,'doctor','1234567890','2025-12-17 08:41:17.205571'),(87,'pbkdf2_sha256$1000000$CM6ae7BTNClIh97edDEJEQ$8sAQeKKhRDrHAaiEvrimlkzBqvYu2mFuDDfXvTR7BH0=','2025-12-19 05:34:23.365716',0,'doctor5@test.com',0,1,'doctor','1234567890','2025-12-17 08:41:17.779568'),(88,'pbkdf2_sha256$1000000$1s37ho3f9ZEwGOSaHVydt7$f1ToUXa7IwR+qZHUTPDWyF3bsn73doPpD6OXLDt0YhE=','2026-01-07 05:11:05.319551',0,'doctor6@test.com',0,1,'doctor','1234567890','2025-12-17 08:41:18.320423'),(89,'pbkdf2_sha256$1000000$zIOEZqsYWgnWq1K1ayCPho$kdDkYAjBwfj2MxGuNRHe8Dhnoff7lXneZgec+e++66U=','2026-01-09 08:18:48.621329',0,'admin_vadodara@cityhospital.com',0,1,'hospital_admin','9876543210','2025-12-19 05:09:27.497040'),(90,'pbkdf2_sha256$1000000$j2EMEp4D5kDTJTWkl4CxYH$O8jzm7stWqGjwoAIDmTq5L6LkhcM+49nWtDC+IzApbc=',NULL,0,'admin_surat@cityhospital.com',0,1,'hospital_admin','9876543210','2025-12-19 05:09:28.132930'),(91,'pbkdf2_sha256$1000000$c20nd4ql6YYNAsnpKiOAzs$8Ns9WH/1bpN7iVk85CS0KGm1OrlimzTOTyg9qYNsfOE=',NULL,0,'admin_ahmedabad@cityhospital.com',0,1,'hospital_admin','9876543210','2025-12-19 05:09:28.744882'),(92,'!wJqTfYZYGttriXURBqQqgu86iqdIlWzOD3NOzHjx',NULL,0,'testexample856@gmail.com',0,1,'patient',NULL,'2026-01-07 06:08:34.983588'),(93,'!eIfDZpQdv2mf0MJPzLMcEEZUTta9p6t8pFOcEdP0',NULL,0,'te@vardaam.email',0,1,'patient',NULL,'2026-01-09 07:22:07.331931'),(94,'!qd74hLA0vZjORKUUmV9BfYsdfNFfiZPJYecbJUIY',NULL,0,'test1@gmail.com',0,1,'patient',NULL,'2026-01-12 04:43:01.245736'),(95,'!EuGG1Z0oVbNZ2oGg2ccC69GqrjxNblyTS3IAoA8F',NULL,0,'test2@gmail.com',0,1,'patient',NULL,'2026-01-12 04:46:42.432646'),(96,'!lOp1Yl4vc6OpOLNPr6ln6oJgEylzYlegcSmH2UH3',NULL,0,'test3@gmail.com',0,1,'patient',NULL,'2026-01-12 04:47:32.607988'),(97,'!BzlHSuLDFkOcjR8YkUOnPzcyXbmXrcun1RWT2KLB',NULL,0,'test4@gmail.com',0,1,'patient',NULL,'2026-01-12 04:48:25.463233'),(98,'!saO9WDE2C8DURxM5YucakcxMy3CFXAXydMvTVGUp',NULL,0,'test5@gmail.com',0,1,'patient',NULL,'2026-01-12 04:49:06.204069'),(99,'pbkdf2_sha256$1000000$XfxepmVpoq96BrJiI9AgcM$i+uckM1n+WHPLyHsIVnHV3WTYJsXs7XPO4Pk7XW/7UI=',NULL,0,'khushipathak2003@gmail.com',0,1,'patient',NULL,'2026-01-12 11:19:24.408850'),(100,'pbkdf2_sha256$1000000$XOGdRHHiKdDud8sgyldtXC$gIU90JF4BXzR20aQsC1wirOcqoucw1WbH2W7DEHRrJA=',NULL,0,'test1example856@gmail.com',0,1,'patient',NULL,'2026-01-13 08:56:10.948152'),(101,'pbkdf2_sha256$1000000$5lyfA5hvGBVhmL1A9p4yyJ$6lIs4Rg//AOx0d++d0078d5m5Njr6Ts1JbIyTKJnHyg=',NULL,0,'bgtemployer@gmail.com',0,1,'patient',NULL,'2026-01-13 09:12:31.772429'),(102,'pbkdf2_sha256$1000000$i6Aro3VCg4SVi9jb17VJLk$RJrvXIAGfDbDfZb+wUSyg64Wqa+2SW+GSgOSzWjNh/w=',NULL,0,'khushi2803@gmail.com',0,1,'patient',NULL,'2026-01-13 11:53:08.842826'),(103,'pbkdf2_sha256$1000000$t1od8BJJl4U4LCwpW2m8P2$v2YDhzSeNQ/MlClrJhGylax0ZTjS1O/mxlacux3u81A=',NULL,0,'bhavan2003@gmail.com',0,1,'patient',NULL,'2026-01-13 12:32:01.604683'),(104,'pbkdf2_sha256$1000000$8s4L6oLl27aoMzXHGXlMPg$9HZN9ZEvaVoBHIuX7rSM0wCB28MFpFjRZFI2qbIxtsg=',NULL,0,'khushpathak2003@gmail.com',0,1,'patient',NULL,'2026-01-13 12:38:12.706519'),(105,'pbkdf2_sha256$1000000$zf89Hd9gk2O5MUhOPD6APS$D6w0Aybum15DwXyETvPetKLAKih1WNLOV72Dn4zDVqM=',NULL,0,'khushipathak12@gmail.com',0,1,'patient',NULL,'2026-01-16 07:20:54.171433'),(106,'',NULL,0,'doc_search@example.com',0,1,'doctor',NULL,'2026-01-16 07:27:26.402256'),(107,'pbkdf2_sha256$1000000$w7iuRVSWfBA5KFYlgMQYk4$l2Xb4cIeZdl+iLnEQ8mJM+ZEaeV/p103sXcOKICHNo4=',NULL,0,'khushi2003@gmail.com',0,1,'patient',NULL,'2026-01-16 09:32:03.570426'),(108,'pbkdf2_sha256$1000000$rmN1zchcq8jYgsw7p7ryoX$XgYMuuUpiVZaQ/RfJ6OS3EhlWzJcZjE5ZVBQrJkUxlY=',NULL,0,'bhavan12@gmail.com',0,1,'patient',NULL,'2026-01-16 10:30:14.437441'),(109,'pbkdf2_sha256$1000000$ldyMVgPgaif077KHVUWf4V$No72H4SY9xdyk7M7SOq8oX08coHxtTQMUCxTNYPuSi8=',NULL,0,'khush@gmail.com',0,1,'patient',NULL,'2026-01-17 07:14:28.731651'),(110,'pbkdf2_sha256$1000000$esx4OatNvb2zE0Li5qAv2V$nFg4id4XZ5Vj1pZDjqKJ1qb1guTKzIPFuXdKwNqTlTo=',NULL,0,'api_tester@example.com',0,1,'patient',NULL,'2026-01-29 12:36:16.012978'),(261,'pbkdf2_sha256$1000000$HpENtKEgj7WaMKh3zmEeDh$5mZpe6BQ2KaBWDZEmg5c/xGmczptqeDryax+7XGiooU=',NULL,0,'admin_surat@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:10:24.411928'),(262,'pbkdf2_sha256$1000000$Vv9B0CdU0y44oNRiWnwNWG$gfUOvn/Bp5hs3o/cGETeZ2QAt/YoKLIu1NIXCF6s+b4=',NULL,0,'admin_amd@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:10:25.090250'),(263,'pbkdf2_sha256$1000000$EDrm9Vt0Q7kEfj4wIl2bUf$X+szeIEuyd9cke+LlcKepQFZOnM2GwyXZpTKoUIwH5g=',NULL,0,'admin_vad@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:10:25.717692'),(264,'pbkdf2_sha256$1000000$wblxdvanYZuCAfhVOgzf3x$fx3JeXQeenzbEnONhdxCvoqGRn4D1y/EP8rLUquJHOI=',NULL,0,'admin_raj@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:10:26.471548'),(265,'pbkdf2_sha256$1000000$lwttaQRURHopnEX7qQLqnF$tvrgVhjvFjkw7uelaMZZgicsZvGXAcwuUY+tGNAMVmI=',NULL,0,'admin_gandhi@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:10:27.108315'),(266,'pbkdf2_sha256$1000000$iFT2mMzWWzCtQDkmKLnpSb$GMcS7zPCeAUo7AXh7PYpcSJwChFSL9K0MtagAON6eTs=',NULL,0,'admin_delaruhospital_81@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:16:40.811311'),(267,'pbkdf2_sha256$1000000$PoJJ0DsyMFhiXl8HnH53Cq$x7S5csXnTcq/L4IgnwO2nyVP3j/GmPRhYBYKMGKKanc=',NULL,0,'admin_seshadrihospitalsurat_87@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:16:41.433693'),(268,'pbkdf2_sha256$1000000$FG3sD8joHZXtqr8rxt7L4q$UKcdmXXWfFVfta1BbQirqYRXY8yQseUeEBW7p4tdfzM=',NULL,0,'admin_datehospitalsurat_88@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:16:42.105288'),(269,'pbkdf2_sha256$1000000$AwMtIKBfrFTNg2GPZl1wLE$W01ErBlSRwgXicQTGJAP9YkvD+y5ZwPb4wEWzg026sM=',NULL,0,'admin_shroffhospitalahmedabad_90@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:16:42.740895'),(270,'pbkdf2_sha256$1000000$1rwT88hHq4ucSuzcEX1BDP$jdkWPBC6uHdAllbH9kGa6RzIYSUdbUZiSLP5ahk9cG0=',NULL,0,'admin_singhhospitalahmedabad_91@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:16:43.353753'),(271,'pbkdf2_sha256$1000000$3dNnwrZaWAQloN9rT77s0c$PL6UCAyrn0Va0Dh/Byh5gCVW9VnSyJFnJFFuIkBTa0I=',NULL,0,'admin_madanhospitalvadodara_92@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:16:43.974480'),(272,'pbkdf2_sha256$1000000$5hNdKDfcNzUo1E2LuDQdGX$08G5siDyEFB7mN14FX2hTlMzCrRL8hwdW01o1a/zaoM=',NULL,0,'admin_kharehospitalvadodara_93@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:16:44.562065'),(273,'pbkdf2_sha256$1000000$DQW1U4hL7oNzjGeLOHnCWj$KyRqHrp9HofjwevkUN6kHM8ECnaEFDCTziVRrMyNwh8=',NULL,0,'admin_kashyaphospitalgandhinagar_94@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:16:45.187201'),(274,'pbkdf2_sha256$1000000$cpcwh6Pvf4ZosB3cn0U9LR$aX6ZdCVj0DnhIZJRxtPg2Zo0H/dI+CguFUhwDfZnVgo=',NULL,0,'admin_jaggihospitalrajkot_97@rhms.com',0,1,'hospital_admin',NULL,'2026-02-02 10:16:45.804927'),(275,'pbkdf2_sha256$1000000$JtsgNUJs9RT3Hvw1Q4JYel$UhQYn9YwQfN1M7GK+U32V+yfDO8FK68a8x/L5B9cy7w=',NULL,0,'dr_neuro_cityh_56@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:20.834625'),(276,'pbkdf2_sha256$1000000$03U9UwwDl904YrQVrX7D0o$B1lSzKKs+LNze3xX8y3y8x7CWaXKJLt8YqCSx+Buwuo=',NULL,0,'dr_neuro_cityh_84@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:21.592656'),(277,'pbkdf2_sha256$1000000$ma8D9M9g0OpAKd4gaHsKxd$lMhFZcAGM3gIlEP/MESuEms9BAooZ7C/u9LPFsSKajY=',NULL,0,'dr_cardi_cityh_48@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:22.193013'),(278,'pbkdf2_sha256$1000000$FRJrtpHkpe3sy9Z3dZjUA7$7eXBWxXGaLOdXn3g68REY2sOl322qObyDLC6jp7dEwc=',NULL,0,'dr_ortho_dateh_77@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:22.797083'),(279,'pbkdf2_sha256$1000000$ZYGarXxeCuLjjjeZNtU7W4$Uob/Ffo8HwaYBWSQqGnsDOQgHBMhl0Msd8+6aK8eyQE=',NULL,0,'dr_cardi_dateh_32@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:23.401111'),(280,'pbkdf2_sha256$1000000$qZoFaDs9jAWAPzS1VEvioO$ScXfB+suRH4s18UO1Ruzoh27f8kC/tfTDJOSPO1iycE=',NULL,0,'dr_oncol_dateh_41@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:24.024601'),(281,'pbkdf2_sha256$1000000$wZpjWSUMH78yFk1vS6BdkE$6MIoeHtxuOV8K5sfMM/RoZIGiruYf+bDHO9aC/i2bFc=',NULL,0,'dr_ortho_varug_31@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:24.634802'),(282,'pbkdf2_sha256$1000000$V8cbT3NhNtFQAuXHiICR31$olbrW8xEbaMCKqeRwMWS1olc0kAv5z4f7mz1q+eIqBM=',NULL,0,'dr_pedia_varug_15@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:25.228663'),(283,'pbkdf2_sha256$1000000$bMM721ArptKtN1RXhD9Dzi$o1C/eIRNFMt5t8aoQqETyWtH6WDh1ONwEcpZPr9pI5A=',NULL,0,'dr_oncol_varug_31@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:25.839183'),(284,'pbkdf2_sha256$1000000$Dqygl4sguUvkBFI3QnBggM$MTvzkbrco4pbUnNIeBu45BiaJoDQ7b4D4s9RBnWezxY=',NULL,0,'dr_derma_shrof_24@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:26.429439'),(285,'pbkdf2_sha256$1000000$ZT1fFhtdGoO0vkmgwa0y1G$IZlFawj0IEURaAZnq9fNNinwX4bfTCw1L5YW1IdGA3E=',NULL,0,'dr_cardi_shrof_80@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:27.017630'),(286,'pbkdf2_sha256$1000000$N1HOOEj4iZW7Wnne5wk1Do$vUxPak28H8Zul62ndyXSD9Tzrw+HtgpDQUb/2uYsn6w=',NULL,0,'dr_neuro_shrof_26@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:27.621314'),(287,'pbkdf2_sha256$1000000$5P19e9fez1YL4O8cPHTvid$NT2RYAsrWGuPzTkfVpxeEwaKQbid7xDkU3uoaFHSEDY=',NULL,0,'dr_cardi_singh_40@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:28.249043'),(288,'pbkdf2_sha256$1000000$MMPokaQYWfFeUlhyGpDNjH$0phhWa1ro5J2TEjtj3dRXASMmvMLx2W+qajvUfIfcUw=',NULL,0,'dr_ortho_singh_12@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:28.980646'),(289,'pbkdf2_sha256$1000000$Mi7rdYcfPDH14UIi8012AX$OCCB0gFH9Ca5p3YNILHc+MrGf5H8j5PwKDQTnbZLk/0=',NULL,0,'dr_derma_singh_71@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:29.746003'),(290,'pbkdf2_sha256$1000000$6FwJjSptcIOBcozOUikfOX$o+9lCC+apvCeQigZVFUhC+JxaIOqCp6tC/d+FxSCCUA=',NULL,0,'dr_pedia_madan_74@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:30.359890'),(291,'pbkdf2_sha256$1000000$pxIZJ65TcPL4qqmjGvSNoU$HN3CJAchL4dbVu/4DmLPfGTKb5ku06vC2cr780F3BIs=',NULL,0,'dr_cardi_madan_92@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:30.958024'),(292,'pbkdf2_sha256$1000000$ABncRs9rncV3BWIFxTjUK8$fmMzTZjFMBEf96947Nue7mbHTzjSFHYR4RU22N1Y9EQ=',NULL,0,'dr_oncol_madan_21@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:31.562542'),(293,'pbkdf2_sha256$1000000$DZPheycKvNpYgXeps9B1Lv$+NF2ntCdedyt4v2pYDiq12ZJlx6oDQ6NrH1cPwNeSV8=',NULL,0,'dr_ortho_khare_22@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:32.162771'),(294,'pbkdf2_sha256$1000000$6WVVlWav1J9wUnmNQMj0g6$0dCdWBWsiDAWvabxpeXL/P6EBt3dOB+qY0MobcmiEng=',NULL,0,'dr_neuro_khare_72@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:32.767666'),(295,'pbkdf2_sha256$1000000$p3HL46wexY4Hq2kJCs9KTz$r0HNXK266fkBgZBsyUlduzwJaAD77822OG9FxvS4pEY=',NULL,0,'dr_oncol_khare_52@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:33.340224'),(296,'pbkdf2_sha256$1000000$5aLV7nDMNbplZGrjsoe6Qq$sh9HpamLj8Qnu5OZs/b8ioPEddaJGYPExCb/KXIGGbs=',NULL,0,'dr_derma_kashy_84@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:33.936358'),(297,'pbkdf2_sha256$1000000$ttQWH3x3ZMd9uMAJ4YDrdu$QP9Fz7SxPZx9S/tICmxDH8hQIIWfmaJX9KZaaqLoaO0=',NULL,0,'dr_neuro_kashy_57@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:34.591606'),(298,'pbkdf2_sha256$1000000$cSJJQ52bHkZlzCuCTxnU7Q$42eqyEFd+rrxaTIPmnUigI2NeGdXTdXxpEC6aCQTSGs=',NULL,0,'dr_pedia_kashy_87@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:35.270284'),(299,'pbkdf2_sha256$1000000$w1CVHBUV8bCn6RPyRWYMaa$YamLqC/2iUhtnZRRTzxX0BMA5i9SZ73TuOCsGhk2QMA=',NULL,0,'dr_ortho_kashy_79@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:35.893919'),(300,'pbkdf2_sha256$1000000$DCfVL9klX2ECOQyBF8I6zi$t1exIbd9JqMijJDnxJAznKQN0OwKfRsfq4WWUx3FXmM=',NULL,0,'dr_cardi_kashy_97@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:36.499936'),(301,'pbkdf2_sha256$1000000$epovbNhMMupWMWkolmG9OI$Kn+wjrSqukXxmf2t132t3fdYTdeSn9cJdXL9ALyIROA=',NULL,0,'dr_oncol_kashy_10@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:37.118601'),(302,'pbkdf2_sha256$1000000$Wqesqs61I5BS9Jhpqmm72V$McfBkuLlSP/4ulLwPKh+aqEJ32y2/0pJbMJpH5YH7fU=',NULL,0,'dr_cardi_narai_98@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:37.722259'),(303,'pbkdf2_sha256$1000000$pmqCgrFq4UOyowVaZQMkRP$TdMxvpYQHwrVD5aW8b4FPFqWsfjpTLHtKL0rpgmRI14=',NULL,0,'dr_ortho_narai_52@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:38.369937'),(304,'pbkdf2_sha256$1000000$duH3MsIbR6umXl4u6pms1O$FNFrDbvVzcerQLFvRIYYf5J/h3lPlDwgykSH68tTrc8=',NULL,0,'dr_neuro_narai_76@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:39.021783'),(305,'pbkdf2_sha256$1000000$RspDltIH9PgwLYjBotUa7H$p/vygOwhjCjoVXvjPWcWjmQECSTz4TDXQ5xBdhcsyDU=',NULL,0,'dr_neuro_jaggi_52@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:39.638541'),(306,'pbkdf2_sha256$1000000$5hS6BxxWzCNcvccH37nvje$XXvmAnDRvpEtK+8UeWs2RtD3/QNZG0BjZzdPWpMya2w=',NULL,0,'dr_pedia_jaggi_65@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:40.287641'),(307,'pbkdf2_sha256$1000000$gfXbMLBzH99ZG9D6k1wqwH$/OMJrfZpj2nmEkpLXh2zfEINWQ8wXCboGccsTqe+Nec=',NULL,0,'dr_derma_jaggi_96@rhms.com',0,1,'doctor',NULL,'2026-02-02 10:23:40.941376'),(308,'pbkdf2_sha256$1000000$xn13Yq3pLaQxTkCM5A2R8p$8KVPZvSn9BMPWiq0HG07ic77HLspTv3DeajDxFmgWWs=',NULL,0,'patient_rudratara_8302@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:19.438756'),(309,'pbkdf2_sha256$1000000$VXh7vvD0wTyOH5sHSrDLtH$bqqMQ8Y1qx9lpVdbc2bKwBpE6Ms0qpiVfHNwLwAmzQI=',NULL,0,'patient_maanassandal_8512@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:20.015298'),(310,'pbkdf2_sha256$1000000$paLmh968F7slBEbJTi84KT$7J5eMJoTxaHPBmsich1Vnfkb3WOzM3A5aV5OuE0txs0=',NULL,0,'patient_nitarajoshi_6519@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:20.660441'),(311,'pbkdf2_sha256$1000000$HilzLTDN2QeGWtVrDUo1HM$WuMximNmpeHeeh0nL2YdkSSG1K4bQ2HXjW1aSZaAQas=',NULL,0,'patient_gaurangipant_1370@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:21.203109'),(312,'pbkdf2_sha256$1000000$fd1GrxRwXdZfYx0mwnjIgR$T1zOys4wA7GFCvudspRn4GUi/vA4SqYjoUHGiswBtw0=',NULL,0,'patient_ijayasinghal_5958@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:21.741406'),(313,'pbkdf2_sha256$1000000$EB1fAQjatB1i7jxuBAJUvy$0nLw29/XoxAtDLhdDPcQgjcVO3nRasS7f4BWzxKG4sg=',NULL,0,'patient_libniaurora_9106@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:22.283918'),(314,'pbkdf2_sha256$1000000$r2gwCYZdCiweAUv3CWQfhP$QkU4yjSIiLNmtfCP7AsxzSIIivhxEDub2N3XUQzHplE=',NULL,0,'patient_haritamani_5686@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:22.844942'),(315,'pbkdf2_sha256$1000000$N4EfpoEJkOCEURQkNdSt3Z$B9QzaeQai+yC2LixTMSn462feGefHo5aKT5k7/tvHj8=',NULL,0,'patient_lavanyasoman_1923@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:23.412558'),(316,'pbkdf2_sha256$1000000$mGSGkhYKui9u5f6FQUf0TS$Tuhk2t+AsqMcEVCFhZy8PfMgtFScpSUkGxnKT6TtVYs=',NULL,0,'patient_dalbirkulkarni_5967@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:23.978597'),(317,'pbkdf2_sha256$1000000$Kvgh2PvZPwvk9WQTGyOGal$pbpL91DYlYKkTPaEqKoECks4peMgc6zDJmHxL+SfHU4=',NULL,0,'patient_chasmumbal_2880@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:24.544742'),(318,'pbkdf2_sha256$1000000$1eVwGQ8sDZeWStaxdN5092$+fBfr6AxtAMKus2S9LZ2ki6s1ve7DtWksQyeaJjcagY=',NULL,0,'patient_ishanvibakshi_6536@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:25.085483'),(319,'pbkdf2_sha256$1000000$hIxNRm2i3UnbKEqIl9v7VY$O3yIdz15Z/Y72GgGa4ycA/Fvi4jaG8VEyV5BgFy/S9Y=',NULL,0,'patient_janakikannan_1628@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:25.674833'),(320,'pbkdf2_sha256$1000000$TtlbWGjadrmKnQyeg2QOXd$kPYF6l6q2eQzn9ovNwugqr3sMO/hQkTD1Sudyl1PeRc=',NULL,0,'patient_jeettella_1826@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:26.243358'),(321,'pbkdf2_sha256$1000000$V4z6jhQNMTndEzvfvxMEbF$PZsfFr54qW3bizxoue075nkaVZF94+7Vky8BVPKsYlc=',NULL,0,'patient_jonathanswamy_7478@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:26.816703'),(322,'pbkdf2_sha256$1000000$npy4oUVSZ5TogjXyhpsGHY$VCs7fMyeel1hLsKmvxyPg+8SQ+CClCT+H42H6M7GmLE=',NULL,0,'patient_vinayabarad_4582@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:27.398609'),(323,'pbkdf2_sha256$1000000$yTSWAnslHKdbVipK7Fki80$N1OLRWTPCYiAVRSVnsjonT90ugN91R/WpnraKt9ACC0=',NULL,0,'patient_anthonybose_2065@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:27.981312'),(324,'pbkdf2_sha256$1000000$dA0UyzbQg7RVeO5nxGEfpd$sQCSW0uNyxoJYwuTCnXKseIJHVEZsrS6IzLsKHok0z4=',NULL,0,'patient_taraksinha_4779@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:28.632555'),(325,'pbkdf2_sha256$1000000$3mFLtSuzJAGzZEIeUKuqlR$UKsq7xLeBM+QkRx4+s6loMdGSoZY7bimIyiFMR4KImE=',NULL,0,'patient_balveerchaudhari_7319@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:29.285858'),(326,'pbkdf2_sha256$1000000$NKIB4LUuTr66NKWRFPuqt9$Zg3pWcgQyXjrVmhvxVpqH6Xbnh055f1OWlMU4+W/J7c=',NULL,0,'patient_rehaandevi_6800@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:30.031703'),(327,'pbkdf2_sha256$1000000$OYu4r0sImvg2Kng92kktCt$2l32SF0QS9Un3etGS6x7aBmOtvhDnISjqTTTZwLh21g=',NULL,0,'patient_yachanakapadia_5267@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:30.608759'),(328,'pbkdf2_sha256$1000000$tfeO0zAoFaAPpqp5b9CFZB$yaF10O+4Wajz4I8R9Ql4brviQlvFjBPKq7dnATJAjDw=',NULL,0,'patient_yashasvisoman_7006@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:31.178170'),(329,'pbkdf2_sha256$1000000$qYJNm7NOQ3xqnwe5oytUzv$dy2tDFUllp6uAzx7ozrfE/BRgqe2dZt94gHa1xlc+tU=',NULL,0,'patient_kashishsom_8853@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:31.742088'),(330,'pbkdf2_sha256$1000000$MKzEPcIvZ3cvm3HUJhVABU$4rKas3OFzANsKW8JAg2SR0IQ+N50ePcqD9BOP0l55Pw=',NULL,0,'patient_revaraja_6234@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:32.287469'),(331,'pbkdf2_sha256$1000000$la29hnGlpFmvoq1FCVMkdM$mytvndOPmyzVe3HZVU0IcDynGlQAaF5twGJf0us2KE4=',NULL,0,'patient_arjunsani_3376@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:32.833426'),(332,'pbkdf2_sha256$1000000$kdmoJv3w8sayEmTFlCAaFO$2qR/DWU+KrO4Qc2zvd8Xltgbyv03s5EX+RoWUCLr2T4=',NULL,0,'patient_nidhirama_8600@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:33.380848'),(333,'pbkdf2_sha256$1000000$eOSsb21I3WpTZxQZ0FvVZd$hduxI3ItNKNC/URRHGexvXpFBnLBWqZ5GgPmnTdhauU=',NULL,0,'patient_onisem_3878@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:33.947091'),(334,'pbkdf2_sha256$1000000$Pt7ttXaY7qCPVevknuwV8G$09++2lzovor28fkvYI6uUoYe1Jreyj7JwCmuOSaLd2o=',NULL,0,'patient_prishachoudhury_8034@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:34.572671'),(335,'pbkdf2_sha256$1000000$uEld1QcLiXP6tnOB9Nl6k4$+Z+Km1XZMYecVR02rf+gTM+ETk7Nj63zI0OdV3B9Z1c=',NULL,0,'patient_hemanggarde_9671@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:35.122175'),(336,'pbkdf2_sha256$1000000$3YurzGNRBYN0FUd0LT4UoQ$4ei9PaoZa4MOXpolL2CgdvVYiNux/8INGlYNdMx6VOw=',NULL,0,'patient_rajeshripurohit_9803@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:35.668870'),(337,'pbkdf2_sha256$1000000$cvQwxez2oqa4tJmALhMj9z$Vtk2NAdqSw3Bm6MEox8AR8p2snBs8nggqncSueFcjQ0=',NULL,0,'patient_urvashiiyer_4578@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:36.214703'),(338,'pbkdf2_sha256$1000000$RwYZR9eyU2hHdzc7wSVfHQ$8yNjK8wXLvusLeMKmP/Nw+juzeOZH8n6HiVjbSzHt3M=',NULL,0,'patient_ucchalbalay_5573@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:36.759137'),(339,'pbkdf2_sha256$1000000$fI2g8vyaUY25vp0yZOHudl$M/fO1QSdijVxO+iHiBEIMIIDb1L6KXQwEMs0hfmgG9o=',NULL,0,'patient_wriddhishdhaliwal_7588@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:37.317442'),(340,'pbkdf2_sha256$1000000$DVvkm82p2l0z5zxqKf2OQg$DOvW8W6vOrP4L6U5OpDVg+YjmEYdHcGX3jXCHdjtQ9E=',NULL,0,'patient_chatreshthaman_1868@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:37.924178'),(341,'pbkdf2_sha256$1000000$TUZmKiU6dMzihamTiy2UF0$1w2gcNX6w3lRoThdu22c+j1pEuSQCAbcobRbB/j2RDc=',NULL,0,'patient_lipikanayak_9999@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:38.626877'),(342,'pbkdf2_sha256$1000000$ZfgrG7W3KRqPJScHtuzepw$PG+sunlH/3xUJZuZnlDGipxbTBX8cBDNTByJvPPHIfE=',NULL,0,'patient_hiteshhegde_4312@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:39.359057'),(343,'pbkdf2_sha256$1000000$LpjK2nbn2jGYLNv0EYh1xC$AzKTuYgGV+Fa7IQyI0UcIsGHXHEv/4ZlnpxEAuJmj/E=',NULL,0,'patient_christopherchadha_9434@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:39.984902'),(344,'pbkdf2_sha256$1000000$zaE8LkI715yh2aQLZGvupc$991TWzKcP8NlHAOav6d0PgcOxzYLE5/yqcBUatuS37M=',NULL,0,'patient_bhavanideo_9655@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:40.623288'),(345,'pbkdf2_sha256$1000000$vfPb3wGIqcoBCohLSlh4CJ$N24i/rBqqPlFIN8UZWezu2BldM6kopuqzBC0Qs2LBlE=',NULL,0,'patient_odikamurthy_8526@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:41.256497'),(346,'pbkdf2_sha256$1000000$Ceod8X6wRHSGxdp7W6Xebh$jnPXLAzQJwYOIqFlWNlH11DDwW7vT5qoPBfEcBl0S9o=',NULL,0,'patient_abhiramsathe_9542@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:41.892738'),(347,'pbkdf2_sha256$1000000$LMXXenr9n1A9kESMfmOH1Z$rd4usHNp6fN0e/bnLozOwQA+WgUSF1lSjBd7HkTZZhk=',NULL,0,'patient_tanishloyal_3541@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:42.530808'),(348,'pbkdf2_sha256$1000000$9WOdgtPEkorYzM9GM5JlJ9$Tkwm8a2nhZ2U/P5VsUUARFm1dA6WXnOh1ry2XwWmBrU=',NULL,0,'patient_widishasagar_7541@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:43.178539'),(349,'pbkdf2_sha256$1000000$yoqPxeabIPygKCcy6zPahE$p+KFLYkKqyinBIQ7k3Sz0M1LpAR+4uLO5pW0R/IXKGk=',NULL,0,'patient_lilaloke_7940@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:43.826239'),(350,'pbkdf2_sha256$1000000$Urq4oCMSiqJaXQ6zHsmcnp$nnKpAgFkUgo/Bt4FacTBidzs9CVuWqHgQpefNxiHvNI=',NULL,0,'patient_pranavsastry_9156@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:44.477475'),(351,'pbkdf2_sha256$1000000$97sJfJc6CtnuATvSIMLC8W$haBICFZohRqrxiApLcgfN4HCnyYYVc5uQhlxiLlN/Sw=',NULL,0,'patient_ronithnagarajan_1192@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:45.124932'),(352,'pbkdf2_sha256$1000000$NV7O24tphRxBaKjjqjLgCD$f2btAxOfqCzORlhFxlDHSexzMdSXUWOJuS/F7folldg=',NULL,0,'patient_rachitabutala_5626@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:45.767243'),(353,'pbkdf2_sha256$1000000$1TEtb8ECcUOOhFdqA9nuwn$9mKG/mEN19a9Q6r73WLE8rAkwV3x2i8586BrauzWdV8=',NULL,0,'patient_charvivirk_7569@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:46.389372'),(354,'pbkdf2_sha256$1000000$aTprV4AamZpdyv0jPeN50P$fxkVzjurKoW3HGmcqtrWB+CsvXyDi7NUqS92Og0Edzg=',NULL,0,'patient_wardamalhotra_8475@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:47.009626'),(355,'pbkdf2_sha256$1000000$MCuYrsu3yBeNfxZ5BUtmma$rB79zIn047MJKpBqlp9++/2BGMTgzl7PahsDKH3p2to=',NULL,0,'patient_gauravarya_3911@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:47.656509'),(356,'pbkdf2_sha256$1000000$2GabpQH9AyexCz8Jke5FkJ$VeBKSsv55d/r07aoAKAygIVhzARJduOxKtk4QGPJDhA=',NULL,0,'patient_lavanyakapoor_5117@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:48.303463'),(357,'pbkdf2_sha256$1000000$ZQpZoomRxodZb4UQADGrgO$orfg1R6SJ5zPXjOYzJVpIjlPC1gF9S0U0v0Nib/E3uM=',NULL,0,'patient_rakshadeep_6491@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:48.957527'),(358,'pbkdf2_sha256$1000000$8XChe8lLp5kEjVt1crdYAd$F2d8TOWkNp8XLi8L9ljyP6mlljttcDlj1wHFUqWjSjk=',NULL,0,'patient_owenamble_9860@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:49.579761'),(359,'pbkdf2_sha256$1000000$z0IlwWSzhng5O0x7mMgtrZ$CI4HOyUY5P7SROr6wocF9WKMzrwgdq6gafWTAoYMlD0=',NULL,0,'patient_aarnamore_2391@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:50.214744'),(360,'pbkdf2_sha256$1000000$JhcPLd6dCfMx1BnExOfaSn$nfvKzcIP7gi1cRy/HTES0hFdE0LWVpIPCxk+aWusLc0=',NULL,0,'patient_vasudhanagi_5187@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:50.838745'),(361,'pbkdf2_sha256$1000000$EnqkZc29WGZ6DfmqlnejQn$UIT9RI68C81vCiYbMbleRtPdFbLkXZHfujmwwMmHlYM=',NULL,0,'patient_wazirdivan_6316@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:51.455562'),(362,'pbkdf2_sha256$1000000$XcZQ6V2q7mAY7aJaRrKqw6$7hThi2c6aQawmg1Py7XrgQyAhzR8jUWZ12waTtxGz/I=',NULL,0,'patient_gautamnayar_9177@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:52.005896'),(363,'pbkdf2_sha256$1000000$V09bqeHQVCoOU0qegx75I2$11xIBX43QuO9AmWTrefP3rOfxF3OCWMLGYnPAcAnDLw=',NULL,0,'patient_parthpandya_8971@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:52.559234'),(364,'pbkdf2_sha256$1000000$JPbgld2bgBMxyZVFhQzBs9$21ZLdrDGTv65zMG13E1uTByzxKoNcJoItqew0hAwNxA=',NULL,0,'patient_mahikasampath_5436@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:53.109182'),(365,'pbkdf2_sha256$1000000$nioxvrQX5xofJ2pBmy9yBy$xEwIigOGa4n9ZK7YycbE0liUDYzP3UYcKxgGf0BclZA=',NULL,0,'patient_tristannair_9463@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:53.676105'),(366,'pbkdf2_sha256$1000000$FSc2NkoGfSf1YRsaG1qMZQ$xcWL0tyPfiRTdK+emKq3YdIv3j4BTBA46nhgEJNq3Eg=',NULL,0,'patient_zilmildada_5457@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:54.230469'),(367,'pbkdf2_sha256$1000000$RjUyHZAteK8fox2LtNmP5X$xQYAlyc+KgqesYc92igQ5A8iljn/nTzLS0OFgBDRRE4=',NULL,0,'patient_urishillabalay_3920@rhms.com',0,1,'patient',NULL,'2026-02-02 10:37:54.789733');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointments_appointment`
--

DROP TABLE IF EXISTS `appointments_appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments_appointment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `patient_name` varchar(150) NOT NULL,
  `appointment_date` datetime(6) NOT NULL,
  `doctor_id` bigint NOT NULL,
  `hospital_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `token_number` int unsigned DEFAULT NULL,
  `cancellation_reason` longtext,
  `cancelled_at` datetime(6) DEFAULT NULL,
  `notes` longtext,
  `status` varchar(20) NOT NULL,
  `report_file` varchar(100) DEFAULT NULL,
  `patient_email` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `appointments_appointment_doctor_id_fb58c3a1_fk_doctors_doctor_id` (`doctor_id`),
  KEY `appointments_appoint_hospital_id_b5912582_fk_rhms_hosp` (`hospital_id`),
  CONSTRAINT `appointments_appoint_hospital_id_b5912582_fk_rhms_hosp` FOREIGN KEY (`hospital_id`) REFERENCES `rhms_hospitals` (`id`),
  CONSTRAINT `appointments_appointment_doctor_id_fb58c3a1_fk_doctors_doctor_id` FOREIGN KEY (`doctor_id`) REFERENCES `doctors_doctor` (`id`),
  CONSTRAINT `appointments_appointment_chk_1` CHECK ((`token_number` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments_appointment`
--

LOCK TABLES `appointments_appointment` WRITE;
/*!40000 ALTER TABLE `appointments_appointment` DISABLE KEYS */;
INSERT INTO `appointments_appointment` VALUES (4,'khushi','2026-01-07 16:00:00.000000',19,83,'2026-01-07 06:08:35.005635',1,NULL,NULL,NULL,'scheduled',NULL,NULL),(5,'khushi','2026-01-07 16:00:00.000000',19,83,'2026-01-07 06:08:39.000976',2,'Cancelled by doctor','2026-01-07 11:04:41.144472',NULL,'completed',NULL,NULL),(6,'bhavan','2026-01-08 09:30:00.000000',19,83,'2026-01-08 05:20:36.824953',1,NULL,NULL,NULL,'scheduled',NULL,NULL),(7,'bhavan','2026-01-08 09:30:00.000000',19,83,'2026-01-08 05:20:55.657296',2,NULL,NULL,NULL,'scheduled',NULL,NULL),(8,'bhavan','2026-01-08 09:30:00.000000',19,83,'2026-01-08 05:20:59.360374',3,NULL,NULL,NULL,'scheduled',NULL,NULL),(9,'bhavan','2026-01-08 09:30:00.000000',19,83,'2026-01-08 05:21:02.945940',4,NULL,NULL,NULL,'scheduled',NULL,NULL),(10,'bhavan','2026-01-08 09:30:00.000000',19,83,'2026-01-08 05:21:06.746495',5,NULL,NULL,NULL,'scheduled',NULL,NULL),(11,'bhavan','2026-01-08 09:30:00.000000',19,83,'2026-01-08 05:21:10.214412',6,NULL,NULL,NULL,'scheduled',NULL,NULL),(12,'mengaly','2026-01-09 09:30:00.000000',19,83,'2026-01-08 05:49:49.534555',1,NULL,NULL,'this is test','completed','patient_reports/images.jpeg',NULL),(13,'mengaly','2026-01-09 09:30:00.000000',19,83,'2026-01-08 05:50:42.934790',2,NULL,NULL,'this is test','completed','patient_reports/ReevanaX_Logo.pdf',NULL),(14,'test','2026-01-08 13:30:00.000000',19,83,'2026-01-08 07:37:32.150964',7,NULL,NULL,'Marked Completed (Quick Action)','completed','',NULL),(15,'Bhavan Badhe','2026-01-09 10:30:00.000000',19,83,'2026-01-09 06:12:36.450522',3,NULL,NULL,NULL,'scheduled','',NULL),(16,'bhavan','2026-01-09 12:30:00.000000',20,83,'2026-01-09 06:43:09.665668',1,NULL,NULL,'this is test','completed','',NULL),(17,'Bhavan Badhe','2026-01-09 15:00:00.000000',20,83,'2026-01-09 07:22:07.346291',2,NULL,NULL,NULL,'scheduled','',NULL),(18,'test1','2026-01-14 09:00:00.000000',19,83,'2026-01-12 04:43:01.270259',1,NULL,NULL,NULL,'scheduled','',NULL),(19,'test2','2026-01-12 11:00:00.000000',19,83,'2026-01-12 04:46:42.436966',1,NULL,NULL,'this is wokring','completed','patient_reports/Screenshot-3_eMuh1il.png',NULL),(20,'test3','2026-01-12 11:30:00.000000',19,83,'2026-01-12 04:47:32.614964',2,NULL,NULL,'Okay this is compleate','completed','patient_reports/Screenshot-3_oil8JKe.png',NULL),(21,'test4','2026-01-12 12:00:00.000000',19,83,'2026-01-12 04:48:25.475024',3,NULL,NULL,'test','completed','patient_reports/Screenshot-3.png',NULL),(22,'test5','2026-01-12 12:30:00.000000',19,83,'2026-01-12 04:49:06.208712',4,NULL,NULL,'test 5 is','completed','patient_reports/Screenshot-3_N59R78O.png',NULL),(23,'bhavan','2026-01-12 16:00:00.000000',19,83,'2026-01-12 09:55:10.833636',5,NULL,NULL,'hello bhavan','completed','patient_reports/Screenshot-3_ehd3UBb.png',NULL),(24,'mengaly','2026-01-12 16:30:00.000000',19,83,'2026-01-12 09:56:05.633175',6,NULL,NULL,NULL,'scheduled','',NULL),(25,'','2026-01-20 09:12:00.000000',20,83,'2026-01-17 06:20:57.474933',NULL,NULL,NULL,NULL,'scheduled','',NULL),(26,'','2026-01-21 09:12:00.000000',20,83,'2026-01-17 06:21:32.751695',NULL,NULL,NULL,NULL,'scheduled','',NULL),(27,'','2026-01-22 09:12:00.000000',20,83,'2026-01-17 06:21:39.344485',NULL,NULL,NULL,NULL,'scheduled','',NULL),(28,'','2026-01-18 09:12:00.000000',20,83,'2026-01-17 07:56:15.586642',NULL,NULL,NULL,NULL,'scheduled','',NULL),(29,'','2026-01-17 09:12:00.000000',20,83,'2026-01-17 08:16:46.221314',NULL,NULL,NULL,NULL,'scheduled','',NULL),(30,'','2026-01-17 09:42:00.000000',20,83,'2026-01-17 08:17:00.904211',NULL,NULL,NULL,NULL,'scheduled','',NULL),(31,'','2026-01-20 09:12:00.000000',20,83,'2026-01-17 08:17:42.507990',NULL,NULL,NULL,NULL,'scheduled','',NULL),(32,'','2026-01-18 09:12:00.000000',20,83,'2026-01-17 08:17:52.976023',NULL,NULL,NULL,NULL,'scheduled','',NULL),(33,'','2026-01-17 10:12:00.000000',20,83,'2026-01-17 08:18:32.773319',NULL,NULL,NULL,NULL,'scheduled','',NULL),(34,'','2026-01-17 10:42:00.000000',20,83,'2026-01-17 08:25:00.593671',NULL,NULL,NULL,NULL,'scheduled','',NULL),(35,'','2026-01-17 11:12:00.000000',20,83,'2026-01-17 08:42:14.892810',5,NULL,NULL,NULL,'scheduled','',NULL),(36,'','2026-01-17 11:42:00.000000',20,83,'2026-01-17 09:04:43.878205',6,NULL,NULL,NULL,'scheduled','',NULL),(37,'','2026-01-17 12:12:00.000000',20,83,'2026-01-17 09:04:53.721632',7,NULL,NULL,NULL,'scheduled','',NULL),(38,'','2026-01-17 12:42:00.000000',20,83,'2026-01-17 09:40:02.739049',8,NULL,NULL,NULL,'scheduled','',NULL),(39,'','2026-01-17 13:12:00.000000',20,83,'2026-01-17 09:40:17.681431',9,NULL,NULL,NULL,'scheduled','',NULL),(40,'','2026-01-17 14:12:00.000000',20,83,'2026-01-17 09:41:17.854233',10,NULL,NULL,NULL,'scheduled','',NULL),(44,'','2026-01-21 05:02:29.946218',21,84,'2026-02-02 05:02:29.946345',1,NULL,NULL,'Initial checkup (System Generated)','completed','','test1@gmail.com'),(47,'','2026-01-21 05:02:29.968743',21,84,'2026-02-02 05:02:29.968790',15,NULL,NULL,'Initial checkup (System Generated)','completed','','test5@gmail.com'),(57,'Krisha Tak','2026-01-23 05:02:30.045530',23,85,'2026-02-02 05:02:30.045569',12,NULL,NULL,'Initial checkup (System Generated)','completed','','rachanarai@example.org'),(59,'Mitesh Shetty','2026-01-21 05:02:30.062150',19,83,'2026-02-02 05:02:30.062193',19,NULL,NULL,'Initial checkup (System Generated)','completed','','etasingh@example.com'),(65,'Bina Dua','2026-01-15 05:02:30.115388',20,83,'2026-02-02 05:02:30.115458',7,NULL,NULL,'Initial checkup (System Generated)','completed','','lucky58@example.net'),(75,'Zarna Das','2026-02-01 05:02:30.198609',23,85,'2026-02-02 05:02:30.198644',4,NULL,NULL,'Initial checkup (System Generated)','completed','','kauraditya@example.net'),(96,'Deepa Sant','2026-01-18 05:02:30.368666',23,85,'2026-02-02 05:02:30.368706',10,NULL,NULL,'Initial checkup (System Generated)','completed','','zansi55@example.net'),(98,'Yuvraj Garde','2026-01-28 05:02:30.399350',24,85,'2026-02-02 05:02:30.399408',5,NULL,NULL,'Initial checkup (System Generated)','completed','','jsami@example.com'),(102,'Harish Sodhi','2026-01-05 05:02:30.424136',23,85,'2026-02-02 05:02:30.424172',4,NULL,NULL,'Initial checkup (System Generated)','completed','','bvarma@example.org'),(106,'Jonathan Saxena','2026-01-17 05:02:30.446712',23,85,'2026-02-02 05:02:30.446750',15,NULL,NULL,'Initial checkup (System Generated)','completed','','mnadig@example.com'),(110,'Sanaya Chakrabarti','2026-01-08 05:02:30.471864',21,84,'2026-02-02 05:02:30.471903',14,NULL,NULL,'Initial checkup (System Generated)','completed','','tdas@example.com');
/*!40000 ALTER TABLE `appointments_appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointments_dailyqueue`
--

DROP TABLE IF EXISTS `appointments_dailyqueue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments_dailyqueue` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `current_token` int unsigned NOT NULL,
  `doctor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `appointments_dailyqueue_doctor_id_date_dd8ec899_uniq` (`doctor_id`,`date`),
  CONSTRAINT `appointments_dailyqueue_doctor_id_1695654d_fk_doctors_doctor_id` FOREIGN KEY (`doctor_id`) REFERENCES `doctors_doctor` (`id`),
  CONSTRAINT `appointments_dailyqueue_chk_1` CHECK ((`current_token` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments_dailyqueue`
--

LOCK TABLES `appointments_dailyqueue` WRITE;
/*!40000 ALTER TABLE `appointments_dailyqueue` DISABLE KEYS */;
INSERT INTO `appointments_dailyqueue` VALUES (1,'2026-01-08',7,19),(2,'2026-01-09',3,19),(3,'2026-01-09',2,20),(4,'2026-01-10',0,19),(5,'2026-01-12',6,19),(6,'2026-01-17',0,20),(7,'2026-01-17',0,19),(8,'2026-01-29',0,19);
/*!40000 ALTER TABLE `appointments_dailyqueue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Token',6,'add_token'),(22,'Can change Token',6,'change_token'),(23,'Can delete Token',6,'delete_token'),(24,'Can view Token',6,'view_token'),(25,'Can add Token',7,'add_tokenproxy'),(26,'Can change Token',7,'change_tokenproxy'),(27,'Can delete Token',7,'delete_tokenproxy'),(28,'Can view Token',7,'view_tokenproxy'),(29,'Can add user',8,'add_user'),(30,'Can change user',8,'change_user'),(31,'Can delete user',8,'delete_user'),(32,'Can view user',8,'view_user'),(33,'Can add hospital',9,'add_hospital'),(34,'Can change hospital',9,'change_hospital'),(35,'Can delete hospital',9,'delete_hospital'),(36,'Can view hospital',9,'view_hospital'),(37,'Can add department',10,'add_department'),(38,'Can change department',10,'change_department'),(39,'Can delete department',10,'delete_department'),(40,'Can view department',10,'view_department'),(41,'Can add hospital admin',11,'add_hospitaladmin'),(42,'Can change hospital admin',11,'change_hospitaladmin'),(43,'Can delete hospital admin',11,'delete_hospitaladmin'),(44,'Can view hospital admin',11,'view_hospitaladmin'),(45,'Can add treatment',12,'add_treatment'),(46,'Can change treatment',12,'change_treatment'),(47,'Can delete treatment',12,'delete_treatment'),(48,'Can view treatment',12,'view_treatment'),(49,'Can add appointment',13,'add_appointment'),(50,'Can change appointment',13,'change_appointment'),(51,'Can delete appointment',13,'delete_appointment'),(52,'Can view appointment',13,'view_appointment'),(53,'Can add doctor availability',14,'add_doctoravailability'),(54,'Can change doctor availability',14,'change_doctoravailability'),(55,'Can delete doctor availability',14,'delete_doctoravailability'),(56,'Can view doctor availability',14,'view_doctoravailability'),(57,'Can add doctor',15,'add_doctor'),(58,'Can change doctor',15,'change_doctor'),(59,'Can delete doctor',15,'delete_doctor'),(60,'Can view doctor',15,'view_doctor'),(61,'Can add patient',16,'add_patient'),(62,'Can change patient',16,'change_patient'),(63,'Can delete patient',16,'delete_patient'),(64,'Can view patient',16,'view_patient'),(65,'Can add doctor availability',17,'add_doctoravailability'),(66,'Can change doctor availability',17,'change_doctoravailability'),(67,'Can delete doctor availability',17,'delete_doctoravailability'),(68,'Can view doctor availability',17,'view_doctoravailability'),(69,'Can add doctor profile',18,'add_doctorprofile'),(70,'Can change doctor profile',18,'change_doctorprofile'),(71,'Can delete doctor profile',18,'delete_doctorprofile'),(72,'Can view doctor profile',18,'view_doctorprofile'),(73,'Can add hospital admin profile',19,'add_hospitaladminprofile'),(74,'Can change hospital admin profile',19,'change_hospitaladminprofile'),(75,'Can delete hospital admin profile',19,'delete_hospitaladminprofile'),(76,'Can view hospital admin profile',19,'view_hospitaladminprofile'),(77,'Can add patient',20,'add_patient'),(78,'Can change patient',20,'change_patient'),(79,'Can delete patient',20,'delete_patient'),(80,'Can view patient',20,'view_patient'),(81,'Can add notification',21,'add_notification'),(82,'Can change notification',21,'change_notification'),(83,'Can delete notification',21,'delete_notification'),(84,'Can view notification',21,'view_notification'),(85,'Can add Notification',22,'add_notification'),(86,'Can change Notification',22,'change_notification'),(87,'Can delete Notification',22,'delete_notification'),(88,'Can view Notification',22,'view_notification'),(89,'Can add daily queue',23,'add_dailyqueue'),(90,'Can change daily queue',23,'change_dailyqueue'),(91,'Can delete daily queue',23,'delete_dailyqueue'),(92,'Can view daily queue',23,'view_dailyqueue'),(93,'Can add search keyword',24,'add_searchkeyword'),(94,'Can change search keyword',24,'change_searchkeyword'),(95,'Can delete search keyword',24,'delete_searchkeyword'),(96,'Can view search keyword',24,'view_searchkeyword');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_searchkeyword`
--

DROP TABLE IF EXISTS `core_searchkeyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_searchkeyword` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `keyword` varchar(100) NOT NULL,
  `mapped_term` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_searchkeyword`
--

LOCK TABLES `core_searchkeyword` WRITE;
/*!40000 ALTER TABLE `core_searchkeyword` DISABLE KEYS */;
INSERT INTO `core_searchkeyword` VALUES (1,'chest pain','Cardiology');
/*!40000 ALTER TABLE `core_searchkeyword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (72,'2025-11-27 10:49:27.957581','41','bhavanbadhe@gmail.com',2,'[{\"changed\": {\"fields\": [\"Is staff\"]}}]',8,40),(73,'2025-11-27 10:50:38.859612','70','mengaly',3,'',9,40),(74,'2025-11-27 10:50:48.179707','41','bhavanbadhe@gmail.com',3,'',8,40),(75,'2025-11-28 06:17:00.897002','6','bhavan badhe - pdcm',3,'',15,40),(76,'2025-11-28 06:17:15.384185','48','bhawan.badhe079@gmail.com',3,'',8,40),(77,'2025-12-01 12:43:12.944074','58','bluedesigner001@gmail.com',3,'',8,40),(78,'2025-12-01 12:43:25.162543','50','bgtemployer@gmail.com',3,'',8,40),(79,'2025-12-04 07:15:53.433192','63','bhavana1@gmail.com',3,'',8,40),(80,'2025-12-04 07:15:53.433221','62','khushi123@gmail.com',3,'',8,40),(81,'2025-12-04 07:15:53.433237','61','khushi12@gmail.com',3,'',8,40),(82,'2025-12-04 07:15:53.433249','60','khush@gmail.com',3,'',8,40),(83,'2025-12-04 09:42:55.199408','67','bhavan@gmail.com',3,'',8,40),(84,'2025-12-04 09:42:55.199555','66','khush@gmail.com',3,'',8,40),(85,'2025-12-05 09:46:13.145287','65','test_verify_patient@example.com',3,'',8,40),(86,'2025-12-05 09:46:13.145315','64','khushipathak008@gmail.com',3,'',8,40),(87,'2025-12-05 09:46:13.145330','59','bgtemployer@gmail.com',3,'',8,40),(88,'2025-12-05 09:46:13.145341','57','bluedesigner002@gmail.com',3,'',8,40),(89,'2025-12-05 09:46:13.145352','54','dr.test@example.com',3,'',8,40),(90,'2025-12-05 09:46:13.145363','53','mehulaffiliatemarketing@gmail.com',3,'',8,40),(91,'2025-12-05 09:46:13.145373','52','mehulsolanki.n70@gmail.com',3,'',8,40),(92,'2025-12-05 09:46:13.145382','51','khushi@gmail.com',3,'',8,40),(93,'2025-12-05 09:46:13.145391','49','bhawan.badhe079@gmail.com',3,'',8,40),(94,'2025-12-05 09:46:13.145401','46','testexample856@gmail.com',3,'',8,40),(95,'2025-12-05 09:46:13.145410','43','bhavanbadhe@gmail.com',3,'',8,40),(96,'2025-12-05 09:46:32.486882','76','pearl womens hospital',3,'',9,40),(97,'2025-12-05 09:46:32.486916','75','Test Hospital',3,'',9,40),(98,'2025-12-05 09:46:32.486931','74','Radhe Multispeciality Hospital',3,'',9,40),(99,'2025-12-05 09:46:32.486943','73','khushi',3,'',9,40),(100,'2025-12-05 09:46:32.486954','72','mengaly',3,'',9,40),(101,'2025-12-06 06:01:41.888259','14','bhavan badhe - test',3,'',15,40),(102,'2025-12-06 06:01:51.721924','70','ombadhe079@gmail.com',3,'',8,40),(103,'2025-12-06 08:14:39.422945','71','ombadhe078@gmail.com',3,'',8,40),(104,'2025-12-10 09:56:21.835676','76','mehulsolanki.n70@gmail.com',3,'',8,40),(105,'2025-12-10 09:56:21.835752','75','bluedesigner001@gmail.com',3,'',8,40),(106,'2025-12-10 09:56:21.835788','74','khushipathak008@gmail.com',3,'',8,40),(107,'2025-12-10 09:56:21.835811','73','testexample856@gmail.com',3,'',8,40),(108,'2025-12-10 09:56:21.835834','72','ombadhe078@gmail.com',3,'',8,40),(109,'2025-12-10 09:56:21.835854','69','bhawan.badhe079@gmail.com',3,'',8,40),(110,'2025-12-10 09:56:21.835873','68','bhavanbadhe@gmail.com',3,'',8,40),(111,'2025-12-15 05:15:53.822803','79','khushi_pathak',3,'',9,40),(112,'2025-12-15 05:15:53.822833','78','nirma',3,'',9,40),(113,'2025-12-15 05:15:53.822848','77','test hospital ',3,'',9,40),(114,'2025-12-16 10:48:44.229518','79','bhavanbadhe@gmail.com',2,'[{\"changed\": {\"fields\": [\"Password\"]}}]',8,40),(115,'2025-12-16 10:59:40.932305','79','bhavanbadhe@gmail.com',3,'',8,40),(116,'2025-12-16 10:59:40.932335','78','bhawan.badhe079@gmail.com',3,'',8,40);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (18,'accounts','doctorprofile'),(19,'accounts','hospitaladminprofile'),(8,'accounts','user'),(1,'admin','logentry'),(13,'appointments','appointment'),(23,'appointments','dailyqueue'),(14,'appointments','doctoravailability'),(20,'appointments','patient'),(3,'auth','group'),(2,'auth','permission'),(6,'authtoken','token'),(7,'authtoken','tokenproxy'),(4,'contenttypes','contenttype'),(24,'core','searchkeyword'),(15,'doctors','doctor'),(17,'doctors','doctoravailability'),(10,'hospitals','department'),(9,'hospitals','hospital'),(11,'hospitals','hospitaladmin'),(12,'hospitals','treatment'),(22,'notifications','notification'),(21,'patients','notification'),(16,'patients','patient'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-11-06 06:37:28.204324'),(2,'contenttypes','0002_remove_content_type_name','2025-11-06 06:37:28.331804'),(3,'auth','0001_initial','2025-11-06 06:37:28.843943'),(4,'auth','0002_alter_permission_name_max_length','2025-11-06 06:37:28.935848'),(5,'auth','0003_alter_user_email_max_length','2025-11-06 06:37:28.945376'),(6,'auth','0004_alter_user_username_opts','2025-11-06 06:37:28.959713'),(7,'auth','0005_alter_user_last_login_null','2025-11-06 06:37:28.966515'),(8,'auth','0006_require_contenttypes_0002','2025-11-06 06:37:28.971093'),(9,'auth','0007_alter_validators_add_error_messages','2025-11-06 06:37:28.980065'),(10,'auth','0008_alter_user_username_max_length','2025-11-06 06:37:28.988867'),(11,'auth','0009_alter_user_last_name_max_length','2025-11-06 06:37:28.998805'),(12,'auth','0010_alter_group_name_max_length','2025-11-06 06:37:29.021938'),(13,'auth','0011_update_proxy_permissions','2025-11-06 06:37:29.029616'),(14,'auth','0012_alter_user_first_name_max_length','2025-11-06 06:37:29.037524'),(15,'accounts','0001_initial','2025-11-06 06:37:29.527248'),(16,'admin','0001_initial','2025-11-06 06:37:29.736954'),(17,'admin','0002_logentry_remove_auto_add','2025-11-06 06:37:29.746349'),(18,'admin','0003_logentry_add_action_flag_choices','2025-11-06 06:37:29.755259'),(19,'hospitals','0001_initial','2025-11-06 06:37:30.336169'),(22,'authtoken','0001_initial','2025-11-06 06:37:31.275740'),(23,'authtoken','0002_auto_20160226_1747','2025-11-06 06:37:31.302671'),(24,'authtoken','0003_tokenproxy','2025-11-06 06:37:31.307001'),(25,'authtoken','0004_alter_tokenproxy_options','2025-11-06 06:37:31.313572'),(26,'hospitals','0002_rename_hospital_hospitaladmin_hospital_and_more','2025-11-06 06:37:31.477774'),(27,'hospitals','0003_remove_hospitaladmin_hospital_and_more','2025-11-06 06:37:31.756325'),(30,'patients','0001_initial','2025-11-06 06:37:34.320275'),(31,'sessions','0001_initial','2025-11-06 06:37:34.367685'),(32,'doctors','0001_initial','2025-11-06 07:16:26.902663'),(33,'appointments','0001_initial','2025-11-06 07:16:27.222872'),(34,'doctors','0002_doctor_status_alter_doctor_years_of_experience','2025-11-06 07:16:27.356734'),(35,'doctors','0003_remove_doctor_aadhaar_remove_doctor_address_and_more','2025-11-06 07:16:29.595916'),(36,'doctors','0004_doctoravailability','2025-11-06 07:16:29.702612'),(37,'accounts','0002_alter_user_options_alter_user_managers_and_more','2025-11-11 05:52:04.658593'),(38,'hospitals','0004_hospital_country_hospital_state','2025-11-11 13:37:54.735757'),(39,'hospitals','0005_hospital_hospital_type_hospital_hours','2025-11-11 13:50:51.592075'),(40,'appointments','0002_patient','2025-11-17 13:10:39.760768'),(41,'patients','0002_remove_patient_hospital_and_more','2025-11-17 13:10:40.082293'),(42,'patients','0003_patient_hospital_patient_medical_history_and_more','2025-11-17 13:10:40.361445'),(43,'patients','0004_patient_photo_alter_patient_hospital','2025-11-17 13:10:40.513870'),(44,'accounts','0003_remove_doctorprofile_availability_status_and_more','2025-11-21 10:30:37.245552'),(45,'accounts','0004_user_date_joined','2025-11-22 06:22:38.822591'),(46,'accounts','0005_user_created_at','2025-11-22 06:24:13.655391'),(47,'accounts','0006_remove_user_created_at','2025-11-22 06:30:01.959909'),(48,'appointments','0003_appointment_created_at','2025-11-22 06:32:13.566297'),(49,'doctors','0005_doctor_is_approved','2025-11-22 07:19:58.751694'),(50,'hospitals','0006_hospital_is_approved','2025-11-22 07:19:58.901736'),(51,'accounts','0007_alter_hospitaladminprofile_contact_number_and_more','2025-11-24 04:47:33.075156'),(52,'hospitals','0007_alter_hospital_hospital_type_alter_hospital_hours','2025-11-24 10:23:32.151910'),(53,'hospitals','0008_alter_hospital_hospital_type','2025-11-24 10:23:32.360310'),(54,'doctors','0006_doctor_status','2025-11-25 11:11:41.485075'),(55,'doctors','0007_remove_doctor_status','2025-11-25 11:24:21.307306'),(56,'hospitals','0009_alter_hospital_hospital_type','2025-11-25 11:24:21.618520'),(57,'doctors','0008_doctor_status','2025-11-25 16:03:53.969020'),(58,'doctors','0009_doctor_department_doctor_treatments','2025-11-27 05:17:43.286359'),(59,'doctors','0010_doctor_name','2025-11-28 05:36:35.860555'),(60,'accounts','0008_alter_doctorprofile_aadhaar','2025-11-28 05:53:33.499588'),(61,'appointments','0004_delete_patient_remove_appointment_status_and_more','2025-12-01 07:53:21.120183'),(62,'patients','0005_notification','2025-12-03 07:36:01.362833'),(63,'accounts','0009_alter_doctorprofile_aadhaar','2025-12-06 04:59:10.042812'),(64,'appointments','0005_doctoravailability_slot_duration','2025-12-06 13:24:20.409283'),(65,'appointments','0006_appointment_cancellation_reason_and_more','2025-12-06 14:38:44.006446'),(66,'notifications','0001_initial','2025-12-16 10:32:35.193694'),(67,'notifications','0002_auto_20150224_1134','2025-12-16 10:32:35.438151'),(68,'notifications','0003_notification_data','2025-12-16 10:32:35.565728'),(69,'notifications','0004_auto_20150826_1508','2025-12-16 10:32:35.584598'),(70,'notifications','0005_auto_20160504_1520','2025-12-16 10:32:35.608955'),(71,'notifications','0006_indexes','2025-12-16 10:32:35.817982'),(72,'notifications','0007_add_timestamp_index','2025-12-16 10:32:35.871423'),(73,'notifications','0008_index_together_recipient_unread','2025-12-16 10:32:35.952527'),(74,'notifications','0009_alter_notification_options_and_more','2025-12-16 10:32:36.617118'),(75,'notifications','0010_rename_notification_recipient_unread_notificatio_recipie_8bedf2_idx','2025-12-16 10:32:36.812735'),(76,'hospitals','0010_department_code_alter_hospital_logo','2026-01-08 06:34:56.819955'),(77,'appointments','0007_dailyqueue','2026-01-08 07:14:09.766055'),(78,'appointments','0008_appointment_report_file','2026-01-08 09:19:53.221290'),(79,'appointments','0009_appointment_patient_email','2026-01-09 08:04:49.436943'),(80,'patients','0006_alter_patient_photo','2026-01-09 08:04:49.454899'),(81,'hospitals','0010_alter_hospital_logo','2026-01-10 06:22:53.657836'),(82,'patients','0007_patient_name','2026-01-13 11:17:50.053624'),(83,'core','0001_initial','2026-01-16 07:23:53.707693');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0ib2e5wslpt97yldoccydh4eatgfmaq7','e30:1vLGB6:8mQFkVZ40DQLoBCy-Z3KPQoYcmHQDXQIMTpLSeqVAyg','2025-12-02 07:31:04.748112'),('0n4kznziggvs2jcsrsex4mis3h4rerti','.eJxVjDsOwjAQBe_iGln-fyjpOYPl3bVxADlSnFSIu0OkFNC-mXkvlvK2trSNsqSJ2Jl5y06_I2R8lL4Tuud-mznOfV0m4LvCDzr4dabyvBzu30HLo33rIK1yhYrRItcAxkYHpIQCilg9WqmDFAGlUkH4KB1h1egr5Gi89kjs_QH-_jfh:1vSYH0:eWp8SefMh_mwEIzBAY08KNk-xMtvbtzLGQ9CS_4BNs4','2025-12-22 10:15:18.974038'),('0oma3bn79ftdkccghu986e8i9eeb00di','.eJxVjEEOwiAQRe_C2hCZAgWX7j0DmWFAqgaS0q6Md7dNutDtf-_9twi4LiWsPc1hYnERWpx-N8L4THUH_MB6bzK2uswTyV2RB-3y1ji9rof7d1Cwl60ejY0alUOTIbsREDKkzJazHrxTAyFZMMwWFGHmzdNe0cDn6CMgefH5AvQdOJA:1vOEmH:PbIILAwm6sp-AVLkCO2h1Uj8jSL3m7qvmPlzxIzCVm0','2025-12-10 12:37:45.249438'),('4lruw93j26cys9jzf8pa8a98b2do86at','.eJxVjMEOwiAQRP-FsyEplN3i0bvfQHZZKlVDk9KeGv9dmvSgmdubN7OrQNuaw1bTEiZRVzVYdfmFTPGVytHIk8pj1nEu6zKxPhR9tlXfZ0nv2-n-HWSqua0RRyKTPDF31rlewABxIuCWTtDjwGBGNN43mJg9I7BYduAcxF59vihdOK4:1ve7jO:uLtjolPyc2jXdtaO_XSf9h0WU9N99zH3O6iNx_Pnbqg','2026-01-23 08:20:26.775299'),('68x50bva2ubmvwcws33y83ktkfo0uoz0','.eJxVjEEOwiAQRe_C2hCgUxhcuvcMzQCDVA0kpV0Z765NutDtf-_9l5hoW8u0dV6mOYmzQC9Ov2Og-OC6k3Snemsytrouc5C7Ig_a5bUlfl4O9--gUC_f2oLyxocc4qDAhhQxMTBb7YwB1uD0CEYjZYxZWRxGT47AZmRUaXRRvD8DljfB:1vaRnx:TNjFDjqP07Kelx0pVV78zqAvNG2oidILi101Y_36j38','2026-01-13 04:57:57.424074'),('8q0xrmhv25d114o8n1emtularhu7agir','.eJxVjMEOwiAQRP-FsyEplN3i0bvfQHZZKlVDk9KeGv9dmvSgmdubN7OrQNuaw1bTEiZRVzVYdfmFTPGVytHIk8pj1nEu6zKxPhR9tlXfZ0nv2-n-HWSqua0RRyKTPDF31rlewABxIuCWTtDjwGBGNN43mJg9I7BYduAcxF59vihdOK4:1vfDWW:AWLb6J_N4GGaVsvTajB_Wc5wpqgkV1obI6huR3l5f1c','2026-01-26 08:43:40.746569'),('8rr8ddxvekqeb9mjf8ty8n4364nbm0jm','.eJxVjDsOwjAQBe_iGln-26GkzxmsXa-DA8iW4qRC3J1ESgHtm5n3ZhG2tcSt5yXOxK7MCHb5HRHSM9eD0APqvfHU6rrMyA-Fn7TzsVF-3U7376BAL3utDBgXUAVFBpNPdggpeEFJG0JvhFVgM-aJ9ISY0e1IDlJqAgdeSsk-Xw4qOFI:1vR3Rg:gIMpo-hlVrIfm7l2NjPVz1NlkiYcEqyk2MbAoWC3KL8','2025-12-18 07:08:08.920460'),('9ywhu39c924o9vedlnnd0zyxej27dhda','.eJxVjEEOwiAQRe_C2hBooQwu3XsGAsyMVA0kpV0Z765NutDtf-_9lwhxW0vYOi1hRnEWIE6_W4r5QXUHeI_11mRudV3mJHdFHrTLa0N6Xg7376DEXr71RFM2MBDDaJmQkbVjH8mj9Yk4o3JGmcGMWqNFnxiScsAjGIaIJov3BxMmOOw:1vLHc2:JzTpGLnxDj4sfSS-kaBPMDdhutr7QLBFxroEcjh1gB4','2025-12-02 09:02:58.132603'),('a64ztjsn5h46cai18nv58rc1k4rv83s6','.eJxVjMEOwiAQRP-FsyEplN3i0bvfQHZZKlVDk9KeGv9dmvSgmdubN7OrQNuaw1bTEiZRVzVYdfmFTPGVytHIk8pj1nEu6zKxPhR9tlXfZ0nv2-n-HWSqua0RRyKTPDF31rlewABxIuCWTtDjwGBGNN43mJg9I7BYduAcxF59vihdOK4:1vfAL6:h03IcNFuRs6XH2ifuv4QoNoRnCSn8WXU4K_fklzCy-I','2026-01-26 05:19:40.196654'),('av3s02n1401v03mox6fadtjkg5gfb2al','.eJxVjEEOwiAQRe_C2hCawgAu3XsGMsMMUjU0Ke3KeHdt0oVu_3vvv1TCba1p67KkidVZOa9OvyNhfkjbCd-x3Wad57YuE-ld0Qft-jqzPC-H-3dQsddvjegshZwRo8Ag1hoogxHrwBnyEqxQQYAywhgCU4wFLYMQUGYfiqj3ByolOUA:1vQ39j:q-NOi7uyg3cUTD8KgFHFNJIRo_hzu_nC7Kis8tWqKlE','2025-12-15 12:37:27.987506'),('axd9rxcnefg8vcx6cjsfjygndfae3q6g','.eJxVjDEOAiEURO9CbQgILB9L-z0D-XxAVg0ky25lvLuSbKHFNPPezIt53Lfi955Wv0R2YUax028ZkB6pDhLvWG-NU6vbugQ-FH7QzucW0_N6uH8HBXv5rl2OhgilDlpARtBwBkGknHWoUg4JEEdAW2Umqaw2Rotsc4ApIUn2_gAfmDh3:1vPEch:BIXDvPA4dQyMz71WcXdHLyVU59BhZmZaEQANRP-mVtE','2025-12-13 06:39:59.605044'),('bp0u0kc84781u0p60k36u6vrxeyt9aj6','.eJxVjMEOwiAQRP-FsyEplN3i0bvfQHZZKlVDk9KeGv9dmvSgmdubN7OrQNuaw1bTEiZRVzVYdfmFTPGVytHIk8pj1nEu6zKxPhR9tlXfZ0nv2-n-HWSqua0RRyKTPDF31rlewABxIuCWTtDjwGBGNN43mJg9I7BYduAcxF59vihdOK4:1vlRVS:GYnEDQX-OlF4n0ef-6kVf7fG_Vs52DWR78l3I9N_CBo','2026-02-12 12:52:18.867415'),('bqz2rmjk71x3lr3kr266g9zadxprg5zq','.eJxVjMEOwiAQRP-FsyEplN3i0bvfQHZZKlVDk9KeGv9dmvSgmdubN7OrQNuaw1bTEiZRVzVYdfmFTPGVytHIk8pj1nEu6zKxPhR9tlXfZ0nv2-n-HWSqua0RRyKTPDF31rlewABxIuCWTtDjwGBGNN43mJg9I7BYduAcxF59vihdOK4:1vfH9d:GWjf0n3IWoC_dW6HHpNL3BksckK-TjtyRsaHEtO0gvQ','2026-01-26 12:36:17.640151'),('dtzre9d777ls6m7z2ehvjr4g6l6vi8qc','.eJxVjEEOgjAQRe_StWkoUGfGpXvO0HQ6U4saSCisjHdXEha6_e-9_zIhbmsJW9UljGIuBntz-h05podOO5F7nG6zTfO0LiPbXbEHrXaYRZ_Xw_07KLGWb00JOXPiHh1pBiLvIbX-LB0JQ8xelBpwrm17dR5QAWOGLpOyYENo3h8dAThE:1vgz3q:CPsruZYZ0Q1t7ILFbWorwSVvLny7MZKqXI9k052PyDs','2026-01-31 05:41:22.839492'),('dz0iw0i2wulyo7368baxb6xwbrdd310a','.eJxVjEEOgjAQRe_StWkoUGfGpXvO0HQ6U4saSCisjHdXEha6_e-9_zIhbmsJW9UljGIuBntz-h05podOO5F7nG6zTfO0LiPbXbEHrXaYRZ_Xw_07KLGWb00JOXPiHh1pBiLvIbX-LB0JQ8xelBpwrm17dR5QAWOGLpOyYENo3h8dAThE:1vgyoA:bdFGSP2owVC6YR8l5dQvEWBvDv_QOduiChvyOfvs6LE','2026-01-31 05:25:10.670194'),('fii55fy2obetu0lna2rl6ruzsmbaqvim','.eJxVjEEOwiAQRe_C2hCwUBiX7nsGMsxMpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uLcur0u2Wkh9Qd8B3rbdY013WZst4VfdCmh5nleT3cv4OCrXxrMGOwjj0ZgC4iGkMBOn_OOZIEBGej7xHYWBMdA5HDUWKU3lEGZlHvD9GlOBg:1vLvqv:g9ObVjfuSQeBGqES1kGtPERYdguaI16VYe2ZbZ4AyPA','2025-12-04 04:01:01.088934'),('g33ey85i3gp623p3rl18vg82rxsiqbz1','e30:1vLG80:BLu3zpaMpBTQD9j6mitZF9KaNk8ONcWGZbbbM44Vs8Y','2025-12-02 07:27:52.899119'),('g8w8x544tjsqo3f5yukrlnwkdic51tjt','.eJxVjMsOwiAQRf-FtSHAUB4u3fsNZGAmUjWQlHZl_Hdt0oVu7znnvkTCba1pG7ykmcRZWBCn3zFjeXDbCd2x3bosva3LnOWuyIMOee3Ez8vh_h1UHPVbB1Y6erCAkEHZYq0z5BVY5OBMIVOyKcHrgJGiU6QQacqsI-CERrN4fwDpSze9:1vQ45I:jeWdDmoEYHedKHAFZ4f7ipcDNQvL4u5gDK1OkR4uEiQ','2025-12-15 13:36:56.139086'),('gwd51vx8asjnabb9pk8etm99hy6gqpyw','.eJxVjMEOwiAQRP-FsyEplN3i0bvfQHZZKlVDk9KeGv9dmvSgmdubN7OrQNuaw1bTEiZRVzVYdfmFTPGVytHIk8pj1nEu6zKxPhR9tlXfZ0nv2-n-HWSqua0RRyKTPDF31rlewABxIuCWTtDjwGBGNN43mJg9I7BYduAcxF59vihdOK4:1vaTyj:e-WdJljDhqKQ3y6wLWyd-5DB31qCYmmeSXANWGYxJDg','2026-01-13 07:17:13.501556'),('i11834dvzusqqo6shanrjsv10n2odrck','.eJxVjMEOwiAQRP-FsyEplN3i0bvfQHZZKlVDk9KeGv9dmvSgmdubN7OrQNuaw1bTEiZRVzVYdfmFTPGVytHIk8pj1nEu6zKxPhR9tlXfZ0nv2-n-HWSqua0RRyKTPDF31rlewABxIuCWTtDjwGBGNN43mJg9I7BYduAcxF59vihdOK4:1vdnG7:G9uMBHAVlULtwted7cbi58gmP4RNNp0_yC7vo3MlxKY','2026-01-22 10:28:51.683143'),('i56masm0owpx321n2mz68puuusc1z2g5','.eJxVjEEOwiAQRe_C2hCawgAu3XsGMsMMUjU0Ke3KeHdt0oVu_3vvv1TCba1p67KkidVZOa9OvyNhfkjbCd-x3Wad57YuE-ld0Qft-jqzPC-H-3dQsddvjegshZwRo8Ag1hoogxHrwBnyEqxQQYAywhgCU4wFLYMQUGYfiqj3ByolOUA:1vQ3b7:YLGI1qfBINUmIXoc9dPRCOqzo7oL1fOE3uj_TwkMQD0','2025-12-15 13:05:45.011229'),('j2cx7pbdha6tqgmou5hevttskclkdluc','.eJxVjMsOwiAQRf-FtSE8B3Hpvt9ABhikaiAp7cr479qkC93ec859sYDbWsM2aAlzZhdm2el3i5ge1HaQ79hunafe1mWOfFf4QQefeqbn9XD_DiqO-q2dRFQpki8OgJRwGZV2YD2AIpSg0RYRVbbRm7Mg9D5rF40xAop0WrL3B-A0N0Y:1vMPGM:r8aym6N6m_iEP0eaSfqDwzDdyN1b3cp4zSS5p3WkQog','2025-12-05 11:25:14.349313'),('jjvud5dljq8aary1l89w256q58st2fsp','.eJxVjMEOwiAQRP-FsyEplN3i0bvfQHZZKlVDk9KeGv9dmvSgmdubN7OrQNuaw1bTEiZRVzVYdfmFTPGVytHIk8pj1nEu6zKxPhR9tlXfZ0nv2-n-HWSqua0RRyKTPDF31rlewABxIuCWTtDjwGBGNN43mJg9I7BYduAcxF59vihdOK4:1vdpYv:6_4FoijtBpFv3BEJ5fC95F79nDwlQJfmm5dwPqCCjsg','2026-01-22 12:56:25.333568'),('m1tvvtxtvv130ckshcb4n5keb6mbrtcs','.eJxVjMsOwiAQRf-FtSHAUB4u3fsNZGAmUjWQlHZl_Hdt0oVu7znnvkTCba1pG7ykmcRZWBCn3zFjeXDbCd2x3bosva3LnOWuyIMOee3Ez8vh_h1UHPVbB1Y6erCAkEHZYq0z5BVY5OBMIVOyKcHrgJGiU6QQacqsI-CERrN4fwDpSze9:1vQNVp:1zFYW_aqw7LZNNlkoOkwbG3Y_2KYdRBp0ZebizSmKqM','2025-12-16 10:21:37.384925'),('meeh7r8mpu97ho4n6ppjpsfcy05jwq0r','.eJxVjDsOwjAQBe_iGln-26GkzxmsXa-DA8iW4qRC3J1ESgHtm5n3ZhG2tcSt5yXOxK7MCHb5HRHSM9eD0APqvfHU6rrMyA-Fn7TzsVF-3U7376BAL3utDBgXUAVFBpNPdggpeEFJG0JvhFVgM-aJ9ISY0e1IDlJqAgdeSsk-Xw4qOFI:1vlm0f:FbptHxueKhMvDiQHTOyvbmT22CUuegZYPvayI_zN6rg','2026-02-13 10:45:53.495016'),('mfn5ygohwk5wrdjsee3b6nl0liofl990','.eJxVjDsOwjAQBe_iGln-xFpDSc8ZrF3vGgeQI8VJhbg7spQC2jcz760S7ltNe5c1zawuKhh1-h0J81PaIPzAdl90Xtq2zqSHog_a9W1heV0P9--gYq-jZsxU0Ev0QE4Kee8kAE8lAKGJRjwAFc4hsvHWTRTOBcEWS2Akgvp8AUEDOPI:1vPxTu:nJGZnebvCW6cWBz8h5D26h6teRS5ynZd47fyW9P2dfg','2025-12-15 06:33:54.033614'),('o3ncl0l9k58sylpovje99l3var2giahe','.eJxVjEEOwiAQRe_C2hAGCgWX7j0DGZhBqoYmpV0Z765NutDtf-_9l4i4rTVunZc4kTgLDeL0OybMD247oTu22yzz3NZlSnJX5EG7vM7Ez8vh_h1U7PVbh6yM0Rw0ORxDogA8jJlMUgUIPWlnCqiSBnbeWMhgrYUCHlgVBZjE-wMGszfv:1vOWB9:BQmh8mUhY2zejiX2CYURjDQGmR6T9lc8uVqYz9RWFOc','2025-12-11 07:12:35.374660'),('p8kylmbkc96hnktj23xm2gehubegdzru','.eJxVjE0OwiAYRO_C2hBpCwWX7j0D-f6QqoGktCvj3W2TLnQ3mfdm3irCuuS4NpnjxOqijFGn3xKBnlJ2wg8o96qplmWeUO-KPmjTt8ryuh7u30GGlre1UKIenOe-Ax4EzZiMQ06yBUL2FLxA4u4MPQRjEQN5k9xgyaJ3o1WfL1LaOYs:1vMifv:_wsTKTYm5ktvWMbZct7BxsU8wqijN_HZ-ReonWUJz5g','2025-12-06 08:08:55.865230'),('pz9qtw7zet1p32zh6yq5nfx3pn4mwtop','.eJxVjDsOwjAQBe_iGln-26GkzxmsXa-DA8iW4qRC3J1ESgHtm5n3ZhG2tcSt5yXOxK7MCHb5HRHSM9eD0APqvfHU6rrMyA-Fn7TzsVF-3U7376BAL3utDBgXUAVFBpNPdggpeEFJG0JvhFVgM-aJ9ISY0e1IDlJqAgdeSsk-Xw4qOFI:1vUOX4:jQnY5cAGForM--vmD2PSu-d3tsifNbZwhJy8vfPm8kk','2025-12-27 12:15:30.646507'),('qwg8dpnx19u9i7q23yxwdyx8ncbadkyt','.eJxVjEEOwiAQRe_C2hCwUBiX7nsGMsxMpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uLcur0u2Wkh9Qd8B3rbdY013WZst4VfdCmh5nleT3cv4OCrXxrMGOwjj0ZgC4iGkMBOn_OOZIEBGej7xHYWBMdA5HDUWKU3lEGZlHvD9GlOBg:1vIhLq:sofuMkpuIEcHD75CFdkJhP7y5w8oGjaJt6Af06nLiMg','2025-11-25 05:55:34.234863'),('qwqwyfnk4i0jd4ko49lmkx1e402y48ep','.eJxVjDsOwjAQBe_iGln-26GkzxmsXa-DA8iW4qRC3J1ESgHtm5n3ZhG2tcSt5yXOxK7MCHb5HRHSM9eD0APqvfHU6rrMyA-Fn7TzsVF-3U7376BAL3utDBgXUAVFBpNPdggpeEFJG0JvhFVgM-aJ9ISY0e1IDlJqAgdeSsk-Xw4qOFI:1vRUXI:5nkBcexACoF71eS_zJvr11K8Wucl9TeLDQSJw30hspA','2025-12-19 12:03:44.629144'),('rg6glh42ibe6g3dqt0eqyrnzfq9ch4d4','.eJxVjDsOwyAQRO9CHSHEZzEp0-cMaFmW4CTCkrErK3ePLblIppz3ZjYRcV1qXDvPccziKrQSl98yIb24HSQ_sT0mSVNb5jHJQ5En7fI-ZX7fTvfvoGKv-1oNkMEbBOOUdkQOA2kuiKD8nqxdstYDMHsbCpnsS2FnAlkzWFBafL70dDeM:1vNQDE:wFqsGbiskbk0xhpRV0BC8u9FziQoYLGr_zPqs6KIhJE','2025-12-08 06:38:12.088379'),('rpkvqs3uvu2qo3qe2nhq0dghgfplsox1','.eJxVjDsOwjAQBe_iGln-26GkzxmsXa-DA8iW4qRC3J1ESgHtm5n3ZhG2tcSt5yXOxK7MCHb5HRHSM9eD0APqvfHU6rrMyA-Fn7TzsVF-3U7376BAL3utDBgXUAVFBpNPdggpeEFJG0JvhFVgM-aJ9ISY0e1IDlJqAgdeSsk-Xw4qOFI:1vOZc3:kqjkZTD52cxg8NHxOFUF8S0pYLrwvzq-RHBlLRJOx4Q','2025-12-11 10:52:35.247080'),('ru2p99rojqrnbpahrhyykovj75pfkkoo','.eJxVjEEOwiAQRe_C2hCgUxhcuvcMzQCDVA0kpV0Z765NutDtf-_9l5hoW8u0dV6mOYmzQC9Ov2Og-OC6k3Snemsytrouc5C7Ig_a5bUlfl4O9--gUC_f2oLyxocc4qDAhhQxMTBb7YwB1uD0CEYjZYxZWRxGT47AZmRUaXRRvD8DljfB:1vaWsi:WzE85dQMrziKnoMJMOdOlgZ0gDb1FkbLAByGGK7U37o','2026-01-13 10:23:12.511628'),('t5m3naurcbahf3k0yjdqeyqicrg48nxz','.eJxVjDEOwjAMRe-SGUVODE3KyM4ZIsd2SAG1UtNOiLtDpQ6w_vfef5lE61LT2nROg5izCd4cfsdM_NBxI3Kn8TZZnsZlHrLdFLvTZq-T6POyu38HlVr91pkl-x57Rzm4KIUB2YFqVxBiVEVkPAEjewckAdhh6aRAJOmPUZ15fwAhtDiA:1vRsLQ:RR0JFJKC2j0_a0Z0Y0wLqEFjsfhOnaKxntuZQcMTvSs','2025-12-20 13:29:04.967578'),('uxl7rselxqngk6on9cgmvum1eg6fu1wz','.eJxVjMsOwiAQRf-FtSEMjwou3fcbyAwMUjU0Ke3K-O_apAvd3nPOfYmI21rj1nmJUxYXAUqcfkfC9OC2k3zHdptlmtu6TCR3RR60y3HO_Lwe7t9BxV6_dXIIXiORhmyBDLlSEhuDmgmV56Adkx3OAwR2ZEPxplhjVUmAQMWL9wcjTziv:1vMOZe:5fe_qIYBmdf-JSNZpTDxIxt9xt724Oz48WdHp8hFqis','2025-12-05 10:41:06.682059'),('wcpwfl1lugj63j3f76l9xct64lxg3u4e','.eJxVjEEOwiAQRe_C2hCwUBiX7nsGMsxMpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uLcur0u2Wkh9Qd8B3rbdY013WZst4VfdCmh5nleT3cv4OCrXxrMGOwjj0ZgC4iGkMBOn_OOZIEBGej7xHYWBMdA5HDUWKU3lEGZlHvD9GlOBg:1vMR1g:1vlXYZYgvMlKV_ZkJoksDS8vFazVCfXsYtK8yYBOhV0','2025-12-05 13:18:12.590370'),('wmn9l7ytpa795dxak7zdgrj2t0g2bz3h','.eJxVjMEOwiAQRP-FsyHQZQU8evcbCOyCVA1NSnsy_rtt0oPeJvPezFuEuC41rD3PYWRxEShOv12K9MxtB_yI7T5Jmtoyj0nuijxol7eJ8-t6uH8HNfa6rdUZEBmoKFaFLJlit4SEqAZtNFmDxUNB7QkHBlA5JY8WorNonQPx-QLOXzbo:1vLKKV:S25G5JUFgWAf-WItG5ay9AdT1ThF41ljJeYl2aGM594','2025-12-02 11:57:03.254968'),('zju1ha5x4i6t0xgy6bqad6b06gfdg4l6','.eJxVjDsOwjAQBe_iGln-26GkzxmsXa-DA8iW4qRC3J1ESgHtm5n3ZhG2tcSt5yXOxK7MCHb5HRHSM9eD0APqvfHU6rrMyA-Fn7TzsVF-3U7376BAL3utDBgXUAVFBpNPdggpeEFJG0JvhFVgM-aJ9ISY0e1IDlJqAgdeSsk-Xw4qOFI:1vfwZn:Ex--3GdgVgx3RxV22f_dUTI2LUQg7dpfu4o4BpQF77k','2026-01-28 08:50:03.264502');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors_doctor`
--

DROP TABLE IF EXISTS `doctors_doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors_doctor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `specialization` varchar(100) NOT NULL,
  `hospital_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `status` varchar(20) NOT NULL,
  `department_id` bigint DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `doctors_doctor_hospital_id_6add0b9b_fk_rhms_hospitals_id` (`hospital_id`),
  KEY `doctors_doctor_department_id_9373bfe8_fk_hospitals_department_id` (`department_id`),
  CONSTRAINT `doctors_doctor_department_id_9373bfe8_fk_hospitals_department_id` FOREIGN KEY (`department_id`) REFERENCES `hospitals_department` (`id`),
  CONSTRAINT `doctors_doctor_hospital_id_6add0b9b_fk_rhms_hospitals_id` FOREIGN KEY (`hospital_id`) REFERENCES `rhms_hospitals` (`id`),
  CONSTRAINT `doctors_doctor_user_id_c371de6c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors_doctor`
--

LOCK TABLES `doctors_doctor` WRITE;
/*!40000 ALTER TABLE `doctors_doctor` DISABLE KEYS */;
INSERT INTO `doctors_doctor` VALUES (19,'Neurology',83,83,1,'approved',20,'Dr. Test 1'),(20,'Cardiology',83,84,1,'approved',22,'Dr. Test 2'),(21,'Orthopedics',84,85,1,'approved',25,'Dr. Test 3'),(22,'Orthopedics',84,86,1,'approved',23,'Dr. Test 4'),(23,'Cardiology',85,87,1,'approved',28,'Dr. Test 5'),(24,'Neurology',85,88,1,'approved',27,'Dr. Test 6'),(25,'Cardiology',86,106,1,'approved',NULL,'Dr. Search Test'),(76,'Neurology',83,275,1,'approved',21,'Dr. Abdul Ganesan'),(77,'Neurology',84,276,1,'approved',24,'Dr. Krish Chaudhry'),(78,'Cardiology',85,277,1,'approved',26,'Dr. Krishna Sagar'),(79,'Orthopedics',88,278,1,'approved',29,'Dr. Samar Mammen'),(80,'Cardiology',88,279,1,'approved',30,'Dr. Atharv Pant'),(81,'Oncology',88,280,1,'approved',31,'Dr. Yashodhara Balakrishnan'),(82,'Orthopedics',89,281,1,'approved',32,'Dr. Kala Srinivas'),(83,'Pediatrics',89,282,1,'approved',33,'Dr. Alexander Mittal'),(84,'Oncology',89,283,1,'approved',34,'Dr. Aahana Bhavsar'),(85,'Dermatology',90,284,1,'approved',35,'Dr. Ekaja Sarma'),(86,'Cardiology',90,285,1,'approved',36,'Dr. Ryan Kamdar'),(87,'Neurology',90,286,1,'approved',37,'Dr. Nathaniel Rajagopalan'),(88,'Cardiology',91,287,1,'approved',38,'Dr. Abhimanyu Borah'),(89,'Orthopedics',91,288,1,'approved',39,'Dr. Suhani Raval'),(90,'Dermatology',91,289,1,'approved',40,'Dr. Yug Khosla'),(91,'Pediatrics',92,290,1,'approved',41,'Dr. Harrison Zachariah'),(92,'Cardiology',92,291,1,'approved',42,'Dr. Siya Dhar'),(93,'Oncology',92,292,1,'approved',43,'Dr. Irya Chandra'),(94,'Orthopedics',93,293,1,'approved',44,'Dr. Ayush Sathe'),(95,'Neurology',93,294,1,'approved',45,'Dr. Tarak Ganesh'),(96,'Oncology',93,295,1,'approved',46,'Dr. Udarsh Barad'),(97,'Dermatology',94,296,1,'approved',47,'Dr. Joshua Puri'),(98,'Neurology',94,297,1,'approved',48,'Dr. Ikshita Vala'),(99,'Pediatrics',94,298,1,'approved',49,'Dr. Ayush Kari'),(100,'Orthopedics',95,299,1,'approved',50,'Dr. Jagrati Hari'),(101,'Cardiology',95,300,1,'approved',51,'Dr. Zinal Vasa'),(102,'Oncology',95,301,1,'approved',52,'Dr. Manya Patla'),(103,'Cardiology',96,302,1,'approved',53,'Dr. Bhavya Dugar'),(104,'Orthopedics',96,303,1,'approved',54,'Dr. Radhika Gopal'),(105,'Neurology',96,304,1,'approved',55,'Dr. Vanya Chaudhari'),(106,'Neurology',97,305,1,'approved',56,'Dr. Jhalak Lal'),(107,'Pediatrics',97,306,1,'approved',57,'Dr. Zashil Seshadri'),(108,'Dermatology',97,307,1,'approved',58,'Dr. Upasna Naik');
/*!40000 ALTER TABLE `doctors_doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors_doctor_treatments`
--

DROP TABLE IF EXISTS `doctors_doctor_treatments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors_doctor_treatments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `doctor_id` bigint NOT NULL,
  `treatment_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `doctors_doctor_treatments_doctor_id_treatment_id_67599be4_uniq` (`doctor_id`,`treatment_id`),
  KEY `doctors_doctor_treat_treatment_id_3a17d7ae_fk_hospitals` (`treatment_id`),
  CONSTRAINT `doctors_doctor_treat_doctor_id_76f1b1e6_fk_doctors_d` FOREIGN KEY (`doctor_id`) REFERENCES `doctors_doctor` (`id`),
  CONSTRAINT `doctors_doctor_treat_treatment_id_3a17d7ae_fk_hospitals` FOREIGN KEY (`treatment_id`) REFERENCES `hospitals_treatment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=210 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors_doctor_treatments`
--

LOCK TABLES `doctors_doctor_treatments` WRITE;
/*!40000 ALTER TABLE `doctors_doctor_treatments` DISABLE KEYS */;
INSERT INTO `doctors_doctor_treatments` VALUES (38,19,43),(39,19,46),(40,20,43),(12,21,58),(13,21,59),(14,21,60),(30,22,52),(31,22,53),(32,22,54),(33,23,67),(34,23,68),(35,23,69),(21,24,64),(22,24,65),(23,24,66),(142,76,46),(143,76,47),(141,76,48),(146,77,55),(144,77,56),(145,77,57),(147,78,61),(148,78,62),(149,78,63),(150,79,70),(151,79,71),(152,80,72),(153,80,73),(154,81,74),(155,81,75),(156,82,76),(157,82,77),(158,83,78),(159,83,79),(160,84,80),(161,84,81),(162,85,82),(163,85,83),(164,86,84),(165,86,85),(166,87,86),(167,87,87),(168,88,88),(169,88,89),(170,89,90),(171,89,91),(172,90,92),(173,90,93),(174,91,94),(175,91,95),(176,92,96),(177,92,97),(178,93,98),(179,93,99),(180,94,100),(181,94,101),(182,95,102),(183,95,103),(184,96,104),(185,96,105),(186,97,106),(187,97,107),(188,98,108),(189,98,109),(190,99,110),(191,99,111),(192,100,112),(193,100,113),(194,101,114),(195,101,115),(196,102,116),(197,102,117),(198,103,118),(199,103,119),(200,104,120),(201,104,121),(202,105,122),(203,105,123),(204,106,124),(205,106,125),(206,107,126),(207,107,127),(208,108,128),(209,108,129);
/*!40000 ALTER TABLE `doctors_doctor_treatments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors_doctoravailability`
--

DROP TABLE IF EXISTS `doctors_doctoravailability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors_doctoravailability` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `start_time` longtext NOT NULL,
  `end_time` time(6) NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `doctor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `doctors_doctoravaila_doctor_id_541fd516_fk_accounts_` (`doctor_id`),
  CONSTRAINT `doctors_doctoravaila_doctor_id_541fd516_fk_accounts_` FOREIGN KEY (`doctor_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors_doctoravailability`
--

LOCK TABLES `doctors_doctoravailability` WRITE;
/*!40000 ALTER TABLE `doctors_doctoravailability` DISABLE KEYS */;
/*!40000 ALTER TABLE `doctors_doctoravailability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospitals_department`
--

DROP TABLE IF EXISTS `hospitals_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospitals_department` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `hospital_id` bigint NOT NULL,
  `code` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hospitals_department_hospital_id_5094d311_fk_rhms_hospitals_id` (`hospital_id`),
  CONSTRAINT `hospitals_department_hospital_id_5094d311_fk_rhms_hospitals_id` FOREIGN KEY (`hospital_id`) REFERENCES `rhms_hospitals` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospitals_department`
--

LOCK TABLES `hospitals_department` WRITE;
/*!40000 ALTER TABLE `hospitals_department` DISABLE KEYS */;
INSERT INTO `hospitals_department` VALUES (18,'General Medicine',82,'GEN'),(19,'Dentistry',82,'GEN'),(20,'Cardiology',83,'GEN'),(21,'Neurology',83,'GEN'),(22,'Orthopedics',83,'GEN'),(23,'Cardiology',84,'GEN'),(24,'Neurology',84,'GEN'),(25,'Orthopedics',84,'GEN'),(26,'Cardiology',85,'GEN'),(27,'Neurology',85,'GEN'),(28,'Orthopedics',85,'GEN'),(29,'Orthopedics',88,'ORT31'),(30,'Cardiology',88,'CAR49'),(31,'Oncology',88,'ONC81'),(32,'Orthopedics',89,'ORT28'),(33,'Pediatrics',89,'PED30'),(34,'Oncology',89,'ONC22'),(35,'Dermatology',90,'DER88'),(36,'Cardiology',90,'CAR98'),(37,'Neurology',90,'NEU52'),(38,'Cardiology',91,'CAR66'),(39,'Orthopedics',91,'ORT10'),(40,'Dermatology',91,'DER76'),(41,'Pediatrics',92,'PED23'),(42,'Cardiology',92,'CAR61'),(43,'Oncology',92,'ONC86'),(44,'Orthopedics',93,'ORT18'),(45,'Neurology',93,'NEU53'),(46,'Oncology',93,'ONC70'),(47,'Dermatology',94,'DER35'),(48,'Neurology',94,'NEU52'),(49,'Pediatrics',94,'PED92'),(50,'Orthopedics',95,'ORT31'),(51,'Cardiology',95,'CAR12'),(52,'Oncology',95,'ONC56'),(53,'Cardiology',96,'CAR45'),(54,'Orthopedics',96,'ORT42'),(55,'Neurology',96,'NEU18'),(56,'Neurology',97,'NEU60'),(57,'Pediatrics',97,'PED50'),(58,'Dermatology',97,'DER12');
/*!40000 ALTER TABLE `hospitals_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospitals_hospitaladmin`
--

DROP TABLE IF EXISTS `hospitals_hospitaladmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospitals_hospitaladmin` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `hospital_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `hospitals_hospitalad_hospital_id_40f1320f_fk_rhms_hosp` (`hospital_id`),
  CONSTRAINT `hospitals_hospitalad_hospital_id_40f1320f_fk_rhms_hosp` FOREIGN KEY (`hospital_id`) REFERENCES `rhms_hospitals` (`id`),
  CONSTRAINT `hospitals_hospitaladmin_user_id_72ddd2da_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospitals_hospitaladmin`
--

LOCK TABLES `hospitals_hospitaladmin` WRITE;
/*!40000 ALTER TABLE `hospitals_hospitaladmin` DISABLE KEYS */;
INSERT INTO `hospitals_hospitaladmin` VALUES (31,81,82),(32,89,83),(33,90,84),(34,91,85),(55,261,89),(56,262,85),(57,263,83),(58,264,96),(59,265,95),(60,266,81),(61,267,87),(62,268,88),(63,269,90),(64,270,91),(65,271,92),(66,272,93),(67,273,94),(68,274,97);
/*!40000 ALTER TABLE `hospitals_hospitaladmin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospitals_treatment`
--

DROP TABLE IF EXISTS `hospitals_treatment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospitals_treatment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `department_id` bigint NOT NULL,
  `hospital_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hospitals_treatment_department_id_6a911c50_fk_hospitals` (`department_id`),
  KEY `hospitals_treatment_hospital_id_e10bfbb1_fk_rhms_hospitals_id` (`hospital_id`),
  CONSTRAINT `hospitals_treatment_department_id_6a911c50_fk_hospitals` FOREIGN KEY (`department_id`) REFERENCES `hospitals_department` (`id`),
  CONSTRAINT `hospitals_treatment_hospital_id_e10bfbb1_fk_rhms_hospitals_id` FOREIGN KEY (`hospital_id`) REFERENCES `rhms_hospitals` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospitals_treatment`
--

LOCK TABLES `hospitals_treatment` WRITE;
/*!40000 ALTER TABLE `hospitals_treatment` DISABLE KEYS */;
INSERT INTO `hospitals_treatment` VALUES (39,'General Consultation',18,82),(40,'Blood Test (CBC)',18,82),(41,'ECG',18,82),(42,'Dental Cleaning',19,82),(43,'ECG',20,83),(44,'Angiography',20,83),(45,'Heart Surgery',20,83),(46,'MRI Scan',21,83),(47,'EEG',21,83),(48,'Brain Mapping',21,83),(49,'X-Ray',22,83),(50,'Fracture Repair',22,83),(51,'Physiotherapy',22,83),(52,'ECG',23,84),(53,'Angiography',23,84),(54,'Heart Surgery',23,84),(55,'MRI Scan',24,84),(56,'EEG',24,84),(57,'Brain Mapping',24,84),(58,'X-Ray',25,84),(59,'Fracture Repair',25,84),(60,'Physiotherapy',25,84),(61,'ECG',26,85),(62,'Angiography',26,85),(63,'Heart Surgery',26,85),(64,'MRI Scan',27,85),(65,'EEG',27,85),(66,'Brain Mapping',27,85),(67,'X-Ray',28,85),(68,'Fracture Repair',28,85),(69,'Physiotherapy',28,85),(70,'Orthopedics Consultation',29,88),(71,'Orthopedics Surgery',29,88),(72,'Cardiology Consultation',30,88),(73,'Cardiology Surgery',30,88),(74,'Oncology Consultation',31,88),(75,'Oncology Surgery',31,88),(76,'Orthopedics Consultation',32,89),(77,'Orthopedics Surgery',32,89),(78,'Pediatrics Consultation',33,89),(79,'Pediatrics Surgery',33,89),(80,'Oncology Consultation',34,89),(81,'Oncology Surgery',34,89),(82,'Dermatology Consultation',35,90),(83,'Dermatology Surgery',35,90),(84,'Cardiology Consultation',36,90),(85,'Cardiology Surgery',36,90),(86,'Neurology Consultation',37,90),(87,'Neurology Surgery',37,90),(88,'Cardiology Consultation',38,91),(89,'Cardiology Surgery',38,91),(90,'Orthopedics Consultation',39,91),(91,'Orthopedics Surgery',39,91),(92,'Dermatology Consultation',40,91),(93,'Dermatology Surgery',40,91),(94,'Pediatrics Consultation',41,92),(95,'Pediatrics Surgery',41,92),(96,'Cardiology Consultation',42,92),(97,'Cardiology Surgery',42,92),(98,'Oncology Consultation',43,92),(99,'Oncology Surgery',43,92),(100,'Orthopedics Consultation',44,93),(101,'Orthopedics Surgery',44,93),(102,'Neurology Consultation',45,93),(103,'Neurology Surgery',45,93),(104,'Oncology Consultation',46,93),(105,'Oncology Surgery',46,93),(106,'Dermatology Consultation',47,94),(107,'Dermatology Surgery',47,94),(108,'Neurology Consultation',48,94),(109,'Neurology Surgery',48,94),(110,'Pediatrics Consultation',49,94),(111,'Pediatrics Surgery',49,94),(112,'Orthopedics Consultation',50,95),(113,'Orthopedics Surgery',50,95),(114,'Cardiology Consultation',51,95),(115,'Cardiology Surgery',51,95),(116,'Oncology Consultation',52,95),(117,'Oncology Surgery',52,95),(118,'Cardiology Consultation',53,96),(119,'Cardiology Surgery',53,96),(120,'Orthopedics Consultation',54,96),(121,'Orthopedics Surgery',54,96),(122,'Neurology Consultation',55,96),(123,'Neurology Surgery',55,96),(124,'Neurology Consultation',56,97),(125,'Neurology Surgery',56,97),(126,'Pediatrics Consultation',57,97),(127,'Pediatrics Surgery',57,97),(128,'Dermatology Consultation',58,97),(129,'Dermatology Surgery',58,97);
/*!40000 ALTER TABLE `hospitals_treatment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications_notification`
--

DROP TABLE IF EXISTS `notifications_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_notification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `level` varchar(20) NOT NULL,
  `unread` tinyint(1) NOT NULL,
  `actor_object_id` varchar(255) NOT NULL,
  `verb` varchar(255) NOT NULL,
  `description` longtext,
  `target_object_id` varchar(255) DEFAULT NULL,
  `action_object_object_id` varchar(255) DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `public` tinyint(1) NOT NULL,
  `action_object_content_type_id` int DEFAULT NULL,
  `actor_content_type_id` int NOT NULL,
  `recipient_id` bigint NOT NULL,
  `target_content_type_id` int DEFAULT NULL,
  `deleted` tinyint(1) NOT NULL,
  `emailed` tinyint(1) NOT NULL,
  `data` longtext,
  PRIMARY KEY (`id`),
  KEY `notifications_notifi_action_object_conten_7d2b8ee9_fk_django_co` (`action_object_content_type_id`),
  KEY `notifications_notifi_actor_content_type_i_0c69d7b7_fk_django_co` (`actor_content_type_id`),
  KEY `notifications_notifi_target_content_type__ccb24d88_fk_django_co` (`target_content_type_id`),
  KEY `notifications_notification_deleted_b32b69e6` (`deleted`),
  KEY `notifications_notification_emailed_23a5ad81` (`emailed`),
  KEY `notifications_notification_public_1bc30b1c` (`public`),
  KEY `notifications_notification_unread_cce4be30` (`unread`),
  KEY `notifications_notification_timestamp_6a797bad` (`timestamp`),
  KEY `notificatio_recipie_8bedf2_idx` (`recipient_id`,`unread`),
  CONSTRAINT `notifications_notifi_action_object_conten_7d2b8ee9_fk_django_co` FOREIGN KEY (`action_object_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `notifications_notifi_actor_content_type_i_0c69d7b7_fk_django_co` FOREIGN KEY (`actor_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `notifications_notifi_recipient_id_d055f3f0_fk_accounts_` FOREIGN KEY (`recipient_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `notifications_notifi_target_content_type__ccb24d88_fk_django_co` FOREIGN KEY (`target_content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_notification`
--

LOCK TABLES `notifications_notification` WRITE;
/*!40000 ALTER TABLE `notifications_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients_notification`
--

DROP TABLE IF EXISTS `patients_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `patients_notification_patient_id_47d85b9d_fk_patients_patient_id` (`patient_id`),
  CONSTRAINT `patients_notification_patient_id_47d85b9d_fk_patients_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients_notification`
--

LOCK TABLES `patients_notification` WRITE;
/*!40000 ALTER TABLE `patients_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `patients_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients_patient`
--

DROP TABLE IF EXISTS `patients_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients_patient` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `age` int unsigned NOT NULL,
  `gender` varchar(10) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `user_id` bigint NOT NULL,
  `hospital_id` bigint DEFAULT NULL,
  `medical_history` longtext,
  `photo` varchar(100) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `patients_patient_hospital_id_e0c73902_fk_rhms_hospitals_id` (`hospital_id`),
  CONSTRAINT `patients_patient_hospital_id_e0c73902_fk_rhms_hospitals_id` FOREIGN KEY (`hospital_id`) REFERENCES `rhms_hospitals` (`id`),
  CONSTRAINT `patients_patient_user_id_b53513b7_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `patients_patient_chk_1` CHECK ((`age` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients_patient`
--

LOCK TABLES `patients_patient` WRITE;
/*!40000 ALTER TABLE `patients_patient` DISABLE KEYS */;
INSERT INTO `patients_patient` VALUES (13,0,'Other','9857675889','',92,90,NULL,'',''),(14,0,'Other','09879647227','',81,96,NULL,'',''),(15,0,'Other','09879647227','',93,90,NULL,'',''),(16,0,'Other','9857675889','',94,84,NULL,'',''),(17,0,'Other','9857675889','',95,92,NULL,'',''),(18,0,'Other','9857675889','',96,97,NULL,'',''),(19,0,'Other','9857675889','',97,87,NULL,'',''),(20,0,'Other','9857675889','',98,84,NULL,'',''),(21,24,'Female','','wrdd',99,97,NULL,'',''),(22,22,'Female','','qqww',100,95,NULL,'',''),(23,22,'Female','','qwe',101,91,NULL,'',''),(24,32,'Female','9998887777','qwe',102,90,NULL,'','Test User'),(25,32,'Male','','qwe',103,92,NULL,'',''),(26,23,'Female','7678983468','wwe',104,93,NULL,'','khushpathak'),(27,22,'Female','8752778543','12/qwe, ABC society, vadodara',105,90,NULL,'','khushi pathak'),(28,22,'Female','345357788998','qbc, Vadodara',107,90,NULL,'','khushi'),(29,22,'Male','25378373898','qwe, vadodara',108,90,NULL,'','bhavan'),(30,21,'Female','56272678887','qwe, vadodara',109,81,NULL,'','khush'),(91,19,'Male','5613911357','964, Patel Path, Karimnagar 449699',308,89,'Corporis beatae libero tenetur.','','Rudra Tara'),(92,36,'Other','2235280592','38/45\nDar Ganj\nRatlam 654659',309,97,'Qui error provident aliquid.','','Maanas Sandal'),(93,49,'Other','+911593799949','411\nKaur Ganj, Phusro-439677',310,93,'Quo cumque quam eius ea.','','Nitara Joshi'),(94,43,'Female','5259435649','60/06, Pillai Path, Durg-195012',311,93,'Quisquam nostrum illum.','','Gaurangi Pant'),(95,48,'Male','+914979735849','H.No. 269, Sekhon Ganj, Ichalkaranji 223608',312,97,'Optio error dolores.','','Ijaya Singhal'),(96,42,'Other','4749234464','77, Mishra Circle, Nagaon-922275',313,91,'Quisquam ipsa doloribus aliquam numquam.','','Libni Aurora'),(97,53,'Other','3846094670','H.No. 60\nRamesh Chowk\nMunger 630266',314,96,'Corporis occaecati distinctio sit libero maxime autem rem.','','Harita Mani'),(98,42,'Other','+914986098591','92/70\nAggarwal Path, Raebareli-683245',315,97,'Laborum magni hic quae.','','Lavanya Soman'),(99,80,'Male','+911650019686','051, Boase Circle, Gurgaon 970750',316,84,'Quos hic voluptate error.','','Dalbir Kulkarni'),(100,44,'Other','08263636252','59/897, Bakshi Road\nBallia 284073',317,83,'Fugiat dolores cupiditate voluptas fugit expedita sint.','','Chasmum Bal'),(101,77,'Male','01072895410','H.No. 00\nCheema Road, Sonipat-006759',318,84,'Optio dolor sit.','','Ishanvi Bakshi'),(102,43,'Female','+914066381347','61/653\nDua Nagar\nKulti-291051',319,94,'Sit doloremque dicta fuga quidem repellat veniam aperiam.','','Janaki Kannan'),(103,19,'Other','+910300103636','H.No. 50\nMandal Path, Vellore-645960',320,91,'Soluta commodi reiciendis alias.','','Jeet Tella'),(104,62,'Female','+911968587309','H.No. 82\nBorah Street, Meerut 074423',321,92,'Facere nulla necessitatibus earum libero saepe.','','Jonathan Swamy'),(105,80,'Other','+912785885433','60/11\nGade Nagar\nDurg 083689',322,85,'Quo dolor possimus ipsam reprehenderit minus quo.','','Vinaya Barad'),(106,76,'Other','7832787872','506, Tank Road\nParbhani-557966',323,91,'Ullam nulla exercitationem praesentium sequi ipsa eius.','','Anthony Bose'),(107,53,'Other','03177527444','106, Konda Nagar\nMaheshtala 257732',324,91,'Dolores occaecati alias saepe.','','Tarak Sinha'),(108,51,'Other','+911304793325','48, Buch Ganj\nBahraich-180071',325,89,'Architecto nulla placeat dolorum possimus.','','Balveer Chaudhari'),(109,42,'Male','02230117544','544, Din Chowk, Shimoga-806250',326,91,'Earum doloremque ullam.','','Rehaan Devi'),(110,49,'Male','03921800188','H.No. 31\nBansal Zila, North Dumdum-886079',327,81,'Totam quo soluta nesciunt odio quia.','','Yachana Kapadia'),(111,60,'Other','3249053604','H.No. 61\nBail Path\nGhaziabad 799736',328,89,'Cumque aut impedit quam.','','Yashasvi Soman'),(112,38,'Male','08644439846','93/173, Choudhry Marg\nMeerut-842161',329,90,'Ducimus commodi beatae eaque.','','Kashish Som'),(113,39,'Male','04430785874','H.No. 703\nVasa Road\nBhagalpur-516015',330,97,'Pariatur iste unde.','','Reva Raja'),(114,49,'Female','+919738977796','73, Toor Zila\nKarawal Nagar-026864',331,87,'Cum id eos alias cum atque facilis.','','Arjun Sani'),(115,62,'Male','01635776566','51/931, Hayer Zila, Vijayanagaram 798254',332,90,'Architecto illum voluptatum est.','','Nidhi Rama'),(116,56,'Other','00273500654','152\nDeshmukh Zila\nNizamabad 986883',333,84,'Repudiandae nam non eum optio totam illo.','','Oni Sem'),(117,25,'Female','2458513204','45/77, Mahajan\nKarnal 619503',334,92,'Quo aut a pariatur porro repudiandae.','','Prisha Choudhury'),(118,69,'Female','04192979186','83/798\nSathe Path\nMirzapur 048788',335,87,'Harum in rerum ullam eius maxime.','','Hemang Garde'),(119,52,'Male','0384030275','21\nSarin Road, Moradabad-411979',336,91,'Inventore facilis repellat iste eos.','','Rajeshri Purohit'),(120,45,'Female','2479978308','H.No. 24, Chaudry Path, Nandyal-104900',337,96,'Cumque quibusdam odit.','','Urvashi Iyer'),(121,34,'Female','05991144432','57/577\nRamanathan Road, Tiruchirappalli 737842',338,90,'Quos asperiores vero dolorum laudantium.','','Ucchal Balay'),(122,66,'Other','9801724709','H.No. 471\nSampath Path, Gorakhpur-739654',339,97,'Animi praesentium perspiciatis eveniet atque.','','Wriddhish Dhaliwal'),(123,55,'Male','6071179946','99/756, Om Marg\nNorth Dumdum-816234',340,81,'Neque repudiandae quidem nobis.','','Chatresh Thaman'),(124,75,'Other','4583377610','51, Upadhyay Ganj\nKolkata 939365',341,89,'Eos iure nulla assumenda eos.','','Lipika Nayak'),(125,78,'Male','05292725437','39, Parikh Zila\nRamagundam-278911',342,85,'Sequi nulla laudantium expedita sint.','','Hitesh Hegde'),(126,81,'Male','+916534356257','H.No. 786, Dutt Nagar, Sangli-Miraj & Kupwad-260784',343,90,'Odio iure qui iste quis doloribus.','','Christopher Chadha'),(127,60,'Other','08479178661','89/33\nNagi Marg\nSurendranagar Dudhrej 765946',344,89,'Nulla eaque reiciendis in blanditiis.','','Bhavani Deo'),(128,59,'Female','03227888584','H.No. 827, Badami Road\nJodhpur 510644',345,87,'Facilis laboriosam aliquid.','','Odika Murthy'),(129,37,'Male','06795523690','781\nDubey Path\nDarbhanga-876612',346,96,'Quidem dolorem vitae ex quo iure.','','Abhiram Sathe'),(130,84,'Female','+917213982084','35\nBahl Street, Howrah 464230',347,81,'Ab perspiciatis rerum vitae voluptates quis recusandae.','','Tanish Loyal'),(131,46,'Male','04002149166','H.No. 740, Hans Ganj\nDurgapur 868810',348,88,'Voluptate hic veritatis eaque tempora repellat distinctio.','','Widisha Sagar'),(132,18,'Female','+919059260927','H.No. 010, Krishnan Marg\nGorakhpur-941924',349,87,'Aliquam perspiciatis soluta repellendus aut.','','Lila Loke'),(133,84,'Other','03574660605','66/13, Sahota Circle\nDharmavaram-789128',350,87,'Commodi dolor sunt aliquid reprehenderit tenetur harum.','','Pranav Sastry'),(134,75,'Other','8965330849','H.No. 45, Parsa Street, Adoni-722674',351,84,'Hic quibusdam ab.','','Ronith Nagarajan'),(135,32,'Other','8943104952','626\nSehgal Zila, Guntakal 395442',352,91,'Modi vero id tempore laboriosam temporibus.','','Rachita Butala'),(136,82,'Other','7175942905','42, Gade Circle\nMuzaffarpur-441013',353,93,'Quisquam tempora velit numquam.','','Charvi Virk'),(137,75,'Male','+917456248686','58/81\nUppal Circle, Dhanbad-869051',354,97,'Iste id perspiciatis nam rem repudiandae ea nostrum.','','Warda Malhotra'),(138,83,'Female','06814989181','H.No. 77, Datta Zila, Rampur 357455',355,85,'Earum reprehenderit expedita tempora provident.','','Gaurav Arya'),(139,74,'Male','07111173269','51\nHari Path, Dharmavaram-812327',356,89,'Iste dolore quaerat voluptate facilis.','','Lavanya Kapoor'),(140,57,'Female','07723624140','78\nPanchal Ganj\nKozhikode 186258',357,96,'Laboriosam iure voluptatum.','','Raksha Deep'),(141,43,'Female','+913417385954','H.No. 72\nTak Zila\nDeoghar-839797',358,88,'Minus accusantium quisquam nesciunt tenetur.','','Owen Amble'),(142,79,'Female','07726014545','603\nRamachandran Path, Bhalswa Jahangir Pur 694104',359,87,'Ipsam in aut odio.','','Aarna More'),(143,44,'Other','+916008844901','H.No. 735\nRadhakrishnan Circle, Bhimavaram 114079',360,90,'Tempora ipsa soluta atque.','','Vasudha Nagi'),(144,71,'Female','04927245066','H.No. 776, Kibe Chowk\nBhiwandi-213993',361,85,'Cupiditate at sunt quaerat labore quibusdam.','','Wazir Divan'),(145,19,'Male','04814548200','H.No. 46\nParekh Chowk, Kottayam 120680',362,92,'In nisi ex quo molestias odio.','','Gautam Nayar'),(146,34,'Female','+913036860094','H.No. 508\nAcharya Path\nTirupati 512278',363,84,'Neque recusandae facilis nobis.','','Parth Pandya'),(147,37,'Female','+918565284086','H.No. 88, Mistry Nagar\nKatihar 621403',364,84,'Vel deserunt nam animi animi.','','Mahika Sampath'),(148,52,'Female','07016331446','H.No. 22, Kapur Circle, Aizawl-734528',365,83,'Ullam quo rerum ratione explicabo.','','Tristan Nair'),(149,43,'Male','+919532638902','14/120\nPandey Street, Pimpri-Chinchwad-991876',366,95,'Est optio nihil officia nulla asperiores.','','Zilmil Dada'),(150,46,'Male','+910874525524','451, Edwin Marg\nNadiad-351349',367,95,'Eos quod ratione aut corporis officiis.','','Urishilla Balay');
/*!40000 ALTER TABLE `patients_patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rhms_doctor_availabilities`
--

DROP TABLE IF EXISTS `rhms_doctor_availabilities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rhms_doctor_availabilities` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `doctor_id` bigint NOT NULL,
  `slot_duration` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rhms_doctor_availabiliti_doctor_id_date_start_tim_4d7e7da3_uniq` (`doctor_id`,`date`,`start_time`,`end_time`),
  CONSTRAINT `rhms_doctor_availabi_doctor_id_41c330a0_fk_doctors_d` FOREIGN KEY (`doctor_id`) REFERENCES `doctors_doctor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=246 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rhms_doctor_availabilities`
--

LOCK TABLES `rhms_doctor_availabilities` WRITE;
/*!40000 ALTER TABLE `rhms_doctor_availabilities` DISABLE KEYS */;
INSERT INTO `rhms_doctor_availabilities` VALUES (94,'2025-12-22','09:00:00.000000','17:00:00.000000',1,19,30),(95,'2025-12-23','09:00:00.000000','17:00:00.000000',1,19,30),(96,'2025-12-24','09:00:00.000000','17:00:00.000000',1,19,30),(97,'2025-12-22','09:00:00.000000','17:00:00.000000',1,20,30),(98,'2025-12-23','09:00:00.000000','17:00:00.000000',1,20,30),(99,'2025-12-24','09:00:00.000000','17:00:00.000000',1,20,30),(100,'2025-12-22','09:00:00.000000','17:00:00.000000',1,21,30),(101,'2025-12-23','09:00:00.000000','17:00:00.000000',1,21,30),(102,'2025-12-24','09:00:00.000000','17:00:00.000000',1,21,30),(103,'2025-12-22','09:00:00.000000','17:00:00.000000',1,23,30),(104,'2025-12-24','09:00:00.000000','17:00:00.000000',1,23,30),(105,'2025-12-23','09:00:00.000000','17:00:00.000000',1,23,30),(106,'2025-12-22','09:00:00.000000','17:00:00.000000',1,24,30),(107,'2025-12-23','09:00:00.000000','17:00:00.000000',1,24,30),(108,'2025-12-24','09:00:00.000000','17:00:00.000000',1,24,30),(109,'2026-01-05','09:00:00.000000','17:00:00.000000',1,19,30),(114,'2026-01-13','09:00:00.000000','17:00:00.000000',1,19,30),(121,'2026-01-16','09:00:00.000000','17:00:00.000000',1,19,30),(123,'2026-01-22','09:00:00.000000','17:00:00.000000',1,19,30),(124,'2026-01-23','09:00:00.000000','17:00:00.000000',1,19,30),(125,'2026-01-19','09:00:00.000000','17:00:00.000000',1,19,30),(127,'2026-01-06','09:00:00.000000','11:00:00.000000',1,19,15),(130,'2026-01-07','09:00:00.000000','17:00:00.000000',1,19,30),(132,'2026-01-15','09:00:00.000000','17:00:00.000000',1,19,30),(133,'2026-01-17','09:00:00.000000','17:00:00.000000',1,19,30),(134,'2026-01-08','09:00:00.000000','20:00:00.000000',1,19,30),(135,'2026-01-14','09:00:00.000000','11:00:00.000000',1,19,30),(136,'2026-01-09','09:00:00.000000','11:00:00.000000',1,19,30),(137,'2026-01-21','09:00:00.000000','17:00:00.000000',1,19,30),(138,'2026-01-10','09:00:00.000000','17:00:00.000000',1,19,30),(141,'2026-01-09','09:00:00.000000','17:00:00.000000',1,20,30),(142,'2026-01-10','09:00:00.000000','17:00:00.000000',1,20,30),(143,'2026-01-12','09:00:00.000000','17:00:00.000000',1,19,30),(144,'2026-01-20','09:00:00.000000','17:00:00.000000',1,19,30),(150,'2026-01-13','09:12:00.000000','17:00:00.000000',1,20,30),(151,'2026-01-14','09:12:00.000000','17:00:00.000000',1,20,30),(152,'2026-01-15','09:12:00.000000','17:00:00.000000',1,20,30),(153,'2026-01-16','09:12:00.000000','17:00:00.000000',1,20,30),(156,'2026-01-17','09:12:00.000000','09:42:00.000000',0,20,30),(157,'2026-01-17','09:42:00.000000','10:12:00.000000',0,20,30),(158,'2026-01-17','10:12:00.000000','10:42:00.000000',0,20,30),(159,'2026-01-17','10:42:00.000000','11:12:00.000000',0,20,30),(160,'2026-01-17','11:12:00.000000','11:42:00.000000',0,20,30),(161,'2026-01-17','11:42:00.000000','12:12:00.000000',0,20,30),(162,'2026-01-17','12:12:00.000000','12:42:00.000000',0,20,30),(163,'2026-01-17','12:42:00.000000','13:12:00.000000',0,20,30),(164,'2026-01-17','13:12:00.000000','13:42:00.000000',0,20,30),(165,'2026-01-17','13:42:00.000000','14:12:00.000000',1,20,30),(166,'2026-01-17','14:12:00.000000','14:42:00.000000',0,20,30),(167,'2026-01-17','14:42:00.000000','15:12:00.000000',1,20,30),(168,'2026-01-17','15:12:00.000000','15:42:00.000000',1,20,30),(169,'2026-01-17','15:42:00.000000','16:12:00.000000',1,20,30),(170,'2026-01-17','16:12:00.000000','16:42:00.000000',1,20,30),(171,'2026-01-18','09:12:00.000000','09:42:00.000000',0,20,30),(172,'2026-01-18','09:42:00.000000','10:12:00.000000',1,20,30),(173,'2026-01-18','10:12:00.000000','10:42:00.000000',1,20,30),(174,'2026-01-18','10:42:00.000000','11:12:00.000000',1,20,30),(175,'2026-01-18','11:12:00.000000','11:42:00.000000',1,20,30),(176,'2026-01-18','11:42:00.000000','12:12:00.000000',1,20,30),(177,'2026-01-18','12:12:00.000000','12:42:00.000000',1,20,30),(178,'2026-01-18','12:42:00.000000','13:12:00.000000',1,20,30),(179,'2026-01-18','13:12:00.000000','13:42:00.000000',1,20,30),(180,'2026-01-18','13:42:00.000000','14:12:00.000000',1,20,30),(181,'2026-01-18','14:12:00.000000','14:42:00.000000',1,20,30),(182,'2026-01-18','14:42:00.000000','15:12:00.000000',1,20,30),(183,'2026-01-18','15:12:00.000000','15:42:00.000000',1,20,30),(184,'2026-01-18','15:42:00.000000','16:12:00.000000',1,20,30),(185,'2026-01-18','16:12:00.000000','16:42:00.000000',1,20,30),(186,'2026-01-19','09:12:00.000000','09:42:00.000000',1,20,30),(187,'2026-01-19','09:42:00.000000','10:12:00.000000',1,20,30),(188,'2026-01-19','10:12:00.000000','10:42:00.000000',1,20,30),(189,'2026-01-19','10:42:00.000000','11:12:00.000000',1,20,30),(190,'2026-01-19','11:12:00.000000','11:42:00.000000',1,20,30),(191,'2026-01-19','11:42:00.000000','12:12:00.000000',1,20,30),(192,'2026-01-19','12:12:00.000000','12:42:00.000000',1,20,30),(193,'2026-01-19','12:42:00.000000','13:12:00.000000',1,20,30),(194,'2026-01-19','13:12:00.000000','13:42:00.000000',1,20,30),(195,'2026-01-19','13:42:00.000000','14:12:00.000000',1,20,30),(196,'2026-01-19','14:12:00.000000','14:42:00.000000',1,20,30),(197,'2026-01-19','14:42:00.000000','15:12:00.000000',1,20,30),(198,'2026-01-19','15:12:00.000000','15:42:00.000000',1,20,30),(199,'2026-01-19','15:42:00.000000','16:12:00.000000',1,20,30),(200,'2026-01-19','16:12:00.000000','16:42:00.000000',1,20,30),(201,'2026-01-20','09:12:00.000000','09:42:00.000000',0,20,30),(202,'2026-01-20','09:42:00.000000','10:12:00.000000',1,20,30),(203,'2026-01-20','10:12:00.000000','10:42:00.000000',1,20,30),(204,'2026-01-20','10:42:00.000000','11:12:00.000000',1,20,30),(205,'2026-01-20','11:12:00.000000','11:42:00.000000',1,20,30),(206,'2026-01-20','11:42:00.000000','12:12:00.000000',1,20,30),(207,'2026-01-20','12:12:00.000000','12:42:00.000000',1,20,30),(208,'2026-01-20','12:42:00.000000','13:12:00.000000',1,20,30),(209,'2026-01-20','13:12:00.000000','13:42:00.000000',1,20,30),(210,'2026-01-20','13:42:00.000000','14:12:00.000000',1,20,30),(211,'2026-01-20','14:12:00.000000','14:42:00.000000',1,20,30),(212,'2026-01-20','14:42:00.000000','15:12:00.000000',1,20,30),(213,'2026-01-20','15:12:00.000000','15:42:00.000000',1,20,30),(214,'2026-01-20','15:42:00.000000','16:12:00.000000',1,20,30),(215,'2026-01-20','16:12:00.000000','16:42:00.000000',1,20,30),(216,'2026-01-21','09:12:00.000000','09:42:00.000000',1,20,30),(217,'2026-01-21','09:42:00.000000','10:12:00.000000',1,20,30),(218,'2026-01-21','10:12:00.000000','10:42:00.000000',1,20,30),(219,'2026-01-21','10:42:00.000000','11:12:00.000000',1,20,30),(220,'2026-01-21','11:12:00.000000','11:42:00.000000',1,20,30),(221,'2026-01-21','11:42:00.000000','12:12:00.000000',1,20,30),(222,'2026-01-21','12:12:00.000000','12:42:00.000000',1,20,30),(223,'2026-01-21','12:42:00.000000','13:12:00.000000',1,20,30),(224,'2026-01-21','13:12:00.000000','13:42:00.000000',1,20,30),(225,'2026-01-21','13:42:00.000000','14:12:00.000000',1,20,30),(226,'2026-01-21','14:12:00.000000','14:42:00.000000',1,20,30),(227,'2026-01-21','14:42:00.000000','15:12:00.000000',1,20,30),(228,'2026-01-21','15:12:00.000000','15:42:00.000000',1,20,30),(229,'2026-01-21','15:42:00.000000','16:12:00.000000',1,20,30),(230,'2026-01-21','16:12:00.000000','16:42:00.000000',1,20,30),(231,'2026-02-05','09:12:00.000000','09:42:00.000000',1,19,30),(232,'2026-02-05','09:42:00.000000','10:12:00.000000',1,19,30),(233,'2026-02-05','10:12:00.000000','10:42:00.000000',1,19,30),(234,'2026-02-05','10:42:00.000000','11:12:00.000000',1,19,30),(235,'2026-02-05','11:12:00.000000','11:42:00.000000',1,19,30),(236,'2026-02-05','11:42:00.000000','12:12:00.000000',1,19,30),(237,'2026-02-05','12:12:00.000000','12:42:00.000000',1,19,30),(238,'2026-02-05','12:42:00.000000','13:12:00.000000',1,19,30),(239,'2026-02-05','13:12:00.000000','13:42:00.000000',1,19,30),(240,'2026-02-05','13:42:00.000000','14:12:00.000000',1,19,30),(241,'2026-02-05','14:12:00.000000','14:42:00.000000',1,19,30),(242,'2026-02-05','14:42:00.000000','15:12:00.000000',1,19,30),(243,'2026-02-05','15:12:00.000000','15:42:00.000000',1,19,30),(244,'2026-02-05','15:42:00.000000','16:12:00.000000',1,19,30),(245,'2026-02-05','16:12:00.000000','16:42:00.000000',1,19,30);
/*!40000 ALTER TABLE `rhms_doctor_availabilities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rhms_hospitals`
--

DROP TABLE IF EXISTS `rhms_hospitals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rhms_hospitals` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `registration_number` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `address` longtext NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `city` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `country` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `hospital_type` json NOT NULL,
  `hours` json NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `registration_number` (`registration_number`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rhms_hospitals`
--

LOCK TABLES `rhms_hospitals` WRITE;
/*!40000 ALTER TABLE `rhms_hospitals` DISABLE KEYS */;
INSERT INTO `rhms_hospitals` VALUES (81,'delaru hospital','1329142424092347','bhawan.badhe079@gmail.com','hospitals/81/logo.png','625 Arno Wells','9879645571','vadodara','approved','2025-12-15 05:17:35.250850','India','Gujarat','[]','{\"Friday\": \"Closed\", \"Monday\": \"Closed\", \"Sunday\": \"Closed\", \"Tuesday\": \"Closed\", \"Saturday\": \"Closed\", \"Thursday\": \"Closed\", \"Wednesday\": \"Closed\"}',1),(82,'mugeye','12313413444','bhavanbadhe@gmail.com','hospitals/82/logo.png','625 Arno Wells','09879647227','test','pending','2025-12-16 11:01:01.757382','India','Gujarat','[]','{\"Friday\": \"Closed\", \"Monday\": \"Closed\", \"Sunday\": \"Closed\", \"Tuesday\": \"Closed\", \"Saturday\": \"Closed\", \"Thursday\": \"Closed\", \"Wednesday\": \"Closed\"}',0),(83,'City Hospital Vadodara','REG-VADODARA-001','info_vadodara@cityhospital.com','','Main Road, Vadodara','9876543210','Vadodara','approved','2025-12-17 08:41:15.300602','India','Gujarat','[\"general\"]','{}',1),(84,'City Hospital Surat','REG-SURAT-001','info_surat@cityhospital.com','','Main Road, Surat','9876543210','Surat','approved','2025-12-17 08:41:15.392427','India','Gujarat','[\"general\"]','{}',1),(85,'City Hospital Ahmedabad','REG-AHMEDABAD-001','info_ahmedabad@cityhospital.com','','Main Road, Ahmedabad','9876543210','Ahmedabad','approved','2025-12-17 08:41:15.456646','India','Gujarat','[\"general\"]','{}',1),(86,'Test Search Hospital','REG123SEARCH','test_search@example.com','','Test Address','1234567890','Vadodara','pending','2026-01-16 07:27:13.129771','India','Gujarat','[]','{}',1),(87,'Seshadri Hospital Surat','86be8548-1c3c-46e0-a406-b1eb31dabaaf','falak91@example.com','','07/98, Dutta Zila, Warangal-193549','3865271239','Surat','approved','2026-02-02 04:29:28.325688','India','Gujarat','[\"general\"]','{\"open\": \"09:00\", \"close\": \"20:00\"}',1),(88,'Date Hospital Surat','c8f0b222-7e20-4028-9ca5-5fb0e84816ca','anushakrish@example.com','','30, Sen\nAmbala-033636','+914962944317','Surat','approved','2026-02-02 04:30:34.886584','India','Gujarat','[\"general\"]','{\"open\": \"09:00\", \"close\": \"20:00\"}',1),(89,'Varughese Hospital Surat','d710ba58-a014-4baa-a55e-e8d51468e598','ydasgupta@example.com','','45/37\nGole Marg\nSasaram 645436','8789685974','Surat','approved','2026-02-02 04:30:34.945411','India','Gujarat','[\"general\"]','{\"open\": \"09:00\", \"close\": \"20:00\"}',1),(90,'Shroff Hospital Ahmedabad','8d12ae76-a478-49cc-b70a-4f780c387f7f','yashoda41@example.org','','H.No. 12, Kothari\nSri Ganganagar-897505','7739573388','Ahmedabad','approved','2026-02-02 04:30:34.990171','India','Gujarat','[\"general\"]','{\"open\": \"09:00\", \"close\": \"20:00\"}',1),(91,'Singh Hospital Ahmedabad','8bd1adde-fe5b-4da8-977c-a60bdc288455','bassiekaja@example.org','','59/992, Dua Circle, Khora -015576','07595219991','Ahmedabad','approved','2026-02-02 04:30:35.031733','India','Gujarat','[\"general\"]','{\"open\": \"09:00\", \"close\": \"20:00\"}',1),(92,'Madan Hospital Vadodara','6336c5a0-3774-4abb-8e34-f275893c59d5','lsamra@example.com','','01/95\nRaja Ganj\nKaraikudi-582045','3286543229','Vadodara','approved','2026-02-02 04:30:35.072896','India','Gujarat','[\"general\"]','{\"open\": \"09:00\", \"close\": \"20:00\"}',1),(93,'Khare Hospital Vadodara','2fd0b476-926a-4a08-a3eb-57ee310ddff5','issacxavier@example.org','','H.No. 41, Som Ganj, Meerut-825662','4974217557','Vadodara','approved','2026-02-02 04:30:35.136350','India','Gujarat','[\"general\"]','{\"open\": \"09:00\", \"close\": \"20:00\"}',1),(94,'Kashyap Hospital Gandhinagar','3587265d-f863-4c3f-8915-2e9e5bf8921f','bakhshi84@example.org','','91/356\nDara Street\nThane 939290','05728492538','Gandhinagar','approved','2026-02-02 04:30:35.198446','India','Gujarat','[\"general\"]','{\"open\": \"09:00\", \"close\": \"20:00\"}',1),(95,'Kashyap Hospital Gandhinagar','6ab3cfe1-9758-406d-8d6a-d879a923eeb6','parsaekansh@example.com','','07/424, Rana Chowk\nRajahmundry-092605','+917321825144','Gandhinagar','approved','2026-02-02 04:30:35.243755','India','Gujarat','[\"general\"]','{\"open\": \"09:00\", \"close\": \"20:00\"}',1),(96,'Narain Hospital Rajkot','4809505d-d453-4695-b6cf-b7f4766e4a91','hariaahana@example.com','','H.No. 821, Ratti, Nanded 304065','+913198650727','Rajkot','approved','2026-02-02 04:30:35.285818','India','Gujarat','[\"general\"]','{\"open\": \"09:00\", \"close\": \"20:00\"}',1),(97,'Jaggi Hospital Rajkot','0e868bf0-6c7f-433e-93a4-45d4f2dfe042','geetikadoshi@example.net','','H.No. 60, Kashyap Nagar\nTiruvottiyur-208128','3877723226','Rajkot','approved','2026-02-02 04:30:35.325981','India','Gujarat','[\"general\"]','{\"open\": \"09:00\", \"close\": \"20:00\"}',1);
/*!40000 ALTER TABLE `rhms_hospitals` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-02 16:42:15
