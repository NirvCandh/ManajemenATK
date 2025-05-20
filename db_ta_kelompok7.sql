-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 21, 2025 at 01:01 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_ta_kelompok7`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `hapus_barang` (IN `p_kode_barang` VARCHAR(10))   BEGIN
    DELETE FROM barang WHERE kode_barang = p_kode_barang;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `hapus_detail_permintaan` (IN `p_id_permintaan` VARCHAR(10), IN `p_kode_barang` VARCHAR(10))   BEGIN
    DELETE FROM detail_permintaan WHERE id_permintaan = p_id_permintaan AND kode_barang = p_kode_barang;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `hapus_penerimaan` (IN `p_id` VARCHAR(10))   BEGIN
    DELETE FROM penerimaan WHERE id_penerimaan = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `hapus_pengeluaran` (IN `p_id` VARCHAR(10))   BEGIN
    DELETE FROM pengeluaran WHERE id_pengeluaran = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `hapus_pengguna` (IN `p_id` VARCHAR(10))   BEGIN
    DELETE FROM pengguna WHERE id_pengguna = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `hapus_permintaan` (IN `p_id` VARCHAR(10))   BEGIN
    DELETE FROM permintaan WHERE id_permintaan = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `hapus_supplier` (IN `p_id` VARCHAR(10))   BEGIN
    DELETE FROM supplier WHERE id_supplier = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `lihat_barang` ()   BEGIN
    SELECT * FROM barang;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `lihat_barang_satu` (IN `p_kode_barang` VARCHAR(10))   BEGIN
    SELECT nama_barang, stok, merek, satuan FROM barang WHERE kode_barang = p_kode_barang;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `lihat_detail_permintaan` ()   BEGIN
    SELECT * FROM detail_permintaan;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `lihat_penerimaan` ()   BEGIN
    SELECT * FROM penerimaan;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `lihat_pengeluaran` ()   BEGIN
    SELECT * FROM pengeluaran;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `lihat_pengeluaran_satu` (IN `p_id_pengeluaran` INT)   BEGIN
    SELECT id_pengeluaran, kode_barang, jml_keluar, tgl_keluar, tujuan, id_pemohon, id_petugas
    FROM pengeluaran
    WHERE id_pengeluaran = p_id_pengeluaran;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `lihat_pengguna` ()   BEGIN
    SELECT * FROM pengguna;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `lihat_permintaan` ()   BEGIN
    SELECT 
        p.id_permintaan,
        p.tgl_permintaan,
        p.status,
        p.id_pemohon,
        pemohon.nama_lengkap AS nama_pemohon,
        p.id_petugas,
        petugas.nama_lengkap AS nama_petugas,
        p.tgl_setuju
    FROM permintaan p
    LEFT JOIN pengguna pemohon ON p.id_pemohon = pemohon.id_pengguna
    LEFT JOIN pengguna petugas ON p.id_petugas = petugas.id_pengguna;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `lihat_supplier` ()   BEGIN
    SELECT * FROM supplier;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `tambah_barang` (IN `p_kode_barang` VARCHAR(10), IN `p_nama_barang` VARCHAR(50), IN `p_merek` VARCHAR(30), IN `p_satuan` VARCHAR(20), IN `p_stok` INT)   BEGIN
    INSERT INTO barang VALUES (p_kode_barang, p_nama_barang, p_merek, p_satuan, p_stok);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `tambah_detail_permintaan` (IN `p_id_permintaan` VARCHAR(10), IN `p_kode_barang` VARCHAR(10), IN `p_jumlah` INT)   BEGIN
    INSERT INTO detail_permintaan VALUES (p_id_permintaan, p_kode_barang, p_jumlah);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `tambah_penerimaan` (IN `p_id` VARCHAR(10), IN `p_kode_barang` VARCHAR(10), IN `p_id_supplier` VARCHAR(10), IN `p_jml_masuk` INT, IN `p_tgl` DATE, IN `p_harga` DECIMAL(10,0), IN `p_petugas` VARCHAR(10))   BEGIN
    INSERT INTO penerimaan VALUES (p_id, p_kode_barang, p_id_supplier, p_jml_masuk, p_tgl, p_harga, p_petugas);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `tambah_pengeluaran` (IN `p_id` VARCHAR(10), IN `p_kode_barang` VARCHAR(10), IN `p_jml_keluar` INT, IN `p_tgl` DATE, IN `p_tujuan` VARCHAR(50), IN `p_pemohon` VARCHAR(10), IN `p_petugas` VARCHAR(10))   BEGIN
    INSERT INTO pengeluaran VALUES (p_id, p_kode_barang, p_jml_keluar, p_tgl, p_tujuan, p_pemohon, p_petugas);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `tambah_pengguna` (IN `p_id` VARCHAR(10), IN `p_nama` VARCHAR(100), IN `p_user` VARCHAR(50), IN `p_pass` VARCHAR(255), IN `p_role` ENUM('Admin','Petugas','Pemohon'), IN `p_unit` VARCHAR(50), IN `p_email` VARCHAR(100), IN `p_status` BOOLEAN, IN `p_login` DATETIME)   BEGIN
    INSERT INTO pengguna VALUES (p_id, p_nama, p_user, p_pass, p_role, p_unit, p_email, p_status, p_login);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `tambah_permintaan` (IN `p_id` VARCHAR(10), IN `p_pemohon` VARCHAR(10), IN `p_tgl` DATE, IN `p_status` VARCHAR(30), IN `p_petugas` VARCHAR(10), IN `p_tgl_setuju` DATE)   BEGIN
    INSERT INTO permintaan VALUES (p_id, p_pemohon, p_tgl, p_status, p_petugas, p_tgl_setuju);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `tambah_supplier` (IN `p_id` VARCHAR(10), IN `p_nama` VARCHAR(50))   BEGIN
    INSERT INTO supplier VALUES (p_id, p_nama);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_barang` (IN `p_kode_barang` VARCHAR(10), IN `p_nama_barang` VARCHAR(50), IN `p_merek` VARCHAR(30), IN `p_satuan` VARCHAR(20), IN `p_stok` INT)   BEGIN
    UPDATE barang
    SET nama_barang = p_nama_barang,
        merek = p_merek,
        satuan = p_satuan,
        stok = p_stok
    WHERE kode_barang = p_kode_barang;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_detail_permintaan` (IN `p_id_permintaan` VARCHAR(10), IN `p_kode_barang` VARCHAR(10), IN `p_jumlah` INT)   BEGIN
    UPDATE detail_permintaan SET jumlah = p_jumlah WHERE id_permintaan = p_id_permintaan AND kode_barang = p_kode_barang;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_penerimaan` (IN `p_id` VARCHAR(10), IN `p_kode_barang` VARCHAR(10), IN `p_id_supplier` VARCHAR(10), IN `p_jml_masuk` INT, IN `p_tgl` DATE, IN `p_harga` DECIMAL(10,0), IN `p_petugas` VARCHAR(10))   BEGIN
    UPDATE penerimaan SET kode_barang = p_kode_barang, id_supplier = p_id_supplier, jml_masuk = p_jml_masuk, tgl_masuk = p_tgl, harga = p_harga, id_petugas = p_petugas WHERE id_penerimaan = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_pengeluaran` (IN `p_id` VARCHAR(10), IN `p_kode_barang` VARCHAR(10), IN `p_jml_keluar` INT, IN `p_tgl` DATE, IN `p_tujuan` VARCHAR(50), IN `p_pemohon` VARCHAR(10), IN `p_petugas` VARCHAR(10))   BEGIN
    UPDATE pengeluaran SET kode_barang = p_kode_barang, jml_keluar = p_jml_keluar, tgl_keluar = p_tgl, tujuan = p_tujuan, id_pemohon = p_pemohon, id_petugas = p_petugas WHERE id_pengeluaran = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_pengguna` (IN `p_id` VARCHAR(10), IN `p_nama` VARCHAR(100), IN `p_user` VARCHAR(50), IN `p_pass` VARCHAR(255), IN `p_role` ENUM('Admin','Petugas','Pemohon'), IN `p_unit` VARCHAR(50), IN `p_email` VARCHAR(100), IN `p_status` BOOLEAN, IN `p_login` DATETIME)   BEGIN
    UPDATE pengguna SET nama_lengkap = p_nama, username = p_user, password = p_pass, role = p_role, unit = p_unit, email = p_email, status_aktif = p_status, last_login = p_login WHERE id_pengguna = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_permintaan` (IN `p_id` VARCHAR(10), IN `p_pemohon` VARCHAR(10), IN `p_tgl` DATE, IN `p_status` VARCHAR(30), IN `p_petugas` VARCHAR(10), IN `p_tgl_setuju` DATE)   BEGIN
    UPDATE permintaan SET id_pemohon = p_pemohon, tgl_permintaan = p_tgl, status = p_status, id_petugas = p_petugas, tgl_setuju = p_tgl_setuju WHERE id_permintaan = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_supplier` (IN `p_id` VARCHAR(10), IN `p_nama` VARCHAR(50))   BEGIN
    UPDATE supplier SET nama_supplier = p_nama WHERE id_supplier = p_id;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `barang`
