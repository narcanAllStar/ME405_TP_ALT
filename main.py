import pyb, os

f1 = 'motor_test.py'
f2 = 'tp_main.py'

print("Please select an option from the list: ")
print("[1]          %s"%(f1))
print("[2]          %s"%(f2))
option = input('')

if option == "1":
    filename = f1
elif option == "2":
    filename = f2
else:
    print("Invalid option")
    exit(99)

print("********************** " + str(filename) + " **************************")

execfile(filename)
