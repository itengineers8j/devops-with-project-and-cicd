<?php

class Task {
    private $description;
    private $completed = false;

    public function __construct($description) {
        $this->description = $description;
    }

    public function getDescription() {
        return $this->description;
    }

    public function isCompleted() {
        return $this->completed;
    }

    public function complete() {
        $this->completed = true;
    }
}
