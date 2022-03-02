# Argon2-passwordgenerator

## Technicalities
Programmed in Python 3.9.7
Needs the following modules:
os.path
argon2
getpass
pandas

## Introduction
Program for creating and saving a password by remembering an easy masterpassword and adding a salt (additional ending) to adapt it to different needs. If you don't know what a salt is, read the section "Example" below. Uses the Argon2 algorithm for secure hashing. Copies the hashed password to your clipboard to be pasted anywhere while not being readable on the screen.
I would say this is a pretty good way to convert easy passwords into hard ones while being hard to crack even if this program code is common knowledge. Of course this is only true if the pre-hashed masterpassword is not one of the easiest known to mankind (see https://en.wikipedia.org/wiki/Wikipedia:10,000_most_common_passwords).

For more convenience, I would still recommend the use of a password manager, but this program makes it possible to have unguessable but deterministic passwords that one can access everywhere where this algoritm is accessible. It makes you independent of having to have a password manager, you can just store an all-purpose masterpassword in your mind.

## Principle
Argon2 is a hashing function that is intended not to be as fast as possible but rather takes some parameters (time, RAM, #processors) that determine how many iterations the hasing algorithm performs, how much RAM is needed to generate the hash and how many processors are used for the hashing. For more details on how it specifically does it, read up on the Argon2 algorithm. For this purpose it is just assumed that we have an algorithm that can be made very slow (seconds or more) on even fast machines so that brute forcing is made very hard.

If one now chooses a set of parameters, one has a slow, but deterministic way of converting an easy password into a hexadecimal string of up to 128 characters length. Since the hashed password can be made *virtually* uncrackable, only the pure, unhashed password still can be guessed. But by making the hashing take a long time, one can effectively make brute-forcing it near impossible, since one can make a single guess take seconds or longer.

But what about pre-calculated hash tables?
Here the parameters come in. Argon2 takes an additional salt besides the above mentioned "time", "RAM" and "#processors"-parameters. My algorithm stores these four parameters locally on the machine you are using for hashing. Since these parameters change the hashed output, an attacker would need a hash table for every set of parameters that exist. Since the salt is a string of (almost) arbitrary length and the other three numbers also have many combinations, hash tables are therefore almost impossible to provide.

And even if an attacker knows your set of parameters, it still takes the usual (parameter-dependend) long time to calculate a hash table (or guess your password).

In conclusion, as far as I know this is a hashing algorithm that makes the brute force way of attacking impossible. Of course your password can still get leaked, your keyboard input can be tracked, your clipboard can be read out and many things more.

But even if your (hashed) password got leaked, it is still impossible to get your (unhashed) masterpassword from it. So you can just keep using it. And you can change the leaked hashed password quickly by just appending a "1" to your unhashed masterpassword or salt (see section "Example"). 

I, however, still recommend the usage of a password manager (like KeePass) to store at least your salts, or maybe even the hashed passwords. You could even write your salts on a piece of paper and put it on your desk. Without the masterpassword, every attacker needs to brute force and therefore has to use the Argon2 hashing algorithm which you made very slow.

## Setup
Needs a file from which the chosen Argon2 parameters (time, ram and processor parameters and fixed salt for reproducibility) are read from. This file is named "pwgenka-config.txt" and has to be placed in the same folder as the python script. These parameters configure your "version". If they are lost, your hashed passwords can not be calculated any more. So: **do not lose your configuration parameters/file**. For configuration, open the configuration file and replace the parameters with your desired values. The file **must** have the following form:

------------------------------------------------------------------------
Time parameter:
int, [1,inf), roughly the number of hash iterations, recommended 1-10
RAM parameter:
int, [1,inf), number of KiB used for the hash, recommended 1000-1000000
Processors parameter:
int, [1,inf), number of involved processors, recommended 2-4
salt parameter:
string, used to make the hash function harder to crack
------------------------------------------------------------------------

That is: Eight lines, four of them indicating the order of parameters and four of them the parameters. A valid configuration could therefore be:

------------------------------------------------------------------------
Time parameter:
3
RAM parameter:
376985
Processors parameter:
2
salt parameter:
thisisasalt
------------------------------------------------------------------------

Time is roughly the number if iterations, RAM is the used memory for the hashing and #processors is the number of processors that are assumed to be used in the calculation. You can choose more processors that your machine has, but e.g. entering two times the processors than your machine has is analogous to just doubling the "time"-parameter. But don't fear that you *have* to have the numbers of processors so that the algorithm even works.
Choosing a weird RAM parameter is harder to guess of course... just saying.

## Example
This is an example for a hashing output with different "purpose salts".
salt: thisisasalt, iteration: 3, memory: 376985 KiB, processors: 2, 20 characters, no capitalization, no special character.

	easypassword		->	b034d36e56c4ed444aef
	easypasswordgmx		->	d27f71f5bed17a32e18f
	easypasswordgmx1	->	4ece6fa9e8913a505780
	easypasswordyahoo	->	f53b36683c18af138261

Since this is intended for password usage and the output is just hexadecimal strings, it comes with the option of choosable length, capitalization of the first letter (to have at least one) and a special symbol option (the last character is converted to "$", also to have at least one). This is still secure, because one can choose really long passwords that are in itself not guessable.

## Usage
Start the program using python. If it finds a working configuration file, you are asked, how long your hashed password should be.
For techincal reasons, you can only have passwords of even numbers between 2 and 128 hexadecimal characters. Just pressing enter gives you a length of 32 characters.
You are then asked to enter the masterpassword plus the optional purpose salt. You are also warned, that your clipboard will be overwritten with the password.
After entering the password and pressing enter, two yes-or-no quesions are asked whether you want your password with capitalised letters or special characters.
After that, your password is copied to your clipboard, so that you can post it anywhere. After pressing enter again, the program overwrites your clipboard with something else (the link to the GitHub-repository of this program), so that you don#t accidentally paste your password on your screen to see.
It then termintes.
