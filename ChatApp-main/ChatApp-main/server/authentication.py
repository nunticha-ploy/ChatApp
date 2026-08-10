import hashlib #The hashlib module is used to hash the password before saving it to the user details file.

#hash the password
user_details_file = "user.txt"

def hash_password(password):
  pwd_bytes = password.encode('utf-8')
  hashed_pwd = hashlib.sha256(pwd_bytes).hexdigest()
  return hashed_pwd

#save the user details
def save_user(username, email, hashed_pwd):
  with open(user_details_file, "a") as f: #a to append new users.
    f.write(f"{username} {email} {hashed_pwd}\n")


#signup
def signup(username, email, password):
  #username
  if not username.strip():
    return False, "Username cannot be empty"
  
  #email
  if user_exists(email):
    return False, "This email is already registered."
  if not email.strip():
    return False, "Email cannot be empty."
  
  #password
  if not password.strip():
    return False, "Password cannot be empty."
  
  #save user
  hashed_pwd = hash_password(password)
  save_user(username, email, hashed_pwd)
  return True, "You have registered successfully!"

#check if the user exists
def user_exists(email):
  try:
    with open(user_details_file, "r") as f:
      for line in f:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == email:
          return True
  except FileNotFoundError:
    return False
  return False


#login
def login(email, password):
  auth_hash = hash_password(password)
  #read the file line by line
  try:                    
    with open(user_details_file, "r") as f:
      for line in f:
        username, stored_email, stored_hash = line.split()
        if email == stored_email and auth_hash == stored_hash:
          return True, "Logged in Successfully!", username
  except FileNotFoundError:
    return False, "No registered users.", None
  return False, "Login failed!", None

#get all lgin user
def get_all_registered_users():
  users = []
  try:
    with open(user_details_file, "r") as f:
      for line in f:
        parts = line.split()

        if len(parts) >= 3:
          username = parts[0]
          users.append(username)
  except FileExistsError:
    pass
  return users
