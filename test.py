"""import threading

# Global variable
global_variable = 0

def my_thread():
    global global_variable
    for i in range(5):
        global_variable += 1
        print(global_variable)

# Create and start the thread
thread = threading.Thread(target=my_thread)
thread.start()

# Wait for the thread to complete
thread.join()

# Access the updated global_variable
  # Output: 1"""
d=()

for k in range(5):
    d=k
   
print(d)