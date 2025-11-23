-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: consultasmedicas
-- ------------------------------------------------------

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

-- Table structure for table `clinica`

DROP TABLE IF EXISTS `clinica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clinica` (
  `CodCli` int NOT NULL AUTO_INCREMENT,
  `NomeCli` varchar(50) NOT NULL,
  `Endereco` varchar(100) DEFAULT NULL,
  `Telefone` varchar(13) DEFAULT NULL,
  `Email` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`CodCli`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

-- Table structure for table `log_auditoria`

DROP TABLE IF EXISTS `log_auditoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_auditoria` (
  `IdLog` int NOT NULL AUTO_INCREMENT,
  `Mensagem` varchar(255) DEFAULT NULL,
  `DataOcorrencia` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`IdLog`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

-- Table structure for table `medico`

DROP TABLE IF EXISTS `medico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medico` (
  `CodMed` int NOT NULL AUTO_INCREMENT,
  `NomeMed` varchar(50) NOT NULL,
  `Sexo` char(1) DEFAULT NULL,
  `Telefone` varchar(13) DEFAULT NULL,
  `Email` varchar(254) DEFAULT NULL,
  `Especialidade` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CodMed`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

-- Table structure for table `paciente`

DROP TABLE IF EXISTS `paciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paciente` (
  `CpfPaciente` char(11) NOT NULL,
  `NomePac` varchar(50) NOT NULL,
  `DataNascimento` date DEFAULT NULL,
  `Sexo` char(1) DEFAULT NULL,
  `Telefone` varchar(13) DEFAULT NULL,
  `Email` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`CpfPaciente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

-- Table structure for table `consulta`

DROP TABLE IF EXISTS `consulta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consulta` (
  `IdConsulta` int NOT NULL AUTO_INCREMENT,
  `CodCli` int DEFAULT NULL,
  `CodMed` int DEFAULT NULL,
  `CpfPaciente` char(11) DEFAULT NULL,
  `Data_Hora` datetime DEFAULT NULL,
  PRIMARY KEY (`IdConsulta`),
  KEY `fk_clinica` (`CodCli`),
  KEY `fk_medico` (`CodMed`),
  KEY `fk_paciente` (`CpfPaciente`),
  CONSTRAINT `fk_clinica` FOREIGN KEY (`CodCli`) REFERENCES `clinica` (`CodCli`),
  CONSTRAINT `fk_medico` FOREIGN KEY (`CodMed`) REFERENCES `medico` (`CodMed`),
  CONSTRAINT `fk_paciente` FOREIGN KEY (`CpfPaciente`) REFERENCES `paciente` (`CpfPaciente`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

-- Dumping data for table `clinica`

LOCK TABLES `clinica` WRITE;
/*!40000 ALTER TABLE `clinica` DISABLE KEYS */;
INSERT INTO `clinica` VALUES 
(1,'Clínica Saúde Total','Av. Paulista, 1000','11999998888','contato@saudetotal.com'),
(2,'Centro Médico Viver Bem','Rua das Flores, 230','11988887777','viverbem@saude.com'),
(3,'Hospital Dia Zona Sul','Av. Santo Amaro, 4500','1133334444','atendimento@hospdia.com'),
(4,'Clínica Oftalmológica Visão','Rua Augusta, 500','1132221111','contato@visaoclinica.com'),
(5,'Espaço Saúde Mulher','Rua dos Pinheiros, 120','11977776666','agendamento@saudemulher.com');
/*!40000 ALTER TABLE `clinica` ENABLE KEYS */;
UNLOCK TABLES;

-- Dumping data for table `log_auditoria`

LOCK TABLES `log_auditoria` WRITE;
/*!40000 ALTER TABLE `log_auditoria` DISABLE KEYS */;

-- Tabela começa vazia, pra quando o Trigger ser criado poder receberr dados

/*!40000 ALTER TABLE `log_auditoria` ENABLE KEYS */;
UNLOCK TABLES;

-- Dumping data for table `medico`

LOCK TABLES `medico` WRITE;
/*!40000 ALTER TABLE `medico` DISABLE KEYS */;
INSERT INTO `medico` VALUES 
(1,'Dr. Roberto Silva','M','11988887777','roberto@medico.com','Cardiologia'),
(2,'Dra. Amanda Vieira','F','11999991111','amanda@medico.com','Pediatria'),
(3,'Dr. Lucas Carvalho','M','11988882222','lucas@medico.com','Oftalmologia'),
(4,'Dra. Fernanda Lima','F','11977773333','fernanda@medico.com','Dermatologia'),
(5,'Dra. Carla Dias','F','11966665555','carla@medico.com','Ginecologia'),
(6,'Dr. Bruno Souza','M','11955554444','bruno@medico.com','Ortopedia'),
(7,'Dra. Juliana Paes','F','11944443333','juliana@medico.com','Cardiologia'),
(8,'Dr. Ricardo Oliveira','M','11933332222','ricardo@medico.com','Neurologia'),
(9,'Dra. Patrícia Santos','F','11922221111','patricia@medico.com','Pediatria'),
(10,'Dr. Marcos Vinícius','M','11911110000','marcos@medico.com','Clínico Geral');
/*!40000 ALTER TABLE `medico` ENABLE KEYS */;
UNLOCK TABLES;

-- Dumping data for table `paciente`

LOCK TABLES `paciente` WRITE;
/*!40000 ALTER TABLE `paciente` DISABLE KEYS */;
INSERT INTO `paciente` VALUES 
('11122233344','Carlos Eduardo','1985-10-10','M','11912341234','carlos@email.com'),
('12312312312','Karen Souza','1982-10-10','F','11911112222','karen@email.com'),
('12345678900','Ana Souza','1990-05-15','F','11977776666','ana.souza@email.com'),
('22233344455','Beatriz Costa','2001-03-30','F','11933334444','bia@email.com'),
('33344455566','Daniel Ferreira','1975-07-12','M','11955556666','daniel@email.com'),
('34512389765','Rebeca Lins','1993-04-15','F','81999454177','rebeca@email.com'),
('44455566677','Eduarda Rocha','1999-09-09','F','11977778888','duda@email.com'),
('55566677788','Felipe Santos','1988-02-14','M','11999990000','felipe@email.com'),
('58961234752','Paulo Martins','2020-08-21','M','81998734312','paulo@email.com'),
('66677788899','Gabriela Silva','1995-11-20','F','11988881111','gabi@email.com'),
('77788899900','Hugo Almeida','2010-06-05','M','11977772222','hugo@email.com'),
('88899900011','Isabela Moura','2015-01-28','F','11966663333','isa@email.com'),
('99900011122','João Pedro','1960-08-15','M','11955554444','jp@email.com'),
('99988877766','Lucas Pereira','1997-04-01','M','11944445555','lucas.pereira@email.com'),
('99999999999','Maria Clara','2005-05-05','F','11933336666','maria@email.com');
/*!40000 ALTER TABLE `paciente` ENABLE KEYS */;
UNLOCK TABLES;

-- Dumping data for table `consulta`
LOCK TABLES `consulta` WRITE;
/*!40000 ALTER TABLE `consulta` DISABLE KEYS */;
INSERT INTO `consulta` VALUES 
(1,1,1,'12345678900','2023-12-20 14:30:00'),
(2,1,1,'12345678900','2023-12-25 10:00:00'),
(3,2,3,'34512389765','2025-12-10 16:40:00'),
(4,2,3,'58961234752','2025-12-11 10:00:00'),
(5,3,4,'11122233344','2025-11-25 14:30:00'),
(6,1,2,'58961234752','2025-11-26 09:00:00'),
(7,4,5,'12312312312','2025-11-27 08:00:00'),
(8,4,5,'22233344455','2025-11-27 09:00:00'),
(9,5,6,'33344455566','2025-11-28 10:00:00'),
(10,5,6,'44455566677','2025-11-28 11:00:00'),
(11,1,7,'55566677788','2025-11-29 14:00:00'),
(12,2,8,'66677788899','2025-12-01 15:00:00'),
(13,3,9,'77788899900','2025-12-02 09:00:00'),
(14,3,9,'88899900011','2025-12-02 10:00:00'),
(15,4,10,'99900011122','2025-12-03 11:00:00'),
(16,1,1,'99988877766','2025-12-05 16:00:00'),
(17,2,3,'99999999999','2025-12-06 08:30:00'),
(18,3,4,'12345678900','2025-12-07 13:00:00'),
(19,5,5,'34512389765','2026-01-10 14:00:00'),
(20,1,6,'11122233344','2026-01-11 09:00:00'),
(21,2,7,'22233344455','2026-01-12 10:00:00');
/*!40000 ALTER TABLE `consulta` ENABLE KEYS */;
UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
