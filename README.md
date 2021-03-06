# Argon2-passwordgenerator

## Technicalities
Programmed in Python 3.9.7. To install Python, follow the instructions on: https://www.python.org/downloads/

Needs the following modules:
- os.path
- argon2
- getpass
- pandas

To install all dependencies/modules (some are default), run

    pip install --upgrade pip
    pip install argon2-cffi
    pip install pandas

## Introduction
Program for creating and remembering passwords that are **very hard** to brute force. Done by choosing an easy masterpassword plus a "purpose salt" (additional varying ending), which is then hashed so that it can be used for different needs/websites/logins. If you don't know what a salt is, read the section "Examples" below, where it is not explained either but rather shown by examples. The program uses the Argon2 algorithm for secure hashing. It copies the hashed password to your clipboard to be pasted anywhere while not being readable on the screen. If you think "hashed passwords don't provide additional security", please read the section "Principle".

I would say this is a pretty good way to convert easy passwords into hard ones while being hard to crack even if this program code is common knowledge. Of course this is only true if the pre-hashed masterpassword is not one of the easiest known to mankind (see https://en.wikipedia.org/wiki/Wikipedia:10,000_most_common_passwords).

For more convenience, I would still recommend the use of a password manager, but this program makes it possible to have unguessable but deterministic passwords that one can access everywhere where this algoritm is accessible. It makes you independent of having to have a password manager, you can just store an all-purpose masterpassword in your mind.

## Principle
Argon2 is a hashing function that is intended not to be as fast as possible but rather takes some parameters (Time, RAM, #Processors) that determine how many iterations the hashing algorithm performs, how much RAM is needed to generate the hash and how many processors are used for the hashing. For more details on how it specifically does it, read up on the Argon2 algorithm. For this purpose it is just assumed that we have an algorithm that can be made very slow (seconds or more) on even fast machines so that brute forcing is made very hard.

If one now chooses a set of parameters, one has a slow, but deterministic way of converting an easy password into a hexadecimal string of up to 128 characters length. Since the hashed password can be made *virtually* uncrackable, only the pure, unhashed password still can be guessed. But by making the hashing take a long time, one can effectively make brute-forcing it near impossible, since one can make a single guess take seconds or longer.

But what about pre-calculated hash tables?

Here the parameters come in. Argon2 takes an additional "fixed salt" (that differs from the purpose salt) besides the above mentioned "time", "RAM" and "#processors"-parameters. My algorithm stores these four parameters locally on the machine you are using for hashing. Since these parameters change the hashed output, an attacker would need a hash table for every set of parameters that exist. Since the salt is a string of (almost) arbitrary length and the other three numbers also have many combinations, hash tables are therefore almost impossible to provide.

And even if an attacker knows your set of parameters, it still takes the usual (parameter-dependend) long time to calculate a hash table (or guess your password).

In conclusion, as far as I know this is a hashing algorithm that makes the brute force way of attacking impossible. Of course your password can still get leaked, your keyboard input can be tracked, your clipboard can be read out and many things more.

But even if your (hashed) password got leaked, it is still impossible to get your (unhashed) masterpassword from it. So you can just keep using it. And you can change the leaked hashed password quickly by just appending a "1" to your unhashed masterpassword or salt (see section "Examples"). 

I, however, still recommend the usage of a password manager (like KeePass) to store at least your salts, or maybe even the hashed passwords. You could even write your salts on a piece of paper and put it on your desk. Without the masterpassword, every attacker needs to brute force and therefore has to use the Argon2 hashing algorithm which you made very slow.

## Setup
The program needs a file from which the chosen Argon2 parameters (time, ram and processor parameters and fixed salt for reproducibility) are read from. This file is named "pwgenka-config.txt" and has to be placed in the same folder as the Python script. These parameters configure your "version". If they are lost, your hashed passwords can not be calculated any more. So: **DO NOT LOSE YOUR CONFIGURATION PARAMETERS/FILE**. For configuration, open the configuration file and replace the parameters with your desired values. The file **must** have the following form:

    Time parameter:
    int, [1,inf), roughly the number of hashing iterations, recommended 1-10
    RAM parameter:
    int, [1,inf), number of KiB used for the hashing, recommended 1000-1000000
    Processors parameter:
    int, [1,inf), number of involved processors, recommended 2-4
    Salt parameter:
    string, used to make the hash function harder to crack

That is: Eight lines, four of them indicating the order of parameters and four of them the parameters. A valid configuration could therefore be:

    Time parameter:
    3
    RAM parameter:
    376985
    Processors parameter:
    2
    Salt parameter:
    thisisasalt

Time is roughly the number of iterations, RAM is the used memory for the hashing and Processors is the number of processors that are used in the calculation.

With the amount of RAM, you have to watch out for too large numbers. If you allocate so much RAM, that your machine has to use all of it's free RAM, it is going to use it's swap memory, then you can potentially make your machine so slow and blocked, that you have to reset it. Choosing even more RAM will definitely block your machine. So choose a reasonable amount of RAM (below a GiB, because modern Smartphones even have at least 4 GiB) to circumvent that. Choosing a weird RAM parameter is harder to guess of course... just saying.

You can choose more processors than your machine has. E.g. entering two times the processor number than your machine has makes the program work with half of your entered number (because there aren't more processors available), but the computation takes double the time. It therefore increases the time analogous to just increasing the "time"-parameter. So don't fear that you **have** to have the numbers of processors so that the algorithm even works.

The salt is a "fixed salt" that stays constant for all the passwords you will hash (if you don't lose your configuration file that is). It personalises your Argon2-passwordgenerator, so that attackers can't use hash tables to guess your password. Just choose a sentence or a word here. Mine isn't too complicated either. 

## Examples
These are examples for a hashing output with different "purpose salts".

    Time:               3
    RAM (KiB):          376985
    Processors:         2
    Salt:               thisisasalt
    Length:             20
    Capitalisation:     No
    Special characters: No

    masterpassword: easypassword
    purpose salt:
    total input:    easypassword
    total output:   b034d36e56c4ed444aef

    masterpassword: easypassword
    purpose salt:   gmx
    total input:    easypasswordgmx
    total output:   d27f71f5bed17a32e18f

    masterpassword: easypassword
    purpose salt:   gmx1
    total input:    easypasswordgmx1
    total output:   4ece6fa9e8913a505780

    masterpassword: easypassword
    purpose salt:   yahoo
    total input:    easypasswordyahoo
    total output:   f53b36683c18af138261

Since this is intended for password usage and the output is just hexadecimal strings, it comes with the option of choosable length (only even numbers), capitalization of the first letter (to have at least one) and a special symbol option (the last character is converted to "$", also to have at least one). This is still secure, because one can choose really long passwords that are in itself not guessable. As one can see, even the masterpasswords (plus salts) that just differ by one character are hashed into completely different hashes.

## Usage
Put the script and the configuration file into a folder of your liking. Customize the configuration file as described in "Examples".

Start the program using Python3. If it finds a working configuration file, you are asked, how long your hashed password should be.

For technical reasons, you can only have passwords of even numbers between 2 and 128 hexadecimal characters. Just pressing enter gives you a length of 32 characters.

You are then asked to enter the masterpassword plus the optional purpose salt. You are also warned, that your clipboard will be overwritten with the password.

After entering the password and pressing enter, two yes-or-no questions are asked: Whether you want your password with capitalised letters and/or special characters.

After that, the hashed password is copied to your clipboard, so that you can post it anywhere. After pressing enter again, the program overwrites your clipboard with something else (the link to the GitHub-repository of this program), so that you don't accidentally paste your password on your screen to see.

It then terminates.

## Acknowledgements
Thanks to Hynek Schlawack for programming a Python version of Argon2 and helping me with some questions. In case all of this is horrible: I didn't tell him what I was doing with this code, so don't blame him.
