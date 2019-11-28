# Welcome to Tabib Web Repository 

## General Info

 -  current version : 0.9B 
 - Language : python 3.7
 - Framework : Django 2.2
 - Part of a graduation project
 - no for real use for now 

## How to install

 1. Install python 3.7 (or any latest version ) from [here](https://www.python.org/)
 2. Install any editor you want (I use Visual studio Code )
 3. Download the Repository
 4. Install all this required module
	 -  Django v2.2
	 -  django-filter
	 -  djangorestframework
	 -  djangorestframework-simplejwt
	 -  Markdown
	 -  mysqlclient (if you will use mysql)
5. Download postman (preferred)
6. Now you are ready to real work

## Configuration
### Database configuration
To make this project ready to work with you need to configure the **database** setting
and this can be done in very easy steps.

in ./Web-Repo/Tabib/setting.py

    DATABASES = {
	    'default' : {
		    'ENGINE': 'django.db.backends.mysql', #database provider
		    'NAME': '',
		    'USER' : '',
		    'PASSWORD': '',
		    'HOST':'',
		    'PORT':''
		    }
	}

 1. **Engine** : use  the database provider you want to use  here we use MySql database  if 				   you just leave this line as it
 2. **Name**  : Write the database name you will use **(important to create the database first django will not create it for you)**
 3. **USER** :  the server username 
 4. **PASSWORD** : server password
 5.  **HOST** : host url **( could be localhost if you will use it locally )**
 6. **PORT** : whatever the port you will use

now you will need couple of steps to finish

  First make migration by this command
  

    python manage.py makemigrations

 Second apply this migration
 

    python manage.py migrate

 by finishing to this two steps you are now read to use the project and be ready to coding 

make sure to create superuser by run this command

    python manage.py createsuperuser
to access all data and mange use this url `admin/` use the username and password that you have just create 

## How to use
By the time you read this document there is only this apps

 - accounts
	 - Registration
	 - Login

you need to run server to see a live version by this command

    python manage.py runserver

### accounts
 - **Registration**
to create new user
	- go to this url  `/api/accounts/register/`
	- if you will use the **browser** you will see something like a general form that you could see in any website just insert data in empty fields then  click **post** 
	- if you will use **postman** you will need more little steps 
		-  first make request of type **POST**
		-  Select **Body**  
		-  Select raw --> JSON
		- write this **JSON** file 

			    {
				    "email" : "",
				    "password : "",
				    "confpassword" : "",
				    "username" : "",
				    "profile": {
					    "phone" : "",
					    "gender" : "",
					    "country" : "",
					    "city" : "",
					    "weight" : "",
					    "height" : ""
					 }
				}
		- fill this empty places with the data you want
		- If your request complete and registration done you will receive **201 Created  status** with the same date you send
		- If your registration failed you will receive **400 Bad Request status** with some validation error to know reason for failed some thing like that
		
			   {
				 "email":[
						"This email has already registered"
				     ],
			   }

- **Login**
	-  from this point  i will use **postman only** 
	- go to this url `/api/accounts/login/`
	- make request of type **POST**
	-  Select **Body**  
	-  Select raw --> JSON
	- write this **JSON** file 
	
	        {
		        "email" : "",
		        "password" : ""
		    }
	- fill this empty places with the data you want
	- If your request complete and registration done you will receive **200 OK status** with token and some data about the user

		    {
			    "refresh" : "refresh token",
			    "access" : "access token",
			    "User" : {
				    "name" : "username",
				    "email" : "user email"
				  }
			}
		 
	- If your registration failed you will receive **400 Bad Request status**

 


## To Do
- list of next to make
