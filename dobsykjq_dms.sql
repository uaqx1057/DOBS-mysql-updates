-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 21, 2026 at 08:09 AM
-- Server version: 11.4.9-MariaDB-cll-lve-log
-- PHP Version: 8.3.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dobsykjq_dms`
--


-- --------------------------------------------------------

--
-- Table structure for table `drivers`
--

CREATE TABLE `drivers` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `branch_id` bigint(20) UNSIGNED DEFAULT NULL,
  `driver_type_id` bigint(20) UNSIGNED NOT NULL,
  `image` text DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `driver_id` varchar(255) DEFAULT NULL,
  `iqaama_number` varchar(255) DEFAULT NULL,
  `iqaama_expiry` date DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `absher_number` varchar(255) DEFAULT NULL,
  `sponsorship` varchar(255) DEFAULT NULL,
  `sponsorship_id` varchar(255) DEFAULT NULL,
  `license_expiry` date DEFAULT NULL,
  `insurance_policy_number` varchar(255) DEFAULT NULL,
  `insurance_expiry` date DEFAULT NULL,
  `vehicle_monthly_cost` decimal(10,2) NOT NULL DEFAULT 0.00,
  `mobile_data` decimal(10,2) NOT NULL DEFAULT 0.00,
  `fuel` decimal(10,2) NOT NULL DEFAULT 0.00,
  `gprs` decimal(10,2) NOT NULL DEFAULT 0.00,
  `government_levy_fee` decimal(10,2) NOT NULL DEFAULT 0.00,
  `accommodation` decimal(8,2) NOT NULL DEFAULT 0.00,
  `remarks` text DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `status` enum('Active','Inactive','Busy','Blocked') NOT NULL DEFAULT 'Inactive',
  `password` varchar(255) DEFAULT NULL,
  `nationality` varchar(255) DEFAULT NULL,
  `language` varchar(255) DEFAULT NULL,
  `saudi_driving_license` tinyint(1) DEFAULT 0,
  `previous_sponsor_number` varchar(50) DEFAULT NULL,
  `iqama_card_upload` varchar(200) DEFAULT NULL,
  `platform` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `car_details` varchar(200) DEFAULT NULL,
  `assignment_date` date DEFAULT NULL,
  `onboarding_stage` varchar(50) DEFAULT 'Ops Manager',
  `qiwa_contract_created` tinyint(1) DEFAULT 0,
  `company_contract_created` tinyint(1) DEFAULT 0,
  `qiwa_transfer_approved` tinyint(1) DEFAULT 0,
  `sponsorship_transfer_done` tinyint(1) DEFAULT 0,
  `qiwa_contract_status` varchar(20) DEFAULT 'Pending',
  `sponsorship_transfer_status` varchar(20) DEFAULT 'Pending',
  `ops_manager_approved_at` datetime DEFAULT NULL,
  `hr_approved_at` datetime DEFAULT NULL,
  `ops_supervisor_approved_at` datetime DEFAULT NULL,
  `fleet_manager_approved_at` datetime DEFAULT NULL,
  `finance_approved_at` datetime DEFAULT NULL,
  `ops_manager_approved` tinyint(1) DEFAULT 0,
  `hr_approved_by` int(11) DEFAULT NULL,
  `platform_id` varchar(50) DEFAULT NULL,
  `mobile_issued` tinyint(1) DEFAULT 0,
  `tamm_authorized` tinyint(1) DEFAULT 0,
  `transfer_fee_paid` tinyint(1) DEFAULT 0,
  `transfer_fee_amount` float DEFAULT NULL,
  `transfer_fee_paid_at` datetime DEFAULT NULL,
  `transfer_fee_receipt` varchar(200) DEFAULT NULL,
  `issued_mobile_number` varchar(20) DEFAULT NULL,
  `issued_device_id` varchar(100) DEFAULT NULL,
  `tamm_authorization_ss` varchar(200) DEFAULT NULL,
  `sponsorship_transfer_proof` varchar(200) DEFAULT NULL,
  `company_contract_file` varchar(200) DEFAULT NULL,
  `promissory_note_file` varchar(200) DEFAULT NULL,
  `qiwa_contract_file` varchar(200) DEFAULT NULL,
  `sponsorship_transfer_completed_at` datetime DEFAULT NULL,
  `offboarding_stage` varchar(50) DEFAULT NULL,
  `offboarding_reason` text DEFAULT NULL,
  `offboarding_requested_at` datetime DEFAULT NULL,
  `offboard_request` tinyint(1) DEFAULT 0,
  `offboard_requested_by` varchar(100) DEFAULT NULL,
  `offboard_reason` varchar(255) DEFAULT NULL,
  `offboard_requested_at` datetime DEFAULT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  `location_address` text DEFAULT NULL,
  `location_updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `drivers`
--

