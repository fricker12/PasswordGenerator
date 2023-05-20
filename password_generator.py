import argparse
import random
import string
import sys
import logging

def generate_password(length, character_set):
    return ''.join(random.choice(character_set) for _ in range(length))

def generate_password_from_template(template, character_set):
    password = ''
    i = 0
    while i < len(template):
        if template[i] == '\\':
            if i + 1 < len(template):
                password += template[i + 1]
                i += 2
            else:
                password += template[i]
                i += 1
        elif template[i] == '{':
            closing_bracket_index = template.find('}', i)
            if closing_bracket_index != -1:
                placeholder = template[i + 1:closing_bracket_index]
                if placeholder.isnumeric():
                    repeat_count = int(placeholder)
                    password += password[-1] * (repeat_count - 1)
                else:
                    password += placeholder
                i = closing_bracket_index + 1
            else:
                password += template[i]
                i += 1
        elif template[i] == '[':
            closing_bracket_index = template.find(']', i)
            if closing_bracket_index != -1:
                custom_set = template[i + 1:closing_bracket_index]
                exclude_placeholders = []
                while '^' in custom_set:
                    caret_index = custom_set.index('^')
                    exclude_placeholders.append(custom_set[caret_index + 1])
                    custom_set = custom_set[:caret_index] + custom_set[caret_index + 2:]
                custom_set = [c for c in custom_set if c not in exclude_placeholders]
                if custom_set:
                    password += random.choice(custom_set)
                i = closing_bracket_index + 1
            else:
                password += template[i]
                i += 1
        else:
            if template[i] == 'd':
                character_set = string.digits
            elif template[i] == 'l':
                character_set = string.ascii_lowercase
            elif template[i] == 'L':
                character_set = string.ascii_uppercase + string.ascii_lowercase
            elif template[i] == 'u':
                character_set = string.ascii_uppercase
            elif template[i] == 'p':
                character_set = string.punctuation
            password += random.choice(character_set)
            i += 1
    return password

def main():
    parser = argparse.ArgumentParser(description='Password Generation Utility')
    parser.add_argument('-n', type=int, help='Set length of password and generate random password from set {small lateral ASCII, big lateral ASCII, digit}')
    parser.add_argument('-t', type=str, help='Set template for generate passwords')
    parser.add_argument('-f', type=str, help='Getting list of patterns from file and generate random password for each')
    parser.add_argument('-c', type=int, default=1, help='Number of passwords to generate')
    parser.add_argument('-S', type=str, help='Character set')
    parser.add_argument('-p', action='store_true', help='Randomly permute characters of password')
    parser.add_argument('-v', action='count', default=0, help='Verbose mode')
    parser.add_argument('-H', action='store_true', help='Help')
    args = parser.parse_args()
    
    if args.H:
        parser.print_help()
        sys.exit(0)
        
    verbose_level = args.v
    
    # Set logging level based on verbosity
    if verbose_level >= 3:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose_level >= 2:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    logger = logging.getLogger(__name__)

    # Log verbosity level
    logger.debug("Verbose mode: Level %d", verbose_level)

    character_set = string.ascii_letters + string.digits + string.punctuation
    if args.S:
        character_set = args.S

    if args.t:
        if args.f:
            print("Error: Both -t and -f options cannot be used together.")
            sys.exit(1)
        password = generate_password_from_template(args.t, character_set)
        if args.p:
            password = ''.join(random.sample(password, len(password)))
        print(password)
    elif args.n:
        for _ in range(args.c):
            password = generate_password(args.n, character_set)
            if args.p:
                password = ''.join(random.sample(password, len(password)))
            print(password)
    elif args.f:
        try:
            with open(args.f, 'r') as file:
                patterns = file.readlines()
            for pattern in patterns:
                password = generate_password_from_template(pattern.strip(), character_set)
                if args.p:
                    password = ''.join(random.sample(password, len(password)))
                print(password)
        except IOError:
            print("Error: Failed to open the file.")
            sys.exit(1)
    else:
        print("Error: No option specified.")
        parser.print_help()

if __name__ == '__main__':
    main()
