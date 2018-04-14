# 9.3best
you already know what it is

# Backend Setup
- Make sure you have python2 installed

### Install Flask
`pip2 install flask-mysqldb`

### Install MySQL

El Capitan (Homebrew)
`https://gist.github.com/nrollr/a8d156206fa1e53c6cd6`

Sierra (Homebrew)
`https://gist.github.com/nrollr/3f57fc15ded7dddddcc4e82fe137b58e`

Download
`https://dev.mysql.com/downloads/mysql/`

### Setup MySQL

In the project directory, run
`cp config.skeleton rollcall.config`

### Setup config

On the line with "mysql_password", enter your root mysql password after the semicolon (leave a space between the semicolon and your password) 
- Same for mysql username (I just used my root and its password)

To test:
- run `python2 app.py`
- go to `http://0.0.0.0:5000` in Chrome

There should be a hello world page
***** Erin's Notes *****
- this will not work unless you create a new database in your mysql, please see notes below 

### To see the database (Erin's added notes)

- run `mysql -u <username> - p
- it will ask for you password

- If you get an error, try running `mysql.server start` and then try again 

-Once mysql is running: 
	`create database rollcall;`
	`show databases;`
- You should now see roll call listed in your databases
- Add rollcall as the databse name in rollcall.config