INSERT INTO `drivers` (`id`, `branch_id`, `driver_type_id`, `image`, `name`, `driver_id`, `iqaama_number`, `iqaama_expiry`, `dob`, `absher_number`, `sponsorship`, `sponsorship_id`, `license_expiry`, `insurance_policy_number`, `insurance_expiry`, `vehicle_monthly_cost`, `mobile_data`, `fuel`, `gprs`, `government_levy_fee`, `accommodation`, `remarks`, `email`, `mobile`, `deleted_at`, `created_at`, `updated_at`, `status`, `password`, `nationality`, `language`, `saudi_driving_license`, `previous_sponsor_number`, `iqama_card_upload`, `platform`, `city`, `car_details`, `assignment_date`, `onboarding_stage`, `qiwa_contract_created`, `company_contract_created`, `qiwa_transfer_approved`, `sponsorship_transfer_done`, `qiwa_contract_status`, `sponsorship_transfer_status`, `ops_manager_approved_at`, `hr_approved_at`, `ops_supervisor_approved_at`, `fleet_manager_approved_at`, `finance_approved_at`, `ops_manager_approved`, `hr_approved_by`, `platform_id`, `mobile_issued`, `tamm_authorized`, `transfer_fee_paid`, `transfer_fee_amount`, `transfer_fee_paid_at`, `transfer_fee_receipt`, `issued_mobile_number`, `issued_device_id`, `tamm_authorization_ss`, `sponsorship_transfer_proof`, `company_contract_file`, `promissory_note_file`, `qiwa_contract_file`, `sponsorship_transfer_completed_at`, `offboarding_stage`, `offboarding_reason`, `offboarding_requested_at`, `offboard_request`, `offboard_requested_by`, `offboard_reason`, `offboard_requested_at`, `latitude`, `longitude`, `location_address`, `location_updated_at`) VALUES
(2, NULL, 1, NULL, 'Adnan Mazhar Mazhar Javed', NULL, '2582280968', '2025-09-15', NULL, '0540920826', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '0', 'adnan_mazhar_mazhar_javed_2582280968.jpg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-11-25 09:56:09', NULL, NULL, NULL, NULL),
(10, NULL, 1, NULL, 'Anik Islam Khan', NULL, '2507197966', '2026-02-12', NULL, '0570051450', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '3', 'anik_islam_khan_2507197966.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(11, NULL, 1, NULL, 'MD Jowel Rana', NULL, '2607600836', '2025-12-06', NULL, '0558192843', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'md_jowel_rana_2607600836.jpeg', NULL, 'Makkah', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:41:36', NULL, NULL, NULL, NULL),
(12, NULL, 1, NULL, 'Delowar Hossain', NULL, '2609537614', '2026-05-11', NULL, '0509327739', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '2', 'delowar_hossain_2609537614.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:40:55', NULL, NULL, NULL, NULL),
(13, NULL, 1, NULL, 'Aneeb Akmal Muhammad Akmal', NULL, '2606270300', '2025-08-24', NULL, '0547715980', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'aneeb_akmal_muhammad_akmal_2606270300.jpg', NULL, 'Makkah', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(14, NULL, 1, NULL, 'MD Munna Molla', NULL, '2597972179', '2025-05-13', NULL, '0554745430', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'md_munna_molla_2597972179.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-11-05 14:37:48', NULL, NULL, NULL, NULL),
(15, NULL, 1, NULL, 'Musa Khan Habib Hassan', NULL, '2610419778', '2025-07-04', NULL, '0570746982', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'musa_khan_habib_hassan_2610419778.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-11-25 10:07:20', NULL, NULL, NULL, NULL),
(16, NULL, 1, NULL, 'Bachu Miah', NULL, '2609606526', '2026-09-25', NULL, '0535414028', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '2', 'bachu_miah_2609606526.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:40:44', NULL, NULL, NULL, NULL),
(17, NULL, 1, NULL, 'Usman Javed Muhammad Javed', NULL, '2596457545', '2025-05-05', NULL, '0574057846', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '2', 'usman_javed_muhammad_javed_2596457545.jpeg', NULL, 'Makkah', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:43:53', NULL, NULL, NULL, NULL),
(18, NULL, 1, NULL, 'Faisal Ibraheem Hafiz Ibraheem', NULL, '2554215828', '2025-09-16', NULL, '0597465497', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '2', 'faisal_ibraheem_hafiz_ibraheem_2554215828.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(19, NULL, 1, NULL, 'Muhammad Shahbaz Muhammad Ilyas', NULL, '2598029581', '2025-09-16', NULL, '0557849371', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'muhammad_shahbaz_muhammad_ilyas_2598029581.jpeg', NULL, 'Makkah', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-12-01 07:09:14', NULL, NULL, NULL, NULL),
(20, NULL, 1, NULL, 'Mageb Naji Mohammed Ahmed', NULL, '2587566841', '2026-01-18', NULL, '0569253071', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Yemen', NULL, 1, '1', 'mageb_naji_mohammed_ahmed_2587566841.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(21, NULL, 1, NULL, 'Basit Ali Basharat Ali', NULL, '2522251202', '2026-02-04', NULL, '0577843251', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'basit_ali_basharat_ali_2522251202.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-11-08 10:26:52', NULL, NULL, NULL, NULL),
(22, NULL, 1, NULL, 'Adil Arif Muhammad Arif', NULL, '2588649315', '2026-04-20', NULL, '0503531850', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'adil_arif_muhammad_arif_2588649315.jpeg', NULL, 'Al Hasa', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:38:57', NULL, NULL, NULL, NULL),
(23, NULL, 1, NULL, 'Saleh Abdo Mohammed Muthanna', NULL, '2604906350', '2025-09-10', NULL, '0575194145', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Yemen', NULL, 1, '1', 'saleh_abdo_mohammed_muthanna_2604906350.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(24, NULL, 1, NULL, 'MD Omor Faruk', NULL, '2528154509', '2023-03-26', NULL, '0574521574', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'md_omor_faruk_2528154509.jpeg', NULL, 'Makkah', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-11-26 08:28:24', NULL, NULL, NULL, NULL),
(25, NULL, 1, NULL, 'Tamer Mahmoud Mohamed Ali', NULL, '2597984372', '2025-09-14', NULL, '0542189876', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Egypt', NULL, 1, '1', 'tamer_mahmoud_mohamed_ali_2597984372.jpeg', NULL, 'Makkah', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(26, NULL, 1, NULL, 'Altayeb Abdelftah Abdelbagi Osman', NULL, '2604521431', '2025-07-15', NULL, '0574707415', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Sudan', NULL, 1, '1', 'altayeb_abdelftah_abdelbagi_osman_2604521431.jpeg', NULL, 'Makkah', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(27, NULL, 1, NULL, 'MD Bayzid Hossen', NULL, '2597971528', '2025-09-09', NULL, '0537569713', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'md_bayzid_hossen_2597971528.jpeg', NULL, 'Makkah', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-11-25 09:56:37', NULL, NULL, NULL, NULL),
(28, NULL, 1, NULL, 'Md Rihan Khan', NULL, '2610550358', '2025-09-27', NULL, '0572396876', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'md_rihan_khan_2610550358.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(29, NULL, 1, NULL, 'Usman Sabir', NULL, '2602107266', '2025-09-16', NULL, '0559329625', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'usman_sabir_2602107266.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:44:24', NULL, NULL, NULL, NULL),
(30, NULL, 1, NULL, 'Amjad Gurashi Abdelzain Alawal', NULL, '2514006341', '2022-08-29', NULL, '0545634038', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Sudan', NULL, 1, '1', 'amjad_gurashi_abdelzain_alawal_2514006341.jpeg', NULL, 'Jeddah', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-11-25 13:35:32', NULL, NULL, NULL, NULL),
(31, NULL, 1, NULL, 'MD Akash Mia', NULL, '2619012194', '2026-03-31', NULL, '0570051450', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 0, '1', 'md_akash_mia_2619012194.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(32, NULL, 1, NULL, 'Muhammad Usama Muhammad Yaqoob', NULL, '2606371629', '2026-06-16', NULL, '0502852678', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'muhammad_usama_muhammad_yaqoob_2606371629.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 1, 'Pending', 'Approved', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:42:46', NULL, NULL, NULL, NULL),
(34, NULL, 1, NULL, 'Tariq Mahmood Muhammad Saleh', NULL, '2562327797', '2024-12-03', NULL, '0595763927', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'tariq_mahmood_muhammad_saleh_2562327797.jpg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-11-29 10:37:43', NULL, NULL, NULL, NULL),
(35, NULL, 1, NULL, 'Muhammad Harun Khalifa', NULL, '2612530424', '2025-10-30', NULL, '0576614124', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'muhammad_harun_khalifa_2612530424.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(36, NULL, 1, NULL, 'Al Amin', NULL, '2561486776', '2025-10-16', NULL, '0557642399', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '2', 'al_amin_2561486776.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-06 08:29:58', NULL, NULL, NULL, NULL),
(38, NULL, 1, NULL, 'Haider Ali Muhammad Riaz', NULL, '2581813918', '2025-12-26', NULL, '0537893694', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '2', 'haider_ali_muhammad_riaz_2581813918.jpeg', NULL, 'Jeddah', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-11-25 13:04:40', NULL, NULL, NULL, NULL),
(39, NULL, 1, NULL, 'MD Jalal Hossain Munna ', NULL, '2561482858', '2025-09-02', NULL, '0538830566', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '2', 'md_jalal_hossain_munna__2561482858.jpg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-06 08:29:34', NULL, NULL, NULL, NULL),
(40, NULL, 1, NULL, 'Raja Wahab Ijaz Ahmed', NULL, '2583149261', '2025-11-27', NULL, '0551736743', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '2', 'raja_wahab_ijaz_ahmed_2583149261.jpg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:43:02', NULL, NULL, NULL, NULL),
(41, NULL, 1, NULL, 'S M Atikur Rahaman Babu', NULL, '2561408523', '2025-12-14', NULL, '0570185383', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '2', 's_m_atikur_rahaman_babu_2561408523.jpg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:43:19', NULL, NULL, NULL, NULL),
(42, NULL, 1, NULL, 'Sajjad Ahmed Muhammad Ishaq', NULL, '2603902632', '2025-07-25', NULL, '0538936701', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '2', 'sajjad_ahmed_muhammad_ishaq_2603902632.jpeg', NULL, 'Al Hasa', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:43:32', NULL, NULL, NULL, NULL),
(43, NULL, 1, NULL, 'Muhammad Daniyal Raza', NULL, '2589563630', '2025-02-21', NULL, '0552604780', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'muhammad_daniyal_raza_2589563630.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-11-25 10:07:10', NULL, NULL, NULL, NULL),
(44, NULL, 1, NULL, 'Mehadi Hasan', NULL, '2589413562', '2025-08-19', NULL, '0572594403', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'mehadi_hasan_2589413562.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:42:04', NULL, NULL, NULL, NULL),
(45, NULL, 1, NULL, 'Abdullah Ahmed Abdullah Haidarah', NULL, '2594766939', '2025-03-24', NULL, '0532541776', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Yemen', NULL, 1, '1', 'abdullah_ahmed_abdullah_haidarah_2594766939.jpeg', NULL, 'Makkah', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(46, NULL, 1, NULL, 'Mueen Nazir Ahmad Khan', NULL, '2487699080', '2025-08-19', NULL, '0558379148', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'India', NULL, 1, '2', 'mueen_nazir_ahmad_khan_2487699080.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(47, NULL, 1, NULL, 'Najm Aldaine Abdullah Ahmed', NULL, '2591011404', '2026-01-10', NULL, '0525910114', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Yemen', NULL, 1, '1', 'najm_aldaine_abdullah_ahmed_2591011404.jpeg', NULL, 'Makkah', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-12-06 08:29:07', NULL, NULL, NULL, NULL),
(48, NULL, 1, NULL, 'Tahir Ali Sabz Ali Khan', NULL, '2615236615', '2025-09-06', NULL, '0526152366', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'tahir_ali_sabz_ali_khan_2615236615.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-11-25 10:15:12', NULL, NULL, NULL, NULL),
(49, NULL, 1, NULL, 'Abdullah Hames Hamood Gumaan', NULL, '2601490101', '2025-10-04', NULL, '0507540711', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Yemen', NULL, 1, '1', 'abdullah_hames_hamood_gumaan_2601490101.jpg', NULL, 'Al Hasa', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:39:05', NULL, NULL, NULL, NULL),
(50, NULL, 1, NULL, 'Naveed Khursheed Khursheed Ahmed', NULL, '2603971819', '2025-07-25', NULL, '0590796385', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'naveed_khursheed_khursheed_ahmed_2603971819.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-11-25 09:57:09', NULL, NULL, NULL, NULL),
(51, NULL, 1, NULL, 'Asad Ali Khan Shakeel', NULL, '2592284463', '2025-08-21', NULL, '0576752427', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'asad_ali_khan_shakeel_2592284463.jpeg', NULL, 'Al Hasa', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:40:06', NULL, NULL, NULL, NULL),
(52, NULL, 1, NULL, 'MD Arif Hosen', NULL, '2607802994', '2025-09-21', NULL, '0571952368', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'md_arif_hosen_2607802994.jpeg', NULL, 'Al Hasa', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:41:24', NULL, NULL, NULL, NULL),
(53, NULL, 1, NULL, 'Ammad Afzal Muhammad Afzal', NULL, '2569270651', '2025-08-26', NULL, '0539581963', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'ammad_afzal_muhammad_afzal_2569270651.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:39:42', NULL, NULL, NULL, NULL),
(54, NULL, 1, NULL, 'Aziz ul Rehman', NULL, '2561484607', '2024-10-27', NULL, '0538042594', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'aziz_ul_rehman_2561484607.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:40:34', NULL, NULL, NULL, NULL),
(55, NULL, 1, NULL, 'Aiyub Ali', NULL, '2610087856', '2026-07-04', NULL, '0578281418', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'aiyub_ali_2610087856.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:39:18', NULL, NULL, NULL, NULL),
(57, NULL, 1, NULL, 'Fares Ahmed Ahmed Alwali', NULL, '2590592396', '2025-12-20', NULL, '0547377326', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Yemen', NULL, 1, '1', 'fares_ahmed_ahmed_alwali_2590592396.jpeg', NULL, 'Makkah', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(58, NULL, 1, NULL, 'Muhammad Saleem Akram', NULL, '2577011113', '2025-09-10', NULL, '0549965768', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'muhammad_saleem_akram_2577011113.jpeg', NULL, 'Al Hasa', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 13:41:54', NULL, NULL, NULL, NULL),
(59, NULL, 1, NULL, 'Samim MD Shahjalal', NULL, '2599839566', '2026-05-25', NULL, '0581172698', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'samim_md_shahjalal_2599839566.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-12-03 07:23:05', NULL, NULL, NULL, NULL),
(60, NULL, 1, NULL, 'Muntaser Ahmed Msaad Ahmed', NULL, '2339142172', '2022-09-30', NULL, '0531459798', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Sudan', NULL, 1, '1', 'muntaser_ahmed_msaad_ahmed_2339142172.jpg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(61, NULL, 1, NULL, 'Zameer Abbas Malik Ilyas Khan', NULL, '2577182922', '2025-07-26', NULL, '0541231443', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'zameer_abbas_malik_ilyas_khan_2577182922.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-11-25 13:06:33', NULL, NULL, NULL, NULL),
(62, NULL, 1, NULL, 'Ebrahim Hubaysh Mahdi Nasser J', NULL, '2466307432', '2025-01-15', NULL, '0500000000', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Yemen', NULL, 1, '1', 'ebrahim_hubaysh_mahdi_nasser_j_2466307432.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-11-25 13:36:50', NULL, NULL, NULL, NULL),
(63, NULL, 1, NULL, 'Muzammel Hoque', NULL, '2609437906', '2026-06-15', NULL, '0576324718', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'muzammel_hoque_2609437906.jpeg', NULL, 'Al Hasa', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-11-29 10:38:51', NULL, NULL, NULL, NULL),
(64, NULL, 1, NULL, 'Muhammad Saqib Hanif Muhammad', NULL, '2259547251', '2025-09-03', NULL, '0594484134', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '1', 'muhammad_saqib_hanif_muhammad_2259547251.jpg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(65, NULL, 1, NULL, 'Omar Abdu Abdullah Othman', NULL, '2190465506', '2025-10-23', NULL, '0500000000', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Yemen', NULL, 1, '1', 'omar_abdu_abdullah_othman_2190465506.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-11-25 13:07:12', NULL, NULL, NULL, NULL),
(66, NULL, 1, NULL, 'MD Rostom Ali', NULL, '2618248005', '2025-12-31', NULL, '0573012819', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'md_rostom_ali_2618248005.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(67, NULL, 1, NULL, 'Anowar Rased Sheikh', NULL, '2591955428', '2026-03-06', NULL, '0534932784', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'anowar_rased_sheikh_2591955428.jpeg', NULL, 'Al Hasa', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-12-30 08:39:55', NULL, NULL, NULL, NULL),
(68, NULL, 1, NULL, 'Mohamed Karar Alshekikh Koko', NULL, '2545619898', '2027-05-20', NULL, '0546652261', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Sudan', NULL, 1, '1', 'mohamed_karar_alshekikh_koko_2545619898.jpeg', NULL, 'Abha', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'تاخير في الرواتب', '2025-11-25 13:33:55', NULL, NULL, NULL, NULL),
(69, NULL, 1, NULL, 'MD Shamim Miah ', NULL, '2615501331', '2025-12-05', NULL, '0578246795', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '1', 'md_shamim_miah__2615501331.jpeg', NULL, 'Dammam', NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'moayad', 'الذهاب الي شركه اخري', '2025-11-25 13:06:00', NULL, NULL, NULL, NULL),
(71, NULL, 1, NULL, 'ALIYU KEBEDE MOHAMMED', NULL, '2615541758', '2026-12-01', NULL, '0531621377', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Ethiopia', NULL, 1, '0', 'aliyu_kebede_mohammed_.jpg', NULL, 'Dammam', NULL, NULL, 'Ops Supervisor', 0, 1, 0, 0, 'Pending', 'Pending', '2025-11-26 12:10:38', '2025-11-26 12:48:42', NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'ALIYU_KEBEDE_MOHAMMED_2615541758_company_contract_file.pdf', 'ALIYU_KEBEDE_MOHAMMED_2615541758_promissory_note_file.pdf', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(174, 3, 2, NULL, 'Lucas Herman', 'D2197', '0909090909', '1977-06-07', '1111-11-11', 'Libero cumque enim q', 'Eligendi autem conse', 'Commodi enim consequ', '2002-02-28', '533', '1999-08-17', 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, 'cafadola@mailinator.com', 'Est quia veniam qui', NULL, '2024-11-25 05:17:19', '2024-11-25 05:21:04', 'Inactive', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(175, 4, 1, 'drivers/V3bQcH1tsFno7XZOp6WM5jaKt3zKVgf6aYwkUPZg.jpg', 'Noel Bonner', 'D2198', '5099090909', '1974-09-18', '1111-11-11', 'Quas voluptates itaq', 'Proident ut placeat', 'Nihil maiores quos e', '1981-06-16', '602', '1978-07-06', 1.00, 100.00, 100.00, 100.00, 880.00, 200.00, 'test', 'ryje@mailinator.com', 'Irure molestiae cons', NULL, '2024-11-25 07:30:50', '2025-11-05 23:43:46', 'Inactive', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'uae', 'Arabic', 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(176, 2, 1, 'drivers/VnMDjCiJPzbMbQ64qU2A1m5C4E8vDZEwDZ9eAaNb.jpg', 'Muhammad Haseeb Muhammad Riaz', 'D2199', '2581758568', '2024-10-22', '1999-03-01', '537482787', 'Speed', '7037959405', '2032-06-23', '25829804', '2025-10-21', 1247.00, 100.00, 100.00, 100.00, 880.00, 200.00, NULL, 'haseebriaz@speed.sa', '582843952', NULL, '2024-11-25 09:12:26', '2024-11-25 09:12:26', 'Inactive', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(178, 1, 1, NULL, 'Manoj', 'D2200', '1234567898', '2025-08-22', '2015-12-28', '11223344', 'bnxb', 'rdgdfgfdg', '2025-08-22', 'gfdgfdgfdg', '2025-08-23', 1247.00, 100.00, 100.00, 100.00, 880.00, 200.00, NULL, 'dd@gmail.com', '8888888888', NULL, '2025-08-21 17:55:20', '2025-08-21 18:17:50', 'Inactive', NULL, 'indian', 'English', 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(179, 1, 1, NULL, 'asd', 'D2201', '1212321323', '1974-09-18', '1111-11-11', '213145', 'Proident ut placeat', 'asdasdq', '1981-06-16', '1', '1978-07-06', 1247.00, 100.00, 100.00, 100.00, 880.00, 200.00, NULL, 'asadwad@1231.com', '9834908214', NULL, '2025-08-23 15:13:33', '2025-12-30 20:50:29', 'Inactive', '$2y$12$BRgu4Kw.OYWyJZzLZDH0NOa81SNDeug17FrNW14CJEwQzBAII9ZJ6', 'safasdf', 'Hindi', 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(180, 2, 2, NULL, 'Ginger Goodwin', 'D2202', '6151111111', '1987-09-28', '2007-08-04', 'Porro neque est dolo', 'Fugiat eum incididu', 'Ratione et excepteur', '2014-04-02', '339', '1977-02-24', 11.00, 100.00, 100.00, 100.00, 880.00, 200.00, NULL, 'hadoxevyx@mailinator.com', 'Blanditiis ipsam eiu', NULL, '2025-10-16 11:25:09', '2025-11-02 18:10:59', 'Inactive', NULL, 'Est sint non hic mol', 'English', 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(181, 3, 1, NULL, 'Reece Bray', 'D2203', '5680999999', '1980-10-20', '1988-12-22', 'Nam dolore cupiditat', 'Quis reiciendis volu', 'Sit id nihil sunt c', '2001-01-03', '941', '1987-08-04', 8.00, 100.00, 100.00, 100.00, 880.00, 200.00, NULL, 'gagovo@mailinator.com', 'Esse esse aut tempo', NULL, '2025-10-16 14:36:52', '2025-12-30 22:09:01', 'Inactive', '$2y$12$BNt8xTzJcUXRBqKyVD7Gf.z9Rl3B7sN4bLzLzPt.MfDiheKoFdb5m', 'Officia voluptatem p', 'Arabic', 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(182, 4, 2, NULL, 'Yoko Yates', 'D2204', '2868888888', '1984-07-07', '1976-12-25', 'Corporis elit volup', 'Pariatur Non et et ', 'Iste blanditiis quae', '1989-10-23', '976', '2022-06-02', 11.00, 100.00, 100.00, 100.00, 880.00, 200.00, NULL, 'dihuqaw@mailinator.com', 'Consequat Facere iu', NULL, '2025-10-18 09:22:48', '2025-11-04 00:59:16', 'Inactive', NULL, 'Duis qui fuga Provi', 'Hindi', 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(183, 3, 1, NULL, 'Kevin Duke', 'D2205', '7331111111', '2011-06-14', '1971-01-13', 'Vel voluptas sunt qu', 'Amet ipsa ea tempo', 'Nihil et sit est et', '2002-05-07', '955', '1998-01-10', 1.00, 100.00, 100.00, 100.00, 880.00, 200.00, NULL, 'jopyziqin@mailinator.com', 'Quisquam in molestia', NULL, '2025-10-18 10:14:47', '2026-01-21 17:05:15', 'Inactive', '$2y$12$qT93fxwP2hu0EbUvHfTe/u1mWvlnZ9ShcTvC7cXvrYb29yJIikaYe', 'Perspiciatis quaera', 'English', 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, '32.329953', '74.349205', NULL, '2026-01-05 00:58:30'),
(184, 4, 1, NULL, 'Pascale Phillips', 'D2206', '9120000000', '2019-10-04', '2020-11-27', 'Voluptas qui vitae e', 'Sunt sit corporis se', 'Dolor inventore nobi', '2015-02-21', '87', '2020-12-02', 4.00, 100.00, 100.00, 100.00, 880.00, 200.00, NULL, 'kezohis@mailinator.com', 'Sed ad laudantium n', NULL, '2025-10-20 08:05:55', '2025-12-30 21:13:09', 'Inactive', '$2y$12$UUyDv9cJkbldrAXYnVY3ae0foUQyc5v14SlAwtBYR5KnPqlIGViL.', 'Tenetur magnam exped', 'Arabic', 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, '26.302368', '50.21029', NULL, '2025-12-30 21:13:09'),
(185, 2, 2, 'drivers/B6USCCWABpiR9JZCZcB3D8Pbq7RITilDlk290GBL.jpg', 'Germaine Potts1', 'D2207', '2167777777', '1979-05-03', '2006-04-16', 'Sit ab animi quas b', 'Voluptates laborum o', 'Molestias quia amet', '1989-01-28', '291', '1987-11-04', 11.00, 100.00, 100.00, 100.00, 880.00, 200.00, NULL, 'lonaje9276@dretnar.com', 'Amet temporibus ea1', NULL, '2025-10-21 23:55:20', '2026-01-21 20:23:30', 'Inactive', '$2y$12$jTlKqPCwwzDJBvVh6UMo1eWEesxFxznznLOfSTsqFnVzGNQ7GbQZ2', 'Nisi reiciendis corp1', 'Hindi1', 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, '32.3371336', '74.3686342', NULL, '2026-01-21 20:23:19'),
(195, NULL, 1, NULL, 'SAMEH MAGD MAGD', NULL, '2516800600', '2026-08-15', NULL, '0566978834', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Egypt', NULL, 1, '2', 'sameh_magd_magd_2516800600.jpeg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-01 12:58:18', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(196, NULL, 1, NULL, 'HMEDAN MOHAMMED BAKHIET', NULL, '2624460180', '2026-09-06', NULL, '0535341678', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Sudan', NULL, 1, '0', 'hmedan_mohammed_bakhiet_2624460180.jpeg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-01 12:58:25', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(197, NULL, 1, NULL, 'GAMIL AHMED QAID ', NULL, '2586454049', '2026-12-01', NULL, '0568757782', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Yemen', NULL, 1, '0', 'gamil_ahmed_qaid__2586454049.jpeg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-01 13:52:01', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(198, 2, 1, NULL, 'usman asif test', 'D2208', '2585305937', '2025-12-10', '1997-12-10', '0568465058', '00000', '124578', '2030-05-01', '124578', '2025-12-10', 1247.00, 100.00, 100.00, 100.00, 880.00, 200.00, NULL, 'usman@ilab.sa', '0568465058', NULL, '2026-01-02 01:06:16', '2026-01-21 21:09:31', 'Inactive', '$2y$12$hh8AxYt7MySLxZf.wtjIW..72SHbtMXZTvlSV.lNoY9xzXHbg1MRC', 'Pakistan', 'English', 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Completed', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, '26.3167327', '50.2232835', NULL, '2026-01-21 21:09:31'),
(199, NULL, 1, NULL, 'ELSIDDIG', NULL, '2385297029', '2026-03-17', NULL, '0502739733', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Sudan', NULL, 1, '1', 'elsiddig_2385297029.jpg', NULL, 'Khamis Mushait', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-03 10:01:03', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(200, NULL, 1, NULL, 'Amr Hafez Abdel Hameed Mansour', NULL, '2246002980', '2026-05-16', NULL, '0563130584', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Egypt', NULL, 1, '1', 'amr_hafez_abdel_hameed_mansour_2246002980.jpg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-04 08:58:46', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(202, NULL, 1, NULL, 'mohamed fouda', NULL, '2605511233', '2026-01-30', NULL, '0550409528', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Egypt', NULL, 1, '1', 'mohamed_fouda_2605511233.jpg', NULL, 'Al Ahsa', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-04 08:59:01', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(203, NULL, 1, NULL, 'Mahmed alhbeb atyeb ahmed', NULL, '2442258774', '2026-09-20', NULL, '0510598941', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Sudan', NULL, 1, '3', 'mahmed_alhbeb_atyeb_ahmed_2442258774.jpg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-04 10:13:53', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(204, NULL, 1, NULL, 'Ahmedmaherfawzy', NULL, '2621565981', '2027-02-01', NULL, '0565785919', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Egypt', NULL, 1, '5', 'ahmedmaherfawzy_2621565981.jpg', NULL, 'Riyadh', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-04 10:24:28', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(205, NULL, 1, NULL, 'KHALFALLAHHMDABDULMOLABLAL', NULL, '2484121831 ', '2025-12-08', NULL, '0535199103', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Sudan', NULL, 1, '2', 'khalfallahhmdabdulmolablal_2484121831_.pdf', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-04 10:24:50', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(207, NULL, 1, NULL, 'MOHAMMED ALHINDI', NULL, '2465350987', '2026-04-11', NULL, '0504470507', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Yemen', NULL, 1, '5', 'mohammed_alhindi_2465350987.png', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-05 07:21:36', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(209, NULL, 1, NULL, 'Abdullah Salem Saleh bh marhool', NULL, '2614655708', '2025-11-19', NULL, '0506102864', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Yemen', NULL, 1, '2', 'abdullah_salem_saleh_bh_marhool_2614655708.jpg', NULL, 'Khobar', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-05 07:21:41', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `drivers` (`id`, `branch_id`, `driver_type_id`, `image`, `name`, `driver_id`, `iqaama_number`, `iqaama_expiry`, `dob`, `absher_number`, `sponsorship`, `sponsorship_id`, `license_expiry`, `insurance_policy_number`, `insurance_expiry`, `vehicle_monthly_cost`, `mobile_data`, `fuel`, `gprs`, `government_levy_fee`, `accommodation`, `remarks`, `email`, `mobile`, `deleted_at`, `created_at`, `updated_at`, `status`, `password`, `nationality`, `language`, `saudi_driving_license`, `previous_sponsor_number`, `iqama_card_upload`, `platform`, `city`, `car_details`, `assignment_date`, `onboarding_stage`, `qiwa_contract_created`, `company_contract_created`, `qiwa_transfer_approved`, `sponsorship_transfer_done`, `qiwa_contract_status`, `sponsorship_transfer_status`, `ops_manager_approved_at`, `hr_approved_at`, `ops_supervisor_approved_at`, `fleet_manager_approved_at`, `finance_approved_at`, `ops_manager_approved`, `hr_approved_by`, `platform_id`, `mobile_issued`, `tamm_authorized`, `transfer_fee_paid`, `transfer_fee_amount`, `transfer_fee_paid_at`, `transfer_fee_receipt`, `issued_mobile_number`, `issued_device_id`, `tamm_authorization_ss`, `sponsorship_transfer_proof`, `company_contract_file`, `promissory_note_file`, `qiwa_contract_file`, `sponsorship_transfer_completed_at`, `offboarding_stage`, `offboarding_reason`, `offboarding_requested_at`, `offboard_request`, `offboard_requested_by`, `offboard_reason`, `offboard_requested_at`, `latitude`, `longitude`, `location_address`, `location_updated_at`) VALUES
(214, NULL, 1, NULL, 'Ahmed elsayed moghazy', NULL, '2620645107', '2026-02-04', NULL, '0507185282', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Egypt', NULL, 1, '0', 'ahmed_elsayed_moghazy_2620645107.jpg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-11 12:39:32', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(219, NULL, 1, NULL, 'Muhammad Ayub', NULL, '2546560240', '2026-07-07', NULL, '0597897115', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '0', 'muhammad_ayub_2546560240.jpg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-12 11:51:53', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(220, NULL, 1, NULL, 'Zamir sultan ', NULL, '2486516418', '2026-12-29', NULL, '0573233078', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '2', 'zamir_sultan__2486516418.jpg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-12 11:52:10', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(221, NULL, 1, NULL, 'Shakirullah Mirtaj Ali ', NULL, '2261714402', '2026-07-18', NULL, '0582520661', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '3', 'shakirullah_mirtaj_ali__2261714402.pdf', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-12 12:36:37', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(222, NULL, 1, NULL, 'Rokan', NULL, '2623394810', '2026-09-26', NULL, '0535358187', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Bangladesh', NULL, 1, '0', 'rokan_2623394810.jpg', NULL, 'Khobar', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-13 07:45:43', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(223, NULL, 1, NULL, 'Yousuf ali', NULL, '2606556187', '2026-06-27', NULL, '0567820383', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'India', NULL, 1, '1', 'yousuf_ali_2606556187.pdf', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-13 07:45:53', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(224, NULL, 1, NULL, 'Shihabdeen Abudul Jabbar', NULL, '2522962816', '2026-10-27', NULL, '0510262968', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'India', NULL, 1, '1', 'shihabdeen_abudul_jabbar_2522962816.pdf', NULL, 'Khobar', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-13 07:45:59', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(225, NULL, 1, NULL, 'Arshad Javed', NULL, '2622333520', '2026-02-23', NULL, '0550180768', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '0', 'arshad_javed_2622333520.jpg', NULL, 'Jeddah', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-13 07:46:26', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(226, NULL, 1, NULL, 'Ashwin sequeira', NULL, '2615004443', '2025-12-02', NULL, '0573354528', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'India', NULL, 0, '0', 'ashwin_sequeira_2615004443.jpg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-17 08:11:09', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(227, NULL, 1, NULL, 'Muhammad Bilal Liaqat Khan ', NULL, '2473633309', '2026-05-10', NULL, '0565657449', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '4', 'muhammad_bilal_liaqat_khan__2473633309.jpg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-14 11:20:57', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(230, NULL, 1, NULL, 'MAZHER KHAN', NULL, '2614194682', '2026-10-17', NULL, '0578809027', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'India', NULL, 1, '0', 'mazher_khan_2614194682.jpg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-14 11:20:39', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(231, NULL, 1, NULL, 'MOHAMMAD NAZEER', NULL, '2617219957', '2026-11-30', NULL, '0532662896', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'India', NULL, 1, '0', 'mohammad_nazeer_2617219957.jpg', NULL, 'Khobar', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-17 08:10:51', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(232, NULL, 1, NULL, 'Ahmed Kabeer', NULL, '2566192338', '2026-03-19', NULL, '0570872346', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'India', NULL, 1, '1', 'ahmed_kabeer_2566192338.jpg', NULL, 'Khobar', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-19 10:42:44', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(233, NULL, 1, NULL, 'Shaik Sameer Basha ', NULL, '2596087961', '2026-03-23', NULL, '0508825154', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'India', NULL, 1, '1', 'shaik_sameer_basha__2596087961.jpg', NULL, 'Dammam', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-20 08:42:05', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(234, NULL, 1, NULL, 'AHAN ALI', NULL, '2599043144', '2026-03-10', NULL, '0543898078', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '0', 'ahan_ali_2599043144.jpg', NULL, 'Abha', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-20 08:42:20', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(236, NULL, 1, NULL, 'USMAN GHANI', NULL, '2620125605', '2027-01-04', NULL, '0550875897', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Pakistan', NULL, 1, '0', 'usman_ghani_2620125605.pdf', NULL, 'Khobar', NULL, NULL, 'HR', 0, 0, 0, 0, 'Pending', 'Pending', '2026-01-20 08:42:26', NULL, NULL, NULL, NULL, 1, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(237, NULL, 1, NULL, 'Ahsan iqbal', NULL, '2610398063', '2026-09-06', NULL, '0562945685', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'Other', NULL, 1, '0', 'ahsan_iqbal_2610398063.png', NULL, 'Khobar', NULL, NULL, 'Ops Manager', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(238, NULL, 1, NULL, 'Mohammad Alam', NULL, '2480979893', '2026-10-20', NULL, '0583733202', NULL, NULL, NULL, NULL, NULL, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL, NULL, NULL, NULL, NULL, NULL, 'Inactive', NULL, 'India', NULL, 1, '2', 'mohammad_alam_2480979893.pdf', NULL, 'Khobar', NULL, NULL, 'Ops Manager', 0, 0, 0, 0, 'Pending', 'Pending', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `driver_attendances`
--

CREATE TABLE `driver_attendances` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `driver_id` bigint(20) UNSIGNED NOT NULL,
  `branch_id` bigint(20) UNSIGNED DEFAULT NULL,
  `checkin_time` timestamp NULL DEFAULT NULL,
  `checkout_time` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `meter_reading` int(11) DEFAULT NULL,
  `meter_image` text DEFAULT NULL,
  `car_image` text DEFAULT NULL,
  `out_meter_reading` varchar(255) DEFAULT NULL,
  `out_meter_image` varchar(255) DEFAULT NULL,
  `checkin_auto` int(11) NOT NULL DEFAULT 0,
  `checkout_auto` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `driver_attendances`
--

INSERT INTO `driver_attendances` (`id`, `driver_id`, `branch_id`, `checkin_time`, `checkout_time`, `created_at`, `updated_at`, `meter_reading`, `meter_image`, `car_image`, `out_meter_reading`, `out_meter_image`, `checkin_auto`, `checkout_auto`) VALUES
(33, 198, 2, '2026-01-20 20:22:31', '2026-01-20 20:22:55', '2026-01-20 20:22:31', '2026-01-20 20:22:55', 1, 'meter_images/J40jr4952uiEe1fzPjzvhcBw5laVsivPZ6w3JJjR.jpg', NULL, '22', 'meter_images/MQFwh45k4UCC0XTIrNtTbcdUrh8TzDNGv0IWS6zP.jpg', 0, 0),
(34, 198, 2, '2026-01-20 20:23:21', '2026-01-21 01:00:16', '2026-01-20 20:23:21', '2026-01-21 01:00:16', 22, 'meter_images/0F38xPg9mfmV7vqlMX9MzX4SlnkVLZXvAtWzSdqR.jpg', NULL, NULL, NULL, 0, 1),
(35, 185, 2, '2026-01-19 20:52:54', '2026-01-20 04:59:59', '2026-01-20 20:52:54', '2026-01-20 04:59:59', 566, 'meter_images/iWuHmpUR3ydlbBIVg89O58VNqeCmCjmCSKdAivRU.jpg', NULL, NULL, NULL, 0, 1),
(37, 185, 2, '2026-01-20 05:00:00', '2026-01-21 04:59:59', '2026-01-20 23:50:11', '2026-01-21 04:59:59', NULL, NULL, NULL, NULL, NULL, 1, 1),
(39, 185, 2, '2026-01-21 05:00:00', '2026-01-21 16:20:21', '2026-01-21 16:20:16', '2026-01-21 16:20:21', NULL, NULL, NULL, NULL, NULL, 1, 1),
(40, 185, 2, '2026-01-21 15:38:32', '2026-01-21 19:45:11', '2026-01-21 16:38:32', '2026-01-21 19:45:11', 666, 'meter_images/0LHdldbx5mBTFsNTsOQVYS8gFgU4LEhbJ94vO6ay.jpg', NULL, NULL, NULL, 0, 1),
(43, 183, 3, '2026-01-21 05:00:00', '2026-01-21 05:40:00', '2026-01-21 16:45:15', '2026-01-21 16:45:16', NULL, NULL, NULL, NULL, NULL, 1, 1),
(44, 183, 3, '2026-01-21 16:15:00', '2026-01-21 17:05:15', '2026-01-21 16:45:15', '2026-01-21 17:05:15', NULL, NULL, NULL, NULL, NULL, 1, 1),
(45, 185, 2, '2026-01-21 19:47:38', '2026-01-21 19:49:44', '2026-01-21 19:47:38', '2026-01-21 19:49:44', 333, 'meter_images/PjvcKwfA7SsCYEurHcOVHWJ73EmevOhzsF78FDFC.jpg', NULL, '66', 'meter_images/WwRDzORcpeIW40kzv9BqbQPjONrpkdsujQFdwOUz.jpg', 0, 0),
(46, 185, 2, '2026-01-21 19:56:51', '2026-01-21 20:05:09', '2026-01-21 19:56:51', '2026-01-21 20:05:09', 555, 'meter_images/27u30zadd0P3dQ50PMsxlyCsadjIzPAd3pZX154Y.jpg', NULL, NULL, NULL, 0, 1),
(47, 185, 2, '2026-01-21 20:10:23', '2026-01-21 20:23:30', '2026-01-21 20:10:23', '2026-01-21 20:23:30', 555, 'meter_images/PtfI6qgJfARDFbVaAbRYhnHoa5ETsxzi0EbJniuj.jpg', NULL, '66', 'meter_images/us6tJQyA5u4N529BrZQn0SeTnBJVBL0EN4h9w8db.jpg', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `driver_business_ids`
--

CREATE TABLE `driver_business_ids` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `driver_id` bigint(20) UNSIGNED NOT NULL,
  `business_id_id` bigint(20) UNSIGNED NOT NULL,
  `previous_driver_id` bigint(20) UNSIGNED DEFAULT NULL,
  `assigned_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `transferred_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `driver_business_ids`
--

INSERT INTO `driver_business_ids` (`id`, `driver_id`, `business_id_id`, `previous_driver_id`, `assigned_at`, `transferred_at`, `created_at`, `updated_at`) VALUES
(3, 187, 21, NULL, '2025-10-21 14:17:48', NULL, '2025-10-21 14:17:48', '2025-10-21 14:17:48'),
(4, 185, 3, NULL, '2025-10-21 23:55:20', '2025-10-21 23:56:24', '2025-10-21 23:55:20', '2025-10-21 23:55:20'),
(5, 185, 3, NULL, '2025-10-21 23:57:06', '2025-10-21 23:58:52', '2025-10-21 23:57:06', '2025-10-21 23:57:06'),
(6, 185, 14, NULL, '2025-10-25 20:29:16', NULL, '2025-10-25 20:29:16', '2025-10-25 20:29:16'),
(7, 180, 3, NULL, '2025-10-28 21:56:50', NULL, '2025-10-28 21:56:50', '2025-10-28 21:56:50'),
(8, 184, 5, NULL, '2025-10-31 01:17:12', NULL, '2025-10-31 01:17:12', '2025-10-31 01:17:12'),
(9, 185, 22, NULL, '2025-11-03 22:59:05', '2025-11-11 00:37:04', '2025-11-03 22:59:05', '2025-11-03 22:59:05'),
(10, 183, 7, NULL, '2025-11-04 00:58:43', NULL, '2025-11-04 00:58:43', '2025-11-04 00:58:43'),
(11, 182, 8, NULL, '2025-11-04 00:59:16', NULL, '2025-11-04 00:59:16', '2025-11-04 00:59:16'),
(12, 185, 24, NULL, '2025-11-04 20:20:12', '2025-11-11 00:37:18', '2025-11-04 20:20:12', '2025-11-04 20:20:12'),
(13, 185, 17, NULL, '2025-11-12 17:43:24', '2025-12-11 20:43:22', '2025-11-12 17:43:24', '2025-11-12 17:43:24'),
(14, 185, 12, NULL, '2025-11-13 18:48:21', '2025-12-11 20:43:22', '2025-11-13 18:48:21', '2025-11-13 18:48:21'),
(15, 185, 18, NULL, '2025-11-13 22:47:10', '2025-12-11 20:43:22', '2025-11-13 22:47:10', '2025-11-13 22:47:10'),
(17, 198, 17, NULL, '2026-01-02 01:06:16', NULL, '2026-01-02 01:06:16', '2026-01-02 01:06:16'),
(18, 198, 13, NULL, '2026-01-14 20:18:47', NULL, '2026-01-14 20:18:47', '2026-01-14 20:18:47');

-- --------------------------------------------------------

--
-- Table structure for table `driver_calculations`
--

CREATE TABLE `driver_calculations` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `business_id` bigint(20) UNSIGNED NOT NULL,
  `calculation_type` enum('RANGE','FIXED') DEFAULT NULL,
  `from` decimal(8,2) DEFAULT NULL,
  `to` decimal(8,2) DEFAULT NULL,
  `amount` decimal(8,2) NOT NULL DEFAULT 0.00,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `driver_calculations`
--

INSERT INTO `driver_calculations` (`id`, `business_id`, `calculation_type`, `from`, `to`, `amount`, `created_at`, `updated_at`) VALUES
(1, 1, 'FIXED', NULL, NULL, 15.00, '2024-11-23 06:00:39', '2024-11-23 06:00:39'),
(2, 2, 'FIXED', NULL, NULL, 15.00, '2024-11-23 06:01:50', '2024-11-23 06:01:50'),
(3, 3, 'FIXED', NULL, NULL, 15.00, '2024-11-23 06:02:07', '2024-11-23 06:02:07'),
(4, 4, 'FIXED', NULL, NULL, 16.00, '2024-11-23 06:02:33', '2024-11-23 06:02:33'),
(5, 5, 'FIXED', NULL, NULL, 15.00, '2024-11-23 06:02:55', '2024-11-23 06:02:55'),
(6, 6, 'FIXED', NULL, NULL, 15.00, '2024-11-23 06:05:58', '2024-11-23 06:05:58');

-- --------------------------------------------------------

--
-- Table structure for table `driver_devices`
--

CREATE TABLE `driver_devices` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `driver_id` bigint(20) UNSIGNED NOT NULL,
  `fcm_token` varchar(255) NOT NULL,
  `device_id` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `driver_devices`
--

INSERT INTO `driver_devices` (`id`, `driver_id`, `fcm_token`, `device_id`, `created_at`, `updated_at`) VALUES
(1, 171, 'epgpBDpURDuI2v-t4L_188:APA91bHGuAjEOdlM_coAUdslZ7dpRi757Z0vjDJC8ryDEjUhok5TeETkA03-ZKHOBHF3D6DAFHtWTwavul0GCb6hVjlyAYhYpQ_WV-TQBUyNJFT1W6NBSAA', 'UP1A.231005.007', '2024-11-23 06:04:16', '2024-11-23 06:04:16'),
(2, 95, 'ePttJZj2S5eghkI96bgTtV:APA91bFuSK6dMxSX_-MgTZLfB1AaG4IkoA6YiTnlVQAsH7hCJ17j_ZIxFbsYi4Akqgz4Dhesezhn_Fpd7prIwDYyQeUejQTF0k-zBJkYZsu3SrlOkG8m0ZM', 'UP1A.231005.007', '2024-11-23 06:08:24', '2024-11-23 06:08:24'),
(3, 172, 'epgpBDpURDuI2v-t4L_188:APA91bHGuAjEOdlM_coAUdslZ7dpRi757Z0vjDJC8ryDEjUhok5TeETkA03-ZKHOBHF3D6DAFHtWTwavul0GCb6hVjlyAYhYpQ_WV-TQBUyNJFT1W6NBSAA', 'UP1A.231005.007', '2024-11-23 07:43:47', '2024-11-23 07:43:47'),
(4, 81, 'cWc3wm5KR3StKND4gNUFHU:APA91bHuRR7vbRFSM2LvoifwHSb_DWKgSgzpOeRtm9sMUogrHJ0NEB7vHEahwH-kMLYsLyIu0f1f4KjZ1kuf6QQjgPOXzchzyRdmAw9CQJobN0Hu7mjSL4g', 'UP1A.231005.007', '2024-11-23 16:16:47', '2025-03-27 20:56:01'),
(5, 173, 'epgpBDpURDuI2v-t4L_188:APA91bHGuAjEOdlM_coAUdslZ7dpRi757Z0vjDJC8ryDEjUhok5TeETkA03-ZKHOBHF3D6DAFHtWTwavul0GCb6hVjlyAYhYpQ_WV-TQBUyNJFT1W6NBSAA', 'UP1A.231005.007', '2024-11-24 07:32:02', '2024-11-24 07:32:02'),
(6, 158, 'd2IttDL8Szq1SttAbfuPsL:APA91bGlpaelgEmjB31yhp0IKVnIUWOeHJQVOF0-KUe4QfMg7xsYpTBCzASwXlIrcMneSY-L3br1rJp7WjtjxPjG-0LU5NziHEGMF3hDEZ6EjyvP0h241oc', 'UP1A.231005.007', '2024-11-24 08:20:35', '2024-11-24 08:20:35'),
(7, 172, 'this is fcm token', 'this is device_id', '2024-11-24 10:19:12', '2024-11-24 10:19:12'),
(8, 174, 'this is fcm token', 'this is device_id', '2024-11-25 05:17:58', '2024-11-25 05:17:58'),
(9, 175, 'this is fcm token', 'this is device_id', '2024-11-25 07:31:05', '2024-11-25 07:31:05'),
(10, 170, 'en-zGLXoS9aZwqTPgBjw0y:APA91bFHJ32ea8Vl2eJ2ZE4NmSXZgDNOoSPdxa2Fv1oZ26PBSLg_9gLB3ENBqt51ghiHDcUPbjlePLoVHbRpPHM4qlDPLPWRZTV8fZCCK-w3k-kcTDx-PUM', 'TP1A.220624.014', '2024-11-26 09:58:50', '2024-11-26 09:58:50'),
(11, 84, 'eUYB7tBAQgeN7J_NBrPxNe:APA91bHXCWAqzx5KUlMLh-BWRP1W4mkUNFdC0tSFOEG9CfYHrYyLsbLqlll0JYJJldttHHeqEywHBNQEv5fBczTdUfVXBul5d_YvFSP1Cmr4rnWu_lwfpos', 'UP1A.231005.007', '2024-11-26 10:00:36', '2024-11-26 10:00:36'),
(12, 18, 'eG6oz_Q6RSG9ApwGuEGdbh:APA91bHeXE1yYijD5DbmBAqUjgzryKZfVIA45AtmRKt9j1Fruyob37W5EZG5C8o3g8Lg16L2ER4JPKDz_ZSJhrxns-u76ieGdFUMR21fzmZjlM_FbMt2K0M', 'UP1A.231005.007', '2024-11-26 18:29:32', '2024-11-26 18:29:32'),
(13, 116, 'ejbm98JXRvimxfmbjR76aa:APA91bGqEnHfdzBmQ1p3yvCN59DHy-QxaH5Wkfen9n6yJMetaWlS7iLK8lqAqp5S3HWWH4BF72kmMjO-ExrwYKDNiKI76knXQ1mTxJ79rmBUWmHMYRcRGQ8', 'UP1A.231005.007', '2024-11-27 06:26:38', '2024-11-27 06:26:38'),
(14, 45, 'dI2tsmyVRcWhTxyIlI7EAC:APA91bGCw7q8am-hgR78KGMgJzVZAyiTRJtU1ouHeu61G8Ej2VFugkdn1dDpU_6q6mhvCfi91eBNkLax4eyhfsd0y0-_59xlxfO_bL67w5WW1F_ol-ETXuA', 'SP1A.210812.003', '2025-02-12 06:37:36', '2025-02-12 06:37:36');

-- --------------------------------------------------------

--
-- Table structure for table `driver_differences`
--

CREATE TABLE `driver_differences` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `driver_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `total_receipt` decimal(10,2) NOT NULL DEFAULT 0.00,
  `total_paid` decimal(10,2) NOT NULL DEFAULT 0.00,
  `total_remaining` decimal(10,2) NOT NULL DEFAULT 0.00,
  `receipt_date` date DEFAULT NULL,
  `receipt_image` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `driver_differences`
--

INSERT INTO `driver_differences` (`id`, `driver_id`, `user_id`, `total_receipt`, `total_paid`, `total_remaining`, `receipt_date`, `receipt_image`, `created_at`, `updated_at`) VALUES
(1, 185, 39, 22155.00, 100.00, 22055.00, NULL, NULL, '2025-11-17 03:53:47', '2025-11-17 03:53:47'),
(2, 185, 40, 22055.00, 10000.00, 12055.00, NULL, NULL, '2025-11-17 18:15:02', '2025-11-17 18:15:02'),
(3, 182, 42, 11102.00, 200.00, 10902.00, NULL, NULL, '2025-11-19 17:30:13', '2025-11-19 17:30:13'),
(4, 184, 41, 5157.00, 200.00, 4957.00, NULL, NULL, '2025-11-19 17:33:18', '2025-11-19 17:33:18'),
(5, 184, 31, 4857.00, 500.00, 4357.00, NULL, NULL, '2025-11-19 18:31:31', '2025-11-19 18:31:31'),
(6, 180, 40, 45592.00, 10.00, 45582.00, '2025-11-19', 'receipts/20251119_180548-Ginger Goodwin-6151111111.jpg', '2025-11-19 23:05:48', '2025-11-19 23:05:48');

-- --------------------------------------------------------

--
-- Table structure for table `driver_receipts`
--

CREATE TABLE `driver_receipts` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `booklet_id` bigint(20) UNSIGNED NOT NULL,
  `reaceipt_no` varchar(255) NOT NULL,
  `receipt_date` date NOT NULL,
  `receipt_image` varchar(255) DEFAULT NULL,
  `driver_id` bigint(20) UNSIGNED NOT NULL,
  `business_id` bigint(20) UNSIGNED NOT NULL,
  `business_id_value` bigint(20) UNSIGNED DEFAULT NULL,
  `amount_received` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `driver_receipts`
--

INSERT INTO `driver_receipts` (`id`, `booklet_id`, `reaceipt_no`, `receipt_date`, `receipt_image`, `driver_id`, `business_id`, `business_id_value`, `amount_received`, `user_id`, `created_at`, `updated_at`) VALUES
(1, 2, '55', '2025-11-16', 'receipts/9qUzZQHJWJXSEZtdNeVTP6x7irIW6B5WqcPNjd7v.jpg', 185, 1, 12, 50, 39, '2025-11-17 03:50:17', '2025-11-17 03:50:17'),
(2, 2, '54', '2025-11-11', 'receipts/2PiejyUei5Xm8p14jUD1YQXIdGyMsI1CTC29RSWv.png', 180, 1, 3, 440, 39, '2025-11-17 18:18:58', '2025-11-17 18:18:58'),
(3, 2, '10', '2025-11-18', 'receipts/20251118_215442-Germaine Potts-2167777777.png', 185, 1, 12, 300, 31, '2025-11-19 02:54:42', '2025-11-19 02:54:42'),
(4, 5, '1', '2025-11-19', 'receipts/20251119_122908-Pascale Phillips-9120000000.jpg', 184, 1, 5, 200, 42, '2025-11-19 17:29:08', '2025-11-19 17:29:08'),
(5, 5, '200', '2025-11-18', 'receipts/20251119_123257-Pascale Phillips-9120000000.webp', 184, 1, 5, 200, 41, '2025-11-19 17:32:57', '2025-11-19 17:32:57'),
(6, 2, '222', '2025-11-16', 'receipts/20251119_133036-Pascale Phillips-9120000000.jpg', 184, 1, 5, 500, 31, '2025-11-19 18:30:36', '2025-11-19 18:30:36'),
(7, 4, '66', '2025-11-17', 'receipts/20251119_133252-Germaine Potts-2167777777.jpg', 185, 1, 12, 500, 31, '2025-11-19 18:32:52', '2025-11-19 18:32:52');

-- --------------------------------------------------------

--
-- Table structure for table `driver_types`
--

CREATE TABLE `driver_types` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `fields` text DEFAULT NULL,
  `is_freelancer` tinyint(1) NOT NULL DEFAULT 0,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `driver_types`
--

INSERT INTO `driver_types` (`id`, `name`, `fields`, `is_freelancer`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Sponsor', 'vehicle_monthly_cost,mobile_data,accommodation,government_cost,fuel,gprs', 0, NULL, NULL, NULL),
(2, 'Freelancer (VMFG)', 'vehicle_monthly_cost,mobile_data,fuel,gprs', 1, NULL, NULL, NULL),
(3, 'Manpower', 'vehicle_monthly_cost,mobile_data,accommodation,fuel,gprs', 0, NULL, '2026-01-06 21:06:25', '2026-01-06 21:06:25');

-- --------------------------------------------------------

--
-- Table structure for table `employment_types`
--

CREATE TABLE `employment_types` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `employment_types`
--

INSERT INTO `employment_types` (`id`, `name`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Full Time', NULL, NULL, NULL),
(2, 'Part Time', NULL, NULL, NULL),
(3, 'On Contract', NULL, NULL, NULL),
(4, 'Internship', NULL, NULL, NULL),
(5, 'Trainee', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `failed_jobs`
--

CREATE TABLE `failed_jobs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `uuid` varchar(255) NOT NULL,
  `connection` text NOT NULL,
  `queue` text NOT NULL,
  `payload` longtext NOT NULL,
  `exception` longtext NOT NULL,
  `failed_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `fields`
--

CREATE TABLE `fields` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `short_name` varchar(255) DEFAULT NULL,
  `type` enum('TEXT','INTEGER','DOCUMENT') NOT NULL DEFAULT 'TEXT',
  `required` tinyint(1) NOT NULL DEFAULT 0,
  `is_default` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `fields`
--

INSERT INTO `fields` (`id`, `name`, `short_name`, `type`, `required`, `is_default`, `created_at`, `updated_at`) VALUES
(1, 'Total Orders', 'total_orders', 'INTEGER', 1, 1, NULL, NULL),
(2, 'Bonus', 'bonus', 'INTEGER', 0, 1, NULL, NULL),
(3, 'Tip', 'tip', 'INTEGER', 0, 1, NULL, NULL),
(4, 'Other Tip', 'other_tip', 'INTEGER', 0, 1, NULL, NULL),
(5, 'Upload Driver Documents', 'upload_driver_documents', 'DOCUMENT', 0, 1, NULL, NULL),
(6, 'Cash Paid at Restaurant', 'cash_paid_at_restaurant', 'INTEGER', 0, 0, NULL, NULL),
(7, 'Cash Collected by Driver', 'cash_collected_by_driver', 'INTEGER', 0, 0, NULL, NULL),
(8, 'Net Cash Received at Branch', 'net_cash_received_at_branch', 'INTEGER', 0, 0, NULL, NULL),
(9, 'Balance In Wallet', 'balance_in_wallet', 'INTEGER', 0, 0, NULL, NULL),
(10, 'Daily Mileage', 'daily_mileage', 'INTEGER', 0, 0, NULL, NULL),
(11, 'Kilometer Driven', 'kilometer_driven', 'INTEGER', 0, 0, NULL, NULL),
(12, 'Fuel Amount', 'fuel_amount', 'INTEGER', 0, 0, NULL, NULL),
(13, 'Remarks', 'remarks', 'TEXT', 0, 0, NULL, NULL),
(14, 'Penalties', 'penalties', 'INTEGER', 0, 0, NULL, NULL),
(15, 'Compensation', 'compensation', 'INTEGER', 0, 0, NULL, NULL),
(16, 'Delivered', 'delivered', 'INTEGER', 0, 0, NULL, NULL),
(17, 'Returned to Store', 'returned_to_store', 'INTEGER', 0, 0, NULL, NULL),
(18, 'Cash Received', 'cash_received', 'INTEGER', 0, 0, NULL, NULL),
(19, 'POS Amount', 'pos_amount', 'INTEGER', 0, 0, NULL, NULL),
(20, 'test', 'test', 'TEXT', 1, 0, '2025-10-07 18:17:52', '2025-10-07 18:17:52'),
(21, 'Wallet Balance', 'wallet_balance', 'INTEGER', 1, 0, '2025-10-29 17:33:44', '2025-10-29 17:33:44'),
(22, 'Wallet Recharge', 'wallet_recharge', 'TEXT', 0, 0, '2025-10-29 17:33:44', '2025-10-29 17:33:44'),
(23, 'USAMA', 'usama', 'INTEGER', 0, 0, '2025-11-04 20:27:30', '2025-11-04 20:27:30'),
(24, 'joined', 'joined', 'TEXT', 0, 0, '2025-10-28 22:00:13', '2025-10-28 22:00:13');

-- --------------------------------------------------------

--
-- Table structure for table `fuels`
--

CREATE TABLE `fuels` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `vehicle_id` bigint(20) UNSIGNED NOT NULL,
  `status` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `fuel_type` set('petrol','diesel','electric','hybrid','cng') DEFAULT NULL,
  `request_liters` varchar(50) DEFAULT NULL,
  `request_amount` varchar(50) DEFAULT NULL,
  `reason_for_request` varchar(255) DEFAULT NULL,
  `number_of_order_deliver` int(11) NOT NULL DEFAULT 1,
  `upload_order_screenshort` varchar(255) DEFAULT NULL,
  `additional_notes` text DEFAULT NULL,
  `requested_by` bigint(20) UNSIGNED DEFAULT NULL,
  `requested_by_user` bigint(20) UNSIGNED DEFAULT NULL,
  `accepted_by` bigint(20) UNSIGNED DEFAULT NULL,
  `accept_status` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `fuels`
--

INSERT INTO `fuels` (`id`, `vehicle_id`, `status`, `fuel_type`, `request_liters`, `request_amount`, `reason_for_request`, `number_of_order_deliver`, `upload_order_screenshort`, `additional_notes`, `requested_by`, `requested_by_user`, `accepted_by`, `accept_status`, `created_at`, `updated_at`) VALUES
(22, 131, 'rejected', 'petrol', NULL, NULL, NULL, 50, 'order_screenshots/uUakX0sQ0NthbsjXYfcduTxqNg1cHVvj5yKbwcAY.jpg', NULL, NULL, NULL, NULL, 'pending', '2025-08-20 13:11:07', '2025-08-20 14:01:46'),
(23, 131, 'approved', 'petrol', NULL, NULL, NULL, 100, NULL, NULL, NULL, NULL, NULL, 'pending', '2025-08-20 13:21:26', '2025-08-20 13:48:25'),
(24, 131, 'rejected', 'petrol', NULL, NULL, NULL, 10000, 'order_screenshots/1giMzJbGuG4SYo6bQJiCeqdac9ThBD568q2ysvVU.png', NULL, NULL, NULL, NULL, 'pending', '2025-08-20 14:46:25', '2025-12-02 19:59:07'),
(25, 131, 'approved', 'petrol', NULL, NULL, NULL, 50, NULL, NULL, NULL, NULL, NULL, 'pending', '2025-08-22 12:48:49', '2025-08-22 12:49:12'),
(30, 143, 'approved', 'petrol', NULL, '10', 'additional_orders', 10, NULL, NULL, 31, NULL, NULL, 'pending', '2025-12-02 18:45:41', '2025-12-02 18:46:02'),
(31, 143, 'approved', 'petrol', NULL, '10', 'regular_refill', 10, NULL, NULL, 31, NULL, NULL, 'pending', '2025-12-02 19:36:54', '2025-12-03 19:39:49'),
(32, 143, 'approved', 'petrol', NULL, '10', 'regular_refill', 10, NULL, NULL, 31, NULL, NULL, 'pending', '2025-12-04 22:55:54', '2025-12-04 22:56:03'),
(33, 143, 'pending', 'petrol', NULL, '10', 'regular_refill', 10, NULL, NULL, 31, NULL, NULL, 'pending', '2025-12-07 17:42:17', '2025-12-07 17:42:17'),
(34, 145, 'pending', 'petrol', NULL, NULL, 'regular_refill', 12, NULL, NULL, 31, NULL, NULL, 'pending', '2025-12-10 02:22:48', '2025-12-10 02:22:48'),
(35, 144, 'pending', 'petrol', NULL, '1', 'regular_refill', 1, NULL, NULL, 31, NULL, NULL, 'pending', '2025-12-10 02:23:04', '2025-12-10 02:23:04'),
(36, 144, 'pending', 'diesel', NULL, NULL, 'regular_refill', 10, NULL, NULL, 31, NULL, NULL, 'pending', '2025-12-10 02:23:26', '2025-12-10 02:23:26'),
(37, 145, 'pending', 'petrol', NULL, NULL, 'regular_refill', 10, NULL, NULL, 31, NULL, NULL, 'pending', '2025-12-10 02:26:08', '2025-12-10 02:26:08'),
(38, 145, 'pending', 'petrol', NULL, '100', 'regular_refill', 10, 'fuel_screenshots/1765355113_cofee.webp', NULL, 31, NULL, NULL, 'pending', '2025-12-10 18:55:13', '2025-12-10 18:55:13'),
(39, 145, 'pending', 'petrol', NULL, '100', 'regular_refill', 100, 'fuel_screenshots/1765355208_request2.png', NULL, 31, NULL, NULL, 'pending', '2025-12-10 18:56:48', '2025-12-10 18:56:48'),
(40, 145, 'pending', 'petrol', NULL, '100', 'regular_refill', 10, 'fuel_screenshots/1765355517_request2.png', NULL, 31, NULL, NULL, 'pending', '2025-12-10 19:01:57', '2025-12-10 19:01:57'),
(41, 143, 'pending', 'petrol', NULL, '46', 'regular_refill', 86, 'fuel_screenshots/1765355729_security2.jpg', 'Asperiores inventore', 31, NULL, NULL, 'pending', '2025-12-10 19:05:29', '2025-12-10 19:05:29'),
(42, 145, 'pending', 'petrol', NULL, NULL, 'regular_refill', 10, NULL, NULL, 31, NULL, NULL, 'pending', '2025-12-10 19:39:50', '2025-12-10 19:39:50'),
(43, 145, 'pending', 'petrol', '10', NULL, 'regular_refill', 10, NULL, NULL, 31, NULL, NULL, 'pending', '2025-12-10 19:43:02', '2025-12-10 19:43:02'),
(44, 145, 'approved', 'petrol', '20', NULL, 'regular_refill', 20, 'fuel_screenshots/1765696410_hamza-mohammed.png', NULL, 31, NULL, NULL, 'pending', '2025-12-14 17:43:30', '2025-12-14 21:03:26'),
(45, 131, 'rejected', 'petrol', '55', NULL, NULL, 123, NULL, NULL, 185, NULL, 31, 'approved', '2025-12-14 20:52:10', '2025-12-18 01:47:12'),
(46, 131, 'approved', 'petrol', '40', NULL, NULL, 1234, 'fuel_screenshots/1765707787_cofee.webp', NULL, 185, NULL, 46, 'approved', '2025-12-14 20:53:07', '2025-12-18 01:46:24'),
(47, 131, 'approved', 'petrol', NULL, '500', NULL, 123, 'fuel_screenshots/1765708239_cofee.webp', NULL, 185, NULL, 31, 'approved', '2025-12-14 21:00:39', '2025-12-18 01:45:34'),
(48, 131, 'approved', 'petrol', NULL, NULL, NULL, 20, 'fuel_screenshots/1765787257_81925e3c-d553-4b0a-b70b-ecfe8b4953a0-2.jpg', NULL, 185, NULL, NULL, 'pending', '2025-12-15 18:57:37', '2025-12-15 18:58:30'),
(49, 146, 'pending', 'petrol', NULL, '100', 'regular_refill', 10, NULL, NULL, NULL, 46, 46, 'approved', '2025-12-18 01:37:53', '2025-12-18 01:37:53'),
(50, 131, 'approved', 'petrol', '', '500', NULL, 200, NULL, NULL, 185, NULL, 31, 'approved', '2025-12-18 21:19:10', '2025-12-18 21:23:12'),
(51, 131, 'pending', 'petrol', NULL, NULL, NULL, 300, 'fuel_screenshots/1766055063_profile-logo-6839267.webp', NULL, 185, NULL, NULL, 'pending', '2025-12-18 21:21:03', '2025-12-18 21:21:03'),
(52, 131, 'approved', 'petrol', '', '550', NULL, 200, NULL, NULL, 185, NULL, 31, 'approved', '2025-12-19 02:46:14', '2025-12-19 02:46:34'),
(53, 141, 'pending', 'petrol', NULL, NULL, NULL, 100, NULL, NULL, 183, NULL, NULL, 'pending', '2026-01-06 00:50:21', '2026-01-06 00:50:21'),
(54, 143, 'approved', 'petrol', '', '20', NULL, 12, 'fuel_screenshots/1767685483_2051264118.png', NULL, 198, NULL, 31, 'approved', '2026-01-06 18:14:43', '2026-01-06 18:24:48'),
(55, 143, 'pending', 'petrol', NULL, NULL, NULL, 10, 'fuel_screenshots/1767686043_2051264118.png', NULL, 198, NULL, NULL, 'pending', '2026-01-06 18:24:04', '2026-01-06 18:24:04'),
(56, 143, 'pending', 'petrol', NULL, NULL, NULL, 15, 'fuel_screenshots/1767686650_jpeg-20260106-110406-5616130371838265822.jpg', NULL, 198, NULL, NULL, 'pending', '2026-01-06 18:34:10', '2026-01-06 18:34:10'),
(57, 143, 'approved', 'petrol', '', '465', NULL, 20, 'fuel_screenshots/1767686699_jpeg-20260106-110454-3672496560896035857.jpg', NULL, 198, NULL, 31, 'approved', '2026-01-06 18:34:59', '2026-01-06 18:36:07'),
(58, 131, 'approved', 'petrol', '8888', '', NULL, 10, NULL, NULL, 185, NULL, 31, 'approved', '2026-01-10 16:36:45', '2026-01-21 19:59:05'),
(59, 131, 'approved', 'petrol', '', '777', NULL, 333, NULL, NULL, 185, NULL, 31, 'approved', '2026-01-21 19:47:08', '2026-01-21 19:58:47');

-- --------------------------------------------------------

--
-- Table structure for table `fuel_expenses`
--

CREATE TABLE `fuel_expenses` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `vehicle_id` bigint(20) UNSIGNED NOT NULL,
  `fuel_type` varchar(255) NOT NULL,
  `fuel_station` varchar(255) DEFAULT NULL,
  `liters` varchar(100) NOT NULL,
  `amount_paid` varchar(100) NOT NULL,
  `odometer_reading` int(11) NOT NULL,
  `distance_since_last_refuel` int(11) DEFAULT NULL,
  `receipt_image` varchar(255) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `recorded_by` bigint(20) UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `fuel_requests`
--

CREATE TABLE `fuel_requests` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `driver_id` bigint(20) UNSIGNED NOT NULL,
  `total_orders` int(11) NOT NULL DEFAULT 0,
  `files` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `status` enum('Pending','Verified','Approved','Rejected') NOT NULL DEFAULT 'Pending',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `fuel_request_approvals`
--

CREATE TABLE `fuel_request_approvals` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `fuel_id` bigint(20) UNSIGNED NOT NULL,
  `approved_by` bigint(20) UNSIGNED NOT NULL,
  `approved_amount` decimal(8,2) DEFAULT NULL,
  `approved_fuel_type` varchar(255) DEFAULT NULL,
  `estimated_cost` decimal(10,2) DEFAULT NULL,
  `scheduled_date` date DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `fuel_request_approvals`
--

INSERT INTO `fuel_request_approvals` (`id`, `fuel_id`, `approved_by`, `approved_amount`, `approved_fuel_type`, `estimated_cost`, `scheduled_date`, `notes`, `created_at`, `updated_at`) VALUES
(9, 23, 31, NULL, 'petrol', NULL, NULL, NULL, '2025-08-20 13:48:25', '2025-08-20 13:48:25'),
(10, 25, 31, NULL, 'petrol', NULL, NULL, NULL, '2025-08-22 12:49:12', '2025-08-22 12:49:12'),
(11, 30, 31, NULL, 'petrol', NULL, NULL, NULL, '2025-12-02 18:46:02', '2025-12-02 18:46:02'),
(12, 31, 31, NULL, 'petrol', NULL, NULL, NULL, '2025-12-03 19:39:49', '2025-12-03 19:39:49'),
(13, 32, 31, NULL, 'petrol', NULL, NULL, NULL, '2025-12-04 22:56:03', '2025-12-04 22:56:03'),
(14, 47, 31, NULL, 'petrol', NULL, NULL, NULL, '2025-12-14 21:03:03', '2025-12-14 21:03:03'),
(15, 44, 31, NULL, 'petrol', NULL, NULL, NULL, '2025-12-14 21:03:26', '2025-12-14 21:03:26'),
(16, 48, 31, NULL, 'petrol', NULL, NULL, NULL, '2025-12-15 18:58:30', '2025-12-15 18:58:30'),
(17, 46, 31, NULL, 'petrol', NULL, NULL, NULL, '2025-12-18 01:46:24', '2025-12-18 01:46:24'),
(18, 50, 31, NULL, 'petrol', NULL, NULL, NULL, '2025-12-18 21:23:12', '2025-12-18 21:23:12'),
(19, 52, 31, NULL, 'petrol', NULL, NULL, NULL, '2025-12-19 02:46:34', '2025-12-19 02:46:34'),
(20, 54, 31, NULL, 'petrol', NULL, NULL, NULL, '2026-01-06 18:24:48', '2026-01-06 18:24:48'),
(21, 57, 31, NULL, 'petrol', NULL, NULL, NULL, '2026-01-06 18:36:07', '2026-01-06 18:36:07'),
(22, 59, 31, NULL, 'petrol', NULL, NULL, NULL, '2026-01-21 19:58:47', '2026-01-21 19:58:47'),
(23, 58, 31, NULL, 'petrol', NULL, NULL, NULL, '2026-01-21 19:59:05', '2026-01-21 19:59:05');

-- --------------------------------------------------------

--
-- Table structure for table `fuel_request_rejects`
--

CREATE TABLE `fuel_request_rejects` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `fuel_id` bigint(20) UNSIGNED NOT NULL,
  `rejected_by` bigint(20) UNSIGNED DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `fuel_request_rejects`
--

INSERT INTO `fuel_request_rejects` (`id`, `fuel_id`, `rejected_by`, `notes`, `created_at`, `updated_at`) VALUES
(1, 22, 31, 'No money in wallet', '2025-08-20 14:01:46', '2025-08-20 14:01:46'),
(3, 24, 31, 'avain ', '2025-12-02 19:59:07', '2025-12-02 19:59:07'),
(4, 45, 31, 'test', '2025-12-18 01:47:12', '2025-12-18 01:47:12');

-- --------------------------------------------------------

--
-- Table structure for table `import_logs`
--

CREATE TABLE `import_logs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `file_name` varchar(255) NOT NULL,
  `original_name` varchar(255) DEFAULT NULL,
  `report_date` date DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `rows_imported` int(11) NOT NULL DEFAULT 0,
  `meta` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`meta`)),
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `import_logs`
--

INSERT INTO `import_logs` (`id`, `user_id`, `file_name`, `original_name`, `report_date`, `model`, `rows_imported`, `meta`, `created_at`, `updated_at`) VALUES
(1, 31, 'reports/YF0fX1kUQ030vwWWiXyFdTAOw8sBvPzUs6QV9qs8.csv', 'file to import.csv', '2025-11-25', 'App\\Models\\CoordinatorReport', 1, '{\"ip\":\"116.71.160.171\",\"user_agent\":\"Mozilla\\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/142.0.0.0 Safari\\/537.36\",\"timestamp\":\"2025-11-25 20:23:23\"}', '2025-11-26 01:23:23', '2025-11-26 01:23:23');

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `queue` varchar(255) NOT NULL,
  `payload` longtext NOT NULL,
  `attempts` tinyint(3) UNSIGNED NOT NULL,
  `reserved_at` int(10) UNSIGNED DEFAULT NULL,
  `available_at` int(10) UNSIGNED NOT NULL,
  `created_at` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `jobs`
--

INSERT INTO `jobs` (`id`, `queue`, `payload`, `attempts`, `reserved_at`, `available_at`, `created_at`) VALUES
(1, 'default', '{\"uuid\":\"a7218058-b924-4f19-9b36-e7c7cf679560\",\"displayName\":\"App\\\\Mail\\\\RequestRechargeMail\",\"job\":\"Illuminate\\\\Queue\\\\CallQueuedHandler@call\",\"maxTries\":null,\"maxExceptions\":null,\"failOnTimeout\":false,\"backoff\":null,\"timeout\":null,\"retryUntil\":null,\"data\":{\"commandName\":\"Illuminate\\\\Mail\\\\SendQueuedMailable\",\"command\":\"O:34:\\\"Illuminate\\\\Mail\\\\SendQueuedMailable\\\":15:{s:8:\\\"mailable\\\";O:28:\\\"App\\\\Mail\\\\RequestRechargeMail\\\":5:{s:10:\\\"driverData\\\";O:45:\\\"Illuminate\\\\Contracts\\\\Database\\\\ModelIdentifier\\\":5:{s:5:\\\"class\\\";s:17:\\\"App\\\\Models\\\\Driver\\\";s:2:\\\"id\\\";i:51;s:9:\\\"relations\\\";a:1:{i:0;s:6:\\\"branch\\\";}s:10:\\\"connection\\\";s:5:\\\"mysql\\\";s:15:\\\"collectionClass\\\";N;}s:14:\\\"superviserData\\\";O:45:\\\"Illuminate\\\\Contracts\\\\Database\\\\ModelIdentifier\\\":5:{s:5:\\\"class\\\";s:15:\\\"App\\\\Models\\\\User\\\";s:2:\\\"id\\\";i:31;s:9:\\\"relations\\\";a:2:{i:0;s:6:\\\"branch\\\";i:1;s:4:\\\"role\\\";}s:10:\\\"connection\\\";s:5:\\\"mysql\\\";s:15:\\\"collectionClass\\\";N;}s:15:\\\"requestRecharge\\\";O:45:\\\"Illuminate\\\\Contracts\\\\Database\\\\ModelIdentifier\\\":5:{s:5:\\\"class\\\";s:26:\\\"App\\\\Models\\\\RequestRecharge\\\";s:2:\\\"id\\\";i:1;s:9:\\\"relations\\\";a:0:{}s:10:\\\"connection\\\";s:5:\\\"mysql\\\";s:15:\\\"collectionClass\\\";N;}s:2:\\\"to\\\";a:1:{i:0;a:2:{s:4:\\\"name\\\";N;s:7:\\\"address\\\";s:20:\\\"jijilec351@cexch.com\\\";}}s:6:\\\"mailer\\\";s:8:\\\"sendmail\\\";}s:5:\\\"tries\\\";N;s:7:\\\"timeout\\\";N;s:13:\\\"maxExceptions\\\";N;s:17:\\\"shouldBeEncrypted\\\";b:0;s:10:\\\"connection\\\";N;s:5:\\\"queue\\\";N;s:5:\\\"delay\\\";N;s:11:\\\"afterCommit\\\";N;s:10:\\\"middleware\\\";a:0:{}s:7:\\\"chained\\\";a:0:{}s:15:\\\"chainConnection\\\";N;s:10:\\\"chainQueue\\\";N;s:19:\\\"chainCatchCallbacks\\\";N;s:3:\\\"job\\\";N;}\"}}', 0, NULL, 1764406630, 1764406630),
(2, 'default', '{\"uuid\":\"38d080dc-c911-406e-9067-914d6b048f2a\",\"displayName\":\"App\\\\Mail\\\\RequestRechargeMail\",\"job\":\"Illuminate\\\\Queue\\\\CallQueuedHandler@call\",\"maxTries\":null,\"maxExceptions\":null,\"failOnTimeout\":false,\"backoff\":null,\"timeout\":null,\"retryUntil\":null,\"data\":{\"commandName\":\"Illuminate\\\\Mail\\\\SendQueuedMailable\",\"command\":\"O:34:\\\"Illuminate\\\\Mail\\\\SendQueuedMailable\\\":15:{s:8:\\\"mailable\\\";O:28:\\\"App\\\\Mail\\\\RequestRechargeMail\\\":5:{s:10:\\\"driverData\\\";O:45:\\\"Illuminate\\\\Contracts\\\\Database\\\\ModelIdentifier\\\":5:{s:5:\\\"class\\\";s:17:\\\"App\\\\Models\\\\Driver\\\";s:2:\\\"id\\\";i:182;s:9:\\\"relations\\\";a:1:{i:0;s:6:\\\"branch\\\";}s:10:\\\"connection\\\";s:5:\\\"mysql\\\";s:15:\\\"collectionClass\\\";N;}s:14:\\\"superviserData\\\";O:45:\\\"Illuminate\\\\Contracts\\\\Database\\\\ModelIdentifier\\\":5:{s:5:\\\"class\\\";s:15:\\\"App\\\\Models\\\\User\\\";s:2:\\\"id\\\";i:46;s:9:\\\"relations\\\";a:2:{i:0;s:6:\\\"branch\\\";i:1;s:4:\\\"role\\\";}s:10:\\\"connection\\\";s:5:\\\"mysql\\\";s:15:\\\"collectionClass\\\";N;}s:15:\\\"requestRecharge\\\";O:45:\\\"Illuminate\\\\Contracts\\\\Database\\\\ModelIdentifier\\\":5:{s:5:\\\"class\\\";s:26:\\\"App\\\\Models\\\\RequestRecharge\\\";s:2:\\\"id\\\";i:2;s:9:\\\"relations\\\";a:0:{}s:10:\\\"connection\\\";s:5:\\\"mysql\\\";s:15:\\\"collectionClass\\\";N;}s:2:\\\"to\\\";a:1:{i:0;a:2:{s:4:\\\"name\\\";N;s:7:\\\"address\\\";s:20:\\\"jijilec351@cexch.com\\\";}}s:6:\\\"mailer\\\";s:8:\\\"sendmail\\\";}s:5:\\\"tries\\\";N;s:7:\\\"timeout\\\";N;s:13:\\\"maxExceptions\\\";N;s:17:\\\"shouldBeEncrypted\\\";b:0;s:10:\\\"connection\\\";N;s:5:\\\"queue\\\";N;s:5:\\\"delay\\\";N;s:11:\\\"afterCommit\\\";N;s:10:\\\"middleware\\\";a:0:{}s:7:\\\"chained\\\";a:0:{}s:15:\\\"chainConnection\\\";N;s:10:\\\"chainQueue\\\";N;s:19:\\\"chainCatchCallbacks\\\";N;s:3:\\\"job\\\";N;}\"}}', 0, NULL, 1764406704, 1764406704);

-- --------------------------------------------------------

--
-- Table structure for table `job_batches`
--

CREATE TABLE `job_batches` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `total_jobs` int(11) NOT NULL,
  `pending_jobs` int(11) NOT NULL,
  `failed_jobs` int(11) NOT NULL,
  `failed_job_ids` longtext NOT NULL,
  `options` mediumtext DEFAULT NULL,
  `cancelled_at` int(11) DEFAULT NULL,
  `created_at` int(11) NOT NULL,
  `finished_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `languages`
--

CREATE TABLE `languages` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `languages`
--

INSERT INTO `languages` (`id`, `name`, `code`, `created_at`, `updated_at`) VALUES
(1, 'Afar', 'aa', NULL, NULL),
(2, 'Abkhazian', 'ab', NULL, NULL),
(3, 'Avestan', 'ae', NULL, NULL),
(4, 'Afrikaans', 'af', NULL, NULL),
(5, 'Akan', 'ak', NULL, NULL),
(6, 'Amharic', 'am', NULL, NULL),
(7, 'Aragonese', 'an', NULL, NULL),
(8, 'Arabic', 'ar', NULL, NULL),
(9, 'Assamese', 'as', NULL, NULL),
(10, 'Avaric', 'av', NULL, NULL),
(11, 'Aymara', 'ay', NULL, NULL),
(12, 'Azerbaijani', 'az', NULL, NULL),
(13, 'Bashkir', 'ba', NULL, NULL),
(14, 'Belarusian', 'be', NULL, NULL),
(15, 'Bulgarian', 'bg', NULL, NULL),
(16, 'Bihari languages', 'bh', NULL, NULL),
(17, 'Bislama', 'bi', NULL, NULL),
(18, 'Bambara', 'bm', NULL, NULL),
(19, 'Bengali', 'bn', NULL, NULL),
(20, 'Tibetan', 'bo', NULL, NULL),
(21, 'Breton', 'br', NULL, NULL),
(22, 'Bosnian', 'bs', NULL, NULL),
(23, 'Catalan; Valencian', 'ca', NULL, NULL),
(24, 'Chechen', 'ce', NULL, NULL),
(25, 'Chamorro', 'ch', NULL, NULL),
(26, 'Corsican', 'co', NULL, NULL),
(27, 'Cree', 'cr', NULL, NULL),
(28, 'Czech', 'cs', NULL, NULL),
(29, 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic', 'cu', NULL, NULL),
(30, 'Chuvash', 'cv', NULL, NULL),
(31, 'Welsh', 'cy', NULL, NULL),
(32, 'Danish', 'da', NULL, NULL),
(33, 'German', 'de', NULL, NULL),
(34, 'Divehi; Dhivehi; Maldivian', 'dv', NULL, NULL),
(35, 'Dzongkha', 'dz', NULL, NULL),
(36, 'Ewe', 'ee', NULL, NULL),
(37, 'Greek, Modern (1453-)', 'el', NULL, NULL),
(38, 'English', 'en', NULL, NULL),
(39, 'Esperanto', 'eo', NULL, NULL),
(40, 'Spanish; Castilian', 'es', NULL, NULL),
(41, 'Estonian', 'et', NULL, NULL),
(42, 'Basque', 'eu', NULL, NULL),
(43, 'Persian', 'fa', NULL, NULL),
(44, 'Fulah', 'ff', NULL, NULL),
(45, 'Finnish', 'fi', NULL, NULL),
(46, 'Fijian', 'fj', NULL, NULL),
(47, 'Faroese', 'fo', NULL, NULL),
(48, 'French', 'fr', NULL, NULL),
(49, 'Western Frisian', 'fy', NULL, NULL),
(50, 'Irish', 'ga', NULL, NULL),
(51, 'Gaelic; Scomttish Gaelic', 'gd', NULL, NULL),
(52, 'Galician', 'gl', NULL, NULL),
(53, 'Guarani', 'gn', NULL, NULL),
(54, 'Gujarati', 'gu', NULL, NULL),
(55, 'Manx', 'gv', NULL, NULL),
(56, 'Hausa', 'ha', NULL, NULL),
(57, 'Hebrew', 'he', NULL, NULL),
(58, 'Hindi', 'hi', NULL, NULL),
(59, 'Hiri Motu', 'ho', NULL, NULL),
(60, 'Croatian', 'hr', NULL, NULL),
(61, 'Haitian; Haitian Creole', 'ht', NULL, NULL),
(62, 'Hungarian', 'hu', NULL, NULL),
(63, 'Armenian', 'hy', NULL, NULL),
(64, 'Herero', 'hz', NULL, NULL),
(65, 'Interlingua (International Auxiliary Language Association)', 'ia', NULL, NULL),
(66, 'Indonesian', 'id', NULL, NULL),
(67, 'Interlingue; Occidental', 'ie', NULL, NULL),
(68, 'Igbo', 'ig', NULL, NULL),
(69, 'Sichuan Yi; Nuosu', 'ii', NULL, NULL),
(70, 'Inupiaq', 'ik', NULL, NULL),
(71, 'Ido', 'io', NULL, NULL),
(72, 'Icelandic', 'is', NULL, NULL),
(73, 'Italian', 'it', NULL, NULL),
(74, 'Inuktitut', 'iu', NULL, NULL),
(75, 'Japanese', 'ja', NULL, NULL),
(76, 'Javanese', 'jv', NULL, NULL),
(77, 'Georgian', 'ka', NULL, NULL),
(78, 'Kongo', 'kg', NULL, NULL),
(79, 'Kikuyu; Gikuyu', 'ki', NULL, NULL),
(80, 'Kuanyama; Kwanyama', 'kj', NULL, NULL),
(81, 'Kazakh', 'kk', NULL, NULL),
(82, 'Kalaallisut; Greenlandic', 'kl', NULL, NULL),
(83, 'Central Khmer', 'km', NULL, NULL),
(84, 'Kannada', 'kn', NULL, NULL),
(85, 'Korean', 'ko', NULL, NULL),
(86, 'Kanuri', 'kr', NULL, NULL),
(87, 'Kashmiri', 'ks', NULL, NULL),
(88, 'Kurdish', 'ku', NULL, NULL),
(89, 'Komi', 'kv', NULL, NULL),
(90, 'Cornish', 'kw', NULL, NULL),
(91, 'Kirghiz; Kyrgyz', 'ky', NULL, NULL),
(92, 'Latin', 'la', NULL, NULL),
(93, 'Luxembourgish; Letzeburgesch', 'lb', NULL, NULL),
(94, 'Ganda', 'lg', NULL, NULL),
(95, 'Limburgan; Limburger; Limburgish', 'li', NULL, NULL),
(96, 'Lingala', 'ln', NULL, NULL),
(97, 'Lao', 'lo', NULL, NULL),
(98, 'Lithuanian', 'lt', NULL, NULL),
(99, 'Luba-Katanga', 'lu', NULL, NULL),
(100, 'Latvian', 'lv', NULL, NULL),
(101, 'Malagasy', 'mg', NULL, NULL),
(102, 'Marshallese', 'mh', NULL, NULL),
(103, 'Maori', 'mi', NULL, NULL),
(104, 'Macedonian', 'mk', NULL, NULL),
(105, 'Malayalam', 'ml', NULL, NULL),
(106, 'Mongolian', 'mn', NULL, NULL),
(107, 'Marathi', 'mr', NULL, NULL),
(108, 'Malay', 'ms', NULL, NULL),
(109, 'Maltese', 'mt', NULL, NULL),
(110, 'Burmese', 'my', NULL, NULL),
(111, 'Nauru', 'na', NULL, NULL),
(112, 'Bokmål, Norwegian; Norwegian Bokmål', 'nb', NULL, NULL),
(113, 'Ndebele, North; North Ndebele', 'nd', NULL, NULL),
(114, 'Nepali', 'ne', NULL, NULL),
(115, 'Ndonga', 'ng', NULL, NULL),
(116, 'Dutch; Flemish', 'nl', NULL, NULL),
(117, 'Norwegian Nynorsk; Nynorsk, Norwegian', 'nn', NULL, NULL),
(118, 'Norwegian', 'no', NULL, NULL),
(119, 'Ndebele, South; South Ndebele', 'nr', NULL, NULL),
(120, 'Navajo; Navaho', 'nv', NULL, NULL),
(121, 'Chichewa; Chewa; Nyanja', 'ny', NULL, NULL),
(122, 'Occitan (post 1500)', 'oc', NULL, NULL),
(123, 'Ojibwa', 'oj', NULL, NULL),
(124, 'Oromo', 'om', NULL, NULL),
(125, 'Oriya', 'or', NULL, NULL),
(126, 'Ossetian; Ossetic', 'os', NULL, NULL),
(127, 'Panjabi; Punjabi', 'pa', NULL, NULL),
(128, 'Pali', 'pi', NULL, NULL),
(129, 'Polish', 'pl', NULL, NULL),
(130, 'Pushto; Pashto', 'ps', NULL, NULL),
(131, 'Portuguese', 'pt', NULL, NULL),
(132, 'Quechua', 'qu', NULL, NULL),
(133, 'Romansh', 'rm', NULL, NULL),
(134, 'Rundi', 'rn', NULL, NULL),
(135, 'Romanian; Moldavian; Moldovan', 'ro', NULL, NULL),
(136, 'Russian', 'ru', NULL, NULL),
(137, 'Kinyarwanda', 'rw', NULL, NULL),
(138, 'Sanskrit', 'sa', NULL, NULL),
(139, 'Sardinian', 'sc', NULL, NULL),
(140, 'Sindhi', 'sd', NULL, NULL),
(141, 'Northern Sami', 'se', NULL, NULL),
(142, 'Sango', 'sg', NULL, NULL),
(143, 'Sinhala; Sinhalese', 'si', NULL, NULL),
(144, 'Slovak', 'sk', NULL, NULL),
(145, 'Slovenian', 'sl', NULL, NULL),
(146, 'Samoan', 'sm', NULL, NULL),
(147, 'Shona', 'sn', NULL, NULL),
(148, 'Somali', 'so', NULL, NULL),
(149, 'Albanian', 'sq', NULL, NULL),
(150, 'Serbian', 'sr', NULL, NULL),
(151, 'Swati', 'ss', NULL, NULL),
(152, 'Sotho, Southern', 'st', NULL, NULL),
(153, 'Sundanese', 'su', NULL, NULL),
(154, 'Swedish', 'sv', NULL, NULL),
(155, 'Swahili', 'sw', NULL, NULL),
(156, 'Tamil', 'ta', NULL, NULL),
(157, 'Telugu', 'te', NULL, NULL),
(158, 'Tajik', 'tg', NULL, NULL),
(159, 'Thai', 'th', NULL, NULL),
(160, 'Tigrinya', 'ti', NULL, NULL),
(161, 'Turkmen', 'tk', NULL, NULL),
(162, 'Tagalog', 'tl', NULL, NULL),
(163, 'Tswana', 'tn', NULL, NULL),
(164, 'Tonga (Tonga Islands)', 'to', NULL, NULL),
(165, 'Turkish', 'tr', NULL, NULL),
(166, 'Tsonga', 'ts', NULL, NULL),
(167, 'Tatar', 'tt', NULL, NULL),
(168, 'Twi', 'tw', NULL, NULL),
(169, 'Tahitian', 'ty', NULL, NULL),
(170, 'Uighur; Uyghur', 'ug', NULL, NULL),
(171, 'Ukrainian', 'uk', NULL, NULL),
(172, 'Urdu', 'ur', NULL, NULL),
(173, 'Uzbek', 'uz', NULL, NULL),
(174, 'Venda', 've', NULL, NULL),
(175, 'Vietnamese', 'vi', NULL, NULL),
(176, 'Volapük', 'vo', NULL, NULL),
(177, 'Walloon', 'wa', NULL, NULL),
(178, 'Wolof', 'wo', NULL, NULL),
(179, 'Xhosa', 'xh', NULL, NULL),
(180, 'Yiddish', 'yi', NULL, NULL),
(181, 'Yoruba', 'yo', NULL, NULL),
(182, 'Zhuang; Chuang', 'za', NULL, NULL),
(183, 'Chinese', 'zh', NULL, NULL),
(184, 'Zulu', 'zu', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `maintenance_approvals`
--

CREATE TABLE `maintenance_approvals` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `maintenance_id` bigint(20) UNSIGNED NOT NULL,
  `estimated_cost` decimal(10,2) NOT NULL,
  `scheduled_date` date NOT NULL,
  `approval_notes` text DEFAULT NULL,
  `approved_by` varchar(255) DEFAULT NULL,
  `tam_authorization` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `maintenance_approvals`
--

INSERT INTO `maintenance_approvals` (`id`, `maintenance_id`, `estimated_cost`, `scheduled_date`, `approval_notes`, `approved_by`, `tam_authorization`, `created_at`, `updated_at`) VALUES
(35, 56, 1000.00, '2025-11-25', NULL, 'Usama Akhtar', NULL, '2025-11-23 19:40:26', '2025-11-23 19:40:26');

-- --------------------------------------------------------

--
-- Table structure for table `maintenance_rejections`
--

CREATE TABLE `maintenance_rejections` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `maintenance_id` bigint(20) UNSIGNED NOT NULL,
  `rejection_note` text DEFAULT NULL,
  `rejected_by` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `migrations`
--

CREATE TABLE `migrations` (
  `id` int(10) UNSIGNED NOT NULL,
  `migration` varchar(255) NOT NULL,
  `batch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(1, '0001_01_01_000001_create_cache_table', 1),
(2, '0001_01_01_000002_create_jobs_table', 1),
(3, '2024_08_07_113050_create_designations_table', 1),
(4, '2024_08_07_113242_create_departments_table', 1),
(5, '2024_08_07_113314_create_roles_table', 1),
(6, '2024_08_07_113405_create_employment_types_table', 1),
(7, '2024_08_07_113451_create_branches_table', 1),
(8, '2024_08_07_115247_create_languages_table', 1),
(9, '2024_08_08_091141_create_driver_types_table', 1),
(10, '2024_08_08_091630_create_drivers_table', 1),
(11, '2024_08_08_091702_create_businesses_table', 1),
(12, '2024_08_08_102014_create_business_fields_table', 1),
(13, '2024_08_08_102014_create_countries_table', 1),
(14, '2024_08_08_102015_create_users_table', 1),
(15, '2024_08_20_092037_create_modules_table', 1),
(16, '2024_09_10_180934_create_driver_calculations_table', 1),
(17, '2024_09_24_162521_create_personal_access_tokens_table', 1),
(18, '2024_10_02_101157_add_status_column_to_drivers_table', 1),
(19, '2024_10_02_104820_create_driver_attendances_table', 1),
(20, '2024_10_02_113838_add_image_column_to_businesses_table', 1),
(21, '2024_10_02_134154_create_orders_table', 1),
(22, '2024_10_02_171849_create_fuel_requests_table', 1),
(23, '2024_10_03_174923_create_coordinator_reports_table', 1),
(24, '2024_10_03_174925_create_coordinator_report_field_values_table', 1),
(25, '2024_10_03_180050_add_driver_attendance_id_to_orders_table', 1),
(26, '2024_10_05_154037_create_business_field_table', 1),
(27, '2024_10_05_154517_create_business_coordinator_report_table', 1),
(28, '2024_10_30_170956_create_driver_devices_table', 1),
(29, '2024_10_31_154119_create_privilege_table', 1),
(30, '2024_11_03_172215_add_meter_data_to_driver_attendances_table', 1),
(31, '2024_11_03_173645_add_status_amount_columns_to_orders_table', 1),
(32, '2024_11_04_145956_add_status_column_to_users_table', 1),
(33, '2024_11_20_101247_create_business_driver_table', 1),
(34, '2025_07_05_143933_create_vehicles_table', 2),
(35, '2025_07_05_145202_create_fuels_table', 3),
(36, '2025_07_07_053924_create_assign_drivers_table', 4),
(37, '2025_07_08_094504_create_vehicle_maintenances_table', 5),
(38, '2025_07_08_123106_create_vehicle_replacements_table', 6),
(39, '2025_07_09_070026_create_maintenance_approvals_table', 7),
(40, '2025_07_09_140854_add_request_by_to_vehicle_maintenances_table', 8),
(41, '2025_07_09_145217_create_maintenance_rejections_table', 9),
(42, '2025_07_09_151633_add_replacement_vehicle_to_vehicle_replacements_table', 10),
(43, '2025_07_10_061321_create_vehicle_replacement_approvals_table', 11),
(44, '2025_07_10_081738_create_replacement_rejections_table', 12),
(45, '2025_07_11_181415_create_fuel_request_rejects_table', 13),
(46, '2025_07_11_183011_add_requested_by_to_fuels_table', 14),
(47, '2025_07_12_071538_create_fuel_request_approvals_table', 15),
(48, '2025_07_12_111123_create_fuel_expenses_table', 16),
(49, '2025_07_12_111601_create_fuel_expenses_table', 17),
(50, '2025_07_12_121640_add_recorded_by_to_fuel_expenses_table', 18),
(51, '2025_07_28_081253_add_password_to_drivers_table', 19),
(52, '2025_07_31_075154_add_nationality_and_language_to_drivers_table', 20),
(53, '2025_08_06_152312_create_assign_driver_reports_table', 21),
(54, '2025_08_15_063524_create_vehicle_maintenances_report_table', 22),
(55, '2025_08_16_051340_create_vehicle_documents_table', 23),
(56, '2025_08_22_132516_add_out_meter_fields_to_driver_attendances_table', 24),
(57, '2025_09_19_122808_add_branch_id_to_vehicles_table', 25),
(58, '2025_09_22_154141_add_branch_id_to_table_businesses', 26),
(59, '2025_10_16_091202_create_business_ids_table', 27),
(60, '2025_10_16_112538_create_driver_business_ids_table', 28),
(61, '2025_10_16_170901_add_business_id_value_to_report_fields_table', 29),
(62, '2025_10_16_173332_add_business_id_value_to_coordinator_report_field_values_table', 30),
(63, '2025_10_30_180733_add_branch_id_to_coordinator_reports_table', 31),
(64, '2025_11_03_161018_create_import_logs_table', 32);

-- --------------------------------------------------------

--
-- Table structure for table `modules`
--

CREATE TABLE `modules` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `data_key` varchar(255) DEFAULT NULL,
  `data_id` varchar(255) DEFAULT NULL,
  `route` varchar(255) DEFAULT NULL,
  `is_view` int(11) NOT NULL DEFAULT 1,
  `is_add` int(11) NOT NULL DEFAULT 0,
  `is_edit` int(11) NOT NULL DEFAULT 0,
  `is_delete` int(11) NOT NULL DEFAULT 0,
  `type` int(11) NOT NULL DEFAULT 1 COMMENT '1=Module, 2=SubModule',
  `is_collapseable` tinyint(1) NOT NULL DEFAULT 0,
  `index` int(11) DEFAULT NULL,
  `parent_id` bigint(20) UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `modules`
--

INSERT INTO `modules` (`id`, `name`, `icon`, `data_key`, `data_id`, `route`, `is_view`, `is_add`, `is_edit`, `is_delete`, `type`, `is_collapseable`, `index`, `parent_id`, `created_at`, `updated_at`) VALUES
(1, 'Dashboard', 'ri-dashboard-2-line', 't-widgets', '', 'dashboard', 1, 0, 0, 0, 1, 0, 1, NULL, NULL, NULL),
(2, 'HR', 'ri-team-line', 't-dashboards', 'sidebarHRs', '', 1, 0, 0, 0, 1, 1, 2, NULL, NULL, NULL),
(3, 'Employees', 'ri-dashboard-2-line', 't-analytics', '', 'employee.index', 1, 1, 1, 0, 2, 0, 2, 2, NULL, NULL),
(4, 'DMS', 'ri-takeaway-line', 't-dashboards', 'sidebarDMSs', '', 1, 0, 0, 0, 1, 1, 3, NULL, NULL, NULL),
(5, 'Driver Types', 'ri-dashboard-2-line', 't-analytics', '', 'driver-types.index', 1, 1, 1, 0, 2, 0, 1, 4, NULL, NULL),
(6, 'Drivers', 'ri-dashboard-2-line', 't-analytics', '', 'drivers.index', 1, 1, 1, 0, 2, 0, 2, 4, NULL, NULL),
(7, 'Businesses', 'ri-dashboard-2-line', 't-analytics', '', 'business.index', 1, 1, 1, 0, 2, 0, 4, 4, NULL, NULL),
(8, 'Coordinator Report', 'ri-dashboard-2-line', 't-analytics', '', 'coordinator-report.index', 1, 1, 1, 0, 2, 0, 5, 4, NULL, NULL),
(9, 'Payroll', 'ri-dashboard-2-line', 't-analytics', '', 'payroll.index', 1, 0, 0, 0, 2, 0, 6, 4, NULL, NULL),
(10, 'Revenue Reporting', 'ri-dashboard-2-line', 't-analytics', '', 'revenue-reporting.index', 1, 0, 0, 0, 2, 0, 7, 4, NULL, NULL),
(11, 'Business Fields', 'ri-dashboard-2-line', 't-analytics', '', 'field.index', 1, 1, 0, 0, 2, 0, 3, 4, NULL, NULL),
(12, 'Role', 'ri-dashboard-2-line', 't-analytics', '', 'role.index', 1, 1, 1, 0, 2, 0, 1, 2, NULL, NULL),
(13, 'Total Orders', 'ri-dashboard-2-line', 't-analytics', '', '', 1, 0, 0, 0, 2, 0, 1, 1, NULL, NULL),
(14, 'Vehicle', 'ri-truck-line', 'vehicle', '', 'vehicle.index', 1, 0, 0, 0, 1, 1, 3, NULL, NULL, NULL),
(15, 'Platform', 'ri-dashboard-2-line', 't-analytics', '', 'businessid.index', 1, 1, 1, 0, 2, 0, 4, 4, NULL, NULL),
(16, 'Platform Ids Report', 'ri-dashboard-2-line', 't-analytics', '', 'platform-ids-report.index', 1, 1, 1, 0, 2, 0, 5, 4, NULL, NULL),
(17, 'Report Logs', 'ri-dashboard-2-line', 't-analytics', '', 'logs.index', 1, 0, 0, 0, 2, 0, 1, 19, NULL, NULL),
(18, 'Penalty Logs', 'ri-dashboard-2-line', 't-analytics', '', 'penalty.index', 1, 0, 0, 0, 2, 0, 1, 19, NULL, NULL),
(19, 'Logs', 'ri-dashboard-2-line', 't-analytics', 'sidebarLogs', NULL, 1, 0, 0, 0, 2, 1, 11, 4, NULL, NULL),
(20, 'Driver Difference', 'ri-dashboard-2-line', 't-analytics', NULL, 'driver-difference.index', 1, 1, 1, 0, 2, 0, 8, 4, '2025-11-15 07:48:08', '2025-11-15 07:48:08'),
(21, 'Booklet', 'ri-dashboard-2-line', 't-analytics', NULL, 'booklet.index', 1, 1, 1, 0, 2, 0, 7, 4, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(22, 'Add Receipt', 'ri-dashboard-2-line', 't-analytics', NULL, 'driver-receipt.create', 1, 1, 1, 0, 2, 0, 7, 4, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(23, 'Receipt Logs', 'ri-dashboard-2-line', 't-analytics', NULL, 'driver-receipt.log', 1, 0, 0, 0, 2, 0, 2, 19, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(24, 'Driver Difference Logs', 'ri-dashboard-2-line', 't-analytics', NULL, 'driver-difference.log', 1, 0, 0, 0, 2, 0, 2, 19, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(25, 'Operation Supervisor Difference', 'ri-dashboard-2-line', 't-analytics', NULL, 'superviser-difference.index', 1, 1, 1, 0, 2, 0, 9, 4, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(26, 'Operation Supervisor Difference Logs', 'ri-dashboard-2-line', 't-analytics', NULL, 'superviser-difference.log', 1, 0, 0, 0, 2, 0, 2, 19, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(27, 'Amount Transfer', 'ri-dashboard-2-line', 't-analytics', NULL, 'amount-transfer.index', 1, 1, 0, 0, 2, 0, 9, 4, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(28, 'Franchise Report', 'ri-dashboard-2-line', 't-analytics', NULL, 'franchise-report.index', 1, 0, 0, 0, 2, 0, 10, 4, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(29, 'Recharge Request', 'ri-dashboard-2-line', 't-analytics', NULL, 'request-recharge.index', 1, 1, 0, 0, 2, 0, 10, 4, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(30, 'Recharge', 'ri-dashboard-2-line', 't-analytics', NULL, 'recharge.index', 1, 1, 0, 0, 2, 0, 10, 4, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(31, 'Recharge Log', 'ri-dashboard-2-line', 't-analytics', NULL, 'recharge.log', 1, 0, 0, 0, 2, 0, 2, 19, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(32, 'Vehicle', 'ri-dashboard-2-line', 't-analytics', NULL, 'vehicle.index', 1, 1, 0, 0, 2, 0, 1, 14, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(33, 'Maintenance Request', 'ri-dashboard-2-line', 't-analytics', NULL, 'vehicle.maintenance-request', 1, 1, 0, 0, 2, 0, 2, 14, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(34, 'Replacement Request', 'ri-dashboard-2-line', 't-analytics', NULL, 'vehicle.replacement-request', 1, 0, 0, 0, 2, 0, 3, 14, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(35, 'Accident Report', 'ri-dashboard-2-line', 't-analytics', NULL, 'vehicle.accident-report', 1, 1, 0, 0, 2, 0, 4, 14, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(36, 'Out of Service', 'ri-dashboard-2-line', 't-analytics', NULL, 'vehicle.out-of-service', 1, 0, 0, 0, 2, 0, 5, 14, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(37, 'Fuel', 'ri-gas-station-line', 't-analytics', 'sidebarFuel', '', 1, 0, 0, 0, 1, 1, 4, NULL, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(38, 'Fuel', 'ri-gas-station-line', 't-analytics', NULL, 'fuel.index', 1, 1, 0, 0, 2, 0, 1, 37, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(39, 'Fuel Request', 'ri-gas-station-line', 't-analytics', NULL, 'fuel.fuel-request', 1, 1, 0, 0, 2, 0, 2, 37, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(40, 'Logs', 'ri-gas-station-line', 't-analytics', NULL, 'fuel.logs', 1, 0, 0, 0, 2, 0, 3, 37, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(41, 'Driver Attendance', 'ri-calendar-check-line', 't-analytics', 'sidebarAttendance', NULL, 1, 0, 0, 0, 1, 1, 3, NULL, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(42, 'Datetime Attendance', 'ri-dashboard-2\r\n-line', 't-analytics', NULL, 'drivers.attendance', 1, 0, 0, 0, 2, 0, 2, 41, '2025-11-15 07:48:33', '2025-11-15 07:48:33'),
(43, 'Date Attendance', 'ri-dashboard-2-line', 't-analytics', NULL, 'drivers.driver-datetime', 1, 0, 0, 0, 2, 0, 1, 41, NULL, NULL),
(44, 'Drivers Monitoring', 'ri-dashboard-2-line', 't-analytics', '', 'drivers.monitoring', 1, 0, 0, 0, 2, 0, 2, 4, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `offboarding`
--

CREATE TABLE `offboarding` (
  `id` int(11) NOT NULL,
  `driver_id` int(11) NOT NULL,
  `requested_by_id` int(11) NOT NULL,
  `requested_at` datetime DEFAULT current_timestamp(),
  `status` varchar(30) DEFAULT 'Requested',
  `ops_supervisor_cleared` tinyint(1) DEFAULT 0,
  `ops_supervisor_cleared_at` datetime DEFAULT NULL,
  `ops_supervisor_note` text DEFAULT NULL,
  `fleet_cleared` tinyint(1) DEFAULT 0,
  `fleet_cleared_at` datetime DEFAULT NULL,
  `fleet_damage_report` text DEFAULT NULL,
  `fleet_damage_cost` float DEFAULT NULL,
  `finance_cleared` tinyint(1) DEFAULT 0,
  `finance_cleared_at` datetime DEFAULT NULL,
  `finance_invoice_file` varchar(200) DEFAULT NULL,
  `finance_adjustments` float DEFAULT NULL,
  `finance_note` text DEFAULT NULL,
  `hr_cleared` tinyint(1) DEFAULT 0,
  `hr_cleared_at` datetime DEFAULT NULL,
  `hr_note` text DEFAULT NULL,
  `tamm_revoked` tinyint(1) DEFAULT 0,
  `tamm_revoked_at` datetime DEFAULT NULL,
  `company_contract_cancelled` tinyint(1) DEFAULT 0,
  `qiwa_contract_cancelled` tinyint(1) DEFAULT 0,
  `salary_paid` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `offboarding`
--

INSERT INTO `offboarding` (`id`, `driver_id`, `requested_by_id`, `requested_at`, `status`, `ops_supervisor_cleared`, `ops_supervisor_cleared_at`, `ops_supervisor_note`, `fleet_cleared`, `fleet_cleared_at`, `fleet_damage_report`, `fleet_damage_cost`, `finance_cleared`, `finance_cleared_at`, `finance_invoice_file`, `finance_adjustments`, `finance_note`, `hr_cleared`, `hr_cleared_at`, `hr_note`, `tamm_revoked`, `tamm_revoked_at`, `company_contract_cancelled`, `qiwa_contract_cancelled`, `salary_paid`, `created_at`, `updated_at`) VALUES
(2, 21, 17, '2025-11-08 11:13:15', 'Finance', 1, '2025-11-08 11:16:02', 'ToYou ID 312064 has been taken from Basit Ali and the password has been changed. No company mobile or sim had been issued by me for the driver.', 1, '2025-11-09 12:42:50', '0', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, NULL, 0, 0, 0, '2025-11-09 12:42:50', '2025-11-08 11:13:15'),
(1, 14, 17, '2025-11-06 08:08:40', 'Finance', 1, '2025-11-06 08:11:54', 'ToYou account 367156 taken and password resetted.\nHe had no mobile and sims issued from my side.', 1, '2025-11-09 12:45:04', '0', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, NULL, 0, 0, 0, '2025-11-09 12:45:04', '2025-11-06 08:08:40'),
(3, 2, 17, '2025-11-25 13:57:33', 'Finance', 1, '2025-11-26 08:05:37', 'ToYou ID 335640 was taken from him and mobile with serial no R92W10HFWBN was not returned.', 1, '2025-11-26 09:59:37', 'Misuse', 1000, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-11-26 09:59:37', 0, 0, 0, '2025-11-25 13:57:33', '2025-11-26 09:59:37'),
(4, 30, 17, '2025-11-25 13:57:40', 'Finance', 1, '2025-11-26 07:30:03', 'All previous IDs were returned & no mobile & sims were issued by me for him.', 1, '2025-11-26 09:11:15', 'Accident/Misuse front back and right side', 2000, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-11-26 09:11:15', 0, 0, 0, '2025-11-25 13:57:40', '2025-11-26 09:11:15'),
(5, 62, 17, '2025-11-25 13:57:47', 'Finance', 1, '2025-11-26 12:32:25', 'ToYou ID 311939 was taken from him and there was no mobile was issued to him by me.', 1, '2025-12-14 07:18:48', 'nil', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-12-14 07:18:48', 0, 0, 0, '2025-11-25 13:57:47', '2025-12-14 07:18:48'),
(6, 38, 17, '2025-11-25 13:57:54', 'Finance', 1, '2025-11-26 07:56:05', 'ToYou ID 311325 was taken from him and mobile with serial number R92W10H5BMZ was not returned.', 1, '2025-11-26 09:32:32', 'Accident', 1500, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-11-26 09:32:32', 0, 0, 0, '2025-11-25 13:57:54', '2025-11-26 09:32:32'),
(7, 27, 17, '2025-11-25 13:58:00', 'Finance', 1, '2025-11-26 07:49:57', 'All previous IDs were taken from him. Please note Mobile with serial no R92W10HFMHL was not returned to me.', 1, '2025-11-26 10:21:23', 'Misuse', 300, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-11-26 10:21:23', 0, 0, 0, '2025-11-25 13:58:00', '2025-11-26 10:21:23'),
(8, 69, 17, '2025-11-25 13:58:04', 'Finance', 1, '2025-11-26 07:53:41', 'No ID was ever assigned to him and no mobile or sim was issued to him by me either', 1, '2025-11-26 10:22:46', 'This is wrong driver name, and we didn\'t give car to this driver.', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-11-26 10:22:46', 0, 0, 0, '2025-11-25 13:58:04', '2025-11-26 10:22:46'),
(9, 68, 17, '2025-11-25 13:58:09', 'Finance', 1, '2025-11-26 07:45:21', 'All previous IDs were taken from him and no mobile or sim was issued to him by me', 1, '2025-11-26 10:17:49', 'nill', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-11-26 10:17:49', 0, 0, 0, '2025-11-25 13:58:09', '2025-11-26 10:17:49'),
(10, 43, 17, '2025-11-25 13:58:14', 'Finance', 1, '2025-11-26 07:48:28', 'ToYou ID 312064 & Jahez ID 404974 were taken from him and no mobile or sim was issued to him by me', 1, '2025-11-26 09:14:28', 'Misuse', 700, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-11-26 09:14:28', 0, 0, 0, '2025-11-25 13:58:14', '2025-11-26 09:14:28'),
(11, 15, 17, '2025-11-25 13:58:19', 'Finance', 1, '2025-11-26 07:43:49', 'ToYou ID 335876 was taken from him and no sim or mobile was issued to him by me', 1, '2025-11-26 10:18:56', 'nill', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-11-26 10:18:56', 0, 0, 0, '2025-11-25 13:58:19', '2025-11-26 10:18:56'),
(12, 50, 17, '2025-11-25 13:58:35', 'Finance', 1, '2025-11-26 07:36:53', 'ToYou ID 335652 was taken from him and mobile with serial no R5CWC1VDXVP was not returned', 1, '2025-11-26 10:02:56', 'nill', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-11-26 10:02:56', 0, 0, 0, '2025-11-25 13:58:35', '2025-11-26 10:02:56'),
(13, 65, 17, '2025-11-25 13:58:39', 'Finance', 1, '2025-11-26 10:48:00', 'ToYou ID 345381 has been taken from him and no mobile or sim was issued to him by me', 1, '2025-12-14 07:24:16', 'nil', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-12-14 07:24:16', 0, 0, 0, '2025-11-25 13:58:39', '2025-12-14 07:24:16'),
(14, 48, 17, '2025-11-25 13:58:44', 'Finance', 1, '2025-11-26 07:34:38', 'ToYou ID 366582 was taken from him and no mobile or sim was issued for him by me', 1, '2025-11-26 10:20:23', 'nill', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-11-26 10:20:23', 0, 0, 0, '2025-11-25 13:58:44', '2025-11-26 10:20:23'),
(15, 61, 17, '2025-11-25 13:58:49', 'Finance', 1, '2025-11-26 07:32:00', 'ToYou ID 284906 taken and no company mobile or sim were issued to him by me', 1, '2025-11-26 10:19:54', 'nill', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-11-26 10:19:54', 0, 0, 0, '2025-11-25 13:58:49', '2025-11-26 10:19:54'),
(16, 24, 17, '2025-11-26 12:11:00', 'Finance', 1, '2025-11-26 12:14:46', 'ToYou ID 335751 and Jahez ID 399327 were taken from him and there are no mobiles or sims issued to him by me.', 1, '2025-12-14 07:21:00', 'nill', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-12-14 07:21:00', 0, 0, 0, '2025-11-26 12:11:00', '2025-12-14 07:21:00'),
(17, 19, 17, '2025-12-01 09:57:14', 'Finance', 1, '2025-12-02 12:45:36', 'ToYou ID 352160 was taken from him. No mobile or sim was issued to him by me.', 1, '2025-12-14 07:19:48', 'nil', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-12-14 07:19:48', 0, 0, 0, '2025-12-01 09:57:14', '2025-12-14 07:19:48'),
(18, 34, 17, '2025-12-01 09:57:28', 'Finance', 1, '2025-12-02 12:42:28', 'Toyou ID 344398 was taken from him. Mobile with serial R8YW312WXBX has not been returned to me.', 1, '2025-12-14 07:18:16', 'nil', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-12-14 07:18:16', 0, 0, 0, '2025-12-01 09:57:28', '2025-12-14 07:18:16'),
(19, 63, 17, '2025-12-01 09:57:34', 'Finance', 1, '2025-12-02 12:39:37', 'All previous IDs were taken already. No mobile or sim was issued to him by me.', 1, '2025-12-14 07:23:22', 'nil', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-12-14 07:23:22', 0, 0, 0, '2025-12-01 09:57:34', '2025-12-14 07:23:22'),
(20, 59, 17, '2025-12-03 07:50:15', 'Finance', 1, '2025-12-03 14:04:28', 'ToYou ID 286647 has been taken from him. No mobile or sim was issued to him by me.', 1, '2025-12-04 10:09:37', 'nill', 0, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2025-12-04 10:09:37', 0, 0, 0, '2025-12-03 07:50:15', '2025-12-04 10:09:37'),
(21, 36, 17, '2025-12-07 06:17:06', 'Fleet', 1, '2026-01-21 11:10:15', 'ToYou ID 364112 taken from him. Mobile with serial R5CWC1YTS6Z not returned to me', 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-07 06:17:06', '2026-01-21 11:10:15'),
(22, 39, 17, '2025-12-07 06:17:15', 'Fleet', 1, '2026-01-21 11:13:19', 'No ID was assigned to him. No mobile or sim was issued to him by me at the time of departure.', 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-07 06:17:15', '2026-01-21 11:13:19'),
(23, 47, 17, '2025-12-07 06:17:23', 'Fleet', 1, '2026-01-21 11:14:34', 'To You ID 335453 was taken from him. No mobile or sim was issued to him by me.', 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-07 06:17:23', '2026-01-21 11:14:34'),
(24, 49, 17, '2025-12-30 08:45:21', 'Fleet', 1, '2026-01-21 11:15:55', 'ToYou ID 349457 was taken from him. No mobile or sim was issued to him by me.', 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:45:21', '2026-01-21 11:15:55'),
(25, 22, 17, '2025-12-30 08:45:26', 'Fleet', 1, '2026-01-21 11:32:06', 'ToYou ID 369823 was taken from him. No mobile or sim was issued to him by me.', 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:45:26', '2026-01-21 11:32:06'),
(26, 55, 17, '2025-12-30 08:45:33', 'Fleet', 1, '2026-01-21 11:33:24', 'ToYou ID 346394 was taken from him. No mobile or sim was issued to him by me.', 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:45:33', '2026-01-21 11:33:24'),
(27, 53, 17, '2025-12-30 08:45:39', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:45:39', '2025-12-30 08:45:39'),
(28, 51, 17, '2025-12-30 08:45:45', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:45:45', '2025-12-30 08:45:45'),
(29, 67, 17, '2025-12-30 08:45:51', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:45:51', '2025-12-30 08:45:51'),
(30, 12, 17, '2025-12-30 08:45:59', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:45:59', '2025-12-30 08:45:59'),
(31, 54, 17, '2025-12-30 08:46:11', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:46:11', '2025-12-30 08:46:11'),
(32, 16, 17, '2025-12-30 08:46:17', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:46:17', '2025-12-30 08:46:17'),
(33, 11, 17, '2025-12-30 08:46:23', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:46:23', '2025-12-30 08:46:23'),
(34, 52, 17, '2025-12-30 08:46:29', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:46:29', '2025-12-30 08:46:29'),
(35, 32, 17, '2025-12-30 08:46:36', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:46:36', '2025-12-30 08:46:36'),
(36, 44, 17, '2025-12-30 08:46:44', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:46:44', '2025-12-30 08:46:44'),
(37, 41, 17, '2025-12-30 08:46:50', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:46:50', '2025-12-30 08:46:50'),
(38, 40, 17, '2025-12-30 08:46:57', 'OpsSupervisor', 0, NULL, NULL, 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:46:57', '2025-12-30 08:46:57'),
(39, 17, 17, '2025-12-30 08:47:06', 'Fleet', 1, '2026-01-21 11:07:34', 'ToYou ID 335883 taken from him. Mobile with serial no. R8YW312Z0MR not returned to me.', 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:47:06', '2026-01-21 11:07:34'),
(40, 42, 17, '2025-12-30 08:47:14', 'Fleet', 1, '2026-01-21 10:47:07', 'ToYou ID 346032 was taken from him. No mobile or sim was issued to him by me.', 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:47:14', '2026-01-21 10:47:07'),
(41, 29, 17, '2025-12-30 08:47:21', 'Fleet', 1, '2026-01-21 10:45:25', 'No ID is registered to him. No sim or mobile was issued to him by me.', 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-30 08:47:21', '2026-01-21 10:45:25'),
(42, 58, 17, '2025-12-31 06:53:20', 'Fleet', 1, '2026-01-21 10:44:18', 'No ID registered to him. No sim or mobile was issued by me to him.', 0, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, '2025-12-31 06:53:20', '2026-01-21 10:44:18');

-- --------------------------------------------------------

--
-- Table structure for table `operation_superviser_differences`
--

CREATE TABLE `operation_superviser_differences` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `superviser_id` bigint(20) UNSIGNED NOT NULL,
  `created_by` bigint(20) UNSIGNED NOT NULL,
  `total_receipt` decimal(10,2) NOT NULL DEFAULT 0.00,
  `total_paid` decimal(10,2) NOT NULL DEFAULT 0.00,
  `total_remaining` decimal(10,2) NOT NULL DEFAULT 0.00,
  `receipt_image` text DEFAULT NULL,
  `receipt_date` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `operation_superviser_differences`
--

INSERT INTO `operation_superviser_differences` (`id`, `superviser_id`, `created_by`, `total_receipt`, `total_paid`, `total_remaining`, `receipt_image`, `receipt_date`, `created_at`, `updated_at`) VALUES
(1, 39, 31, 590.00, 10.00, 580.00, 'receipts/20251118_220349-Kylie Spencer.jpg', NULL, '2025-11-19 03:03:49', '2025-11-19 03:03:49'),
(2, 41, 42, 400.00, 100.00, 300.00, 'receipts/20251119_123500-operational supervisor al hasa.jpg', NULL, '2025-11-19 17:35:00', '2025-11-19 17:35:00'),
(3, 41, 42, 300.00, 200.00, 100.00, 'receipts/20251119_133402-operational supervisor al hasa.jpg', NULL, '2025-11-19 18:34:02', '2025-11-19 18:34:02'),
(4, 39, 40, 580.00, 10.00, 570.00, 'receipts/20251119_180747-oprationnsupervisor damam.jpg', '2025-11-19', '2025-11-19 23:07:47', '2025-11-19 23:07:47');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `driver_id` bigint(20) UNSIGNED NOT NULL,
  `business_id` bigint(20) UNSIGNED NOT NULL,
  `business_id_id` bigint(20) UNSIGNED DEFAULT NULL,
  `order_id` varchar(255) NOT NULL,
  `pickup_time` timestamp NULL DEFAULT NULL,
  `delivered_time` timestamp NULL DEFAULT NULL,
  `cancelled_time` timestamp NULL DEFAULT NULL,
  `drop_time` timestamp NULL DEFAULT NULL,
  `cancel_reason` text DEFAULT NULL,
  `status` enum('Pickup','Drop','Cancel') DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `driver_attendance_id` bigint(20) UNSIGNED NOT NULL,
  `type` int(11) DEFAULT NULL COMMENT '0=Wallet, 1=Cash , 2=Online',
  `amount_paid` decimal(8,2) NOT NULL DEFAULT 0.00,
  `amount_received` decimal(8,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `driver_id`, `business_id`, `business_id_id`, `order_id`, `pickup_time`, `delivered_time`, `cancelled_time`, `drop_time`, `cancel_reason`, `status`, `created_at`, `updated_at`, `driver_attendance_id`, `type`, `amount_paid`, `amount_received`) VALUES
(1, 185, 2, 14, '100', '2025-12-25 00:14:23', '2025-12-25 00:14:40', NULL, NULL, NULL, 'Drop', '2025-12-25 00:07:44', '2025-12-25 00:14:40', 1, 2, 0.00, 0.00),
(2, 185, 2, 14, '100', '2025-12-25 00:13:35', '2025-12-25 00:13:53', NULL, NULL, NULL, 'Drop', '2025-12-25 00:13:32', '2025-12-25 00:13:53', 2, 2, 0.00, 0.00),
(3, 185, 2, 14, '100', '2025-12-30 02:46:35', '2025-12-30 02:52:00', NULL, NULL, NULL, 'Drop', '2025-12-27 19:40:29', '2025-12-30 02:52:00', 7, 2, 0.00, 0.00),
(4, 185, 2, 14, '200', '2025-12-30 02:45:48', '2025-12-30 02:46:05', NULL, NULL, NULL, 'Drop', '2025-12-27 19:44:05', '2025-12-30 02:46:05', 7, 2, 0.00, 0.00),
(5, 183, 1, 7, '400', '2026-01-06 21:32:25', '2026-01-06 21:32:35', NULL, NULL, NULL, 'Drop', '2026-01-01 23:46:27', '2026-01-06 21:32:35', 16, 1, 0.00, 1000.00),
(6, 198, 1, 17, '1', '2026-01-02 01:09:57', '2026-01-02 01:10:27', NULL, NULL, NULL, 'Drop', '2026-01-02 01:09:40', '2026-01-02 01:10:27', 17, 2, 0.00, 0.00),
(7, 198, 1, 17, '1', '2026-01-04 22:05:12', '2026-01-04 22:05:17', NULL, NULL, NULL, 'Drop', '2026-01-02 01:10:56', '2026-01-04 22:05:17', 17, 2, 0.00, 0.00),
(8, 183, 1, 7, '100', '2026-01-03 18:43:19', '2026-01-06 21:32:23', NULL, NULL, NULL, 'Drop', '2026-01-03 18:42:29', '2026-01-06 21:32:23', 18, 2, 0.00, 0.00),
(9, 183, 2, 13, '500', '2026-01-05 20:50:59', '2026-01-05 20:52:21', NULL, '2026-01-05 20:52:21', NULL, 'Drop', '2026-01-05 20:50:05', '2026-01-05 20:52:21', 20, 1, 0.00, 1000.00),
(10, 198, 1, 17, '1245', '2026-01-05 21:47:34', '2026-01-05 21:47:45', NULL, '2026-01-05 21:47:45', NULL, 'Drop', '2026-01-05 21:47:24', '2026-01-05 21:47:45', 22, 2, 0.00, 0.00),
(11, 198, 1, 17, '8795', '2026-01-05 21:57:58', '2026-01-05 21:58:17', NULL, '2026-01-05 21:58:17', NULL, 'Drop', '2026-01-05 21:57:54', '2026-01-05 21:58:17', 23, 2, 0.00, 0.00),
(12, 198, 1, 17, '1122', '2026-01-05 22:11:02', '2026-01-05 22:11:43', NULL, '2026-01-05 22:11:43', NULL, 'Drop', '2026-01-05 22:10:58', '2026-01-05 22:11:43', 24, 1, 0.00, 100.00),
(13, 198, 1, 17, '1244', '2026-01-05 22:19:27', '2026-01-05 22:19:47', NULL, '2026-01-05 22:19:47', NULL, 'Drop', '2026-01-05 22:19:23', '2026-01-05 22:19:47', 25, 0, 0.00, 0.00),
(14, 198, 1, 17, '12345', '2026-01-05 22:46:59', '2026-01-05 22:47:12', NULL, '2026-01-05 22:47:12', NULL, 'Drop', '2026-01-05 22:46:52', '2026-01-05 22:47:12', 27, 0, 0.00, 0.00),
(15, 198, 1, 17, '566', '2026-01-06 20:44:47', '2026-01-06 20:51:35', NULL, NULL, NULL, 'Drop', '2026-01-06 20:44:43', '2026-01-06 20:51:35', 31, 2, 0.00, 0.00),
(16, 198, 1, 17, '1234', '2026-01-06 20:55:51', '2026-01-06 20:56:22', NULL, NULL, NULL, 'Drop', '2026-01-06 20:55:47', '2026-01-06 20:56:22', 35, 2, 0.00, 0.00),
(17, 198, 1, 17, '34533', '2026-01-06 20:58:46', '2026-01-06 20:59:04', NULL, NULL, NULL, 'Drop', '2026-01-06 20:58:41', '2026-01-06 20:59:04', 35, 2, 0.00, 0.00),
(18, 198, 1, 17, '1122', '2026-01-06 20:59:40', '2026-01-06 20:59:58', NULL, NULL, NULL, 'Drop', '2026-01-06 20:59:32', '2026-01-06 20:59:58', 35, 1, 0.00, 100.00),
(19, 198, 1, 17, '112233', '2026-01-06 21:00:28', '2026-01-06 21:00:56', NULL, '2026-01-06 21:00:56', NULL, 'Drop', '2026-01-06 21:00:23', '2026-01-06 21:00:56', 35, 0, 50.00, 0.00),
(20, 198, 1, 17, '112277', '2026-01-06 21:03:54', '2026-01-06 21:23:29', NULL, '2026-01-06 21:23:29', NULL, 'Drop', '2026-01-06 21:03:50', '2026-01-06 21:23:29', 36, 2, 0.00, 0.00),
(21, 198, 1, 17, '1111', '2026-01-06 21:35:25', '2026-01-06 21:41:56', NULL, NULL, NULL, 'Drop', '2026-01-06 21:35:21', '2026-01-06 21:41:56', 36, 2, 0.00, 0.00),
(22, 198, 1, 17, '12457766', '2026-01-06 21:48:14', '2026-01-06 22:13:27', NULL, '2026-01-06 22:13:27', NULL, 'Drop', '2026-01-06 21:48:05', '2026-01-06 22:13:27', 37, 1, 0.00, 10.00),
(23, 198, 1, 17, '20000', '2026-01-06 22:13:43', '2026-01-06 22:13:47', NULL, '2026-01-06 22:13:47', NULL, 'Drop', '2026-01-06 22:13:40', '2026-01-06 22:13:47', 37, 2, 0.00, 0.00),
(24, 198, 1, 17, '122211', '2026-01-06 22:17:59', '2026-01-06 22:18:13', NULL, '2026-01-06 22:18:13', NULL, 'Drop', '2026-01-06 22:17:54', '2026-01-06 22:18:13', 38, 1, 0.00, 100.00),
(25, 198, 1, 17, '32245', '2026-01-06 22:18:26', '2026-01-06 22:18:31', NULL, '2026-01-06 22:18:31', NULL, 'Drop', '2026-01-06 22:18:23', '2026-01-06 22:18:31', 38, 2, 0.00, 0.00),
(26, 198, 1, 17, '113344', '2026-01-07 14:42:38', '2026-01-07 14:42:51', NULL, '2026-01-07 14:42:51', NULL, 'Drop', '2026-01-07 14:42:27', '2026-01-07 14:42:51', 38, 1, 0.00, 100.00),
(27, 198, 1, 17, '8374', '2026-01-07 14:45:05', '2026-01-07 14:45:09', NULL, '2026-01-07 14:45:09', NULL, 'Drop', '2026-01-07 14:44:59', '2026-01-07 14:45:09', 38, 2, 0.00, 0.00),
(28, 198, 1, 17, '124578', '2026-01-07 15:31:01', '2026-01-07 15:31:08', NULL, '2026-01-07 15:31:08', NULL, 'Drop', '2026-01-07 15:30:56', '2026-01-07 15:31:08', 38, 1, 0.00, 50.00),
(29, 198, 1, 17, '644', '2026-01-07 15:58:04', '2026-01-07 15:58:10', NULL, '2026-01-07 15:58:10', NULL, 'Drop', '2026-01-07 15:57:55', '2026-01-07 15:58:10', 38, 2, 0.00, 0.00),
(30, 198, 1, 17, '6346', '2026-01-07 16:23:09', '2026-01-07 16:37:43', NULL, '2026-01-07 16:37:43', NULL, 'Drop', '2026-01-07 15:58:36', '2026-01-07 16:37:43', 38, 2, 0.00, 0.00),
(31, 198, 1, 17, '355', '2026-01-07 16:57:07', '2026-01-07 16:57:12', NULL, '2026-01-07 16:57:12', NULL, 'Drop', '2026-01-07 16:57:03', '2026-01-07 16:57:12', 38, 2, 0.00, 0.00),
(32, 198, 1, 17, '44', '2026-01-08 20:52:53', '2026-01-08 20:52:57', NULL, NULL, NULL, 'Drop', '2026-01-08 20:50:54', '2026-01-08 20:52:57', 38, 2, 0.00, 0.00),
(33, 185, 2, 14, '1', '2026-01-10 15:57:29', '2026-01-10 16:15:40', NULL, '2026-01-10 16:15:40', NULL, 'Drop', '2026-01-10 15:39:00', '2026-01-10 16:15:40', 39, 1, 0.00, 1000.00),
(34, 198, 1, 17, '11', '2026-01-10 16:46:32', '2026-01-10 16:49:59', NULL, '2026-01-10 16:49:59', NULL, 'Drop', '2026-01-10 16:46:15', '2026-01-10 16:49:59', 43, 1, 0.00, 10.00),
(35, 185, 2, 14, '555', '2026-01-10 16:58:58', '2026-01-10 17:03:02', NULL, '2026-01-10 17:03:02', NULL, 'Drop', '2026-01-10 16:54:39', '2026-01-10 17:03:02', 45, 1, 0.00, 100.00),
(36, 198, 1, 17, '43', '2026-01-10 16:59:00', '2026-01-10 16:59:06', NULL, '2026-01-10 16:59:06', NULL, 'Drop', '2026-01-10 16:58:41', '2026-01-10 16:59:06', 46, 2, 0.00, 0.00),
(37, 185, 2, 14, '555', '2026-01-10 17:06:48', '2026-01-10 17:07:29', NULL, '2026-01-10 17:07:29', NULL, 'Drop', '2026-01-10 17:06:20', '2026-01-10 17:07:29', 48, 1, 0.00, 1000.00),
(38, 198, 1, 17, '654', '2026-01-10 17:16:16', '2026-01-10 17:16:22', NULL, '2026-01-10 17:16:22', NULL, 'Drop', '2026-01-10 17:14:00', '2026-01-10 17:16:22', 46, 2, 0.00, 0.00),
(39, 185, 2, 14, '5555', '2026-01-10 17:27:15', '2026-01-10 17:27:23', NULL, '2026-01-10 17:27:23', NULL, 'Drop', '2026-01-10 17:26:49', '2026-01-10 17:27:23', 50, 1, 0.00, 500.00),
(40, 185, 2, 14, '555', '2026-01-10 17:34:05', '2026-01-10 17:34:15', NULL, '2026-01-10 17:34:15', NULL, 'Drop', '2026-01-10 17:33:00', '2026-01-10 17:34:15', 51, 1, 0.00, 6000.00),
(41, 185, 2, 14, '6666', '2026-01-10 17:33:48', '2026-01-10 17:33:59', NULL, '2026-01-10 17:33:59', NULL, 'Drop', '2026-01-10 17:33:27', '2026-01-10 17:33:59', 51, 1, 0.00, 5000.00),
(42, 198, 1, 17, '123', '2026-01-11 14:19:17', '2026-01-11 14:20:01', NULL, '2026-01-11 14:20:01', NULL, 'Drop', '2026-01-11 14:18:40', '2026-01-11 14:20:01', 46, 2, 0.00, 0.00),
(43, 198, 1, 17, '124', '2026-01-11 14:19:17', '2026-01-11 14:19:53', NULL, '2026-01-11 14:19:53', NULL, 'Drop', '2026-01-11 14:18:47', '2026-01-11 14:19:53', 46, 2, 0.00, 0.00),
(44, 198, 1, 17, '125', '2026-01-11 14:19:17', '2026-01-11 14:19:46', NULL, '2026-01-11 14:19:46', NULL, 'Drop', '2026-01-11 14:19:02', '2026-01-11 14:19:46', 46, 2, 0.00, 0.00),
(45, 183, 2, 13, '500', '2026-01-11 17:46:39', NULL, '2026-01-11 17:50:20', NULL, 'test', 'Cancel', '2026-01-11 17:43:26', '2026-01-11 17:50:20', 52, NULL, 0.00, 0.00),
(46, 183, 1, 7, '666', '2026-01-11 18:18:08', '2026-01-11 18:18:17', NULL, NULL, NULL, 'Drop', '2026-01-11 17:50:44', '2026-01-11 18:18:17', 52, 1, 0.00, 343.00),
(47, 183, 1, 7, '66', '2026-01-11 18:03:28', NULL, '2026-01-11 18:18:02', NULL, 'Platform (Hunger Station-600)', 'Cancel', '2026-01-11 17:51:52', '2026-01-11 18:18:02', 52, NULL, 0.00, 0.00),
(48, 183, 1, 7, '343', NULL, NULL, '2026-01-11 18:04:05', NULL, '3434', 'Cancel', '2026-01-11 18:03:56', '2026-01-11 18:04:05', 52, NULL, 0.00, 0.00),
(49, 198, 1, 17, '1122785', '2026-01-11 21:23:12', NULL, '2026-01-11 21:23:26', NULL, 'customer cancelled', 'Cancel', '2026-01-11 21:23:07', '2026-01-11 21:23:26', 46, NULL, 0.00, 0.00),
(50, 198, 1, 17, '1144', NULL, NULL, '2026-01-11 21:29:36', NULL, 'customer', 'Cancel', '2026-01-11 21:29:16', '2026-01-11 21:29:36', 46, NULL, 0.00, 0.00),
(51, 198, 1, 17, 'ddad', NULL, NULL, '2026-01-11 21:29:56', NULL, 'business', 'Cancel', '2026-01-11 21:29:44', '2026-01-11 21:29:56', 46, NULL, 0.00, 0.00),
(52, 198, 1, 17, '43425', NULL, NULL, '2026-01-11 21:30:04', NULL, 'avain', 'Cancel', '2026-01-11 21:29:51', '2026-01-11 21:30:04', 46, NULL, 0.00, 0.00),
(53, 198, 1, 17, '11111', '2026-01-11 22:24:08', '2026-01-11 22:24:14', NULL, '2026-01-11 22:24:14', NULL, 'Drop', '2026-01-11 22:05:36', '2026-01-11 22:24:14', 46, 2, 0.00, 0.00),
(54, 198, 1, 17, '12457', NULL, NULL, '2026-01-12 14:29:14', NULL, 'customer', 'Cancel', '2026-01-12 14:29:07', '2026-01-12 14:29:14', 46, NULL, 0.00, 0.00),
(55, 198, 1, 17, '123', '2026-01-12 16:00:11', '2026-01-12 16:00:39', NULL, '2026-01-12 16:00:39', NULL, 'Drop', '2026-01-12 15:59:53', '2026-01-12 16:00:39', 54, 2, 0.00, 0.00),
(57, 185, 2, 14, '55', '2026-01-12 19:52:55', '2026-01-12 19:53:19', NULL, NULL, NULL, 'Drop', '2026-01-12 19:52:22', '2026-01-12 19:53:19', 55, 1, 0.00, 555.00),
(61, 198, 1, 17, '755', '2026-01-12 20:52:33', '2026-01-12 20:52:36', NULL, '2026-01-12 20:52:36', NULL, 'Drop', '2026-01-12 20:51:56', '2026-01-12 20:52:36', 54, 2, 0.00, 0.00),
(62, 198, 1, 17, '1', '2026-01-14 20:19:46', '2026-01-14 20:21:05', NULL, '2026-01-14 20:21:05', NULL, 'Drop', '2026-01-14 20:19:34', '2026-01-14 20:21:05', 1, 2, 0.00, 0.00),
(63, 198, 2, 13, '23', '2026-01-14 20:19:46', '2026-01-14 20:21:12', NULL, '2026-01-14 20:21:12', NULL, 'Drop', '2026-01-14 20:19:41', '2026-01-14 20:21:12', 1, 2, 0.00, 0.00),
(65, 198, 1, 17, '55', '2026-01-15 18:26:13', '2026-01-15 18:37:16', NULL, '2026-01-15 18:37:16', NULL, 'Drop', '2026-01-15 18:25:12', '2026-01-15 18:37:16', 9, 2, 0.00, 0.00),
(66, 198, 2, 13, '45', '2026-01-15 19:25:21', '2026-01-15 19:30:32', NULL, '2026-01-15 19:30:32', NULL, 'Drop', '2026-01-15 19:22:55', '2026-01-15 19:30:32', 12, 2, 0.00, 0.00),
(68, 198, 1, 17, '66', '2026-01-15 20:33:53', '2026-01-15 20:39:23', NULL, '2026-01-15 20:39:23', NULL, 'Drop', '2026-01-15 20:21:42', '2026-01-15 20:39:23', 15, 2, 0.00, 0.00),
(69, 185, 2, 14, '66', '2026-01-15 20:42:50', '2026-01-15 21:37:23', NULL, NULL, NULL, 'Drop', '2026-01-15 20:37:06', '2026-01-15 21:37:23', 16, 1, 0.00, 7777.00),
(70, 198, 1, 17, '67', '2026-01-15 20:41:55', '2026-01-15 20:43:54', NULL, '2026-01-15 20:43:54', NULL, 'Drop', '2026-01-15 20:39:03', '2026-01-15 20:43:54', 15, 2, 0.00, 0.00),
(71, 185, 2, 14, '55', '2026-01-15 21:35:57', '2026-01-15 21:36:14', NULL, NULL, NULL, 'Drop', '2026-01-15 20:43:34', '2026-01-15 21:36:14', 16, 1, 0.00, 666.00),
(72, 198, 2, 13, '4', '2026-01-15 20:50:34', '2026-01-15 20:50:42', NULL, '2026-01-15 20:50:42', NULL, 'Drop', '2026-01-15 20:46:27', '2026-01-15 20:50:42', 15, 2, 0.00, 0.00),
(73, 198, 2, 13, '1111', '2026-01-15 20:52:50', '2026-01-15 20:53:15', NULL, NULL, NULL, 'Drop', '2026-01-15 20:52:14', '2026-01-15 20:53:15', 15, 2, 0.00, 0.00),
(74, 198, 1, 17, '56', '2026-01-15 20:55:19', '2026-01-15 20:55:31', NULL, '2026-01-15 20:55:31', NULL, 'Drop', '2026-01-15 20:55:11', '2026-01-15 20:55:31', 15, 2, 0.00, 0.00),
(75, 198, 1, 17, '55', '2026-01-15 21:36:53', '2026-01-15 21:37:03', NULL, '2026-01-15 21:37:03', NULL, 'Drop', '2026-01-15 21:34:18', '2026-01-15 21:37:03', 17, 2, 0.00, 0.00),
(76, 185, 2, 14, '888', '2026-01-15 21:39:48', '2026-01-15 21:40:09', NULL, NULL, NULL, 'Drop', '2026-01-15 21:39:44', '2026-01-15 21:40:09', 16, 1, 0.00, 888.00),
(77, 198, 1, 17, '56', '2026-01-15 22:36:52', '2026-01-15 22:37:34', NULL, '2026-01-15 22:37:34', NULL, 'Drop', '2026-01-15 22:36:43', '2026-01-15 22:37:34', 19, 2, 0.00, 0.00),
(78, 198, 1, 17, '4566', '2026-01-15 23:12:02', '2026-01-15 23:28:20', NULL, '2026-01-15 23:28:20', NULL, 'Drop', '2026-01-15 23:11:42', '2026-01-15 23:28:20', 20, 2, 0.00, 0.00),
(79, 198, 2, 13, '544', '2026-01-16 00:01:57', '2026-01-16 00:02:02', NULL, '2026-01-16 00:02:02', NULL, 'Drop', '2026-01-15 23:27:51', '2026-01-16 00:02:02', 20, 2, 0.00, 0.00),
(80, 185, 2, 14, '666', '2026-01-17 18:32:25', '2026-01-17 18:32:45', NULL, '2026-01-17 18:32:45', NULL, 'Drop', '2026-01-17 18:32:18', '2026-01-17 18:32:45', 22, 1, 0.00, 1000.00),
(81, 185, 2, 14, '555', '2026-01-17 18:33:26', '2026-01-17 18:33:44', NULL, '2026-01-17 18:33:44', NULL, 'Drop', '2026-01-17 18:33:23', '2026-01-17 18:33:44', 22, 1, 0.00, 660.00),
(82, 185, 2, 14, '666', '2026-01-17 18:34:50', '2026-01-17 18:35:04', NULL, '2026-01-17 18:35:04', NULL, 'Drop', '2026-01-17 18:33:54', '2026-01-17 18:35:04', 22, 1, 0.00, 600.00),
(83, 185, 2, 14, '1212', '2026-01-17 18:39:14', '2026-01-17 18:39:28', NULL, '2026-01-17 18:39:28', NULL, 'Drop', '2026-01-17 18:35:51', '2026-01-17 18:39:28', 22, 1, 0.00, 600.00),
(84, 185, 2, 14, '66', '2026-01-17 18:39:58', '2026-01-17 18:40:18', NULL, '2026-01-17 18:40:18', NULL, 'Drop', '2026-01-17 18:39:53', '2026-01-17 18:40:18', 22, 1, 0.00, 696.00),
(85, 185, 2, 14, '677', '2026-01-17 18:40:47', '2026-01-17 18:41:01', NULL, '2026-01-17 18:41:01', NULL, 'Drop', '2026-01-17 18:40:33', '2026-01-17 18:41:01', 22, 1, 0.00, 666.00),
(86, 185, 2, 14, '666', '2026-01-21 16:39:12', '2026-01-21 16:39:28', NULL, '2026-01-21 16:39:28', NULL, 'Drop', '2026-01-21 16:38:52', '2026-01-21 16:39:28', 40, 1, 0.00, 1000.00),
(87, 185, 2, 14, '88', '2026-01-21 19:39:49', '2026-01-21 19:39:57', NULL, '2026-01-21 19:39:57', NULL, 'Drop', '2026-01-21 16:39:50', '2026-01-21 19:39:57', 40, 1, 0.00, 999.00),
(88, 183, 1, 7, '777', NULL, NULL, NULL, NULL, NULL, NULL, '2026-01-21 16:44:23', '2026-01-21 16:44:23', 42, NULL, 0.00, 0.00),
(89, 185, 2, 14, '666', NULL, NULL, '2026-01-21 19:48:06', NULL, 'business', 'Cancel', '2026-01-21 19:47:56', '2026-01-21 19:48:06', 45, NULL, 0.00, 0.00),
(90, 185, 2, 14, '78', '2026-01-21 19:48:34', '2026-01-21 19:48:48', NULL, '2026-01-21 19:48:48', NULL, 'Drop', '2026-01-21 19:48:18', '2026-01-21 19:48:48', 45, 2, 0.00, 0.00),
(91, 185, 2, 14, '88', '2026-01-21 19:48:53', '2026-01-21 19:49:10', NULL, '2026-01-21 19:49:10', NULL, 'Drop', '2026-01-21 19:48:29', '2026-01-21 19:49:10', 45, 1, 0.00, 66.00),
(92, 185, 2, 14, '78', NULL, NULL, '2026-01-21 19:57:34', NULL, 'test', 'Cancel', '2026-01-21 19:57:19', '2026-01-21 19:57:34', 46, NULL, 0.00, 0.00),
(93, 185, 2, 14, '888', '2026-01-21 19:57:56', '2026-01-21 19:58:11', NULL, '2026-01-21 19:58:11', NULL, 'Drop', '2026-01-21 19:57:52', '2026-01-21 19:58:11', 46, 2, 0.00, 0.00),
(94, 185, 2, 14, '555', '2026-01-21 20:12:42', '2026-01-21 20:22:20', NULL, '2026-01-21 20:22:20', NULL, 'Drop', '2026-01-21 20:10:31', '2026-01-21 20:22:20', 47, 1, 0.00, 66.00);

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `password_reset_tokens`
--

INSERT INTO `password_reset_tokens` (`email`, `token`, `created_at`) VALUES
('govoli6813@atinjo.com', '$2y$12$yRf2wwTzi59RwB6LLx/t5OakJNtmC1b.sfHyQgsHFugSS56/HR12q', '2026-01-13 16:58:43'),
('manoj@digitalmediafox.info', '$2y$12$nLH.7fcFftS8xrgURqVx0uqi5nlPoczxl6RZ0kMeILCGwGZxN8Lz6', '2025-09-02 11:53:23'),
('staff@gmail.com', '$2y$12$wkoCkcLn3cwTDWMNqivsEe4DpRw8oGgAcIY2gllNXIBIbkWonoPHG', '2025-08-07 13:24:53'),
('usama@ilab.sa', '$2y$12$iEREz/gilbsZhNgrHmITHuZkNOlujVUT69WEXHDPdfPd6d/njAWDS', '2025-08-16 09:16:44'),
('z11ain@ilab.sa', '$2y$12$vpI8/OnQ8/3oS0M4PsGJQOvC/YM5yUrY978SDTB3jF2zknsOqE9wW', '2025-08-07 13:25:05'),
('zain@ilab.sa', '$2y$12$eQIBrBqmneoQBTWjMOmRM.WIbZA4Yd26crH0B4/FRzSdahFosMjt.', '2025-08-16 09:17:14');

-- --------------------------------------------------------

--
-- Table structure for table `penalties`
--

CREATE TABLE `penalties` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `driver_id` bigint(20) UNSIGNED NOT NULL,
  `business_id` bigint(20) UNSIGNED NOT NULL,
  `business_id_value` bigint(20) UNSIGNED DEFAULT NULL,
  `coordinator_report_id` bigint(20) UNSIGNED DEFAULT NULL,
  `penalty_date` date NOT NULL,
  `penalty_value` int(11) NOT NULL,
  `penalty_file` varchar(255) DEFAULT NULL,
  `is_from_coordinate` int(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `penalties`
--

INSERT INTO `penalties` (`id`, `driver_id`, `business_id`, `business_id_value`, `coordinator_report_id`, `penalty_date`, `penalty_value`, `penalty_file`, `is_from_coordinate`, `created_at`, `updated_at`) VALUES
(2, 185, 5, 24, 102, '2025-11-09', 2000, 'penalties/xUDzm4YW1Yz0VnPCfUNNw2THsUaPikZepwE14v51.png', 0, '2025-11-09 20:55:52', '2025-11-09 20:55:52'),
(3, 184, 1, 5, 105, '2025-10-29', 100, NULL, 0, '2025-11-09 22:08:06', '2025-11-09 22:08:06'),
(4, 185, 5, 24, 102, '2025-11-09', 2000, 'penalties/qXQUkKbtoNwop6qBFvwrtEn9W4teuPqWRb47tn0S.jpg', 0, '2025-11-10 01:46:21', '2025-11-10 01:46:21'),
(5, 185, 1, 17, 106, '2025-11-17', 10, 'penalties/r4Tb8DxjXxCGWSpaTzz1QA3FJ0sGokhtKWdsy53y.png', 0, '2025-11-24 19:15:54', '2025-11-24 19:15:54'),
(6, 185, 1, 17, 107, '2025-11-23', 55, 'penalties/Ef8PXw3EECIAPdGebUoFPA0Q0WQ1lHKnDDrxzPjV.png', 0, '2025-11-24 19:16:47', '2025-11-24 19:16:47'),
(7, 185, 1, 17, 108, '2025-11-24', 100, 'penalties/JWm0gvrIDyOSwlYyP21EzbwBIBB6Qs1HyltOw387.png', 0, '2025-11-24 19:21:41', '2025-11-24 19:21:41'),
(8, 185, 1, 17, 109, '2025-11-22', 50, 'penalties/xteayXjbgdVzSuOIcVNUTNuWI4Y9ycGgyA8uLN6M.png', 0, '2025-11-24 19:22:50', '2025-11-24 19:22:50'),
(9, 185, 1, 17, 109, '2025-11-22', 100, 'penalties/wD2PR5OeCVJOSOfm0z2JBIFzxfMos4ZRUFpKV7Cn.png', 0, '2025-11-24 19:23:26', '2025-11-24 19:23:26'),
(10, 185, 1, 17, 110, '2025-11-25', 1000, NULL, 1, '2025-11-26 01:18:48', '2025-11-26 01:18:48'),
(11, 185, 1, 17, 110, '2025-11-25', 200, 'penalties/y1CXIj2oI4Xs7S6lnLi75YCKncfycTZfLiV9K5O1.jpg', 0, '2025-11-26 01:20:12', '2025-11-26 01:20:12');

-- --------------------------------------------------------

--
-- Table structure for table `personal_access_tokens`
--

CREATE TABLE `personal_access_tokens` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `tokenable_type` varchar(255) NOT NULL,
  `tokenable_id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `token` varchar(64) NOT NULL,
  `abilities` text DEFAULT NULL,
  `last_used_at` timestamp NULL DEFAULT NULL,
  `expires_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `personal_access_tokens`
--

INSERT INTO `personal_access_tokens` (`id`, `tokenable_type`, `tokenable_id`, `name`, `token`, `abilities`, `last_used_at`, `expires_at`, `created_at`, `updated_at`) VALUES
(1, 'App\\Models\\Driver', 84, 'driver-token', 'bbe4aaa080a66e0acf483693dba1a12254d0f3ab2ab466605893b4fc55d8ed87', '[\"*\"]', '2024-12-01 14:44:27', NULL, '2024-11-26 14:18:14', '2024-12-01 14:44:27'),
(2, 'App\\Models\\Driver', 18, 'driver-token', '497508a03074dc256364bb3f29febdcd681ca87e429715992083f74340bfd010', '[\"*\"]', '2024-11-26 20:16:19', NULL, '2024-11-26 18:29:32', '2024-11-26 20:16:19'),
(3, 'App\\Models\\Driver', 116, 'driver-token', '41c5570f71be9bd0021e639a2a93834ff1ca567571738a6d5a8f4ebd50db89bb', '[\"*\"]', '2024-11-27 18:29:07', NULL, '2024-11-27 06:26:38', '2024-11-27 18:29:07'),
(4, 'App\\Models\\Driver', 172, 'driver-token', 'bc317e06ef59952144bed32625dcf81da0bf628c09cf527473e676061b27dbd4', '[\"*\"]', '2025-02-03 09:35:30', NULL, '2024-12-18 07:57:42', '2025-02-03 09:35:30'),
(5, 'App\\Models\\Driver', 45, 'driver-token', '83ef36302a92b8b861ed4ec438a6f45032072a6ed26bac7bbb5a7712cf8b00e6', '[\"*\"]', '2025-02-15 06:00:09', NULL, '2025-02-12 06:37:36', '2025-02-15 06:00:09'),
(6, 'App\\Models\\Driver', 81, 'driver-token', '10538ae752e16e213a15ee8c09d0a1221104c4fbb612a596b1f1a12f1ec46ebe', '[\"*\"]', '2025-03-27 20:57:13', NULL, '2025-03-27 20:56:01', '2025-03-27 20:57:13'),
(7, 'App\\Models\\Driver', 184, 'driver-token', 'e0031bb4138fbd279047b48484dc7fc26fcfbed81dc0da0b699c979c7a4b626f', '[\"*\"]', NULL, NULL, '2026-01-03 22:42:36', '2026-01-03 22:42:36'),
(10, 'App\\Models\\Driver', 184, 'driver-token', 'f084a1e1991831335805e2e65e2be0b0f467a71d4c28f3c9e093f2ed67df195f', '[\"*\"]', NULL, NULL, '2026-01-04 19:22:27', '2026-01-04 19:22:27'),
(19, 'App\\Models\\Driver', 184, 'driver-token', '3ae5ca1546bc172f7d5d62127a497870fe96c01afebca0701405e405ebc2437e', '[\"*\"]', '2026-01-04 23:02:17', NULL, '2026-01-04 23:01:24', '2026-01-04 23:02:17'),
(20, 'App\\Models\\Driver', 183, 'driver-token', 'e674f26f8bef1a89bd7ca91f5cfeaa3fd767f0f5767313937dcfaa89ca246832', '[\"*\"]', '2026-01-05 23:46:35', NULL, '2026-01-04 23:31:14', '2026-01-05 23:46:35'),
(34, 'App\\Models\\Driver', 183, 'driver-token', 'eb8f1583c9bd147c3834d5ecbe888af933afc55054d3fdf310cd361bd30252e2', '[\"*\"]', '2026-01-11 17:46:39', NULL, '2026-01-05 20:46:18', '2026-01-11 17:46:39'),
(89, 'App\\Models\\Driver', 183, 'driver-token', 'd1ebe73b926eb35adeaa9f32fe54248c1a9ebb9dc693f8c4c94e6c5c62cf9d38', '[\"*\"]', '2026-01-11 17:50:20', NULL, '2026-01-11 17:41:25', '2026-01-11 17:50:20'),
(104, 'App\\Models\\Driver', 198, 'driver-token', 'ea02dd480885debae787847145072f8b247c4f922eccb11d87bbc46f3523dc9b', '[\"*\"]', '2026-01-15 15:16:13', NULL, '2026-01-15 14:58:52', '2026-01-15 15:16:13'),
(105, 'App\\Models\\Driver', 198, 'driver-token', '0f3fbce7ff97ce711f06859010177fea6cbcaac2ed32f0797443f79cda96a15e', '[\"*\"]', '2026-01-15 20:10:36', NULL, '2026-01-15 15:20:54', '2026-01-15 20:10:36'),
(106, 'App\\Models\\Driver', 198, 'driver-token', '723e9315f9c70e84471bf3c0536691277e2a089e12f1ddf5510a39ed7c948a11', '[\"*\"]', '2026-01-15 17:32:55', NULL, '2026-01-15 17:32:13', '2026-01-15 17:32:55'),
(107, 'App\\Models\\Driver', 198, 'driver-token', '2f42e1377bd8157d6ded4b940e7a6f73444fab4b39e41883283e656f9be9ec9e', '[\"*\"]', '2026-01-15 18:07:50', NULL, '2026-01-15 17:36:49', '2026-01-15 18:07:50'),
(108, 'App\\Models\\Driver', 198, 'driver-token', '2da79fbab20a0991bb82da8499bb5f1f299836390abdebce359008f9533566c1', '[\"*\"]', '2026-01-15 18:09:20', NULL, '2026-01-15 18:09:14', '2026-01-15 18:09:20'),
(109, 'App\\Models\\Driver', 198, 'driver-token', '93c20f9ca2156af9d43001327e08c21113a2a52ef892df09ec9dfd3d97d6a3b4', '[\"*\"]', '2026-01-15 19:57:52', NULL, '2026-01-15 18:24:45', '2026-01-15 19:57:52'),
(110, 'App\\Models\\Driver', 198, 'driver-token', '8a268a02aafbb7cf4c611277db7cfd805e35490be83fa8553096819ea979a123', '[\"*\"]', '2026-01-15 21:31:39', NULL, '2026-01-15 20:12:17', '2026-01-15 21:31:39'),
(111, 'App\\Models\\Driver', 198, 'driver-token', '394398f5a2998c6b1ae1f99cf57feea012f45cf67affe6aad6c230821b8fda3f', '[\"*\"]', '2026-01-16 00:01:04', NULL, '2026-01-15 21:32:42', '2026-01-16 00:01:04'),
(112, 'App\\Models\\Driver', 198, 'driver-token', '8cac2e163cb2603244e633d09422cd164f089cd391014f40b85af78abefc6ef7', '[\"*\"]', '2026-01-17 03:25:39', NULL, '2026-01-16 00:01:26', '2026-01-17 03:25:39'),
(114, 'App\\Models\\Driver', 198, 'driver-token', '3fbd1c90b8a53f1e65b36a91e56a71bb51d803181492777d84e4b2bfe72af18d', '[\"*\"]', '2026-01-19 20:48:26', NULL, '2026-01-19 20:48:25', '2026-01-19 20:48:26'),
(115, 'App\\Models\\Driver', 198, 'driver-token', '850290120d451eb137a919bc66faa59cf216b269f88df5d81b4d4a00c06b56a6', '[\"*\"]', '2026-01-20 19:42:51', NULL, '2026-01-19 21:32:34', '2026-01-20 19:42:51'),
(116, 'App\\Models\\Driver', 198, 'driver-token', '3acae7b62eab4c5f851314c759e7575e9faf778b3e6c6ae3cf1c13acff1aa13e', '[\"*\"]', '2026-01-20 19:55:30', NULL, '2026-01-20 19:44:04', '2026-01-20 19:55:30'),
(117, 'App\\Models\\Driver', 198, 'driver-token', '5180a666f8377cbd5ec6949d9322c8ea98afa539b81bcc1d264dbee58ace87d5', '[\"*\"]', '2026-01-21 21:09:31', NULL, '2026-01-20 19:56:19', '2026-01-21 21:09:31'),
(118, 'App\\Models\\Driver', 185, 'driver-token', '97d743c97f979c100abd47439cf04f811006041e9aeed1d6f136c09d36c23e62', '[\"*\"]', '2026-01-21 20:23:48', NULL, '2026-01-21 19:39:27', '2026-01-21 20:23:48');

-- --------------------------------------------------------

--
-- Table structure for table `privileges`
--

CREATE TABLE `privileges` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `role_id` int(11) NOT NULL,
  `module_id` int(11) NOT NULL,
  `is_view` int(11) NOT NULL DEFAULT 0,
  `is_add` int(11) NOT NULL DEFAULT 0,
  `is_edit` int(11) NOT NULL DEFAULT 0,
  `is_delete` int(11) NOT NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `privileges`
--

INSERT INTO `privileges` (`id`, `role_id`, `module_id`, `is_view`, `is_add`, `is_edit`, `is_delete`, `created_at`, `updated_at`) VALUES
(1, 1, 1, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(2, 1, 5, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(3, 1, 12, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(4, 1, 13, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(5, 1, 2, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(6, 1, 3, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(7, 1, 6, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(8, 1, 4, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(9, 1, 11, 1, 1, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(10, 1, 7, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(11, 1, 8, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(12, 1, 9, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(13, 1, 10, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(14, 2, 1, 1, 0, 0, 0, '2025-01-26 08:07:17', '2025-01-26 08:07:17'),
(15, 2, 5, 1, 0, 0, 0, '2025-01-26 08:07:17', '2025-01-26 08:07:17'),
(16, 2, 12, 1, 0, 0, 0, '2025-01-26 08:07:17', '2025-01-26 08:07:17'),
(17, 2, 13, 1, 0, 0, 0, '2025-01-26 08:07:17', '2025-01-26 08:07:17'),
(18, 2, 2, 1, 0, 0, 0, '2025-01-26 08:07:17', '2025-01-26 08:07:17'),
(19, 2, 3, 1, 0, 0, 0, '2025-01-26 08:07:17', '2025-01-26 08:07:17'),
(20, 2, 6, 1, 0, 0, 0, '2025-01-26 08:07:17', '2025-01-26 08:07:17'),
(21, 2, 4, 1, 0, 0, 0, '2025-01-26 08:07:17', '2025-01-26 08:07:17'),
(22, 2, 11, 1, 0, 0, 0, '2025-01-26 08:07:17', '2025-01-26 08:07:17'),
(23, 2, 7, 1, 0, 0, 0, '2025-01-26 08:07:18', '2025-01-26 08:07:18'),
(24, 2, 8, 1, 0, 0, 0, '2025-01-26 08:07:18', '2025-01-26 08:08:01'),
(25, 2, 9, 1, 0, 0, 0, '2025-01-26 08:07:18', '2025-01-26 08:07:18'),
(26, 2, 10, 1, 0, 0, 0, '2025-01-26 08:07:18', '2025-01-26 08:08:01'),
(27, 3, 1, 1, 0, 0, 0, '2025-07-28 10:16:05', '2025-07-28 10:16:05'),
(28, 3, 5, 1, 0, 0, 0, '2025-07-28 10:16:05', '2025-08-23 16:10:29'),
(29, 3, 12, 1, 0, 0, 0, '2025-07-28 10:16:05', '2025-08-23 16:10:29'),
(30, 3, 13, 1, 0, 0, 0, '2025-07-28 10:16:05', '2025-08-23 16:10:29'),
(31, 3, 2, 1, 0, 0, 0, '2025-07-28 10:16:05', '2025-07-28 10:16:05'),
(32, 3, 3, 1, 0, 0, 0, '2025-07-28 10:16:05', '2025-08-23 16:10:29'),
(33, 3, 6, 1, 1, 1, 0, '2025-07-28 10:16:05', '2025-08-23 15:03:53'),
(34, 3, 4, 1, 0, 0, 0, '2025-07-28 10:16:05', '2025-07-28 10:16:05'),
(35, 3, 11, 1, 0, 0, 0, '2025-07-28 10:16:05', '2025-08-23 16:10:29'),
(36, 3, 7, 1, 0, 0, 0, '2025-07-28 10:16:05', '2025-08-23 16:10:29'),
(37, 3, 8, 1, 1, 1, 0, '2025-07-28 10:16:05', '2025-08-23 15:03:53'),
(38, 3, 9, 1, 0, 0, 0, '2025-07-28 10:16:05', '2025-08-23 15:03:53'),
(39, 3, 10, 1, 0, 0, 0, '2025-07-28 10:16:05', '2025-08-23 15:03:53'),
(40, 4, 1, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(41, 4, 5, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(42, 4, 12, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(43, 4, 13, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(44, 4, 2, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(45, 4, 3, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(46, 4, 6, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(47, 4, 4, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(48, 4, 11, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(49, 4, 7, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(50, 4, 8, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(51, 4, 9, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(52, 4, 10, 1, 0, 0, 0, '2025-07-28 11:55:29', '2025-07-28 11:55:29'),
(53, 5, 1, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(54, 5, 5, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(55, 5, 12, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(56, 5, 13, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(57, 5, 14, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(58, 5, 2, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(59, 5, 3, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(60, 5, 6, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(61, 5, 4, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(62, 5, 11, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(63, 5, 7, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(64, 5, 8, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(65, 5, 9, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(66, 5, 10, 1, 0, 0, 0, '2025-08-23 15:03:15', '2025-08-23 15:03:15'),
(67, 6, 1, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:16:26'),
(68, 6, 5, 1, 1, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:17:06'),
(69, 6, 12, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:16:26'),
(70, 6, 13, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:16:26'),
(71, 6, 14, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:16:26'),
(72, 6, 2, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:16:26'),
(73, 6, 3, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:16:26'),
(74, 6, 6, 1, 1, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:17:06'),
(75, 6, 4, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:16:26'),
(76, 6, 11, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:16:26'),
(77, 6, 7, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:17:06'),
(78, 6, 8, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:17:06'),
(79, 6, 9, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:17:06'),
(80, 6, 10, 1, 0, 0, 0, '2025-09-18 14:16:26', '2025-09-18 14:17:06'),
(81, 7, 1, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(82, 7, 5, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(83, 7, 12, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(84, 7, 13, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:50'),
(85, 7, 14, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(86, 7, 2, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(87, 7, 3, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(88, 7, 6, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(89, 7, 4, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(90, 7, 11, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(91, 7, 7, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(92, 7, 8, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(93, 7, 9, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(94, 7, 10, 1, 0, 0, 0, '2025-10-07 18:10:22', '2025-10-07 18:10:22'),
(95, 1, 15, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(96, 1, 16, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(97, 1, 17, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(98, 8, 0, 1, 1, 1, 0, '2025-11-16 16:01:16', '2025-11-16 16:01:16'),
(99, 9, 0, 1, 1, 1, 0, '2025-11-16 16:01:49', '2025-11-16 16:01:49'),
(100, 1, 18, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(101, 1, 19, 1, 1, 1, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(102, 8, 1, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(103, 8, 5, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(104, 8, 12, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(105, 8, 13, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(106, 8, 14, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(107, 8, 18, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(108, 8, 2, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(109, 8, 3, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(110, 8, 6, 1, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:35'),
(111, 8, 19, 1, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(112, 8, 20, 1, 1, 1, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:35'),
(113, 8, 21, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-19 17:31:55'),
(114, 8, 4, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(115, 8, 11, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(116, 8, 7, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(117, 8, 15, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(118, 8, 8, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(119, 8, 16, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(120, 8, 9, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(121, 8, 10, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(122, 8, 17, 0, 0, 0, 0, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(123, 9, 1, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(124, 9, 5, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(125, 9, 12, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(126, 9, 13, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(127, 9, 14, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(128, 9, 18, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(129, 9, 2, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(130, 9, 3, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(131, 9, 6, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-23 19:03:36'),
(132, 9, 19, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-23 19:03:36'),
(133, 9, 20, 1, 1, 1, 0, '2025-11-17 02:57:49', '2025-11-17 02:58:08'),
(134, 9, 21, 1, 1, 1, 0, '2025-11-17 02:57:49', '2025-11-17 02:58:08'),
(135, 9, 4, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(136, 9, 11, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(137, 9, 7, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(138, 9, 15, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(139, 9, 8, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(140, 9, 16, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(141, 9, 9, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(142, 9, 10, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(143, 9, 17, 0, 0, 0, 0, '2025-11-17 02:57:49', '2025-11-17 02:57:49'),
(144, 1, 22, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(145, 1, 23, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(146, 1, 24, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(147, 1, 25, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(148, 1, 26, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(149, 1, 20, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(150, 1, 21, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(151, 9, 26, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(152, 9, 25, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(153, 9, 24, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(154, 9, 23, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(155, 9, 22, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(156, 8, 24, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(157, 8, 23, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(158, 8, 22, 1, 1, 1, 1, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(159, 8, 25, 0, 0, 0, 0, '2025-11-19 17:31:55', '2025-11-19 17:31:55'),
(160, 1, 27, 1, 1, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(161, 1, 28, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(162, 9, 27, 1, 1, 0, 0, '2025-11-22 20:27:26', '2025-11-23 19:03:36'),
(163, 9, 28, 1, 0, 0, 0, '2025-11-22 20:27:26', '2025-11-22 20:27:26'),
(164, 8, 27, 1, 1, 0, 0, '2025-11-22 20:30:07', '2025-11-22 20:30:07'),
(165, 8, 28, 0, 0, 0, 0, '2025-11-22 20:30:07', '2025-11-22 20:30:07'),
(166, 8, 26, 0, 0, 0, 0, '2025-11-22 20:30:07', '2025-11-22 20:30:07'),
(167, 10, 1, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(168, 10, 5, 1, 1, 1, 0, '2025-11-23 18:57:59', '2025-11-23 18:59:20'),
(169, 10, 12, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(170, 10, 13, 1, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:59:20'),
(171, 10, 14, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(172, 10, 17, 1, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:59:20'),
(173, 10, 18, 1, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:59:20'),
(174, 10, 2, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(175, 10, 3, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(176, 10, 6, 1, 1, 1, 0, '2025-11-23 18:57:59', '2025-11-23 18:59:20'),
(177, 10, 23, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(178, 10, 24, 1, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:59:20'),
(179, 10, 26, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(180, 10, 4, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(181, 10, 11, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(182, 10, 7, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(183, 10, 15, 1, 1, 1, 0, '2025-11-23 18:57:59', '2025-11-23 18:59:20'),
(184, 10, 8, 1, 1, 1, 0, '2025-11-23 18:57:59', '2025-11-23 18:59:20'),
(185, 10, 16, 1, 1, 1, 0, '2025-11-23 18:57:59', '2025-11-23 18:59:20'),
(186, 10, 9, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(187, 10, 10, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(188, 10, 21, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(189, 10, 22, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(190, 10, 20, 1, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:59:20'),
(191, 10, 25, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(192, 10, 27, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(193, 10, 28, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(194, 10, 19, 0, 0, 0, 0, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(195, 11, 1, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(196, 11, 5, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(197, 11, 12, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(198, 11, 13, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(199, 11, 14, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(200, 11, 17, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(201, 11, 18, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(202, 11, 2, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(203, 11, 3, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(204, 11, 6, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(205, 11, 23, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(206, 11, 24, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(207, 11, 26, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(208, 11, 4, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(209, 11, 11, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(210, 11, 7, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(211, 11, 15, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(212, 11, 8, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(213, 11, 16, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(214, 11, 9, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(215, 11, 10, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(216, 11, 21, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(217, 11, 22, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(218, 11, 20, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(219, 11, 25, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(220, 11, 27, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(221, 11, 28, 1, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:01:57'),
(222, 11, 19, 0, 0, 0, 0, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(223, 12, 1, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(224, 12, 5, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(225, 12, 12, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(226, 12, 13, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(227, 12, 14, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(228, 12, 17, 1, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(229, 12, 18, 1, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(230, 12, 2, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(231, 12, 3, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(232, 12, 6, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(233, 12, 23, 1, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(234, 12, 24, 1, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(235, 12, 26, 1, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(236, 12, 4, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(237, 12, 11, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(238, 12, 7, 1, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(239, 12, 15, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(240, 12, 8, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(241, 12, 16, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(242, 12, 9, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(243, 12, 10, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(244, 12, 21, 1, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(245, 12, 22, 1, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(246, 12, 20, 1, 1, 1, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(247, 12, 25, 1, 1, 1, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(248, 12, 27, 1, 1, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(249, 12, 28, 1, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:05:10'),
(250, 12, 19, 0, 0, 0, 0, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(251, 13, 1, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(252, 13, 5, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(253, 13, 12, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(254, 13, 13, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(255, 13, 14, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(256, 13, 17, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(257, 13, 18, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(258, 13, 2, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(259, 13, 3, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(260, 13, 6, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(261, 13, 23, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(262, 13, 24, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(263, 13, 26, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(264, 13, 4, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(265, 13, 11, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(266, 13, 7, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(267, 13, 15, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(268, 13, 8, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(269, 13, 16, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(270, 13, 9, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(271, 13, 10, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(272, 13, 21, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(273, 13, 22, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(274, 13, 20, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(275, 13, 25, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(276, 13, 27, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(277, 13, 28, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(278, 13, 19, 0, 0, 0, 0, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(279, 14, 1, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(280, 14, 5, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(281, 14, 12, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(282, 14, 13, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(283, 14, 14, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(284, 14, 17, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(285, 14, 18, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(286, 14, 2, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(287, 14, 3, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(288, 14, 6, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(289, 14, 23, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(290, 14, 24, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(291, 14, 26, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(292, 14, 4, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(293, 14, 11, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(294, 14, 7, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(295, 14, 15, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(296, 14, 8, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(297, 14, 16, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(298, 14, 9, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(299, 14, 10, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(300, 14, 21, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(301, 14, 22, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(302, 14, 20, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(303, 14, 25, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(304, 14, 27, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(305, 14, 28, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(306, 14, 19, 0, 0, 0, 0, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(307, 15, 1, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(308, 15, 5, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(309, 15, 12, 1, 1, 1, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:32'),
(310, 15, 13, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(311, 15, 14, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(312, 15, 17, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(313, 15, 18, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(314, 15, 2, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(315, 15, 3, 1, 1, 1, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:32'),
(316, 15, 6, 1, 1, 1, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:32'),
(317, 15, 23, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(318, 15, 24, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(319, 15, 26, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(320, 15, 4, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(321, 15, 11, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(322, 15, 7, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(323, 15, 15, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(324, 15, 8, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(325, 15, 16, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(326, 15, 9, 1, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:32'),
(327, 15, 10, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(328, 15, 21, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(329, 15, 22, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(330, 15, 20, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(331, 15, 25, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(332, 15, 27, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(333, 15, 28, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(334, 15, 19, 0, 0, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(335, 1, 29, 1, 1, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(336, 1, 30, 1, 1, 0, 0, '2025-11-23 19:06:11', '2025-11-23 19:06:11'),
(337, 8, 29, 1, 1, 0, 0, '2025-11-29 19:06:30', '2025-11-29 19:06:30'),
(338, 8, 30, 0, 0, 0, 0, '2025-11-29 19:06:30', '2025-11-29 19:06:30'),
(339, 11, 29, 1, 0, 0, 0, '2025-11-29 19:06:53', '2025-11-29 19:06:53'),
(340, 11, 30, 0, 0, 0, 0, '2025-11-29 19:06:53', '2025-11-29 19:06:53'),
(341, 12, 29, 0, 0, 0, 0, '2025-11-29 19:07:06', '2025-11-29 19:07:06'),
(342, 12, 30, 1, 1, 0, 0, '2025-11-29 19:07:06', '2025-11-29 19:07:06'),
(343, 1, 31, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(344, 1, 14, 1, 1, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(345, 1, 32, 1, 1, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(346, 1, 33, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(347, 1, 34, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(348, 1, 35, 1, 1, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(349, 1, 36, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(350, 1, 37, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(351, 1, 38, 1, 1, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(352, 1, 39, 1, 1, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(353, 1, 40, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(354, 8, 32, 0, 0, 0, 0, '2025-12-18 01:37:08', '2025-12-18 01:37:08'),
(355, 8, 33, 0, 0, 0, 0, '2025-12-18 01:37:08', '2025-12-18 01:37:08'),
(356, 8, 34, 0, 0, 0, 0, '2025-12-18 01:37:08', '2025-12-18 01:37:08'),
(357, 8, 35, 0, 0, 0, 0, '2025-12-18 01:37:08', '2025-12-18 01:37:08'),
(358, 8, 36, 0, 0, 0, 0, '2025-12-18 01:37:08', '2025-12-18 01:37:08'),
(359, 8, 38, 0, 0, 0, 0, '2025-12-18 01:37:08', '2025-12-18 01:37:08'),
(360, 8, 39, 1, 1, 0, 0, '2025-12-18 01:37:08', '2025-12-18 01:37:08'),
(361, 8, 40, 0, 0, 0, 0, '2025-12-18 01:37:08', '2025-12-18 01:37:08'),
(362, 8, 31, 0, 0, 0, 0, '2025-12-18 01:37:08', '2025-12-18 01:37:08'),
(363, 1, 41, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(364, 1, 42, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(365, 1, 43, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(366, 1, 44, 1, 0, 0, 0, '2024-11-23 05:30:05', '2024-11-23 05:30:05');

-- --------------------------------------------------------

--
-- Table structure for table `recharges`
--

CREATE TABLE `recharges` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `request_recharge_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `amount` bigint(20) NOT NULL,
  `date` datetime DEFAULT NULL,
  `image` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `recharges`
--

INSERT INTO `recharges` (`id`, `request_recharge_id`, `user_id`, `amount`, `date`, `image`, `created_at`, `updated_at`) VALUES
(1, 1, 31, 2000, '2025-12-01 18:14:00', 'recharge/20251201_184508-Germaine Potts-2167777777.pdf', '2025-12-01 23:45:08', '2025-12-01 23:45:08'),
(2, 4, 31, 100, '2025-12-03 11:17:00', 'recharge/20251203_134724-Usman Asif Qureshi for test-2585305937.png', '2025-12-03 18:47:24', '2025-12-03 18:47:24'),
(3, 5, 45, 100, '2025-12-03 11:23:00', 'recharge/20251203_135350-Ginger Goodwin-6151111111.png', '2025-12-03 18:53:50', '2025-12-03 18:53:50');

-- --------------------------------------------------------

--
-- Table structure for table `replacement_rejections`
--

CREATE TABLE `replacement_rejections` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `replacement_id` bigint(20) UNSIGNED NOT NULL,
  `rejection_note` text NOT NULL,
  `rejected_by` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `replacement_rejections`
--

INSERT INTO `replacement_rejections` (`id`, `replacement_id`, `rejection_note`, `rejected_by`, `created_at`, `updated_at`) VALUES
(14, 45, '', 'Zain', '2025-12-03 19:36:21', '2025-12-03 19:36:21');

-- --------------------------------------------------------

--
-- Table structure for table `request_recharges`
--

CREATE TABLE `request_recharges` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `driver_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `opearator` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `reason` text DEFAULT NULL,
  `approved_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `request_recharges`
--

INSERT INTO `request_recharges` (`id`, `driver_id`, `user_id`, `mobile`, `opearator`, `status`, `reason`, `approved_by`, `created_at`, `updated_at`) VALUES
(1, 185, 46, '1234567899', '123', 'Accepted', NULL, 44, '2025-12-01 23:40:46', '2025-12-01 23:43:58'),
(2, 184, 31, '1234567', '1234', 'Rejected', 'Recharge Rejected', 31, '2025-12-01 23:45:45', '2025-12-01 23:48:32'),
(3, 186, 31, '0568465058', 'stc', 'pending', NULL, NULL, '2025-12-02 18:39:11', '2025-12-02 18:39:11'),
(4, 186, 31, '0568465058', 'stc', 'Accepted', NULL, 31, '2025-12-03 18:42:58', '2025-12-03 18:43:16'),
(5, 180, 46, '0568465058', 'stc', 'Accepted', NULL, 44, '2025-12-03 18:50:02', '2025-12-03 18:51:23');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `is_default` int(11) NOT NULL DEFAULT 0 COMMENT '1=Yes, 0=No',
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`, `is_default`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Administrator', 1, NULL, '2024-11-23 05:30:05', '2024-11-23 05:30:05'),
(8, 'operation supervisor', 0, NULL, '2025-11-17 02:57:06', '2025-11-17 02:57:06'),
(9, 'Cashier', 0, NULL, '2025-11-17 02:57:49', '2025-11-23 19:02:09'),
(10, 'Platform Operations Executive ', 0, NULL, '2025-11-23 18:57:59', '2025-11-23 18:57:59'),
(11, 'Operation Manager', 0, NULL, '2025-11-23 19:00:15', '2025-11-23 19:00:15'),
(12, 'Finance Manager', 0, NULL, '2025-11-23 19:03:44', '2025-11-23 19:03:44'),
(13, 'Fleet Manager', 0, NULL, '2025-11-23 19:05:30', '2025-11-23 19:05:30'),
(14, 'Fleet Supervisor', 0, NULL, '2025-11-23 19:05:57', '2025-11-23 19:05:57'),
(15, 'HR Manager', 0, NULL, '2025-11-23 19:06:11', '2025-11-23 19:06:11');

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `id` varchar(255) NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `payload` longtext NOT NULL,
  `last_activity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sessions`
--

INSERT INTO `sessions` (`id`, `user_id`, `ip_address`, `user_agent`, `payload`, `last_activity`) VALUES
('3qvyCtiRbPrDfYAunuXMD0IMMnFAXnnxvfDv0VQ0', 31, '103.191.119.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0', 'YTo0OntzOjY6Il90b2tlbiI7czo0MDoiajl1eGJ1Rzd6bjYzZXBGUkVjTDFqOWJTaFlFR0pybml6STNsalR2UCI7czo5OiJfcHJldmlvdXMiO2E6MTp7czozOiJ1cmwiO3M6MzI6Imh0dHBzOi8vZG1zLmRvYnMuY2xvdWQvZGFzaGJvYXJkIjt9czo2OiJfZmxhc2giO2E6Mjp7czozOiJvbGQiO2E6MDp7fXM6MzoibmV3IjthOjA6e319czo1MDoibG9naW5fd2ViXzU5YmEzNmFkZGMyYjJmOTQwMTU4MGYwMTRjN2Y1OGVhNGUzMDk4OWQiO2k6MzE7fQ==', 1768996306),
('CFovIEQI3OElCCq9WiJ8PWxzt0z3sQssPrdZVuRw', 185, '103.191.119.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'YTo0OntzOjY6Il90b2tlbiI7czo0MDoiV2NUOHBVMk01MEZhQ3l3S3N5dXZ0dERtU2JIOUd3OU5SQmsxR1hyUCI7czo5OiJfcHJldmlvdXMiO2E6MTp7czozOiJ1cmwiO3M6Mzc6Imh0dHBzOi8vZG1zLmRvYnMuY2xvdWQvZHJpdmVyL3Byb2ZpbGUiO31zOjY6Il9mbGFzaCI7YToyOntzOjM6Im9sZCI7YTowOnt9czozOiJuZXciO2E6MDp7fX1zOjUzOiJsb2dpbl9kcml2ZXJfNTliYTM2YWRkYzJiMmY5NDAxNTgwZjAxNGM3ZjU4ZWE0ZTMwOTg5ZCI7aToxODU7fQ==', 1768995938),
('HxtPUSe2KX0ufov8mgouubcCuFxGjXAEMwkFVfw6', 31, '103.191.119.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'YTo0OntzOjY6Il90b2tlbiI7czo0MDoiOXhZYTRqMDlIbkhESlI2OHNsOWtjR09LRWM4VXc4T1BIUnJFNXR4VSI7czo5OiJfcHJldmlvdXMiO2E6MTp7czozOiJ1cmwiO3M6MzI6Imh0dHBzOi8vZG1zLmRvYnMuY2xvdWQvZGFzaGJvYXJkIjt9czo2OiJfZmxhc2giO2E6Mjp7czozOiJvbGQiO2E6MDp7fXM6MzoibmV3IjthOjA6e319czo1MDoibG9naW5fd2ViXzU5YmEzNmFkZGMyYjJmOTQwMTU4MGYwMTRjN2Y1OGVhNGUzMDk4OWQiO2k6MzE7fQ==', 1768996204),
('mO9Wv394y9kuykmnY8zftDRibZqQzXJC67V6HsdS', 31, '103.191.119.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0', 'YTo1OntzOjY6Il90b2tlbiI7czo0MDoiTjBhSnd3U3Bkd2dkVGhFQVY5UFZNdVZKYm1EZ1Z4TEdIOTREOE9IbiI7czozOiJ1cmwiO2E6MTp7czo4OiJpbnRlbmRlZCI7czoyMjoiaHR0cHM6Ly9kbXMuZG9icy5jbG91ZCI7fXM6OToiX3ByZXZpb3VzIjthOjE6e3M6MzoidXJsIjtzOjQxOiJodHRwczovL2Rtcy5kb2JzLmNsb3VkL2RyaXZlcnMvYXR0ZW5kYW5jZSI7fXM6NjoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fXM6NTA6ImxvZ2luX3dlYl81OWJhMzZhZGRjMmIyZjk0MDE1ODBmMDE0YzdmNThlYTRlMzA5ODlkIjtpOjMxO30=', 1768997420),
('oj3o33QIPp61YepNbhlueyEjynJ97Go7V8AUfgPb', 31, '103.191.119.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0', 'YTo0OntzOjY6Il90b2tlbiI7czo0MDoiTE51Y0tXdjBxSkJIR2hRTEc1bG9VMFVIWFhoQXNPRU5CYVZJazNXciI7czo5OiJfcHJldmlvdXMiO2E6MTp7czozOiJ1cmwiO3M6MzI6Imh0dHBzOi8vZG1zLmRvYnMuY2xvdWQvZGFzaGJvYXJkIjt9czo2OiJfZmxhc2giO2E6Mjp7czozOiJvbGQiO2E6MDp7fXM6MzoibmV3IjthOjA6e319czo1MDoibG9naW5fd2ViXzU5YmEzNmFkZGMyYjJmOTQwMTU4MGYwMTRjN2Y1OGVhNGUzMDk4OWQiO2k6MzE7fQ==', 1768996349),
('QSFAAVezma6qWXfycQWj2fc70rtSduYiu18dipub', 31, '103.191.119.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0', 'YTo1OntzOjY6Il90b2tlbiI7czo0MDoiV0U2TmJhUlRkV2tOSk8yM09SdXRRaGxwVWRObERadkE3SklrY2tDWCI7czozOiJ1cmwiO2E6MTp7czo4OiJpbnRlbmRlZCI7czoyMjoiaHR0cHM6Ly9kbXMuZG9icy5jbG91ZCI7fXM6OToiX3ByZXZpb3VzIjthOjE6e3M6MzoidXJsIjtzOjMyOiJodHRwczovL2Rtcy5kb2JzLmNsb3VkL2Rhc2hib2FyZCI7fXM6NjoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fXM6NTA6ImxvZ2luX3dlYl81OWJhMzZhZGRjMmIyZjk0MDE1ODBmMDE0YzdmNThlYTRlMzA5ODlkIjtpOjMxO30=', 1768994484);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `designation_id` bigint(20) UNSIGNED NOT NULL,
  `department_id` bigint(20) UNSIGNED NOT NULL,
  `role_id` bigint(20) UNSIGNED NOT NULL,
  `employment_type_id` bigint(20) UNSIGNED NOT NULL,
  `branch_id` bigint(20) UNSIGNED NOT NULL,
  `country_id` bigint(20) UNSIGNED NOT NULL,
  `language_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `salutation` enum('Mrs','Mr','Miss','Dr.','Sir','Madam') DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `image` text DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `gender` enum('Male','Female','Others') NOT NULL DEFAULT 'Male',
  `dob` date DEFAULT NULL,
  `joining_date` date DEFAULT NULL,
  `reporting_to` bigint(20) UNSIGNED DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `about` longtext DEFAULT NULL,
  `is_login_allowed` tinyint(1) NOT NULL DEFAULT 1,
  `is_receive_email_notification` tinyint(1) NOT NULL DEFAULT 1,
  `hourly_rate` decimal(8,2) DEFAULT 0.00,
  `slack_memember_id` varchar(255) DEFAULT NULL,
  `skills` varchar(255) DEFAULT NULL,
  `probation_end_date` date DEFAULT NULL,
  `notice_period_start_date` date DEFAULT NULL,
  `notice_period_end_date` date DEFAULT NULL,
  `marital_status` enum('Single','Married','Widower','Widow','Seprate','Divorced','Engaged') NOT NULL DEFAULT 'Single',
  `remember_token` varchar(100) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `status` enum('Active','Inactive') NOT NULL DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `designation_id`, `department_id`, `role_id`, `employment_type_id`, `branch_id`, `country_id`, `language_id`, `user_id`, `salutation`, `name`, `email`, `email_verified_at`, `image`, `password`, `mobile`, `gender`, `dob`, `joining_date`, `reporting_to`, `address`, `about`, `is_login_allowed`, `is_receive_email_notification`, `hourly_rate`, `slack_memember_id`, `skills`, `probation_end_date`, `notice_period_start_date`, `notice_period_end_date`, `marital_status`, `remember_token`, `deleted_at`, `created_at`, `updated_at`, `status`) VALUES
(2, 4, 1, 1, 1, 1, 1, 1, 'E1000', 'Mr', 'Abdulrahman Al Zayani', 'ceo@ilab.sa', NULL, NULL, '$2y$12$IAcg5rdvB9yDb6qysMslfe0JwdIBOJ6M2U9kw0wp50LXKyUSac0py', NULL, 'Male', NULL, '2024-05-16', NULL, NULL, NULL, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, 'Single', NULL, NULL, NULL, NULL, 'Active'),
(5, 28, 1, 10, 1, 1, 166, 38, 'E1006', 'Mr', 'Ahmed Akhtar', 'ahmed@ilab.sa', NULL, NULL, '$2y$12$nQrCGepGeXOYinF.gEAP1O3f7KowmI5hX7Dqfhr5PcfxKmrRtMImq', NULL, 'Male', '1997-09-06', '2022-04-02', 30, 'Dammam Iskan, Saudi Arabia', NULL, 1, 1, 0.00, NULL, '', '2025-11-27', '2025-11-19', '2025-11-19', 'Single', NULL, NULL, NULL, '2025-11-23 19:11:08', 'Active'),
(16, 12, 1, 1, 1, 1, 1, 1, 'E1037', 'Mr', 'Kashif Akbar', 'kashif.fleet@speed.sa', NULL, NULL, '$2y$12$xEcWqT0dhsB5ucYJS/WECOekw.WVeg0mis6c73UlggnN51qHM6C5i', NULL, 'Male', NULL, '2023-06-11', NULL, 'Khobar, Saudi Arabia', NULL, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, 'Single', NULL, NULL, NULL, NULL, 'Active'),
(30, 5, 1, 1, 1, 2, 166, 38, 'E1003', 'Mr', 'Usama Akhtar', 'usama1@ilab.sa', NULL, NULL, '$2y$12$zThTLifs4FT4S7mHYFooDukq13gNGsqHspQgrOBCoirQCjhQYoIHi', NULL, 'Male', '2025-08-07', '2022-12-01', 30, 'Dammam Iskan, Saudi Arabia', NULL, 1, 1, 0.00, NULL, '', '2025-08-07', '2025-08-07', '2025-08-07', 'Single', NULL, NULL, NULL, '2025-12-26 00:00:28', 'Active'),
(31, 1, 1, 1, 1, 1, 1, 1, 'E1032', 'Mr', 'Zain', 'zain@ilab.sa', NULL, NULL, '$2y$12$Imlf6ANnKoKvS75OqGsyquH.GdkC/4HA0CWLc7METy76Dvmb0qnCi', NULL, 'Male', NULL, '2024-03-03', NULL, 'Dammam, Saudi Arabia', NULL, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, 'Single', 'Idj3WYt3FSYsAxuXZKEWoaMnAsFzpue2mvXimWjZ5sUGoqYMJJpkFQVrsk2m', NULL, NULL, NULL, 'Active'),
(39, 7, 6, 8, 5, 2, 174, 134, 'E1092', 'Sir', 'oprationnsupervisor damam', 'operationsupervisor@gmail.com', NULL, NULL, '$2y$12$K26ex4yRpVfpi/0KU0HaD.zBrtUNfMCvDZ7OH/iiD3qcOYW3lgWrC', 'Iure voluptatem ut ', 'Male', '1998-07-23', '2013-03-18', NULL, NULL, NULL, 0, 1, 10.00, NULL, 'Sequi et rerum qui q', '1996-06-30', '1976-06-05', '1972-12-08', 'Widow', NULL, NULL, '2025-11-17 02:59:46', '2025-11-19 17:22:24', 'Active'),
(40, 2, 6, 9, 3, 2, 156, 9, 'E1093', 'Mr', 'Cashier dammam', 'cashier@gmail.com', NULL, NULL, '$2y$12$RiGk2r38ftae6fEpSY4iOedkRdTK9VkfQyBcVbAvmYF7Dd7btugs.', 'Ut vel tempor rerum ', 'Others', '2013-02-21', '1970-10-25', NULL, NULL, NULL, 0, 0, 5.00, NULL, 'Aspernatur temporibu', '1979-10-31', '1992-02-14', '1975-10-29', 'Seprate', NULL, NULL, '2025-11-17 03:01:24', '2025-11-19 17:22:00', 'Active'),
(41, 32, 1, 8, 4, 4, 85, 48, 'E1094', 'Sir', 'operational supervisor al hasa', 'operationsupervisor2@gmail.com', NULL, NULL, '$2y$12$OJJu2JcI1MVvnqP.cBWRr.9YNXPSQJGqXqyABFVx8CtQL26XRWo1m', 'Aute tempor Nam do a', 'Female', '1982-03-06', '2018-10-03', NULL, NULL, NULL, 0, 0, 10.00, NULL, 'Aut aut placeat ut ', '2021-01-25', '1970-07-14', '1991-07-31', 'Divorced', NULL, NULL, '2025-11-19 17:19:57', '2025-11-19 17:21:42', 'Active'),
(42, 32, 4, 9, 3, 4, 191, 8, 'E1095', 'Mr', 'Ali Abdulwahid', 'ali@ilab.sa', NULL, NULL, '$2y$12$xAQjPd6sETpKUIGP4iQVLeMisp1vq91GlNDj2qRpXi8SbmFzKYd5K', '', 'Male', '2025-02-05', '1981-04-10', 2, NULL, NULL, 1, 0, 20.00, NULL, 'Numquam quia delenit', '1978-01-03', '2010-01-25', '1997-04-21', 'Single', NULL, NULL, '2025-11-19 17:20:35', '2025-11-23 19:28:38', 'Active'),
(43, 14, 4, 12, 1, 3, 153, 9, 'E1096', 'Madam', 'Benedict Mcintyre', 'cofaso6007@bipochub.com', NULL, NULL, '$2y$12$sJ.ZSFyCzwG0vrqEZI91h.3lfRlEm5ncLLg6nKf7qAfg.cSshxRGy', 'Qui qui amet accusa', 'Female', '1999-05-15', '1981-04-10', 40, NULL, NULL, 0, 1, 10.00, NULL, 'Accusantium sint exe', '1981-02-20', '2013-09-24', '2024-07-02', 'Seprate', NULL, NULL, '2025-11-25 18:55:16', '2025-11-25 18:55:16', 'Active'),
(44, 13, 4, 11, 4, 2, 67, 87, 'E1097', 'Dr.', 'Noelani Joyce', 'jijilec351@cexch.com', NULL, NULL, '$2y$12$29/mNrKh/Cixn5.kRUUP8eFuvV4Rk1atUaMorrfkYylngFDIviAlu', 'Nulla omnis dolores ', 'Male', '2009-05-25', '1988-06-23', 2, NULL, NULL, 0, 0, 10.00, NULL, 'A dolor dicta fuga ', '1981-09-24', '2023-06-06', '2011-11-30', 'Seprate', '9XFFk0M1qnjLg6YftBZXOOtSY7cESo8mBJrln2uv7ZqiEiZ5KEDRkPcQSjXr', NULL, '2025-11-29 19:08:14', '2025-12-01 23:42:01', 'Active'),
(45, 9, 6, 12, 2, 3, 172, 54, 'E1098', 'Madam', 'Finance manager', 'byfogyba@denipl.com', NULL, NULL, '$2y$12$CLoKew077/xLvtQdPUeea.Qdp9I69hurFgENZwjpLQoxGpU7whWqi', 'Reprehenderit qui pa', 'Male', '1999-12-07', '1984-09-14', 41, NULL, NULL, 0, 0, 5.00, NULL, 'Laborum Perspiciati', '1980-03-19', '2022-07-15', '2022-04-15', 'Married', NULL, NULL, '2025-11-29 19:09:55', '2025-11-29 19:09:55', 'Active'),
(46, 32, 2, 8, 1, 2, 136, 50, 'E1099', 'Mrs', 'Ora Walters', 'mvaguc@mailto.plus', NULL, NULL, '$2y$12$.jSPnIuEFoRdKP0lZYuCL.oFVWRAiroGVh4pPRDwLHONGAv.cIXsG', 'Libero repudiandae s', 'Male', '1990-09-22', '2016-12-05', 39, NULL, NULL, 1, 1, 5.00, NULL, 'Assumenda et consequ', '1994-07-05', '1995-11-20', '2014-05-28', 'Engaged', NULL, NULL, '2025-11-29 19:18:16', '2025-12-01 23:40:20', 'Active'),
(47, 17, 8, 1, 1, 3, 57, 20, 'E1100', 'Mrs', 'Leroy Dalton', 'violet956@comfythings.com', NULL, NULL, '$2y$12$owkhrn4XVRfAoqtOBSzIgepLHjgXEJPHx9VpdlJPtj6TkqoNPu2lC', 'Delectus saepe ulla', 'Female', '1996-03-24', '1975-10-19', 5, NULL, NULL, 1, 0, 5.00, NULL, 'Ipsa dicta illum v', '2000-08-15', '2021-03-25', '1975-02-25', 'Engaged', NULL, NULL, '2025-11-29 19:19:22', '2025-11-29 19:19:22', 'Active'),
(48, 1, 1, 1, 1, 2, 166, 38, 'E1101', 'Mr', 'Usman Asif', 'usman1@ilab.sa', NULL, NULL, '$2y$12$CB4k1buBbT0ANFZKU/800.imRtlRyQ7X.yZET9FNx0aJ4eLSK1aXe', '0568465058', 'Male', '1997-12-10', '2025-09-21', 30, NULL, NULL, 1, 1, 0.00, NULL, '', '2025-12-21', '2025-12-21', '2025-12-21', 'Single', NULL, NULL, '2025-12-25 21:22:32', '2025-12-25 23:57:47', 'Active'),
(49, 5, 7, 1, 2, 3, 18, 138, 'E1102', 'Mr', 'Justine Puckett', 'hidit46323@m3player.com', NULL, NULL, '$2y$12$1XwwL92lajgq4/voMcMR3eF1uLJs4sKGe1vkEQPcRMVkbjcgnSEGO', 'Ea inventore officii', 'Others', '1991-10-18', '1975-07-17', 30, NULL, NULL, 1, 0, 10.00, NULL, 'Fugiat iusto cupida', '2003-04-15', '1982-06-02', '2016-02-06', 'Divorced', NULL, NULL, '2025-12-25 21:30:46', '2025-12-25 21:30:46', 'Active'),
(50, 17, 2, 1, 1, 1, 166, 38, 'E1103', 'Mr', 'Muteeb', 'muteebaliofficial@gmail.com', NULL, NULL, '$2y$12$tlfA6BkpBmivRie918/gwOpEjkFb5k8Qax0NSjgIdz4WkptQJF9jq', '+923026490627', 'Male', '2025-12-25', '2025-12-25', 31, NULL, NULL, 1, 1, 0.00, NULL, '', '2025-12-25', '2025-12-31', '2026-01-07', 'Single', NULL, NULL, '2025-12-25 23:54:22', '2025-12-25 23:54:22', 'Active'),
(51, 16, 11, 1, 1, 1, 166, 38, 'E1104', 'Mr', 'Usman', 'usman@ilab.sa', NULL, NULL, '$2y$12$bqnhrsqcWd494R1Ohmud..ruWF.PI9XmhMiiSOjRyG0AJm1cu3vZq', '+923020200202', 'Male', '2025-12-25', '2025-12-25', 45, NULL, NULL, 1, 1, 0.00, NULL, '', '2025-12-25', '2026-01-07', '2026-01-06', 'Single', NULL, NULL, '2025-12-25 23:59:04', '2025-12-25 23:59:04', 'Active'),
(52, 16, 12, 1, 1, 1, 166, 38, 'E1105', 'Mr', 'Usama', 'usama@ilab.sa', NULL, NULL, '$2y$12$.hyZH3FVlOQPnEZk9RuLVeba6zbIPDf54Ybfy0j0RwXQnaVPXG.c.', '+930303003030', 'Male', '2025-12-25', '2025-12-25', 45, NULL, NULL, 1, 1, 0.00, NULL, '', '2025-12-25', '2025-12-31', '2026-01-03', 'Single', NULL, NULL, '2025-12-26 00:01:33', '2025-12-26 00:01:33', 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `registration_number` varchar(255) NOT NULL,
  `make` varchar(255) NOT NULL,
  `model` varchar(255) NOT NULL,
  `year` year(4) NOT NULL,
  `vin` varchar(255) DEFAULT NULL,
  `current_location` varchar(255) DEFAULT NULL,
  `status` enum('available','assigned','maintenance','out_of_service','in-replacement') NOT NULL DEFAULT 'available',
  `fuel_type` enum('petrol','diesel','electric','hybrid') NOT NULL,
  `mileage` int(11) NOT NULL DEFAULT 0,
  `notes` text DEFAULT NULL,
  `color` varchar(255) DEFAULT NULL,
  `rental_company` varchar(255) DEFAULT NULL,
  `company_sticker` varchar(255) DEFAULT NULL,
  `gps` varchar(255) DEFAULT NULL,
  `branch_id` int(20) UNSIGNED DEFAULT NULL,
  `images` text DEFAULT NULL,
  `car_type` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`id`, `registration_number`, `make`, `model`, `year`, `vin`, `current_location`, `status`, `fuel_type`, `mileage`, `notes`, `color`, `rental_company`, `company_sticker`, `gps`, `branch_id`, `images`, `car_type`, `created_at`, `updated_at`) VALUES
(131, 'DL-010211', 'TATA', 'Tiago', '2024', 'V-001', 'Delhi', 'assigned', 'petrol', 15, NULL, NULL, NULL, NULL, NULL, 2, NULL, NULL, '2025-07-12 19:43:33', '2025-12-21 20:09:56'),
(137, '0000', 'MITSUBISHIU', 'Pajero', '2025', '22222', 'sddad', 'out_of_service', 'petrol', 20212, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-08-20 16:10:44', '2025-12-14 21:06:12'),
(140, '3179drr', 'Suzuki', 'Dzire', '2025', '54654', 'dammam', 'in-replacement', 'petrol', 4545412, NULL, NULL, NULL, NULL, NULL, 2, NULL, NULL, '2025-10-21 21:25:39', '2025-12-14 21:06:12'),
(141, '475646', 'hond', 'acord', '2025', '531', 'dammam', 'assigned', 'petrol', 5465, NULL, NULL, NULL, NULL, NULL, 2, NULL, NULL, '2025-11-23 19:36:30', '2026-01-06 00:50:11'),
(142, '444', 'toyota', 'aurion', '2024', '56', 'dammam', 'available', 'petrol', 454564, NULL, NULL, NULL, NULL, NULL, 2, NULL, NULL, '2025-11-23 20:29:44', '2026-01-06 17:56:27'),
(143, '9151TXA', 'Sedan', 'Sedan', '2022', '0000000000', 'Dammam', 'assigned', 'petrol', 0, NULL, NULL, NULL, NULL, NULL, 2, NULL, NULL, '2025-12-02 18:43:54', '2026-01-06 17:56:54'),
(144, '123456', '12345', '1234', '2025', NULL, NULL, 'available', 'petrol', 10, NULL, 'Royal Blue', 'test1', 'no', 'installed', 4, NULL, NULL, '2025-12-04 02:17:05', '2025-12-04 02:17:24'),
(145, 'test vehicle', '2025', 'test vehicle', '2025', NULL, NULL, 'available', 'petrol', 1000, 'test', 'Royal Blue', 'test', 'no', 'installed', 4, '[\"vehicle\\/20251209_131110--6937d296cfd6c.png\"]', 'replacement', '2025-12-09 18:11:10', '2025-12-09 18:11:10'),
(146, 'test2', '2025', 'test2', '2025', NULL, NULL, 'available', 'petrol', 10, NULL, 'Sky Blue', '10', 'no', 'installed', 5, '[\"vehicle\\/20251211_205612--693ae2941be7f.png\"]', 'primary', '2025-12-12 01:56:12', '2025-12-12 01:56:12');

-- --------------------------------------------------------

--
-- Table structure for table `vehicle_documents`
--

CREATE TABLE `vehicle_documents` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `vehicle_id` bigint(20) UNSIGNED NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `vehicle_documents`
--

INSERT INTO `vehicle_documents` (`id`, `vehicle_id`, `file_path`, `created_at`, `updated_at`) VALUES
(3, 131, 'vehicle_documents/lwHfr0D20L1O136oAeNAVdo8E5b4PbYAh3kiKbew.pdf', '2025-08-16 07:53:05', '2025-08-16 07:53:05'),
(7, 145, 'vehicle_documents/gjkjyL7JU8O2BMkR31WsEdmKd5bM71JbMgVgrtT1.pdf', '2025-12-09 18:11:10', '2025-12-09 18:11:10');

-- --------------------------------------------------------

--
-- Table structure for table `vehicle_maintenances`
--

CREATE TABLE `vehicle_maintenances` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `vehicle_id` bigint(20) UNSIGNED NOT NULL,
  `maintenance_type` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `urgency` enum('low','normal','high','critical') NOT NULL,
  `status` enum('pending','approved','completed','rejected') NOT NULL DEFAULT 'pending',
  `request_by` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `vehicle_maintenances`
--

INSERT INTO `vehicle_maintenances` (`id`, `vehicle_id`, `maintenance_type`, `description`, `urgency`, `status`, `request_by`, `created_at`, `updated_at`) VALUES
(3, 145, 'accident', 'test', 'low', 'pending', '31', '2025-12-09 18:34:18', '2025-12-09 18:34:18'),
(18, 140, 'service', 'test', 'low', 'pending', '31', '2025-12-14 20:19:49', '2025-12-14 20:19:49');

-- --------------------------------------------------------

--
-- Table structure for table `vehicle_maintenances_report`
--

CREATE TABLE `vehicle_maintenances_report` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `vehicle_id` bigint(20) UNSIGNED NOT NULL,
  `maintenance_type` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `urgency` varchar(255) DEFAULT NULL,
  `status` varchar(255) NOT NULL DEFAULT 'pending',
  `request_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `vehicle_maintenances_report`
--

INSERT INTO `vehicle_maintenances_report` (`id`, `vehicle_id`, `maintenance_type`, `description`, `urgency`, `status`, `request_by`, `created_at`, `updated_at`) VALUES
(1, 137, 'service', 'test', 'low', 'completed', '31', '2025-12-09 18:03:32', '2025-12-09 18:04:58'),
(2, 137, 'accident', 'test', 'low', 'approved', '31', '2025-12-09 18:13:00', '2025-12-09 18:28:29'),
(3, 145, 'accident', 'test', 'low', 'pending', '31', '2025-12-09 18:34:18', '2025-12-09 18:34:18');

-- --------------------------------------------------------

--
-- Table structure for table `vehicle_replacements`
--

CREATE TABLE `vehicle_replacements` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `vehicle_id` bigint(20) UNSIGNED NOT NULL,
  `reason` varchar(255) NOT NULL,
  `replacement_period` varchar(255) NOT NULL,
  `notes` text DEFAULT NULL,
  `status` varchar(255) NOT NULL DEFAULT 'pending',
  `replacement_vehicle` varchar(255) DEFAULT NULL,
  `request_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `vehicle_replacements`
--

INSERT INTO `vehicle_replacements` (`id`, `vehicle_id`, `reason`, `replacement_period`, `notes`, `status`, `replacement_vehicle`, `request_by`, `created_at`, `updated_at`) VALUES
(1, 137, 'breakdown', 'temporary', 'test', 'completed', '140', 31, '2025-12-09 18:36:30', '2025-12-11 20:10:30'),
(2, 137, 'breakdown', 'permanent', 'test', 'approved', '140', NULL, '2025-12-14 21:05:58', '2025-12-14 21:06:12');

-- --------------------------------------------------------

--
-- Table structure for table `vehicle_replacement_approvals`
--

CREATE TABLE `vehicle_replacement_approvals` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `replacement_id` bigint(20) UNSIGNED NOT NULL,
  `replacement_vehicle` bigint(20) UNSIGNED DEFAULT NULL,
  `replacement_period` enum('temporary','permanent') NOT NULL,
  `expected_return_date` date DEFAULT NULL,
  `approval_notes` text DEFAULT NULL,
  `approved_by` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `vehicle_replacement_approvals`
--

INSERT INTO `vehicle_replacement_approvals` (`id`, `replacement_id`, `replacement_vehicle`, `replacement_period`, `expected_return_date`, `approval_notes`, `approved_by`, `created_at`, `updated_at`) VALUES
(1, 1, NULL, 'permanent', NULL, 'test', 'Zain', '2025-12-09 18:36:52', '2025-12-09 18:36:52'),
(2, 2, NULL, 'permanent', NULL, 'test', 'Zain', '2025-12-14 21:06:12', '2025-12-14 21:06:12');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accident_reports`
--
ALTER TABLE `accident_reports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accident_reports_driver_id_foreign` (`driver_id`),
  ADD KEY `accident_reports_vehicle_id_foreign` (`vehicle_id`),
  ADD KEY `accident_reports_vehicle_maintenance_id_foreign` (`vehicle_maintenance_id`),
  ADD KEY `accident_reports_vehicle_replacement_id_foreign` (`vehicle_replacement_id`),
  ADD KEY `accident_reports_created_by_foreign` (`created_by`);

--
-- Indexes for table `amount_transfers`
--
ALTER TABLE `amount_transfers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `amount_transfers_superviser_id_foreign` (`supervisor_id`),
  ADD KEY `amount_transfers_created_by_foreign` (`created_by`),
  ADD KEY `amount_transfers_branch_id_foreign` (`branch_id`);

--
-- Indexes for table `assign_drivers`
--
ALTER TABLE `assign_drivers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `assign_drivers_vehicle_id_foreign` (`vehicle_id`),
  ADD KEY `assign_drivers_driver_id_foreign` (`driver_id`);

--
-- Indexes for table `assign_driver_reports`
--
ALTER TABLE `assign_driver_reports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `assign_driver_reports_vehicle_id_foreign` (`vehicle_id`),
  ADD KEY `assign_driver_reports_driver_id_foreign` (`driver_id`);

--
-- Indexes for table `booklets`
--
ALTER TABLE `booklets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `branches`
--
ALTER TABLE `branches`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `businesses`
--
ALTER TABLE `businesses`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `business_coordinator_report`
--
ALTER TABLE `business_coordinator_report`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `business_ids`
--
ALTER TABLE `business_ids`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `business_ids_business_id_value_unique` (`business_id`,`value`);

--
-- Indexes for table `cache`
--
ALTER TABLE `cache`
  ADD PRIMARY KEY (`key`);

--
-- Indexes for table `cache_locks`
--
ALTER TABLE `cache_locks`
  ADD PRIMARY KEY (`key`);

--
-- Indexes for table `coordinator_reports`
--
ALTER TABLE `coordinator_reports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `coordinator_reports_branch_id_foreign` (`branch_id`);

--
-- Indexes for table `coordinator_report_field_values`
--
ALTER TABLE `coordinator_report_field_values`
  ADD PRIMARY KEY (`id`),
  ADD KEY `coordinator_report_field_values_business_id_value_foreign` (`business_id_value`);

--
-- Indexes for table `countries`
--
ALTER TABLE `countries`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `designations`
--
ALTER TABLE `designations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dobs_user`
--
ALTER TABLE `dobs_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `drivers`
--
ALTER TABLE `drivers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `iqaama_number` (`iqaama_number`),
  ADD KEY `drivers_branch_id_foreign` (`branch_id`),
  ADD KEY `drivers_driver_type_id_foreign` (`driver_type_id`);

--
-- Indexes for table `driver_attendances`
--
ALTER TABLE `driver_attendances`
  ADD PRIMARY KEY (`id`),
  ADD KEY `driver_attendances_branch_id_foreign` (`branch_id`);

--
-- Indexes for table `driver_business_ids`
--
ALTER TABLE `driver_business_ids`
  ADD PRIMARY KEY (`id`),
  ADD KEY `driver_business_ids_previous_driver_id_foreign` (`previous_driver_id`),
  ADD KEY `driver_business_ids_business_id_id_assigned_at_index` (`business_id_id`,`assigned_at`),
  ADD KEY `driver_business_ids_driver_id_transferred_at_index` (`driver_id`,`transferred_at`);

--
-- Indexes for table `driver_calculations`
--
ALTER TABLE `driver_calculations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `driver_calculations_business_id_foreign` (`business_id`);

--
-- Indexes for table `driver_devices`
--
ALTER TABLE `driver_devices`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `driver_differences`
--
ALTER TABLE `driver_differences`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `driver_receipts`
--
ALTER TABLE `driver_receipts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `driver_receipts_driver_id_foreign` (`driver_id`),
  ADD KEY `driver_receipts_business_id_foreign` (`business_id`),
  ADD KEY `driver_receipts_business_id_value_foreign` (`business_id_value`);

--
-- Indexes for table `driver_types`
--
ALTER TABLE `driver_types`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employment_types`
--
ALTER TABLE `employment_types`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `failed_jobs_uuid_unique` (`uuid`);

--
-- Indexes for table `fields`
--
ALTER TABLE `fields`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fuels`
--
ALTER TABLE `fuels`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fuels_vehicle_id_foreign` (`vehicle_id`),
  ADD KEY `fuels_requested_by_foreign` (`requested_by`),
  ADD KEY `fuels_requested_by_user_foreign` (`requested_by_user`),
  ADD KEY `fuels_accepted_by_foreign` (`accepted_by`);

--
-- Indexes for table `fuel_expenses`
--
ALTER TABLE `fuel_expenses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fuel_expenses_vehicle_id_foreign` (`vehicle_id`);

--
-- Indexes for table `fuel_requests`
--
ALTER TABLE `fuel_requests`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fuel_request_approvals`
--
ALTER TABLE `fuel_request_approvals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fuel_request_approvals_fuel_id_foreign` (`fuel_id`),
  ADD KEY `fuel_request_approvals_approved_by_foreign` (`approved_by`);

--
-- Indexes for table `fuel_request_rejects`
--
ALTER TABLE `fuel_request_rejects`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fuel_request_rejects_fuel_id_foreign` (`fuel_id`);

--
-- Indexes for table `import_logs`
--
ALTER TABLE `import_logs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jobs_queue_index` (`queue`);

--
-- Indexes for table `job_batches`
--
ALTER TABLE `job_batches`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `languages`
--
ALTER TABLE `languages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `maintenance_approvals`
--
ALTER TABLE `maintenance_approvals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `maintenance_approvals_maintenance_id_foreign` (`maintenance_id`);

--
-- Indexes for table `maintenance_rejections`
--
ALTER TABLE `maintenance_rejections`
  ADD PRIMARY KEY (`id`),
  ADD KEY `maintenance_rejections_maintenance_id_foreign` (`maintenance_id`);

--
-- Indexes for table `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `modules`
--
ALTER TABLE `modules`
  ADD PRIMARY KEY (`id`),
  ADD KEY `modules_parent_id_foreign` (`parent_id`);

--
-- Indexes for table `offboarding`
--
ALTER TABLE `offboarding`
  ADD PRIMARY KEY (`id`),
  ADD KEY `driver_id` (`driver_id`),
  ADD KEY `requested_by_id` (`requested_by_id`);

--
-- Indexes for table `operation_superviser_differences`
--
ALTER TABLE `operation_superviser_differences`
  ADD PRIMARY KEY (`id`),
  ADD KEY `operation_superviser_differences_superviser_id_foreign` (`superviser_id`),
  ADD KEY `operation_superviser_differences_created_by_foreign` (`created_by`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `orders_business_id_id_foreign` (`business_id_id`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `penalties`
--
ALTER TABLE `penalties`
  ADD PRIMARY KEY (`id`),
  ADD KEY `penalties_driver_id_foreign` (`driver_id`),
  ADD KEY `penalties_business_id_foreign` (`business_id`),
  ADD KEY `penalties_business_id_value_foreign` (`business_id_value`),
  ADD KEY `penalties_coordinator_report_id_foreign` (`coordinator_report_id`);

--
-- Indexes for table `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `personal_access_tokens_token_unique` (`token`),
  ADD KEY `personal_access_tokens_tokenable_type_tokenable_id_index` (`tokenable_type`,`tokenable_id`);

--
-- Indexes for table `privileges`
--
ALTER TABLE `privileges`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `recharges`
--
ALTER TABLE `recharges`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `replacement_rejections`
--
ALTER TABLE `replacement_rejections`
  ADD PRIMARY KEY (`id`),
  ADD KEY `replacement_rejections_replacement_id_foreign` (`replacement_id`);

--
-- Indexes for table `request_recharges`
--
ALTER TABLE `request_recharges`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sessions_user_id_index` (`user_id`),
  ADD KEY `sessions_last_activity_index` (`last_activity`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `users_designation_id_foreign` (`designation_id`),
  ADD KEY `users_department_id_foreign` (`department_id`),
  ADD KEY `users_role_id_foreign` (`role_id`),
  ADD KEY `users_employment_type_id_foreign` (`employment_type_id`),
  ADD KEY `users_branch_id_foreign` (`branch_id`),
  ADD KEY `users_country_id_foreign` (`country_id`),
  ADD KEY `users_language_id_foreign` (`language_id`),
  ADD KEY `users_reporting_to_foreign` (`reporting_to`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `vehicles_registration_number_unique` (`registration_number`),
  ADD UNIQUE KEY `vehicles_vin_unique` (`vin`);

--
-- Indexes for table `vehicle_documents`
--
ALTER TABLE `vehicle_documents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vehicle_documents_vehicle_id_foreign` (`vehicle_id`);

--
-- Indexes for table `vehicle_maintenances`
--
ALTER TABLE `vehicle_maintenances`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vehicle_maintenances_vehicle_id_foreign` (`vehicle_id`);

--
-- Indexes for table `vehicle_maintenances_report`
--
ALTER TABLE `vehicle_maintenances_report`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_vehicle_maintenances_report_id` (`id`),
  ADD KEY `vehicle_maintenances_report_vehicle_id_foreign` (`vehicle_id`);

--
-- Indexes for table `vehicle_replacements`
--
ALTER TABLE `vehicle_replacements`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vehicle_replacements_vehicle_id_foreign` (`vehicle_id`);

--
-- Indexes for table `vehicle_replacement_approvals`
--
ALTER TABLE `vehicle_replacement_approvals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vehicle_replacement_approvals_replacement_id_foreign` (`replacement_id`),
  ADD KEY `vehicle_replacement_approvals_replacement_vehicle_foreign` (`replacement_vehicle`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accident_reports`
--
ALTER TABLE `accident_reports`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `amount_transfers`
--
ALTER TABLE `amount_transfers`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `assign_drivers`
--
ALTER TABLE `assign_drivers`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `assign_driver_reports`
--
ALTER TABLE `assign_driver_reports`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `booklets`
--
ALTER TABLE `booklets`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `branches`
--
ALTER TABLE `branches`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `businesses`
--
ALTER TABLE `businesses`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `business_coordinator_report`
--
ALTER TABLE `business_coordinator_report`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=144;

--
-- AUTO_INCREMENT for table `business_ids`
--
ALTER TABLE `business_ids`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `coordinator_reports`
--
ALTER TABLE `coordinator_reports`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=112;

--
-- AUTO_INCREMENT for table `coordinator_report_field_values`
--
ALTER TABLE `coordinator_report_field_values`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=862;

--
-- AUTO_INCREMENT for table `countries`
--
ALTER TABLE `countries`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=244;

--
-- AUTO_INCREMENT for table `departments`
--
ALTER TABLE `departments`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `designations`
--
ALTER TABLE `designations`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `dobs_user`
--
ALTER TABLE `dobs_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `drivers`
--
ALTER TABLE `drivers`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=239;

--
-- AUTO_INCREMENT for table `driver_attendances`
--
ALTER TABLE `driver_attendances`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `driver_business_ids`
--
ALTER TABLE `driver_business_ids`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `driver_calculations`
--
ALTER TABLE `driver_calculations`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `driver_devices`
--
ALTER TABLE `driver_devices`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `driver_differences`
--
ALTER TABLE `driver_differences`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `driver_receipts`
--
ALTER TABLE `driver_receipts`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `driver_types`
--
ALTER TABLE `driver_types`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `employment_types`
--
ALTER TABLE `employment_types`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fields`
--
ALTER TABLE `fields`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `fuels`
--
ALTER TABLE `fuels`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT for table `fuel_expenses`
--
ALTER TABLE `fuel_expenses`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `fuel_requests`
--
ALTER TABLE `fuel_requests`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fuel_request_approvals`
--
ALTER TABLE `fuel_request_approvals`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `fuel_request_rejects`
--
ALTER TABLE `fuel_request_rejects`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `import_logs`
--
ALTER TABLE `import_logs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `languages`
--
ALTER TABLE `languages`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=185;

--
-- AUTO_INCREMENT for table `maintenance_approvals`
--
ALTER TABLE `maintenance_approvals`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `maintenance_rejections`
--
ALTER TABLE `maintenance_rejections`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT for table `modules`
--
ALTER TABLE `modules`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `offboarding`
--
ALTER TABLE `offboarding`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `operation_superviser_differences`
--
ALTER TABLE `operation_superviser_differences`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=95;

--
-- AUTO_INCREMENT for table `penalties`
--
ALTER TABLE `penalties`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=119;

--
-- AUTO_INCREMENT for table `privileges`
--
ALTER TABLE `privileges`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=367;

--
-- AUTO_INCREMENT for table `recharges`
--
ALTER TABLE `recharges`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `replacement_rejections`
--
ALTER TABLE `replacement_rejections`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `request_recharges`
--
ALTER TABLE `request_recharges`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=147;

--
-- AUTO_INCREMENT for table `vehicle_documents`
--
ALTER TABLE `vehicle_documents`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `vehicle_maintenances`
--
ALTER TABLE `vehicle_maintenances`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `vehicle_maintenances_report`
--
ALTER TABLE `vehicle_maintenances_report`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `vehicle_replacements`
--
ALTER TABLE `vehicle_replacements`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `vehicle_replacement_approvals`
--
ALTER TABLE `vehicle_replacement_approvals`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accident_reports`
--
ALTER TABLE `accident_reports`
  ADD CONSTRAINT `accident_reports_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `accident_reports_driver_id_foreign` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `accident_reports_vehicle_id_foreign` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `accident_reports_vehicle_maintenance_id_foreign` FOREIGN KEY (`vehicle_maintenance_id`) REFERENCES `vehicle_maintenances` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `accident_reports_vehicle_replacement_id_foreign` FOREIGN KEY (`vehicle_replacement_id`) REFERENCES `vehicle_replacements` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `amount_transfers`
--
ALTER TABLE `amount_transfers`
  ADD CONSTRAINT `amount_transfers_branch_id_foreign` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  ADD CONSTRAINT `amount_transfers_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `amount_transfers_superviser_id_foreign` FOREIGN KEY (`supervisor_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `assign_drivers`
--
ALTER TABLE `assign_drivers`
  ADD CONSTRAINT `assign_drivers_driver_id_foreign` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `assign_drivers_vehicle_id_foreign` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `assign_driver_reports`
--
ALTER TABLE `assign_driver_reports`
  ADD CONSTRAINT `assign_driver_reports_driver_id_foreign` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `assign_driver_reports_vehicle_id_foreign` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `business_ids`
--
ALTER TABLE `business_ids`
  ADD CONSTRAINT `business_ids_business_id_foreign` FOREIGN KEY (`business_id`) REFERENCES `businesses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `coordinator_reports`
--
ALTER TABLE `coordinator_reports`
  ADD CONSTRAINT `coordinator_reports_branch_id_foreign` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`);

--
-- Constraints for table `coordinator_report_field_values`
--
ALTER TABLE `coordinator_report_field_values`
  ADD CONSTRAINT `coordinator_report_field_values_business_id_value_foreign` FOREIGN KEY (`business_id_value`) REFERENCES `business_ids` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `drivers`
--
ALTER TABLE `drivers`
  ADD CONSTRAINT `drivers_branch_id_foreign` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  ADD CONSTRAINT `drivers_driver_type_id_foreign` FOREIGN KEY (`driver_type_id`) REFERENCES `driver_types` (`id`);

--
-- Constraints for table `driver_attendances`
--
ALTER TABLE `driver_attendances`
  ADD CONSTRAINT `driver_attendances_branch_id_foreign` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `driver_business_ids`
--
ALTER TABLE `driver_business_ids`
  ADD CONSTRAINT `driver_business_ids_business_id_id_foreign` FOREIGN KEY (`business_id_id`) REFERENCES `business_ids` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `driver_business_ids_driver_id_foreign` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `driver_business_ids_previous_driver_id_foreign` FOREIGN KEY (`previous_driver_id`) REFERENCES `drivers` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `driver_calculations`
--
ALTER TABLE `driver_calculations`
  ADD CONSTRAINT `driver_calculations_business_id_foreign` FOREIGN KEY (`business_id`) REFERENCES `businesses` (`id`);

--
-- Constraints for table `driver_receipts`
--
ALTER TABLE `driver_receipts`
  ADD CONSTRAINT `driver_receipts_business_id_foreign` FOREIGN KEY (`business_id`) REFERENCES `businesses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `driver_receipts_business_id_value_foreign` FOREIGN KEY (`business_id_value`) REFERENCES `business_ids` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `driver_receipts_driver_id_foreign` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `fuels`
--
ALTER TABLE `fuels`
  ADD CONSTRAINT `fuels_accepted_by_foreign` FOREIGN KEY (`accepted_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fuels_requested_by_foreign` FOREIGN KEY (`requested_by`) REFERENCES `drivers` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fuels_requested_by_user_foreign` FOREIGN KEY (`requested_by_user`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fuels_vehicle_id_foreign` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `fuel_expenses`
--
ALTER TABLE `fuel_expenses`
  ADD CONSTRAINT `fuel_expenses_vehicle_id_foreign` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `fuel_request_approvals`
--
ALTER TABLE `fuel_request_approvals`
  ADD CONSTRAINT `fuel_request_approvals_approved_by_foreign` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fuel_request_approvals_fuel_id_foreign` FOREIGN KEY (`fuel_id`) REFERENCES `fuels` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `fuel_request_rejects`
--
ALTER TABLE `fuel_request_rejects`
  ADD CONSTRAINT `fuel_request_rejects_fuel_id_foreign` FOREIGN KEY (`fuel_id`) REFERENCES `fuels` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `maintenance_approvals`
--
ALTER TABLE `maintenance_approvals`
  ADD CONSTRAINT `maintenance_approvals_maintenance_id_foreign` FOREIGN KEY (`maintenance_id`) REFERENCES `vehicle_maintenances` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `maintenance_rejections`
--
ALTER TABLE `maintenance_rejections`
  ADD CONSTRAINT `maintenance_rejections_maintenance_id_foreign` FOREIGN KEY (`maintenance_id`) REFERENCES `vehicle_maintenances` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `modules`
--
ALTER TABLE `modules`
  ADD CONSTRAINT `modules_parent_id_foreign` FOREIGN KEY (`parent_id`) REFERENCES `modules` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `operation_superviser_differences`
--
ALTER TABLE `operation_superviser_differences`
  ADD CONSTRAINT `operation_superviser_differences_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `operation_superviser_differences_superviser_id_foreign` FOREIGN KEY (`superviser_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `penalties`
--
ALTER TABLE `penalties`
  ADD CONSTRAINT `penalties_business_id_foreign` FOREIGN KEY (`business_id`) REFERENCES `businesses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `penalties_business_id_value_foreign` FOREIGN KEY (`business_id_value`) REFERENCES `business_ids` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `penalties_coordinator_report_id_foreign` FOREIGN KEY (`coordinator_report_id`) REFERENCES `coordinator_reports` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `penalties_driver_id_foreign` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `replacement_rejections`
--
ALTER TABLE `replacement_rejections`
  ADD CONSTRAINT `replacement_rejections_replacement_id_foreign` FOREIGN KEY (`replacement_id`) REFERENCES `vehicle_replacements` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_branch_id_foreign` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  ADD CONSTRAINT `users_country_id_foreign` FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`),
  ADD CONSTRAINT `users_department_id_foreign` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`),
  ADD CONSTRAINT `users_designation_id_foreign` FOREIGN KEY (`designation_id`) REFERENCES `designations` (`id`),
  ADD CONSTRAINT `users_employment_type_id_foreign` FOREIGN KEY (`employment_type_id`) REFERENCES `employment_types` (`id`),
  ADD CONSTRAINT `users_language_id_foreign` FOREIGN KEY (`language_id`) REFERENCES `languages` (`id`),
  ADD CONSTRAINT `users_reporting_to_foreign` FOREIGN KEY (`reporting_to`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `users_role_id_foreign` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

--
-- Constraints for table `vehicle_documents`
--
ALTER TABLE `vehicle_documents`
  ADD CONSTRAINT `vehicle_documents_vehicle_id_foreign` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `vehicle_maintenances`
--
ALTER TABLE `vehicle_maintenances`
  ADD CONSTRAINT `vehicle_maintenances_vehicle_id_foreign` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `vehicle_maintenances_report`
--
ALTER TABLE `vehicle_maintenances_report`
  ADD CONSTRAINT `vehicle_maintenances_report_vehicle_id_foreign` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `vehicle_replacements`
--
ALTER TABLE `vehicle_replacements`
  ADD CONSTRAINT `vehicle_replacements_vehicle_id_foreign` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `vehicle_replacement_approvals`
--
ALTER TABLE `vehicle_replacement_approvals`
  ADD CONSTRAINT `vehicle_replacement_approvals_replacement_id_foreign` FOREIGN KEY (`replacement_id`) REFERENCES `vehicle_replacements` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `vehicle_replacement_approvals_replacement_vehicle_foreign` FOREIGN KEY (`replacement_vehicle`) REFERENCES `vehicles` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
