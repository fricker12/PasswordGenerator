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

The -H option displays the help information.


```

