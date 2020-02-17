# Welcome to Tabib Web Repository 

## General Info

 - Current version : v1.0(Beta) 
 - Language : python v3.7
 - Framework : Django v2.2
 - Part of a graduation project 

## How to install

 1. Install Python v3.7 (or any latest version) from [here](https://www.python.org/)
 2. Install any editor you want (I use Visual studio Code )
 3. Clone the Repository
 4. Install all of the required dependencies with command (pip install -r requirements.txt):
	 -  Django v2.2
	 -  django-filter
	 -  djangorestframework
	 -  djangorestframework-simplejwt
	 -  Markdown
	 -  mysqlclient (if you will use mysql)
5. Download Postman (preferred)

## Configuration
### Database configuration
To make this project ready to work with you need to configure the **database** setting
and this can be done in the following easy steps.

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

 1. **Engine** : Specify the database engine you wanna use. We use MySQL database.
 2. **Name**  : Write the database name you will use **(It's important to create the database first, Django won't create it for you)**
 3. **USER** :  the server username 
 4. **PASSWORD** : the server password
 5.  **HOST** : host url **(could be localhost on dev mode)**
 6. **PORT** : Specify the port you'd use here


**Now you'd need couple of steps to finish:**

  First, make the initial migration by the following commands: 

    python manage.py makemigrations
    python manage.py migrate

 Now you're ready to start the application, now we need to make sure there's a super account created:

    python manage.py createsuperuser

To access all data and manage GO to this URL followed by /admin/ path 
`http://whatever-url(would be localhost:8000 on dev mode)/admin/`  
Use the username and password that you have just created above

---

## How to use
The project for now only contains one app(the Registration & Login functionality), we'll continue to add to it in the future.

 - accounts
	 - Registration
	 - Login

You need to run the server to be able to see the app, run this command: 

    python manage.py runserver

### accounts
 - **Registration**
To create new user
	- Go to this URL `(http://whatever-url(localhost):portHERE)/api/accounts/register/`
	- If you will use the **browser** you will see something like any general form you've seen in previous websites. Just insert the data in empty fields/inputs and click **POST** 
	- If you gonna use **Postman** you'd few other steps: 
		-  First specify a request of type **POST**
		-  Select **Body** tab  
		-  Select raw --> JSON
		-  Write this **JSON** file 

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
		- Fill the above empty places with the data you wanna send
		- If your request was successful, you'd receive **201 Created status code** and receive the samen data you sent
		- If your registration failed(wasn't successful) you'd receive **400 Bad Request status code** with some validation error specifying the exact issue with your request, EX:
		
			   {
				 "email":[
						"This email has already registered"
				     ],
			   }

- **Login**
	- From this point on, I will explain the steps using **Postman** as the HTTP client 
	- Go to this URL `(http://localhost(whatever-domain))/api/accounts/login/`
	- Make request of type **POST**
	-  Select **Body**  
	-  Select raw --> JSON
	-  Write this **JSON** file 
	
	        {
		        "email" : "",
		        "password" : ""
		    }
	- Fill these empty places with the data you wanna send
	- If your request was successful and you're authorized you will receive **200 OK status code** with the token ID and some other data about the user

		    {
			    "refresh" : "refresh token",
			    "access" : "access token",
			    "User" : {
				    "name" : "username",
				    "email" : "user email"
				  }
			}
		 
	- If your Login/Authorization process failed you will receive **400 Bad Request status code**

---

# Chatbot
## How to use  ./test
1. Need to login
2. Add bearer token 
3. For first time use **GET** request you will get first question
4. in next request will be **POST** request 

Question get in this form
`{'question':"Do you have ***********?"}`

answer will be in this form
`{"ans":"y/n"}`

Result will be in this from
`{"disease":"It is likely you have : *********** "}`

after geting the result back to **GET** request to start again

## TODO
- Connect the API to the AI model to return the predication results
