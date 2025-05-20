-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 20, 2025 at 07:32 AM
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
('B001', 'Pulpen', 'Snowman', 'pcs', 20),
('B002', 'Pensil', 'Faber Castell', 'pcs', 80),
('B003', 'Penghapus', 'Joyko', 'pcs', 50);

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
