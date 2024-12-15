-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: elective
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `address_id` int NOT NULL AUTO_INCREMENT,
  `number_building` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(100) NOT NULL,
  `zip_postcode` varchar(20) NOT NULL,
  `state_province_county` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  PRIMARY KEY (`address_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
INSERT INTO `addresses` VALUES (1,'739','Derrick Plaza','Sellersview','48771','West Virginia','Sao Tome and Principe'),(2,'527','Mosley Mall','Port Mitchell','61589','Colorado','Djibouti'),(3,'6815','Scott Villages','Aaronstad','34340','Virginia','Finland'),(4,'134','Lee Walk','Mitchellmouth','07762','Alaska','Wallis and Futuna'),(5,'305','Chase Corners','Port Joseph','80444','Oregon','Zambia'),(6,'2496','Matthew Drive','South Courtney','24444','Tennessee','Turks and Caicos Islands'),(7,'7624','Joseph Via','New Ryan','17199','Washington','Kiribati'),(8,'06687','Thompson Mill','Lake Gabriela','04902','Alaska','Monaco'),(9,'591','Davis Corners','West Alexander','28869','Texas','Israel'),(10,'35208','Parrish Squares','Wheelerville','12780','Virginia','Qatar'),(11,'97578','Taylor Islands','Rosalesshire','15225','Nebraska','Burkina Faso'),(12,'38336','Heather Junction','Jerryhaven','73975','Georgia','Gibraltar'),(13,'27972','Ryan Locks','East Sheliaborough','68926','Alabama','Norway'),(14,'6371','Adams Plains','South Scottmouth','58352','Kansas','Palau'),(15,'885','Ebony Ranch','Sarahberg','91926','Utah','Uzbekistan'),(16,'884','Cole Greens','Rosebury','91574','Kansas','Gabon'),(17,'98113','Jimenez Cape','North Patriciashire','99649','Tennessee','Ukraine'),(18,'112','William Rapids','Smithshire','90136','Washington','British Indian Ocean Territory (Chagos Archipelago)'),(19,'92409','Grant Lane','Sandraland','68521','New York','Liberia'),(20,'51362','Ortega Parkway','Lake Anna','41248','Wyoming','Indonesia'),(21,'55927','Chen Parkways','Lake Aaron','11436','Virginia','Heard Island and McDonald Islands'),(22,'81904','Parrish Island','South Lori','13819','Maine','Oman'),(23,'07003','Reed Springs','Smithtown','16202','New Jersey','Chad'),(24,'55839','Bowers Dam','Russellland','93005','Washington','Malaysia'),(25,'68248','Torres Roads','Bellmouth','74765','Louisiana','Latvia');
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_orders`
--

DROP TABLE IF EXISTS `customer_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `order_status` enum('Pending','Completed','Shipped','Cancelled','In Progress') NOT NULL,
  `order_date` date NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `customer_orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_orders`
--

LOCK TABLES `customer_orders` WRITE;
/*!40000 ALTER TABLE `customer_orders` DISABLE KEYS */;
INSERT INTO `customer_orders` VALUES (1,20,'Cancelled','2024-04-30','2024-11-02','2024-08-20'),(2,23,'In Progress','2024-02-28','2024-11-27','2024-03-14'),(3,20,'In Progress','2024-09-08','2024-06-26',NULL),(4,17,'Pending','2024-10-09','2024-08-20','2024-11-12'),(5,2,'Completed','2024-03-17','2024-06-26',NULL),(6,16,'Cancelled','2024-10-18','2024-04-23',NULL),(7,9,'In Progress','2024-02-06','2024-04-18','2024-01-21'),(8,14,'Cancelled','2024-05-11','2024-01-19',NULL),(9,20,'Cancelled','2024-10-05','2024-04-12',NULL),(10,4,'Cancelled','2024-08-08','2024-01-02','2024-09-19'),(11,7,'In Progress','2024-11-27','2024-09-01','2024-01-26'),(12,1,'Completed','2024-07-17','2024-10-07',NULL),(13,21,'Pending','2024-08-30','2024-01-06',NULL),(14,22,'Pending','2024-01-29','2024-12-10',NULL),(15,23,'Pending','2024-07-02','2024-02-21','2024-08-05'),(16,6,'Completed','2024-08-22','2024-04-07','2024-09-15'),(17,9,'Shipped','2024-11-29','2024-08-10','2024-10-29'),(18,5,'Shipped','2024-02-13','2024-04-20',NULL),(19,25,'In Progress','2024-07-16','2024-09-13',NULL),(20,18,'Shipped','2024-09-27','2024-04-17','2024-07-07'),(21,9,'Completed','2024-03-18','2024-07-10','2024-05-01'),(22,13,'Cancelled','2024-06-01','2024-05-29','2024-08-17'),(23,10,'In Progress','2024-09-21','2024-06-03','2024-07-16'),(24,3,'Shipped','2024-03-26','2024-02-13',NULL),(25,25,'Pending','2024-06-01','2024-01-26',NULL);
/*!40000 ALTER TABLE `customer_orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_payment_details`
--

DROP TABLE IF EXISTS `customer_payment_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_payment_details` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `payment_date` date NOT NULL,
  `payment_amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `transaction_reference` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `customer_payment_details_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `customer_orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_payment_details`
--

LOCK TABLES `customer_payment_details` WRITE;
/*!40000 ALTER TABLE `customer_payment_details` DISABLE KEYS */;
INSERT INTO `customer_payment_details` VALUES (1,6,'2024-08-01',251.31,'Credit Card','d21f4e7d-0da0-4573-8878-27a89da699e5'),(2,13,'2024-09-12',102.57,'Cash','e076a02b-23e5-4945-b75b-8cc84db32e80'),(3,1,'2024-01-26',371.83,'Bank Transfer','5e8ba428-4ba0-4f59-bdcb-802cd7706d34'),(4,3,'2024-07-07',298.82,'PayPal','ff5629bc-beb8-4588-be2a-5e7631ee5c00'),(5,17,'2024-11-23',303.28,'Cash','5e0931f6-2e59-462b-8784-fc57f3991cbb'),(6,18,'2024-11-10',354.35,'PayPal','227a4508-3a65-47a4-b981-c4fa0d76f734'),(7,3,'2024-09-10',489.57,'PayPal','97f11e38-ecfd-43c7-aaab-c6adb0506e1a'),(8,11,'2024-05-04',108.42,'Credit Card','240c3e19-1974-4ff6-a88c-690bb01770ea'),(9,12,'2024-03-11',392.53,'Credit Card','c1415ff5-7e09-46a9-b7c3-23c97702cad9'),(10,10,'2024-11-05',356.83,'Bank Transfer','53e69904-598b-47de-8f60-562b5661d654'),(11,23,'2024-01-18',404.86,'PayPal','e7a04274-6ee5-4dfc-877f-843acaa62a0c'),(12,3,'2024-09-13',166.59,'Cash','d2479c6c-8c4e-4704-9715-464ff8ace5ab'),(13,10,'2024-05-29',251.88,'Credit Card','45f68971-7ee2-4183-aa63-ba8199ea9d8a'),(14,7,'2024-01-03',441.25,'PayPal','9673abd1-4d57-4547-81f9-3bc2ae2116fa'),(15,21,'2024-08-30',293.89,'Bank Transfer','71a3474a-ec08-4ab6-9d55-482edcbc0a12'),(16,4,'2024-08-12',130.43,'PayPal','ef99919a-89df-4511-9200-b1c9d35bd48c'),(17,3,'2024-09-30',391.32,'PayPal','d38f05b6-6cac-43cd-9d87-76e6585df40a'),(18,13,'2024-02-18',145.39,'Bank Transfer','7dd7f1c4-d1f0-4544-a609-af1accdb031d'),(19,13,'2024-10-28',260.98,'PayPal','9f8c3215-293f-4a05-a6de-3225800a636a'),(20,25,'2024-06-16',84.73,'Bank Transfer','108ba593-0b1d-4ebb-aad7-651b7801677f'),(21,22,'2024-10-11',485.99,'PayPal','d1f40f89-8e9b-41db-9d6b-83412a451053'),(22,16,'2024-02-03',384.62,'Cash','18ce0949-348e-4c44-9532-32bf59ea6e53'),(23,12,'2024-02-13',76.07,'Credit Card','fa4e9d9f-e1b4-4e38-92aa-4d948d716573'),(24,21,'2024-02-12',455.52,'Credit Card','e1eac847-515b-4112-a6e7-4623672e4815'),(25,10,'2024-09-11',229.40,'Credit Card','3e582cf8-468f-4f03-89a6-7bec56dafb6c');
/*!40000 ALTER TABLE `customer_payment_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `address_id` int NOT NULL,
  `customer_name` varchar(255) NOT NULL,
  `customer_phone` varchar(20) NOT NULL,
  `customer_email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  KEY `address_id` (`address_id`),
  CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`address_id`) REFERENCES `addresses` (`address_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,11,'Jennifer Novak','353.817.6665x517','tracy52@example.com'),(2,13,'Earl Walton','001-322-696-3936x586','jason10@example.net'),(3,4,'Norma Herrera','384.477.3979x4971','bankscaleb@example.com'),(4,13,'Mary Edwards','(345)284-0290','joshua94@example.net'),(5,17,'Stephanie Suarez','2366393234','carterbrooke@example.org'),(6,17,'Amber Hernandez','+1-437-796-0548x1641','brendaclark@example.net'),(7,2,'Brian Bailey','668-976-9888x9275','kevinmunoz@example.org'),(8,20,'Cynthia Lowe','821.558.6344','marymclean@example.net'),(9,5,'Dominique Henry','(456)852-1277','daniellegates@example.com'),(10,15,'Taylor Davis','(513)898-4829x194','theodoreho@example.org'),(11,24,'Stephen Jones','+1-935-697-5611x4603','johncantu@example.net'),(12,10,'Tyler Pitts','001-836-957-7162x725','jordan95@example.com'),(13,19,'Logan Hunt','9772059443','bbarry@example.net'),(14,11,'Paul Campos','3787526259','tiffany19@example.com'),(15,7,'Mr. David Davis','460-677-0873','adambriggs@example.org'),(16,15,'John Mcpherson','567.926.0496x273','michael73@example.net'),(17,9,'Tyler Bell','(239)497-5707x784','eclark@example.org'),(18,4,'Shawn Graham','(771)515-8295x87183','cgraham@example.net'),(19,12,'Kimberly Roberts','336.868.0748','uwilliams@example.org'),(20,23,'Andre Rodriguez','001-715-643-3460x699','brianmendoza@example.org'),(21,8,'Megan Weiss','(366)590-0500x6814','munozkendra@example.org'),(22,20,'Trevor Carter','(498)490-1612','hamptonsonia@example.com'),(23,8,'Dr. Jamie Kent','420-307-0751','martinezana@example.net'),(24,10,'Elizabeth Barnes DVM','(935)783-7072','abrandt@example.org'),(25,15,'Mr. Brett Richardson','(696)963-1608','paige02@example.org');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `order_item_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `service_id` int NOT NULL,
  `order_quantity` int NOT NULL,
  `monthly_payment_amount` decimal(10,2) DEFAULT NULL,
  `monthly_payment_date` date DEFAULT NULL,
  PRIMARY KEY (`order_item_id`),
  KEY `order_id` (`order_id`),
  KEY `service_id` (`service_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `customer_orders` (`order_id`),
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,8,12,3,92.18,'2024-08-05'),(2,17,21,2,50.31,'2024-06-02'),(3,9,11,3,46.12,'2024-08-26'),(4,24,8,2,61.50,'2024-07-21'),(5,7,11,3,27.39,'2024-08-12'),(6,21,4,2,40.84,'2024-05-15'),(7,23,17,3,85.15,'2024-07-12'),(8,4,23,5,10.54,'2024-07-25'),(9,11,11,4,67.02,'2024-06-11'),(10,11,15,1,43.12,'2024-04-22'),(11,17,21,4,66.02,'2024-05-29'),(12,4,19,3,37.54,'2024-03-22'),(13,20,12,1,69.26,'2024-01-09'),(14,23,5,2,65.52,'2024-03-06'),(15,12,24,2,64.45,'2024-07-23'),(16,10,24,5,66.28,'2024-06-07'),(17,12,16,4,78.48,'2024-04-17'),(18,6,13,3,31.09,'2024-11-14'),(19,1,4,3,75.71,'2024-04-27'),(20,5,19,2,36.61,'2024-12-10'),(21,24,7,1,83.58,'2024-05-01'),(22,7,19,1,34.30,'2024-05-30'),(23,9,17,5,91.15,'2024-11-03'),(24,17,22,3,61.67,'2024-06-29'),(25,2,3,1,71.58,'2024-10-18');
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `service_id` int NOT NULL AUTO_INCREMENT,
  `service_name` varchar(255) NOT NULL,
  `price_per_period` decimal(10,2) NOT NULL,
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (1,'Incubate dot-com synergies',96.30),(2,'Re-contextualize value-added markets',95.18),(3,'Reinvent dot-com e-commerce',38.78),(4,'Matrix sticky functionalities',34.62),(5,'Orchestrate viral networks',44.95),(6,'Re-intermediate cross-media networks',95.61),(7,'Target turn-key architectures',26.53),(8,'Envisioneer viral applications',47.23),(9,'Incubate bricks-and-clicks platforms',70.91),(10,'Whiteboard open-source interfaces',20.40),(11,'Envisioneer sticky supply-chains',78.78),(12,'Productize mission-critical roi',52.79),(13,'Morph plug-and-play experiences',19.62),(14,'Cultivate ubiquitous portals',40.93),(15,'Integrate one-to-one roi',59.40),(16,'Morph synergistic deliverables',89.12),(17,'Deploy e-business web-readiness',47.45),(18,'E-enable collaborative metrics',92.68),(19,'Brand web-enabled web services',99.79),(20,'Visualize open-source synergies',46.28),(21,'Extend collaborative paradigms',26.33),(22,'Morph sticky users',51.57),(23,'Whiteboard e-business e-business',13.03),(24,'Streamline real-time e-markets',25.43),(25,'Redefine e-business models',28.63);
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-14 15:58:27
