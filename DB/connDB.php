<?php

	$servername = "localhost"; // Servername
	$username = "u824500046_fyp"; // Server Username
	$password = "shing4848"; // Server Password
	$dbname = "u824500046_fyp"; // Database Name

	// Create connection
	$conn = mysqli_connect($servername, $username, $password, $dbname);
	
	// Check connection
	if (!$conn) {
		die("Connection failed: " . mysqli_connect_error());
	}
?>