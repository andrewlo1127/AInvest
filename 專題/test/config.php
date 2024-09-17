<?php
// config.php
$servername = "127.0.0.1";
$username = "root";
$password = "";
$dbname = "專題";

// 創建連接
$conn = new mysqli($servername, $username, $password, $dbname);

// 檢查連接
if ($conn->connect_error) {
    die("連接失敗: " . $conn->connect_error);
}
