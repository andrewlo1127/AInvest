<?php
// 引入配置文件
include 'config.php';

// 查詢會員資料
$sql = "SELECT name, email FROM members WHERE m_id = 3"; // 假設您要查詢會員ID為1的資料
$result = $conn->query($sql);

$member = null;
if ($result->num_rows > 0) {
    // 輸出每行資料
    $member = $result->fetch_assoc();
} else {
    echo "沒有找到會員資料";
}
$conn->close();
?>


<!DOCTYPE html>
<html lang="zh-TW">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>會員資訊</title>
    <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 500px;
            margin: 40px auto;
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.7);
        }

        h1 {
            color: #e0e0e0;
            text-align: center;
            font-size: 28px;
            margin-bottom: 20px;
        }

        .member-info {
            margin-bottom: 20px;
        }

        .member-info p {
            margin: 12px 0;
            font-size: 16px;
        }

        .member-info strong {
            color: #bb86fc;
        }

        .button {
            display: block;
            width: 100%;
            padding: 12px;
            background-color: #bb86fc;
            color: #121212;
            text-align: center;
            text-decoration: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            border: none;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }

        .button:hover {
            background-color: #8c52fc;
            transform: scale(1.05);
        }

        .button:focus {
            outline: none;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>會員資訊</h1>
        <?php if ($member) : ?>
            <div class="member-info">
                <p><strong>姓名:</strong> <?php echo htmlspecialchars($member['name']); ?></p>
                <p><strong>電子郵件:</strong> <?php echo htmlspecialchars($member['email']); ?></p>
            </div>
        <?php endif; ?>
        <button class="button" onclick="changePassword()">更改密碼</button>
    </div>

    <script>
        function changePassword() {
            // 這裡可以寫更改密碼的功能或跳轉到更改密碼的頁面
            alert('這裡可以添加更改密碼的功能');
        }
    </script>
</body>

</html>