--

CREATE TABLE `barang` (
  `kode_barang` varchar(10) NOT NULL,
  `nama_barang` varchar(50) NOT NULL,
  `merek` varchar(30) NOT NULL,
  `satuan` varchar(20) NOT NULL,
  `stok` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `barang`
--

INSERT INTO `barang` (`kode_barang`, `nama_barang`, `merek`, `satuan`, `stok`) VALUES
('B001', 'Pulpen', 'Snowman', 'pcs', 25),
('B002', 'Pensil', 'Faber Castell', 'pcs', 80);

-- --------------------------------------------------------

--
-- Table structure for table `detail_permintaan`
--

CREATE TABLE `detail_permintaan` (
  `id_permintaan` varchar(10) NOT NULL,
  `kode_barang` varchar(10) NOT NULL,
  `jumlah` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `detail_permintaan`
--

INSERT INTO `detail_permintaan` (`id_permintaan`, `kode_barang`, `jumlah`) VALUES
('PR001', 'B001', 10),
('PR002', 'B002', 5);

-- --------------------------------------------------------

--
-- Table structure for table `penerimaan`
--

CREATE TABLE `penerimaan` (
  `id_penerimaan` varchar(10) NOT NULL,
  `kode_barang` varchar(10) NOT NULL,
  `id_supplier` varchar(10) NOT NULL,
  `jml_masuk` int(11) NOT NULL,
  `tgl_masuk` date NOT NULL,
  `harga` decimal(12,2) NOT NULL,
  `id_petugas` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `penerimaan`
--

INSERT INTO `penerimaan` (`id_penerimaan`, `kode_barang`, `id_supplier`, `jml_masuk`, `tgl_masuk`, `harga`, `id_petugas`) VALUES
('P001', 'B001', 'S001', 50, '2024-01-10', 2000.00, 'PG001'),
('P002', 'B002', 'S002', 30, '2024-02-15', 1500.00, 'PG001');

--
-- Triggers `penerimaan`
--
DELIMITER $$
CREATE TRIGGER `trg_kurangi_stok_setelah_hapus_penerimaan` AFTER DELETE ON `penerimaan` FOR EACH ROW BEGIN
    UPDATE barang
    SET stok = stok - OLD.jml_masuk
    WHERE kode_barang = OLD.kode_barang;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_tambah_stok_setelah_penerimaan` AFTER INSERT ON `penerimaan` FOR EACH ROW BEGIN
    UPDATE barang
    SET stok = stok + NEW.jml_masuk
    WHERE kode_barang = NEW.kode_barang;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `pengeluaran`
--

CREATE TABLE `pengeluaran` (
  `id_pengeluaran` varchar(10) NOT NULL,
  `kode_barang` varchar(10) NOT NULL,
  `jml_keluar` int(11) NOT NULL,
  `tgl_keluar` date NOT NULL,
  `tujuan` varchar(50) NOT NULL,
  `id_pemohon` varchar(10) NOT NULL,
  `id_petugas` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pengeluaran`
--

INSERT INTO `pengeluaran` (`id_pengeluaran`, `kode_barang`, `jml_keluar`, `tgl_keluar`, `tujuan`, `id_pemohon`, `id_petugas`) VALUES
('K001', 'B001', 10, '2024-01-12', 'Kelas X IPA', 'PM001', 'PG001'),
('K002', 'B001', 5, '2024-02-17', 'TU', 'PM001', 'PG001');

--
-- Triggers `pengeluaran`
--
DELIMITER $$
CREATE TRIGGER `trg_kurangi_stok_setelah_pengeluaran` AFTER INSERT ON `pengeluaran` FOR EACH ROW BEGIN
    UPDATE barang
    SET stok = stok - NEW.jml_keluar
    WHERE kode_barang = NEW.kode_barang;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_restore_stok_setelah_hapus_pengeluaran` AFTER DELETE ON `pengeluaran` FOR EACH ROW BEGIN
    UPDATE barang
    SET stok = stok + OLD.jml_keluar
    WHERE kode_barang = OLD.kode_barang;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `pengguna`
--

CREATE TABLE `pengguna` (
  `id_pengguna` varchar(10) NOT NULL,
  `nama_lengkap` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Admin','Petugas','Pemohon','') NOT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pengguna`
--

INSERT INTO `pengguna` (`id_pengguna`, `nama_lengkap`, `username`, `password`, `role`, `unit`, `email`) VALUES
('', 'Nirw Candh', 'nirw', '$2b$12$RTc5Om3FMydvHCKBlF/Sw.U7bakkblZAOHFOQd1P6kViLIh7g0MEq', 'Pemohon', NULL, 'nirw@sekolah.ac.id'),
('AD001', 'Admin Sistem', 'admin_sistem', 'hashed_pass3', 'Admin', '', 'admin@sekolah.ac.id'),
('PG001', 'Yopin Winda', 'yopin_wnd', 'hashed_pass1', 'Petugas', 'TU', 'yopin@sekolah.ac.id\r\n\r\n'),
('PM001', 'Nadia Rahma', 'nadiarhm', 'hashed_pass2', 'Pemohon', 'Guru', 'nadia@sekolah.ac.id');

-- --------------------------------------------------------

--
-- Table structure for table `permintaan`
--

CREATE TABLE `permintaan` (
  `id_permintaan` varchar(10) NOT NULL,
  `id_pemohon` varchar(10) NOT NULL,
  `tgl_permintaan` date NOT NULL,
  `status` varchar(30) NOT NULL,
  `id_petugas` varchar(10) NOT NULL,
  `tgl_setuju` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `permintaan`
--

INSERT INTO `permintaan` (`id_permintaan`, `id_pemohon`, `tgl_permintaan`, `status`, `id_petugas`, `tgl_setuju`) VALUES
('PR001', 'PM001', '2024-01-10', 'Disetujui', 'PG001', '2024-01-11'),
('PR002', 'PM001', '2024-02-10', 'Menunggu Persetujuan', 'PG001', '2024-02-12');

-- --------------------------------------------------------

--
-- Table structure for table `supplier`
--

CREATE TABLE `supplier` (
  `id_supplier` varchar(10) NOT NULL,
  `nama_supplier` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `supplier`
--

INSERT INTO `supplier` (`id_supplier`, `nama_supplier`) VALUES
('S001', 'Toko ATK Jaya'),
('S002', 'ATK Murah Meriah');

-- --------------------------------------------------------

--
-- Stand-in structure for view `view_detail_permintaan`
-- (See below for the actual view)
--
CREATE TABLE `view_detail_permintaan` (
`id_permintaan` varchar(10)
,`nama_barang` varchar(50)
,`jumlah` int(11)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `view_laporan_penerimaan`
-- (See below for the actual view)
--
CREATE TABLE `view_laporan_penerimaan` (
`id_penerimaan` varchar(10)
,`tgl_masuk` date
,`nama_barang` varchar(50)
,`nama_supplier` varchar(50)
,`jml_masuk` int(11)
,`harga` decimal(12,2)
,`petugas` varchar(100)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `view_laporan_pengeluaran`
-- (See below for the actual view)
--
CREATE TABLE `view_laporan_pengeluaran` (
`id_pengeluaran` varchar(10)
,`tgl_keluar` date
,`nama_barang` varchar(50)
,`jml_keluar` int(11)
,`tujuan` varchar(50)
,`pemohon` varchar(100)
,`petugas` varchar(100)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `view_permintaan_disetujui`
-- (See below for the actual view)
--
CREATE TABLE `view_permintaan_disetujui` (
`id_permintaan` varchar(10)
,`tgl_permintaan` date
,`pemohon` varchar(100)
,`petugas` varchar(100)
,`tgl_setuju` date
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `view_stok_barang`
-- (See below for the actual view)
--
CREATE TABLE `view_stok_barang` (
`kode_barang` varchar(10)
,`nama_barang` varchar(50)
,`merek` varchar(30)
,`satuan` varchar(20)
,`stok` int(11)
);

-- --------------------------------------------------------

--
-- Structure for view `view_detail_permintaan`
--
DROP TABLE IF EXISTS `view_detail_permintaan`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_detail_permintaan`  AS SELECT `dp`.`id_permintaan` AS `id_permintaan`, `b`.`nama_barang` AS `nama_barang`, `dp`.`jumlah` AS `jumlah` FROM (`detail_permintaan` `dp` join `barang` `b` on(`dp`.`kode_barang` = `b`.`kode_barang`)) ;

-- --------------------------------------------------------

--
-- Structure for view `view_laporan_penerimaan`
--
DROP TABLE IF EXISTS `view_laporan_penerimaan`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_laporan_penerimaan`  AS SELECT `p`.`id_penerimaan` AS `id_penerimaan`, `p`.`tgl_masuk` AS `tgl_masuk`, `b`.`nama_barang` AS `nama_barang`, `s`.`nama_supplier` AS `nama_supplier`, `p`.`jml_masuk` AS `jml_masuk`, `p`.`harga` AS `harga`, `u`.`nama_lengkap` AS `petugas` FROM (((`penerimaan` `p` join `barang` `b` on(`p`.`kode_barang` = `b`.`kode_barang`)) join `supplier` `s` on(`p`.`id_supplier` = `s`.`id_supplier`)) join `pengguna` `u` on(`p`.`id_petugas` = `u`.`id_pengguna`)) ;

-- --------------------------------------------------------

--
-- Structure for view `view_laporan_pengeluaran`
--
DROP TABLE IF EXISTS `view_laporan_pengeluaran`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_laporan_pengeluaran`  AS SELECT `k`.`id_pengeluaran` AS `id_pengeluaran`, `k`.`tgl_keluar` AS `tgl_keluar`, `b`.`nama_barang` AS `nama_barang`, `k`.`jml_keluar` AS `jml_keluar`, `k`.`tujuan` AS `tujuan`, `pemohon`.`nama_lengkap` AS `pemohon`, `petugas`.`nama_lengkap` AS `petugas` FROM (((`pengeluaran` `k` join `barang` `b` on(`k`.`kode_barang` = `b`.`kode_barang`)) join `pengguna` `pemohon` on(`k`.`id_pemohon` = `pemohon`.`id_pengguna`)) join `pengguna` `petugas` on(`k`.`id_petugas` = `petugas`.`id_pengguna`)) ;

-- --------------------------------------------------------

--
-- Structure for view `view_permintaan_disetujui`
--
DROP TABLE IF EXISTS `view_permintaan_disetujui`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_permintaan_disetujui`  AS SELECT `pr`.`id_permintaan` AS `id_permintaan`, `pr`.`tgl_permintaan` AS `tgl_permintaan`, `pg`.`nama_lengkap` AS `pemohon`, `pt`.`nama_lengkap` AS `petugas`, `pr`.`tgl_setuju` AS `tgl_setuju` FROM ((`permintaan` `pr` join `pengguna` `pg` on(`pr`.`id_pemohon` = `pg`.`id_pengguna`)) join `pengguna` `pt` on(`pr`.`id_petugas` = `pt`.`id_pengguna`)) WHERE `pr`.`status` = 'Disetujui' ;

-- --------------------------------------------------------

--
-- Structure for view `view_stok_barang`
--
DROP TABLE IF EXISTS `view_stok_barang`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_stok_barang`  AS SELECT `barang`.`kode_barang` AS `kode_barang`, `barang`.`nama_barang` AS `nama_barang`, `barang`.`merek` AS `merek`, `barang`.`satuan` AS `satuan`, `barang`.`stok` AS `stok` FROM `barang` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `barang`
--
ALTER TABLE `barang`
  ADD PRIMARY KEY (`kode_barang`);

--
-- Indexes for table `detail_permintaan`
--
ALTER TABLE `detail_permintaan`
  ADD PRIMARY KEY (`id_permintaan`),
  ADD KEY `fk_detailpermintaan_barang` (`kode_barang`);

--
-- Indexes for table `penerimaan`
--
ALTER TABLE `penerimaan`
  ADD PRIMARY KEY (`id_penerimaan`),
  ADD KEY `fk_penerimaan_kodebarang` (`kode_barang`),
  ADD KEY `fk_penerimaan_idsupplier` (`id_supplier`),
  ADD KEY `fk_penerimaan_idpetugas` (`id_petugas`);

--
-- Indexes for table `pengeluaran`
--
ALTER TABLE `pengeluaran`
  ADD PRIMARY KEY (`id_pengeluaran`),
  ADD KEY `fk_pengeluaran_idpemohon` (`id_pemohon`),
  ADD KEY `fk_pengeluaran_idpetugas` (`kode_barang`),
  ADD KEY `fk_pengeluaran_petugas` (`id_petugas`);

--
-- Indexes for table `pengguna`
--
ALTER TABLE `pengguna`
  ADD PRIMARY KEY (`id_pengguna`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `permintaan`
--
ALTER TABLE `permintaan`
  ADD PRIMARY KEY (`id_permintaan`),
  ADD KEY `fk_permintaan_idpemohon` (`id_pemohon`),
  ADD KEY `fk_permintaan_idpetugas` (`id_petugas`);

--
-- Indexes for table `supplier`
--
ALTER TABLE `supplier`
  ADD PRIMARY KEY (`id_supplier`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `detail_permintaan`
--
ALTER TABLE `detail_permintaan`
  ADD CONSTRAINT `fk_detailpermintaan_barang` FOREIGN KEY (`kode_barang`) REFERENCES `barang` (`kode_barang`),
  ADD CONSTRAINT `fk_detailpermintaan_idpermintaan` FOREIGN KEY (`id_permintaan`) REFERENCES `permintaan` (`id_permintaan`);

--
-- Constraints for table `penerimaan`
--
ALTER TABLE `penerimaan`
  ADD CONSTRAINT `fk_penerimaan_idpetugas` FOREIGN KEY (`id_petugas`) REFERENCES `pengguna` (`id_pengguna`),
  ADD CONSTRAINT `fk_penerimaan_idsupplier` FOREIGN KEY (`id_supplier`) REFERENCES `supplier` (`id_supplier`),
  ADD CONSTRAINT `fk_penerimaan_kodebarang` FOREIGN KEY (`kode_barang`) REFERENCES `barang` (`kode_barang`);

--
-- Constraints for table `pengeluaran`
--
ALTER TABLE `pengeluaran`
  ADD CONSTRAINT `fk_pengeluaran_idpemohon` FOREIGN KEY (`id_pemohon`) REFERENCES `pengguna` (`id_pengguna`),
  ADD CONSTRAINT `fk_pengeluaran_idpetugas` FOREIGN KEY (`kode_barang`) REFERENCES `barang` (`kode_barang`),
  ADD CONSTRAINT `fk_pengeluaran_kodebarang` FOREIGN KEY (`kode_barang`) REFERENCES `barang` (`kode_barang`),
  ADD CONSTRAINT `fk_pengeluaran_petugas` FOREIGN KEY (`id_petugas`) REFERENCES `pengguna` (`id_pengguna`);

--
-- Constraints for table `permintaan`
--
ALTER TABLE `permintaan`
  ADD CONSTRAINT `fk_permintaan_idpemohon` FOREIGN KEY (`id_pemohon`) REFERENCES `pengguna` (`id_pengguna`),
  ADD CONSTRAINT `fk_permintaan_idpetugas` FOREIGN KEY (`id_petugas`) REFERENCES `pengguna` (`id_pengguna`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
