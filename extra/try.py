# from cryptography.fernet import Fernet

# # key = Fernet.generate_key()

# # print(key)
# key = b'-ko3jzYj8kzzHnn6epl_hrR9eS-6oag2UVn8QxwrZk8='
# cipher = Fernet(key)
# # cipher = Fernet(key)
# message = 'gitbash' # Users real password

# message = message.encode('latin-1') # processed

# encyrpted_text = cipher.encrypt(message)
#  # Got the value
# some_value = encyrpted_text.decode()
# encyrpted_text = some_value.encode()
# original_text = cipher.decrypt(encyrpted_text)
# print(original_text.decode())


from datetime import datetime  
    
# using now() to get current time  
# current_time = datetime.datetime.now()  
    
# # Printing attributes of now().  
 
      
# month = current_time.month


# day = current_time.day

# print(month, day)

today = datetime.today().strftime('%Y-%m-%d')

print(type(today))
print(today)