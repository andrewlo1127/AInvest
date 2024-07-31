-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024 年 07 月 27 日 15:54
-- 伺服器版本： 10.4.24-MariaDB
-- PHP 版本： 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `專題`
--

-- --------------------------------------------------------

--
-- 資料表結構 `code`
--

CREATE TABLE `code` (
  `code_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `strategy` text NOT NULL COMMENT '策略名稱',
  `FileName` text NOT NULL COMMENT '檔案名稱',
  `public` tinyint(1) NOT NULL COMMENT '0不公開/1公開',
  `description` text NOT NULL COMMENT '策略描述'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 資料表結構 `members`
--

CREATE TABLE `members` (
  `m_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` text NOT NULL,
  `userbot_api` text NOT NULL,
  `temp_code` text NOT NULL COMMENT '暫存聊天機器人輸出的code'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 傾印資料表的資料 `members`
--

INSERT INTO `members` (`m_id`, `name`, `email`, `password`, `userbot_api`, `temp_code`) VALUES
(3, '然', '1@gmail.com', '', '', '');

-- --------------------------------------------------------

--
-- 資料表結構 `target`
--

CREATE TABLE `target` (
  `t_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `target_id` text NOT NULL COMMENT '標的代號'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 資料表結構 `test_body`
--

CREATE TABLE `test_body` (
  `tb_id` int(11) NOT NULL,
  `th_id` int(11) NOT NULL COMMENT 'test_head',
  `enter_date` int(11) NOT NULL COMMENT '進場日期',
  `exit_date` int(11) NOT NULL COMMENT '出場日期',
  `enter_price` int(11) NOT NULL COMMENT '進場價格',
  `exit_price` int(11) NOT NULL COMMENT '出場價格',
  `size` tinyint(1) NOT NULL COMMENT '張數',
  `profit` int(11) NOT NULL COMMENT '獲利',
  `profit_margin` float NOT NULL COMMENT '獲利率'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 資料表結構 `test_head`
--

CREATE TABLE `test_head` (
  `th_id` int(11) NOT NULL,
  `code_id` int(11) NOT NULL,
  `target_name` varchar(10) NOT NULL,
  `times` int(11) NOT NULL COMMENT '次數',
  `sucess_p` float NOT NULL COMMENT '勝率',
  `acc_profit` float NOT NULL COMMENT '累積獲利',
  `acc_profit_margin` float NOT NULL COMMENT '累積獲利率',
  `enter_time` date NOT NULL COMMENT '進場時間',
  `exit_time` date NOT NULL COMMENT '出場時間',
  `continue_time` int(11) NOT NULL COMMENT '持續持間(天)',
  `buy_and_hold_return` float NOT NULL COMMENT '買入並持有報酬[%]',
  `html` text NOT NULL COMMENT '檔案名稱'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `code`
--
ALTER TABLE `code`
  ADD PRIMARY KEY (`code_id`),
  ADD KEY `member_id` (`member_id`);

--
-- 資料表索引 `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`m_id`);

--
-- 資料表索引 `target`
--
ALTER TABLE `target`
  ADD PRIMARY KEY (`t_id`),
  ADD KEY `fk_target_member` (`member_id`);

--
-- 資料表索引 `test_body`
--
ALTER TABLE `test_body`
  ADD PRIMARY KEY (`tb_id`),
  ADD KEY `fk_test_body_head` (`th_id`);

--
-- 資料表索引 `test_head`
--
ALTER TABLE `test_head`
  ADD PRIMARY KEY (`th_id`),
  ADD KEY `fk_test_head_code` (`code_id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `code`
--
ALTER TABLE `code`
  MODIFY `code_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `members`
--
ALTER TABLE `members`
  MODIFY `m_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `target`
--
ALTER TABLE `target`
  MODIFY `t_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `test_body`
--
ALTER TABLE `test_body`
  MODIFY `tb_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `test_head`
--
ALTER TABLE `test_head`
  MODIFY `th_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `code`
--
ALTER TABLE `code`
  ADD CONSTRAINT `fk_code_member` FOREIGN KEY (`member_id`) REFERENCES `members` (`m_id`);

--
-- 資料表的限制式 `target`
--
ALTER TABLE `target`
  ADD CONSTRAINT `fk_target_member` FOREIGN KEY (`member_id`) REFERENCES `members` (`m_id`);

--
-- 資料表的限制式 `test_body`
--
ALTER TABLE `test_body`
  ADD CONSTRAINT `fk_test_body_head` FOREIGN KEY (`th_id`) REFERENCES `test_head` (`th_id`);

--
-- 資料表的限制式 `test_head`
--
ALTER TABLE `test_head`
  ADD CONSTRAINT `fk_test_head_code` FOREIGN KEY (`code_id`) REFERENCES `code` (`code_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
