steps to install the code 

1. git clone https://github.com/razeenmohamedrasheed/TaskScheduler.git
2. create an environment
3. pip install -r requirements.txt ## for installing all the packages
4. activate the environment
5. Run python main.py 


API flow
2 Users Admin and Users
1 . Signup by using credentials
        user role 1 for Admin and 2 for users
        payload
        {
            "role_id": 1,
            "username": "string",
            "email": "string",
            "contact": "string",
            "password": "string"
        }
2. Token Generation and API Access

Once a user successfully signs up, a token will be generated. This token is essential for accessing all other APIs within the application. 

- **User Permissions:**  
  - Users can create, read, update, and delete their own tasks.
  
- **Admin Permissions:**  
  - Admins have the ability to view all tasks, regardless of ownership.

To access any API endpoint, users must include the generated token in the request header. This ensures secure access and proper authorization based on user roles.

in taskroute.py
    sender_email = ''  # Your email address
    sender_password = ''  # Your email password

    please configure this ..