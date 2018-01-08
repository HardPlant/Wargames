<?php
$mysql_hostname = "localhost";
$mysql_user = "root";
$mysql_password = "is119";
$mysql_database = "wordpress";

$conn = mysqli_connect($mysql_hostname, $mysql_user, $mysql_password,$mysql_database) or die("db connect error");


?>
