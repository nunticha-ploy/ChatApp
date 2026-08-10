def menu():
  
  while True:
    print("****** Chat Application ******")
    print("1.Login")
    print("2.Signup")
    print("3.Exit")

    choice = input("Choose an option: ").strip()
    if choice == "1":
      email = input("Email: ")
      password = input("Password: ")
      return f"LOGIN {email} {password}"

    elif choice == "2":
      username = input("Username: ")
      email = input("Email: ")
      password = input("Password: ")
      return f"SIGNUP {username} {email} {password}"

    elif choice == "3":
      return "EXIT"
      
    else:
      print ("Invalid choice. Please try again.")