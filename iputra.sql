-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 04, 2021 at 05:36 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `iputra`
--

-- --------------------------------------------------------

--
-- Table structure for table `iputrastaff`
--

CREATE TABLE `iputrastaff` (
  `staffid` int(11) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `iputrastaff`
--

INSERT INTO `iputrastaff` (`staffid`, `password`) VALUES
(1001, '12345');

-- --------------------------------------------------------

--
-- Table structure for table `notif`
--

CREATE TABLE `notif` (
  `id` int(11) NOT NULL,
  `vid` int(11) NOT NULL,
  `remark` varchar(1000) NOT NULL DEFAULT 'Accepted'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `notif`
--

INSERT INTO `notif` (`id`, `vid`, `remark`) VALUES
(1, 6, 'Invalid image');

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE `registration` (
  `matric` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `passport` varchar(50) NOT NULL,
  `faculty` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`matric`, `name`, `passport`, `faculty`, `password`) VALUES
('P103490', 'Yusuf Sunusi', 'A08021212', 'FTSM', '12345');

-- --------------------------------------------------------

--
-- Table structure for table `vapply`
--

CREATE TABLE `vapply` (
  `id` int(11) NOT NULL,
  `type` varchar(20) NOT NULL DEFAULT 'Renewal',
  `matric` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `passport` varchar(50) NOT NULL,
  `photo` varchar(500) NOT NULL,
  `passp` varchar(500) NOT NULL,
  `offer` varchar(500) NOT NULL,
  `val` varchar(500) NOT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vapply`
--

INSERT INTO `vapply` (`id`, `type`, `matric`, `email`, `phone`, `passport`, `photo`, `passp`, `offer`, `val`, `status`) VALUES
(1, 'Renewal', 'P103490', 'yusufsunusi63@gmail.com', '0196812507', 'A08021212', 'Photograph.jpg', '006aab07-a0c0-4778-9cf4-d482cfc9033f.jpg', 'AOB.xlsx', '2001.07331.pdf', 'Approved'),
(2, 'Renewal', 'P103490', 'yusufsunusi63@gmail.com', '0196812507', 'A08021212', 'Photograph.jpg', '006aab07-a0c0-4778-9cf4-d482cfc9033f.jpg', 'AOB.xlsx', '2001.07331.pdf', 'Approved'),
(3, 'Renewal', 'P103490', 'yusufsunusi63@gmail.com', '0196812507', 'A08021212', 'Photograph.jpg', '006aab07-a0c0-4778-9cf4-d482cfc9033f.jpg', 'AOB.xlsx', '2001.07331.pdf', 'Approved'),
(4, 'New', 'P103490', 'yusufsunusi63@gmail.com', '0196812507', 'A08021212', '1705.04304.pdf', '2001.07331.pdf', 'arXiv_2001.07331v1 [cs.CL] 21 Jan 2020.pdf', 'c70e2def6c953ac34706f153f3d3ab2371d7.pdf', 'Approved'),
(5, 'Renewal', 'P103490', 'yusufsunusi63@gmail.com', '0196812507', 'A08021212', '1705.04304.pdf', '2001.07331.pdf', 'arXiv_2001.07331v1 [cs.CL] 21 Jan 2020.pdf', 'c70e2def6c953ac34706f153f3d3ab2371d7.pdf', 'Approved'),
(6, 'Dependent', 'P103490', 'yusufsunusi63@gmail.com', '0196812507', 'A08021212', '006aab07-a0c0-4778-9cf4-d482cfc9033f.jpg', '67211600-b0d3-4b37-ad52-82ee59a6dd06.jpg', '1495787226228-grocery banner.jpg', '3332a502-e333-4d01-902a-5ce348777232.jpg', 'Declined');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `iputrastaff`
--
ALTER TABLE `iputrastaff`
  ADD PRIMARY KEY (`staffid`);

--
-- Indexes for table `notif`
--
ALTER TABLE `notif`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `registration`
--
ALTER TABLE `registration`
  ADD PRIMARY KEY (`matric`);

--
-- Indexes for table `vapply`
--
ALTER TABLE `vapply`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `notif`
--
ALTER TABLE `notif`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `vapply`
--
ALTER TABLE `vapply`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
