# Password Generator

## Requirements

You need the followin to be able to run this code:



## Usage

First install the script and it's requirements:

```
git clone https://github.com/fricker12/PasswordGenerator
cd PasswordGenerator

```
Then run the script as follows:
```
To generate a random password of a specific length, use the -n option:
python password_generator.py -n 10

To generate a password using a template, use the -t option:
python password_generator.py -t "u{4}d{3}\-l{2}"

To generate passwords for each pattern listed in a file, use the -f option:
python password_generator.py -f patterns.txt

You can specify the number of passwords to generate using the -c option (default is 1):
python password_generator.py -n 8 -c 5

You can specify a custom character set using the -S option:
python password_generator.py -n 12 -S "abcd1234"

You can enable random permutation of characters in the generated password using the -p option:
python password_generator.py -n 10 -p

Verbose mode can be enabled using -v, -vv, or -vvv options to show detailed information during processing.

example:
python password_generator.py -t "u{4}d{3}\-l{2}" -vvv
DEBUG:__main__:Verbose mode: Level 3
INFO:__main__:Generating password from template: u{4}d{3}\-l{2}
DEBUG:__main__:Generating password from template: u{4}d{3}\-l{2}
DEBUG:__main__:Choosing character from set: ABCDEFGHIJKLMNOPQRSTUVWXYZ
DEBUG:__main__:Generating uppercase characters: 3
DEBUG:__main__:Choosing character from set: 0123456789
DEBUG:__main__:Generating digit characters: 2
DEBUG:__main__:Choosing character from set: abcdefghijklmnopqrstuvwxyz
DEBUG:__main__:Generating lowercase characters: 1
DEBUG:__main__:Generated password from template: DRKM681-fi
INFO:__main__:Generated password: DRKM681-fi

python password_generator.py -t "u{4}d{3}\-l{2}" -v
INFO:__main__:Generating password from template: u{4}d{3}\-l{2}
INFO:__main__:Generated password: KLSA102-vc


The -H option displays the help information.


```

