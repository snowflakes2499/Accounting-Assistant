-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: invoice_assistant
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.22.04.1

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
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `client_name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text,
  `client_address` varchar(1000) DEFAULT NULL,
  `client_email` varchar(255) DEFAULT NULL,
  `client_phone` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expense`
--

DROP TABLE IF EXISTS `expense`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expense` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `amount` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expense`
--

LOCK TABLES `expense` WRITE;
/*!40000 ALTER TABLE `expense` DISABLE KEYS */;
INSERT INTO `expense` VALUES (1,2500,'2025-05-15','Lunch with client'),(2,500,'2025-05-17','Lunch with client'),(3,3500,'2025-05-13','Lunch with client');
/*!40000 ALTER TABLE `expense` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `invoice_number` varchar(255) DEFAULT NULL,
  `client_id` bigint DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `issue_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `invoice_date` date DEFAULT NULL,
  `invoice_due_date` date DEFAULT NULL,
  `invoice_status` varchar(255) DEFAULT NULL,
  `invoice_total` decimal(38,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK6y01j0975eqwmnb0gckttrbj2` (`client_id`),
  CONSTRAINT `FK6y01j0975eqwmnb0gckttrbj2` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice`
--

LOCK TABLES `invoice` WRITE;
/*!40000 ALTER TABLE `invoice` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_product`
--

DROP TABLE IF EXISTS `invoice_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_product` (
  `invoice_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`invoice_id`,`product_id`),
  KEY `FK806bu27uepq9jw1gksvegoqkd` (`product_id`),
  CONSTRAINT `FK806bu27uepq9jw1gksvegoqkd` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `FKhrqne4uostar9vds76ynsosov` FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_product`
--

LOCK TABLES `invoice_product` WRITE;
/*!40000 ALTER TABLE `invoice_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoice_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loans` (
  `person_name` varchar(255) NOT NULL,
  `amount` int DEFAULT NULL,
  `loan_type` varchar(255) DEFAULT NULL,
  `loan_amount` int DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`person_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
INSERT INTO `loans` VALUES ('adam',NULL,NULL,9500,'None Reminder to repay the loan Buying charity Loan repayment Petrol for car','suyash.dongre23@vit.edu'),('edwards',NULL,NULL,8000,'None Bike rent','khushi.bora23@vit.edu'),('john',NULL,NULL,7500,'None Buying a calculator Buying a water bottle',NULL);
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255) NOT NULL,
  `product_price` decimal(38,2) DEFAULT NULL,
  `product_quantity` int DEFAULT NULL,
  `product_tax` decimal(38,2) DEFAULT NULL,
  `selling_price` decimal(38,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (35,'mobile',1700.00,8,20.00,22000.00),(54,'bottle',3000.00,4,6.00,2400.00),(61,'clock',500.00,2,12.00,600.00),(69,'camera',400.00,2,10.00,800.00),(73,'flower',200.00,20,12.00,300.00),(74,'stapler',30.00,10,10.00,60.00);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `selling_ledger`
--

DROP TABLE IF EXISTS `selling_ledger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `selling_ledger` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sold_amount` decimal(38,2) DEFAULT NULL,
  `sold_product_id` bigint DEFAULT NULL,
  `sold_product_quantity` int DEFAULT NULL,
  `sold_product_selling_price` decimal(38,2) DEFAULT NULL,
  `sold_product_actual_price` decimal(38,2) DEFAULT NULL,
  `sold_product_tax` decimal(38,2) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selling_ledger`
--

LOCK TABLES `selling_ledger` WRITE;
/*!40000 ALTER TABLE `selling_ledger` DISABLE KEYS */;
INSERT INTO `selling_ledger` VALUES (1,60000.00,35,3,20000.00,16000.00,18.00,'mobile'),(2,60000.00,35,3,20000.00,16000.00,18.00,'mobile'),(3,20000.00,35,1,20000.00,16000.00,18.00,'mobile'),(4,47200.00,35,2,20000.00,16000.00,18.00,'mobile'),(5,23600.00,35,2,20000.00,16000.00,18.00,'mobile'),(6,5280.00,54,2,2400.00,1500.00,10.00,'bottle'),(7,23600.00,35,1,20000.00,15000.00,18.00,'mobile'),(8,5280.00,54,2,2400.00,1500.00,10.00,'bottle'),(9,23600.00,35,1,20000.00,15000.00,18.00,'mobile'),(10,2640.00,54,4,2400.00,1500.00,10.00,'bottle'),(11,24780.00,35,1,21000.00,16000.00,18.00,'mobile'),(12,2640.00,54,1,2400.00,1500.00,10.00,'bottle'),(13,24780.00,35,1,21000.00,16000.00,18.00,'mobile'),(14,2640.00,54,1,2400.00,1500.00,10.00,'bottle'),(15,24780.00,35,1,21000.00,16000.00,18.00,'mobile'),(16,1760.00,69,2,800.00,400.00,10.00,'camera'),(17,0.00,69,0,800.00,400.00,10.00,'camera');
/*!40000 ALTER TABLE `selling_ledger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `operation` varchar(255) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`operation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES ('language','en'),('processing','false');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` varchar(255) DEFAULT NULL,
  `loan_amount` int DEFAULT NULL,
  `loan_type` varchar(255) DEFAULT NULL,
  `person_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,'Bike purchase',10000,'lent','john'),(2,'',2000,'repayment','john'),(3,'',3000,'lent','john'),(4,'',5000,'lent','edwards'),(5,'Bike rent',3000,'lent','edwards'),(6,'',1000,'repayment','john'),(7,'',2000,'repayment','john'),(8,'Buying a calculator',1000,'debt','john'),(9,'Buying a water bottle',500,'lent','john'),(10,'Petrol',2000,'lent','adam'),(11,'Reminder to repay the loan',0,'repayment','adam'),(12,'Buying charity',5000,'lent','adam'),(13,'Loan repayment',3000,'repayment','adam'),(14,'',0,'debt','Adam'),(15,'Petrol for car',2000,'lent','Adam'),(16,'Calculator purchase',3500,'lent','Adam');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transcript`
--

DROP TABLE IF EXISTS `transcript`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transcript` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `transcript` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=207 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transcript`
--

LOCK TABLES `transcript` WRITE;
/*!40000 ALTER TABLE `transcript` DISABLE KEYS */;
INSERT INTO `transcript` VALUES (1,NULL),(2,NULL),(3,'This is a test'),(4,' Can you create a product charger costing 100 Rs 5% tax and 12 quantity?\n'),(5,' Delete the product with the ID25.\n'),(6,' Delete the product 25.\n'),(7,' send 1000 rupees to the vendor ABC I\'m lending him money\n'),(8,' Send 500,000 to Mr. Ramesh. He will be returning that later.\n'),(9,' I am landing 5000 Rupis to Kendrick\n'),(10,' I am lending money to Kendrick which is amounting to 5,000 Rs.\n'),(11,' (wind blowing)\n'),(12,' I am sending 5000 rupees to Mr. Kendrick. You will be returning that later.\n'),(13,' I\'m landing 10,000 rupees to Mr. Kendrick.\n'),(14,' Rs. 5,000 received from Mr. Kendrick.\n'),(15,' Rs 10,000 received from Mr. Candic\n'),(16,' Rs. 5,000 received from Mr. Kendrick.\n'),(17,' Rs 1,000 received from Mr. Kendrick for the purpose of buying mobile phone.\n'),(18,' Rupees 2000 received from Mr. Kendrick for the purpose of buying water bottle.\n'),(19,' Rs 1,000 received from Mr. Candrate for the purpose of buying mobile phone.\n'),(20,' Rs 1,000 received from Mr Kendrick for the purpose of buying mobile phone.\n'),(21,' Mr. Kendrick gave me 1000 Rs back after buying mobile phone.\n'),(22,' received 1000 Rs. back from Mr. Kendrick after he bought a new mobile.\n'),(23,' He received 1000 rupees from Kendrick after he gained his salary.\n'),(24,' Rs 2,000 received from Kendrick after his salary was credited.\n'),(25,' Kendrick gave me 5000 rupees. I have to give him back.\n'),(26,' Receive 2,000 rupees from Kendrick after purchasing phone.\n'),(27,' Kendrick gave me Rs 2000 after he bought a new phone.\n'),(28,' Kendrick gave me 1000 rupees after he bought a new car.\n'),(29,' I gave Kendrick 10,000 rupees\n'),(30,' I gave Kendrick 10,000 rupees\n'),(31,' I gave rupees 2000 to Kendrick for petrol.\n'),(32,' I gave rupees 7000 to candic for petrol\n'),(33,' I gave rupees 7000 to Kendrick for per patrol\n'),(34,' Create a new product water bottle costing 50 rupees 2% taxes.\n'),(35,' delete the product with the ID26 and also create a new product brick costing\n'),(36,' Can you please remove the product 26\n'),(37,' Can you please delete the product 26 and also delete the product 23?\n'),(38,' Delete the product 24, also delete the product 27.\n'),(39,' Create a new product, Magbook Pro priced at $2400 with 2 units. Create a product airport for $199.\n The airport should have 18% tax on it. Create a product office chair priced at $130 with 5 units.\n And 10% tax. The Magbook Pro has a tax of 8%.\n'),(40,' update the product 29 to have the cost 200 dollars and\n'),(41,' update the product 29 to have cost $200 and 5 quantity\n'),(42,' Update the product 99 to have cost 205 quantity.\n'),(43,' update the product 29 to have the cost 500\n'),(44,' Update the product 29 to have the cost 500.\n'),(45,' Update the product 29 to have the cost 500.\n'),(46,' update the product 29 to have the cost 500\n'),(47,' update the product 29 to have price 200\n'),(48,' update the product 29 to have price 400\n'),(49,' update the product 29 to have the price 401(1) tax 9\n'),(50,' update the product 29 to have price 400 quantity 1 tax 9\n'),(51,' update the product 29 to have price 4011 tax 9\n'),(52,' update the product 29 to have price 400 quantity to tax 10\n'),(53,' Create new loan for John of 10,000 rupees.\n'),(54,' Create a new product mobile phone costing 30,000 rupees type 10% tax and 5 quantity.\n'),(55,' Create a new product, water, water, costing 20 rupees, 5% tax, 3 quantity.\n'),(56,' Create new loan for John of Rs. 10,000 is requiring that for his bike.\n'),(57,' John paid me back rupees 2000 after he got his salary.\n'),(58,' Update the product 29, change the price to 500 rupees.\n'),(59,' Update product 29. Change the price of it to 500 rupees.\n'),(60,' Update product 29 change the price of it to rupees 600.\n'),(61,' Update the product 29, change its price to rupees 500 and the quantity to 2.\n'),(62,' Update product 30. Change the price of it to rupees 200.\n'),(63,' Update product 22. Change the cost of it to rupees 400.\n'),(64,' Create a new product, water bottle costing 20 rupees with the quantity 50 and 3 percent\n tax.\n Also, update the product 28 to have the price 3000 rupees and update its quantity to be\n 5 and 18 percent tax.\n'),(65,' Delete the product 30, also update the cost of product 20 to 600 rupees.\n'),(66,' Delete the product with the ID30.\n Also update the cost of the product 31 to rupees 40.\n'),(67,' Delete the product 31, also update the cost of the product 29 to 700 Rs. Update the tax\n of product 22 to 12 percent.\n'),(68,' Update the cost of the product 29 to 700 Rs. Update the tax of product 22 to 12% also create\n a new product brick costing 18 Rs. 100 quantity and 18% tax.\n'),(69,' Delete the product 22, update the cost of product 32 to 32 rupees, also update its tax\n to 9% and also create a new product, milk powder costing 8 rupees with the quantity 200\n and tax 4%.\n'),(70,' I gave 3,000 rupees to John and he needs to return it.\n'),(71,' Delete the product with the IID 33A.\n'),(72,' Create product watch costing 5,000 rupees, 12% tax and 3 quantity.\n Also update the product 29, increase its price to 1000 rupees and the quantity to 6.\n Also delete the product 32.\n'),(73,' You\n'),(74,' Create product ID 35 name mobile price 10,000 quantity 6 tax 18% in stock it should be 6.\n Also delete product ID 29 which having quantity 6 from quantities delete only 3.\n'),(75,' Create new loan to Edwards, I have lent him 5000 rupees.\n'),(76,' AdWords paid me back for £5,000.\n'),(77,' New product.\n ABC.\n Price.\n 20.\n Tax.\n 15%.\n Ski quantity.\n 6.\n'),(78,' Item Number 6 - Stoxel Delete & Item Number 5 - Update + 20,000\n'),(79,' 1 nya product banayaja, his name is mobile iphone, this is the price of this, it is Rs.50,000 and 2 quantity and 12% tax.\n And the product is Rs.60,000 and the product is Rs.60,000.\n'),(80,' Create a new product piece here or costing 2,000 rupees with 17% tax and the quality of\n it should be 18.\n'),(81,' Create a new product x,y,z costing 500 Rs.\n'),(82,' Can you create a new product X costing 50 rupees?\n'),(83,' Can you please delete the product 40 and also update the product 40?\n'),(84,' Can you delete the product 39 and update price of product 36 to 50 rupees?\n'),(85,' Channel Delete the product 38.\n'),(86,' Can you delete the product 37?\n'),(87,' Can you delete the product 29?\n'),(88,' Can you create a new product, guitar, costing 2000 rupees with 3 quantity and 9% tax?\n'),(89,' Can you create a new product, hat, costing 200 rupees and 8 quantity, 4% tax?\n'),(90,' Can you update the price of product 42 to Rs 500 in the tax to 6 percent?\n'),(91,' Can you update the price of product 42 to 300 rupees?\n'),(92,''),(93,' Can you update the price of Product 42 to 800 Rs?\n'),(94,' can you update the price of product 42 to 400 rupees also the removal quantity of product\n'),(95,' Can you delete the product 42?\n'),(96,' Can you also delete product 41?\n'),(97,' Can you create a new product, guitar, costing 2000 rupees, 4 quantity 8% tax?\n'),(98,' Can you delete the product 43?\n'),(99,' Can you create a new product that are costing 5000 rupees 3 quantity?\n'),(100,' I gave 3000 rupees to Edwards for his bike rent.\n'),(101,' Edward paid me back Rs. 7,000 after he got his salary for bike rent.\n'),(102,' Adverts paid me back Rs.7,000 after his bike rent.\n'),(103,' Jones paid me back rupees 1000 after he got his salary\n'),(104,' John paid me back Rs 1,000 after he got his salary.\n'),(105,' 1-2-3\n 1-2-3\n 1-2-3\n 1-2-3\n'),(106,' Can you delete the product 36?\n'),(107,' Can you delete the product 36?\n'),(108,' Can you delete the product 36?\n'),(109,' Update the price of the product 35 to 12,000 rupees and also John\n'),(110,' Delete the product 45 and also John paid me back 2000 rupees.\n'),(111,' [Motor]\n'),(112,' Can you update the product 35 to cost 15,000 rupees and also John has to pay me 1000 rupees\n for buying calculator?\n'),(113,' I gave John Rs 500 for buying a water bottle and update the quantity of product 3527.\n'),(114,' कि एक नया प्रोडक्ट बनाओ जिसका नाम है चार्जर उसकी कीमत है 500 रुपए और 18 परसेंट जीएसपी उस पर लागू है कि अ'),(115,' प्रोडक्ट नंबर 46 की कीमत 700 किया जाए और उसकी quantity 8 कीजिए और प्रोडक्ट नंबर 34 को डिलीट किया जाए'),(116,' Update the cost of the product 46 to 900 rupees.\n'),(117,' नया प्रोडक्ट बनाओ फ्लावर जिसका कॉस्ट 1200 रुपए है और 6 क्वांटिटी है और 5% GST है'),(118,' कि एक नया प्रोडक्ट बनाओ जिसका नाम है गाड़ी उसका कीमत है 5000 रुपए और वह है 20 परसेंट जीएसटी अजय को'),(119,' एक नया product बनाओ, wallet जिसकी कीमत 2000 रुपए है, 5% GST है, 6 quantity है और product 46 को delete कर दो'),(120,' एक नया product create करो wallet जिसकी कीमत 2000 रुपए है 6 quantity है 3% tax है और product 35 को delete कर दो'),(121,' तुम्माज्टाइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्राइप्र'),(122,' एक नया प्रोडक् क्रेट करो वालेट जिसकी केमत 2000 रूपय है, 8 खॉन्तिटी है, 3% GST है और प्रोडक् 46 को डिलिट कर दो.'),(123,' एक नाया प्रोडक्ट बनाओ कालिकॉलेटर जिसकी कीमत बारा सो रूपय है, दो खौन्तिटी है और अट्रा परसंट टाक्स है और प्रोडक्ट 46 को डिलीट कर दो.'),(124,' Update the price of the product 48 to 1200 rupees. The quantity should be 6. Tax should\n be 12 percent. Also delete the product 46.\n'),(125,' Update the name of the product 48 to Calculator.\n'),(126,' Update the name of the product 48 to calculator.\n'),(127,' product 48 for delete करो'),(128,' नया प्रोडक् करो इप्टोड़ इप्टोड़ जिसकी किमत 50,000 है ये दो गौन्टीती है और 6% टाक्स है और प्रोडक् 47 को डिलिट कर दो'),(129,' एक नाया प्रोडक्ट करो इट जिसकी कीमत है बीस रूपय खौन्तिटी है 5000 और टैक्स है 18% और प्रोडक्ट 47 को डिलिट करो'),(130,' एक नहाँ प्रोडक् करो इट जिसकी कीमत है बीस रूप्ध है खौन्टीटी है 5000 तक्स है 8% और प्रोडक् 47 को डिलीट करो'),(131,' Can you update product 35 to cost 16,000 rupees?\n'),(132,' Can you update quantity of the product 35 to 10?\n'),(133,' Can you update the Product 35, quantity to 10?\n'),(134,' Cell Product 35 with 3 Quantity D.\n'),(135,' Sell Product 35 with 3 Quantity.\n'),(136,' Sell Product 35 with 1 Quantity.\n'),(137,' Cell Product 35 with 1 quantity.\n'),(138,' Sell product 35, sell it 2 quantities.\n'),(139,' add 10 quantity to the product 35\n'),(140,' Update the selling price of product 54, 2 rupees 400 rupees and also update the price\n of product 35 to 15,000 rupees.\n'),(141,' Sell the product 54 with 2 quantities, also sell product 35 with 1 quantity.\n'),(142,' प्रोडब् 54 की कीमाथ बेचने वाली कीमाथ पचिश्थो रूपे की जाये और उसकी क्वान्टिटी को चार कीजे'),(143,' प्रोडक् 54 में 6 खुड़ीटी आड कीजिया और प्रोडक् 35 में उसकी कीमत 16,000 कीजिया'),(144,' प्रोडक्ट 54 में 6 quantity add कीजिए और product 35 में उसकी selling कीमत 21,000 कीजिए और product 35'),(145,' Sell the product 35 with 1 quantity and sell the product 54 with 1 quantity.\n'),(146,' I gave John 5000 rupees for him to buy his mobile phone.\n'),(147,' मैंने जॉन को हजार रुपए दिये पेट्रोल के लिए'),(148,' मैंने जॉन को 2000 रुपए दिया है पेट्रोल के लिए'),(149,' मैंने जौन को दो हजार रुपाई दिया पेट्रोल के लिए'),(150,' प्रोडक्नॉम्बर 54 की कीमत 1600 रूपय कीए जाए और उसकी खॉन्तिटी 6 कर दिये जाए और प्रोडक्नॉम्बर 35 की बेचने वाली कीमत को 22000 कीए जाए.'),(151,' प्रोडक्न नम्बर 54 की खौन्तिटी 8 करीए और उसका टाक्स 12% कीजे और प्रोडक्न नम्बर 35 की कीमत 18000 रहे हैं।'),(152,' प्रोडक्ट 54 की कीमत 1700 रुपए किये जाए और उसकी quantity 8 कर दीजिए और प्रोडक्ट 35 की quantity 7 कीजिए और उसका tax 20%'),(153,' एक नया प्रोडक्ट बनाओ टीवी जिसकी कीमत दस हजार रुपए है दो क्वांटिटी है और दस परसेंट टैक्स है और प्रोडक्ट 54 की कीमत बनाओ'),(154,' एक नया प्रोडक्ट बनाओ टीवी जिसकी कीमत 10,000 रुपए है उसकी बेचने वाली कीमत 12,000 रुपए है 6 quantity है 12% tax है और product 35 की बेचने वाली कीमत 24,000 कीमत'),(155,' एक नया प्रोड़क बनाओ टीवी जिसकी कीमत दस हजार रुपए है बारा हजार उसकी बेचने वाली कीमत है दो क्वांटिटी दस परसन टैक्स है और प्रोड़क थर्टी फाइ की कीमत सोला सो रुपए करो'),(156,' एक नया प्रोडक्ट बनाओ क्लॉक जिसकी कीमत 500 रुपए है बेचने वाली कीमत 600 रुपए है दो क्वांटिटी है 12% टैक्स है'),(157,' प्रोडक्ट 54 की कीमत 1700 रुपई करो उसकी बेचने वाली कीमत 2500 रुपई करो'),(158,' प्रोडक्ट 54 की कीमत 1700 रुपए करिये और उसकी बेचने वाली कीमत 3000 कीजिये'),(159,' Create a new product brick costing 8 rupees and the selling price is 12 rupees.\n The quantity is 5000 and tax is 9%. Also delete the product 54.\n'),(160,' can you create new product break costing 5 rupees selling price 8 rupees\n quantity is 2000 tax at 9%\n'),(161,' एक नया प्रोड़क बनाओ कार जिसकी प्राइस है 50,000 उसकी सेलिंग प्राइस है 80,000 उसकी क्वांटिटी 6 है और टैक्स उसपे 18% है'),(162,' Create profit loss report for the product IDs 35 and 54.\n'),(163,' Create profit loss report for the product, i.e. 35 and 54.\n'),(164,' Can you create profit loss report for the product 35 and 54?\n'),(165,' Please create profit loss report for the product 35 and 54\n'),(166,' Create Profit Loss Report for Product 35 and 54\n'),(167,' Please create a profit loss report for product 35 and 54.\n'),(168,' Can you create profit and loss report on product 35 and 54?\n'),(169,' Create new loan for Adam. I gave him 2000 rupees for petrol.\n'),(170,' Can you send an email to Adam regarding reprimand of the loan given to him?\n'),(171,' Send and remind the email to Adam to repay his loan back.\n'),(172,' I gave Adam $5,000 for buying chairs.\n'),(173,' I gave Adam Rs 5000 for buying chairs.\n'),(174,' I gave Adam a loan of Rs. 5000 for buying chair.\n'),(175,' I gave a loan of rupees 5,000 to Adam for buying a chair.\n'),(176,' I gave a loan of Rs. 5000 to Adam for buying a chair.\n'),(177,' I gave a loan of Rs. 5000 to Adam for buying charity.\n'),(178,' Send an reminder email to Adam for being by the loan.\n'),(179,' Send a reminder email to Adam for paying back the loan taken for charity.\n'),(180,' Send a reminder email to item for paying back the loan taken for charity.\n'),(181,' Send a Reminder email to Adam for paying back the loan taken for charity.\n'),(182,' Send a reminder email to Adam for paying back the loan taken for charity.\n'),(183,' Adam paid me back Rs. 3000 after he got his salary.\n'),(184,' Adam paid his debt back after he got his salary.\n He paid me rupees 3000 to fulfill the loan.\n'),(185,' Send an email to Adam for reminding him to pay his loan back.\n'),(186,' Send an email to Adam reminding him to pay his loan back which he had borrowed from me.\n'),(187,' Send an email to Adam to repay his loan which he borrowed from me for charity.\n'),(188,' Send an email to Adam reminding him to pay his loan back which he borrowed from me.\n'),(189,' Send an email to Adam to remind him that he needs to pay his loan back, that he borrowed.\n'),(190,' Send an email to Adam to remind him to pay his loan back that he borrowed.\n'),(191,' Now remind Adam to pay his loan back that he borrowed from me.\n'),(192,' Send an email to a adam to pay his loan back that he borrowed from me pay the remaining\n amount.\n'),(193,' Send an email to Ganesh.Boothkar@vit.edu\n'),(194,' create new loan Jake with the email address as backup triple 9 at gmail.com with\n the loan amount 2000\n'),(195,' मैंने आडम को 2000 रुपए ऐस लोन दिये उसे गाड़ी में पेट्रोल डालना था इसलिए'),(196,' कि मुझे एक नया आइटम बनाना है जिसका नाम है कैमेरा उसकी कीमत है 700 रुपए और उसकी सेलिंग कीमत है 800 रुपए उसके चार क्वांटिटी है और 14 परसेंट टैक्स है अ'),(197,' मुझे एक नया आइटम बनाना है जिसका नाम है कैमेरा उसकी 400 रुपई कीमत है उसकी सेलिंग कीमत 800 रुपई है और उसकी क्वांटिटी 6 है टैक्स 14% है ये आइटम बनाओ'),(198,' मुझे एक नया आइटम बनाना है जिसका नाम है कैमेरा उसकी कीमत 400 रुपए है और उसकी बेचने वाली कीमत 800 रुपए है उसकी क्वांटिटी 4 है और टैक्स 10%'),(199,' मुझे जो प्रोडक्ट नंबर 69 है उसमें के दो प्रोडक्ट बेच दीजिये उसे सेल कर देना है'),(200,' I gave Rs. 3500 to Adam for him to buy a calculator.\n'),(201,' I gave Rs 3500 to Adam as a loan for him to buy a calculator.\n'),(202,' Send an email to Adam referring him to pay back his loan due amount.\n'),(203,' Generate the profit and loss report for the product 35, 54 and 69.\n'),(204,' Then rate profit and loss report for the product 35, 54 and 69.\n'),(205,' Create the sales report for the product, 35, 69 and 54.\n'),(206,' So, I create a new product called Stapler which price is 30 rupees, the selling price is 60 rupees, quantity is 10 and the tax is 10 as well, also update the price of product 54 to 3000 rupees.\n');
/*!40000 ALTER TABLE `transcript` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor`
--

DROP TABLE IF EXISTS `vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `vendor_name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text,
  `vendor_address` varchar(1000) DEFAULT NULL,
  `vendor_email` varchar(255) DEFAULT NULL,
  `vendor_phone` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor`
--

LOCK TABLES `vendor` WRITE;
/*!40000 ALTER TABLE `vendor` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-17  7:34:56
