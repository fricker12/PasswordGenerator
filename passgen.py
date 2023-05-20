import argparse
import logging
import random
import re
import string
import sys

#parser = argparse.ArgumentParser(description='Password generator utility')
#parser.add_argument('-t', '--template', help='Password template')
#parser.add_argument('-l', '--length', type=int, default=8, help='Password length')
#parser.add_argument('-u', '--uppercase', action='store_true', help='Include uppercase letters')
#parser.add_argument('-d', '--digits', action='store_true', help='Include digits')
#parser.add_argument('-s', '--symbols', action='store_true', help='Include symbols')
#parser.add_argument('-S', '--set', default='', help='Additional characters to include')
#parser.add_argument('-vvv', '--verbose', action='count', default=0, help='Show detailed information during processing')
#args = parser.parse_args()


parser = argparse.ArgumentParser(description='Password generator utility')
parser.add_argument('-n', '--length', type=int, default=8, help='Set length of password and generate random password from set {small lateral ASCII, big lateral ASCII, digit}')
parser.add_argument('-t', '--template', help='Set template for generate passwords')
parser.add_argument('-f', '--file', help='Getting list of patterns from file and generate for each random password')
parser.add_argument('-c', '--count', type=int, default=1, help='Number of passwords')
parser.add_argument('-S', '--set', default='', help='Character set')
parser.add_argument('-p', '--permute', action='store_true', help='Randomly permute characters of password')
parser.add_argument('-vvv', '--verbose', action='count', default=0, help='Verbose mode (-v |-vv |-vvv )')
args = parser.parse_args()

def generate_password(template: str, charset: str, permute: bool) -> str:
    if template:
        password = ''
        matches = re.findall(r'(\w)\{(\d+)\}|\[(.+?)\]\{(\d+)\}', template)
        for match in matches:
            if match[0]:
                placeholder, n = match[0], match[1]
                password += placeholder * int(n)
            else:
                custom_set, n = match[2], match[3]
                custom_set = re.sub(r'\^(.)', '', custom_set)
                password += ''.join(random.choice(custom_set) for _ in range(int(n)))
        if permute:
            password = ''.join(random.sample(password, len(password)))
        return password
    else:
        return ''.join(random.choice(charset) for _ in range(args.length))


#def generate_password(template: str, charset: str) -> str:
#    if template:
#        matches = re.findall(r'(\w)\{(\d+)\}', template)
#        for match in matches:
#            placeholder, n = match
#            template = template.replace(f'{placeholder}{{{n}}}', placeholder * int(n))
#        return template
#    else:
#        return ''.join(random.choice(charset) for _ in range(args.length))
    
#def generate_password(template: str,charset: str) -> str:
#    password = ''
#    for match in re.finditer(r'(\[.+?\]|\w)\{?(\d+)?\}?', template):
#        char_set, count = match.groups()
#        if count:
#            count = int(count)
#        else:
#            count = 1
#        if char_set.startswith('[') and char_set.endswith(']'):
#            char_set = char_set[1:-1]
#            char_set = re.sub(r'\^(.)', '', char_set)
#            char_set = re.sub(r'\\(.)', r'\1', char_set)
#            if 'd' in char_set:
#                char_set = char_set.replace('d', string.digits)
#            if 'p' in char_set:
#                char_set = char_set.replace('p', string.punctuation)
#            if 'u' in char_set:
#                char_set = char_set.replace('u', string.ascii_uppercase)
#            if '_' in char_set:
#                char_set = char_set.replace('_', ' ')
#        elif char_set == 'd':
#            char_set = string.digits
#        elif char_set == 'u':
#            char_set = string.ascii_uppercase
#        password += ''.join(random.choices(char_set, k=count))
#    return password

#def generate_password(template: str,charset: str) -> str:
#    password = ''
#    for match in re.finditer(r'((?:\[.+?\]|\w|\\.)\{?\d*\}?)', template):
#        char_set = match.group(1)
#        count = 1
#        if '{' in char_set and '}' in char_set:
#            count = int(char_set[char_set.index('{') + 1:char_set.index('}')])
#            char_set = char_set[:char_set.index('{')]
#        if char_set.startswith('[') and char_set.endswith(']'):
#            char_set = char_set[1:-1]
#            char_set = re.sub(r'\^(.)', '', char_set)
#            char_set = re.sub(r'\\(.)', r'\1', char_set)
#            if 'd' in char_set:
#                char_set = char_set.replace('d', string.digits)
#            if 'l' in char_set:
#                char_set = char_set.replace('l', string.ascii_lowercase)
#            if 'L' in char_set:
#                char_set = char_set.replace('L', string.ascii_uppercase+string.ascii_lowercase)
#            if 'u' in char_set:
#                char_set = char_set.replace('u', string.ascii_uppercase)
#            if 'p' in char_set:
#                char_set = char_set.replace('p', string.punctuation)
#            if '_' in char_set:
#                char_set = char_set.replace('_', ' ')
#        elif char_set == 'd':
#            char_set = string.digits
#        elif char_set == 'l':
#            char_set = string.ascii_lowercase
#        elif char_set == 'L':
#            char_set= string.ascii_uppercase + string.ascii_lowercase
#        elif char_set == 'u':
#            char_set = string.ascii_uppercase
#        elif char_set == 'p':
#            char_set = string.punctuation
#        elif '\\' in char_set:
#            char_set = re.sub(r'\\(.)', r'\1', char_set)
#        password += ''.join(random.choices(char_set, k=count))
#    return password

def main():
    
    log_level = logging.WARNING - args.verbose * 10
    logging.basicConfig(level=log_level)

    charset = args.set or string.ascii_letters + string.digits

    logging.debug(f'Charset: {charset}')

    templates = []
    if args.template:
        templates.append(args.template)
    elif args.file:
        with open(args.file) as f:
            templates.extend(f.read().splitlines())

    for template in templates:
        for _ in range(args.count):
            password = generate_password(template, charset, args.permute)
            print(password)
    
    #log_level = logging.WARNING - args.verbose * 10
    #logging.basicConfig(level=log_level)

    #charset = args.set
    #if args.uppercase:
    #    charset += string.ascii_uppercase
    #if args.digits:
    #    charset += string.digits
    #if args.symbols:
    #    charset += string.punctuation

    #logging.debug(f'Charset: {charset}')

    #password = generate_password(args.template, charset)
    #print(password)


  
if __name__ == "__main__":
    main()