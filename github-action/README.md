# CI/CD Pipeline Documentation for PHP Code Deployment via GitHub Actions

## Introduction

This documentation outlines the setup of a CI/CD pipeline using GitHub Actions to automate the PHP code build, test, and deployment process to an FTP destination. The primary goal is to ensure code quality by automating these processes while maintaining the security and robustness of the pipeline.

## GitHub Repository Contents

The final GitHub repository contains:

1. **PHP Code to Deploy**: The PHP code consists of three files, all located in the "app" directory:
    - `index.php`: The entry point of the application containing HTML and PHP code.
    - `Task.php`: The logical part of the application.
    - `tasktest.php`: The file containing unit tests for the application.

2. **GitHub Actions YAML File (`main.yml`)**: A YAML file containing the GitHub Actions workflow configuration.

## Pipeline Configuration

Here's our pipeline configuration:

```yaml
name: Deploy PHP code to an FTP destination

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:

  deploy:
    name: Deploy the application to an FTP destination
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Set up PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: 7.4
      - name: Install PHPUnit
        run: composer require --dev phpunit/phpunit 
      - name: Run tests
        run: |
          vendor/bin/phpunit app/taskTest.php
      - name: Sync files with the hosting
        uses: Samkirkland/FTP-Deploy-Action@4.0.0
        with:
          server: ${{ secrets.FTP_SERVER }}
          username: ${{ secrets.FTP_USERNAME }}
          password: ${{ secrets.FTP_PASSWORD }}
          local-dir: ./app/
```

### Step 1: PHP Code Preparation

- This step is named **Checkout.**
- It uses the `actions/checkout@v3` action to check out the code from the GitHub repository.
- The purpose is to make the code accessible for subsequent steps in the pipeline.

### Step 2: PHP Environment Configuration

- This step is named **Set up PHP.**
- It uses the `shivammathur/setup-php@v2` action to set up and configure PHP.
- Specifically, it configures PHP version 7.4 to ensure that the correct PHP environment is available for later steps in the pipeline.

### Step 3: PHPUnit Installation

- This step is named **Install PHPUnit.**
- It runs the command `composer require --dev phpunit/phpunit` to install PHPUnit as a development dependency.
- PHPUnit is a testing framework for PHP, and installing it is essential for running unit tests on the code.

### Step 4: Running Tests

- This step is named **Run tests.**
- It runs PHPUnit tests using the command `vendor/bin/phpunit app/taskTest.php`.
- The purpose is to execute the unit tests defined in the `taskTest.php` file to ensure that the code passes these tests successfully.

### Step 5: Deployment to FTP Destination

- This step is named **Sync files with the hosting.**
- It uses the `Samkirkland/FTP-Deploy-Action@4.0.0` action to deploy the code to an FTP destination.
- The deployment action requires specific parameters:
  - `server`: This should be a secret containing the FTP server address.
  - `username`: This should be a secret containing the FTP username.
  - `password`: This should be a secret containing the FTP password.
  - `local-dir`: This specifies the local directory from which the code will be deployed (`./app/` in this case).

## Security

- Sensitive information, such as FTP credentials (server, username, and password), is stored as GitHub secrets.
- Secrets provide a secure way to store and access sensitive information required for the pipeline.
- Storing sensitive data directly in the YAML file or a public repository is strongly discouraged to ensure security and protect confidential information.

## Usage

To trigger this pipeline, simply push changes to the `main` branch of the repository or manually trigger the workflow using the "workflow_dispatch" action from the GitHub interface.


