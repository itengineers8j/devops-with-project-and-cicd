<?php

require_once('Task.php');
use PHPUnit\Framework\TestCase;

class TaskTest extends TestCase {
    public function testTaskDescription() {
        $task = new Task('Grocery shopping');
        $this->assertEquals('Grocery shopping', $task->getDescription());
    }

    public function testTaskCompletion() {
        $task = new Task('Grocery shopping');
        $this->assertFalse($task->isCompleted());

        $task->complete();
        $this->assertTrue($task->isCompleted());
    }
}
