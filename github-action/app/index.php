<!DOCTYPE html>
<html>
<head>
    <title>To-do list</title>
</head>
<body>
    <h1>To-do list</h1>
    <ul>
        <?php
        require_once('Task.php');

        $task1 = new Task('Grocery shopping');
        $task2 = new Task('Respond to emails');

        $tasks = [$task1, $task2];

        foreach ($tasks as $task) {
            echo '<li>' . $task->getDescription() . '</li>';
        }
        ?>
    </ul>
</body>
</html>
