import argparse
import secrets
import string
from random import sample, choice
from argparse import ArgumentParser

def printBanner():
    banner = """
    ****************************************************
    * Password generator according to a given template 
    * that supports the CLI interface,be able to work in PIPE and logging
    * (-vvv – show detailed information during processing)
    * Author: @fricker12                               *
    * Date: May 2023                                   *
    * Version: v0.1                                    *
    ****************************************************
    """
    print(banner)
    
    
def Generator():
# Setting up the Argument Parser
parser = ArgumentParser(
    prog='Password Generator.',
    description='Generate any number of passwords with this tool.'
)

# Adding the arguments to the parser
parser.add_argument("-n", "--numbers", default=0, help="Number of digits in the PW", type=int)
parser.add_argument("-l", "--lowercase", default=0, help="Number of lowercase chars in the PW", type=int)