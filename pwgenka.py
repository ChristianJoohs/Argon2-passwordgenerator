# Programmed in Python 3.9.7

"""
	Program for creating and saving a password by remembering an easy masterpassword
	and adding a salt (additional ending) to adapt it to different needs. Uses the argon2
	algorithm for secure hashing. Upon first creation creates a file (if it doesn't exist yet)
	in which the chosen security parameters (time and ram parameter and fixed salt for
	reproducibility) are saved or read from.
	Since this is intended for password usage and the output is just hexadecimal strings, it comes 
	with the option of choosable length, capitalization of the first letter and a special symbol option
	(the last character is converted to "$"). This is still secure, because one can choose really long
	passwords that are in itself not guessable. Brute-force attacks are also almost impossible since each
	guessing try using argon2 takes a choosable amount of time, limiting the guessable passwords per second
	in the lower 100s for university-like computational power.
	This is an example for a hashing output with different "purpose salts".
	salt: thisisasalt, iteration: 2, memory: 1000 KiB, processors:4, 20 characters, no capitalization, no special character.
	easypassword		->	
	easypasswordgmx		->	
	easypasswordyahoo	->	
	I would say this is a pretty good way to convert easy passwords into hard ones while
	being hard to crack even if this program code is common knowledge. Of course only if the
	pre-hashing password is not one of the easiest known to mankind
	(see https://en.wikipedia.org/wiki/Wikipedia:10,000_most_common_passwords).
	For more convenience, I would still recommend the use of a password manager, but this program makes it
	possible to have almost-random but deterministic passwords that one can access everywhere where this algoritm
	is accessible.
"""

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
	configfile = open("pwgenka-config.txt","w")
	print("\nFound no configuration file. Please choose parameters.\n")
	print("The algorith is only safe when one computation takes a considerable amount of time.")
	print("Therefore choose the parameters high enough so that one password generation takes between 1 - 5 seconds.")
	print("This has to be found out separately for each machine but there are recommended start values.\n")
	print("The higher the product for time t and RAM c the safer the algorith will be but the longer it takes.")
	print("The time t corresponds to the number of iteration the algorithm does.")
	print("RAM c decides how much RAM the algorithm uses. So don't go to high here.")
	print("#processors p decides, how many processors should be used for calculation. More=safer.\n")
	print("Choose a time parameter t (1 to 10). Recommended t=3. Press enter to accept.\n")
	timeparam=input()

	# Convert the string to an integer if the string contains only integers.
	if not timeparam.isdigit():
		getpass.getpass("\nNo valid number entered. Press enter to exit.\n")
		quit()
	else:
		timeparam=int(timeparam)

	# If a number below 1 or larger than 10 is entered, the program exits.
	if timeparam<1 or timeparam>10:
		getpass.getpass("\nNo valid number entered. Press enter to exit.\n")
		quit()
	
	configfile.write("Time parameter:\n")
	configfile.write(str(timeparam) + "\n")
	configparams[0]=timeparam

	print("\nNow choose your corresponding RAM space. Recommended c=7. Press enter to accept.\n")
	print("1: 1 KiB\n2: 10 KiB\n3: 100 KiB\n4: 1 MiB\n5: 10 MiB\n6: 100 MiB\n7: 500 MiB\n8: 1 GiB\n9: 2 GiB\n")
	ramparam=input()

	# Convert the string to an integer if the string contains only integers.
	if not ramparam.isdigit():
		getpass.getpass("\nNo valid number entered. Press enter to exit.\n")
		quit()
	else:
		ramparam=int(ramparam)

	# If a number below 1 or larger than 10 is entered, the program exits.
	if ramparam<1 or ramparam>9:
		getpass.getpass("\nNo valid number entered. Press enter to exit.\n")
		quit()

	if ramparam==2:
		ramparam=10
	elif ramparam==3:
		ramparam=100
	elif ramparam==4:
		ramparam=1000
	elif ramparam==5:
		ramparam=10^4
	elif ramparam==6:
		ramparam=10^5
	elif ramparam==7:
		ramparam=5*10^5
	elif ramparam==8:
		ramparam=10^6
	elif ramparam==9:
		ramparam=2*10^6
	
	configfile.write("RAM parameter:\n")
	configfile.write(str(ramparam) + "\n")
	configparams[1]=ramparam

	print("Choose a processor parameter p (1 to 8). Recommended p=4. Press enter to accept.\n")
	processorparam=input()

	# Convert the string to an integer if the string contains only integers.
	if not processorparam.isdigit():
		getpass.getpass("\nNo valid number entered. Press enter to exit.\n")
		quit()
	else:
		processorparam=int(processorparam)

	# If a number below 1 or larger than 10 is entered, the program exits.
	if processorparam<1 or processorparam>8:
		getpass.getpass("\nNo valid number entered. Press enter to exit.\n")
		quit()
	
	configfile.write("Processors parameter:\n")
	configfile.write(str(processorparam) + "\n")
	configparams[2]=processorparam

	print("\nNow you will have to choose the salt that argon2 requires for hashing.")
	print("It is held fix so that your hashing is unique and gives reproducible results.")
	print("IF YOU LOSE YOUR COONFIG FILE, YOU LOSE ALL YOUR PASSWORDS. Save it somewhere. It's not bad if people read it.")
	print("The salt can be any random sentence or collection of characters. Dont go too long (>100). Press enter to accept.\n")
	saltparam=input()

	# If it is longer than 100 characters then fail.
	if len(saltparam)>100:
		getpass.getpass("I said not longer than 100 characters. Press enter to exit.\n")
		quit()
	configfile.write("salt parameter:\n")
	configfile.write(saltparam)
	configfile.close()
	configparams[3]=saltparam

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