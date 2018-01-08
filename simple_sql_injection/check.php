<?php
include("config.php");
if(mysqli_connect_errno()) {echo "Failed to connect to MySQL: " . mysqli_connect_error();}
if($conn == null) {echo "connection is null";}
$myusername=$_POST["username"];
$mypassword=$_POST["password"];

if(strpos($myusername, "'1'") !== false){
	$myusername=' ';
}
if(strpos($mypassword, "'1'") !== false){
	$mypassword=' ';
}
if(strpos($myusername, "'a'") !== false){
	$myusername=' ';
}

$sql = "SELECT user_login, user_pass, user_email
        FROM wp_users
        WHERE user_login='$myusername' and user_pass='$mypassword'";
$result=mysqli_query($conn, $sql);
?>

<html>

<head>
    <meta http-equiv="Content-Type" content="text/html" charset="utf-8">
    <title>Simple Login Page</title>
</head>
<body>
    <?php

    if(mysqli_num_rows($result) == 0){echo "<center>Login Failed.</center>";}
    else{
        while($str = mysqli_fetch_array($result)){
            echo "
                $str[user_login],
                $str[user_pass],
                $str[user_email]<br>
            ";
        }
    }

    ?>
</body>

</html>
