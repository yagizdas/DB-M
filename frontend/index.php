<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registered Users</title>
</head>
<body>
    <h1>User List</h1>
    <ul>
        <?php
        $json = file_get_contents('http://flask_app:4000/users');
        $users = json_decode($json, true);

        if (is_array($users)) {
            foreach ($users as $user) {
                echo "<li>Username: " . htmlspecialchars($user['username']) . "/ Email: " . htmlspecialchars($user['email']) . "/ id: " . htmlspecialchars($user['id']) . "</li>";
            }
        } else {
            echo "<li>ERR: No users found.</li>";
        }
        ?>
    </ul>
    <h2>Upload CSV file</h2>
    <form method= "POST" action="http://localhost:4000/upload" enctype="multipart/form-data">
	<p><input type="file" name="file"></p>
	<p><input type="submit" value="Submit"></p>
    </form>
    <h2>Service Health</h2>
	<?php
	$timing = file_get_contents('http://flask_app:4000/time');
	echo "<h3> Last execution took: " . htmlspecialchars($timing) . " seconds.</h3>";
	?>
</body>
</html>
