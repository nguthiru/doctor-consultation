# WELCOME TO THE CONSULT INSTALLATION PROCESS

# REQUIEREMENTS
1. An installation of python on your computer

## INSTALLATION
1. Clone the github repository to a folder of your liking
2. Open the folder using VSCode
3. Using the VSCode terminal run the following commands:
   1. pip install -r requirements.txt
   2. python manage.py migrate
   3. python manage.py createsuperuser 
      - Fill in the username,email,password as this will be the admin credentials

    4. To run the server use: 
         - python manage.py runserver


### Admin Console
To access the admin console use the following url: http://127.0.0.1:8000/admin. Log in with the credentilas in section 1 part 3



