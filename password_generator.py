import argparse
import random
import string
import sys
import logging


def generate_password(length, character_set,logger):
    logger.debug("Generating password of length %d", length)
    password = ''.join(random.choice(character_set) for _ in range(length))
    logger.debug("Generated password: %s", password)
    return password


def generate_password_from_template(template, character_set, logger):
    logger.debug("Generating password from template: %s", template)
    symbol_dict = {
        "d": string.digits,
        "l": string.ascii_lowercase,
        "L": string.ascii_uppercase + string.ascii_lowercase,
        "u": string.ascii_uppercase,
        "p": string.punctuation,
        'a': string.ascii_lowercase + string.digits,
        'A': string.ascii_letters + string.digits,
        'U': string.ascii_uppercase + string.digits,
        'h': string.digits + 'abcdef',
        'H': string.digits + 'ABCDEF',
        'v': 'aeiou',
        'V': 'AEIOUaeiou',
        'Z': 'AEIOU',
        'c': string.ascii_lowercase.translate(str.maketrans('', '', 'aeiou')),
        'C': string.ascii_letters.translate(str.maketrans('', '', 'aeiou')),
        'z': string.ascii_uppercase.translate(str.maketrans('', '', 'AEIOU')),
        'b': '()[]{}<>',
        's': string.printable.translate(str.maketrans('', '', string.whitespace)),
        'S': string.printable,
        'x': ''.join(chr(i) for i in range(0xA1, 0x100) if i != 0xAD),
        "|": None
    }
    
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
                    if i > 0 and template[i - 1] in symbol_dict:
                        character_set = symbol_dict[template[i - 1]]
                        password += ''.join(random.sample(character_set, repeat_count-1))
                        logger.debug("Generating %s characters: %d", template[i - 1], repeat_count)
                    else:
                        password += password[-1] * (repeat_count - 1)
                        logger.debug("Generated repeat character: %s", password[-1])
                else:
                    character_set = symbol_dict.get(placeholder)
                    if character_set:
                        password += random.choice(character_set)
                        logger.debug("Generated character from set: %s", character_set)
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
                    logger.debug("Generated character from custom set: %s", custom_set)
                i = closing_bracket_index + 1
            else:
                password += template[i]
                i += 1
        else:
            character_set = symbol_dict.get(template[i])
            if character_set is not None:
                if character_set == "|":
                    choices = template[i + 1:].split("|", 1)
                    if len(choices) == 2:
                        choice1 = generate_password_from_template(choices[0], character_set, logger)
                        choice2 = generate_password_from_template(choices[1], character_set, logger)
                        password += random.choice([choice1, choice2])
                        logger.debug("Generated choice between: %s and %s", choice1, choice2)
                        break
                else:
                    password += random.choice(character_set)
                    logger.debug("Generated character from set: %s", character_set)
            i += 1
    return password


def main():
    
    parser = argparse.ArgumentParser(description='Password Generation Utility')
    parser.add_argument('-n', type=int,
                        help='Set length of password and generate random password from set {small lateral ASCII, big lateral ASCII, digit}')
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
    elif verbose_level >= 1:
        logging.basicConfig(level=logging.INFO)
    elif verbose_level == 2:
        logging.basicConfig(level=logging.WARNING)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    # Log verbosity level
    logger.debug("Verbose mode: Level %d", verbose_level)

    character_set = string.ascii_letters + string.digits + string.punctuation
    if args.S:
        character_set = args.S

    if args.t:
        logger.info("Generating password from template: %s", args.t)
        password = generate_password_from_template(args.t, character_set,logger)
        if args.p:
            logger.debug("Permuting characters of the password")
            password = ''.join(random.sample(password, len(password)))
        logger.info("Generated password: %s", password)
    elif args.n:
        for _ in range(args.c):
            logger.info("Generating password of length %d", args.n)
            password = generate_password(args.n, character_set,logger)
            if args.p:
                logger.debug("Permuting characters of the password")
                password = ''.join(random.sample(password, len(password)))
            logger.info("Generated password: %s", password)
    elif args.f:
        try:
            with open(args.f, 'r') as file:
                patterns = file.readlines()
            for pattern in patterns:
                pattern = pattern.strip()
                logger.info("Generating password from template: %s", pattern)
                password = generate_password_from_template(pattern, character_set,logger)
                if args.p:
                    logger.debug("Permuting characters of the password")
                    password = ''.join(random.sample(password, len(password)))
                logger.info("Generated password: %s", password)
        except IOError:
            print("Error: Failed to open the file.")
            logger.warning("Error: Failed to open the file.: %s", file)
            sys.exit(1)
    else:
        print("Error: No option specified.")
        parser.print_help()


if __name__ == '__main__':
    main()
