# Programmed in Python 3.9.7

# Module for checking file existence
import os.path
# Module for hash functions
import argon2
# Module for getting suppressed input
import getpass
# Module for copying text to the clipboard
import pandas

# Check for the existence of the configuration file and read or create it.
configparams =  [0,0,0,0]
directory=os.path.dirname(os.path.abspath(__file__))
if os.path.exists(directory + "/pwgenka-config.txt"):
	print("\nFound a configuration file. Loading parameters.")
	configfile=open(os.path.dirname(os.path.abspath(__file__)) + "/pwgenka-config.txt","r")
	for i in range(4):
		for j in range(2):
			configparams[i]=configfile.readline()[:-1]
	configfile.close()
	# Process the imported values and check for sanity
	for i in range(3):
		if configparams[i].isdigit():
			configparams[i]=int(configparams[i])
		else:
			getpass.getpass("Configfile faulty. Time, RAM and #processors must be integers. Press enter to exit.\n")
			quit()
	if len(configparams[3])>100:
		getpass.getpass("Configfile faulty. The salt is too long (>100). Press enter to exit.\n")
		quit()

else:
	print("\nFound no configuration file. Please read the readme.\n")
	quit()

# Now the desired hashed passwordlength is determined.
print("\nHow many digits should the hashed password have? (\"Enter\"=32)\n")
print("Minimal length: 1, maximal length: 128. Has to be an even number.\n")

length=getpass.getpass("")

# If only enter without input is pressed, length=32.
if length=="":
	length="32"

# Convert the string to an integer if the string contains only integers.
if not length.isdigit():
	getpass.getpass("No valid number entered. Press enter to exit.\n")
	quit()
else:
    length=int(length)

# If a number below 1 or larger than $hashlength is entered, the program exits.
if length<1 or length>128 or length%2==1:
	getpass.getpass("No valid number entered. Press enter to exit.\n")
	quit()
else:
	# Half the length because argon2 puts out "length" bytes which is 2*"length" hexadecimal characters.
	length=int(length/2)

# Now the easy masterpassword plus the optional desired salt is determined.
print("Please enter the masterpassword plus optional salt.\n")
print("WARNING: The clipboard will be overwritten with the hashed password.\n")

password=getpass.getpass("")

# Now it is determined, whether the password has to contain at least one capitalized letter.
# This program just takes the first occuring one and capitalizes it. Of course this will not
# always work, for there is a very small chance (for passwords longer than, lets say 10 characters)
# that the password does only contain numbers, but lets face it: The chance is negligible.
print("Does the password have to contain a capitalised letter? (y/n) (\"Enter\"=n)\n")

capitalise=getpass.getpass("")

# If only enter without input is pressed, capitalise="n".
if capitalise=="":
	capitalise="n"

# If neither y nor n nor no input is entered the program exits.
if capitalise!="y" and capitalise!="n":
	getpass.getpass("Not a valid input. Press enter to exit.\n")
	quit()

# Now it is determined, whether the password has to contain at least one special character.
# This program will just take the last character and turn it into a "$", which is almost every
# time allowed as a special character.
print("Does the password have to contain a special character? (y/n) (\"Enter\"=n)\n")

specialise=getpass.getpass("")

# If only enter without input is pressed, specialise="n".
if specialise=="":
	specialise="n"

# If neither y nor n nor no input is entered the program exits.
if specialise!="y" and specialise!="n":
	getpass.getpass("Not a valid input. Press enter to exit.\n")
	quit()

# --------------------------------------
# From here, the password is calculated.
# --------------------------------------

# Create the full-length hash from the determined password with the determined algorithm.
shapasswordbytes=argon2.low_level.hash_secret_raw(bytes(password,'utf8'),bytes(configparams[3],'utf8'),time_cost=configparams[0],memory_cost=configparams[1],parallelism=4,hash_len=length,type=argon2.low_level.Type.ID)
# Convert the password to a hex string.
shapassword=shapasswordbytes.hex()

# If the password has to contain a capitalized letter, it is done here.
if capitalise=="y":
    for letter in shapassword:
        if letter in ["a", "b", "c", "d", "e", "f"]:
            shapassword=shapassword.replace(letter,letter.upper(),1)
            break

# If the password has to contain a special character, it is done here. The last digit will be replaced by a "$".
if specialise=="y":
	shapassword=shapassword[0:len(shapassword)-1] + "$"

# The result is copied to the clipboard using pandas
df=pandas.DataFrame([shapassword])
df.to_clipboard(header=False,excel=False,index=False)

# This section gives the user time to paste the password to some location before it is again overwritten and the program exits.
getpass.getpass("The password has been copied to the clipboard. Copy it to the desired\ndestination and after that, press enter to exit this program and\noverwrite the clipboard with something else.")

# Overwrite the clipboard with "blub" to not leak password by accident.
df=pandas.DataFrame(["https://github.com/ChristianJoohs/Argon2-passwordgenerator"])
df.to_clipboard(header=False,excel=False,index=False)