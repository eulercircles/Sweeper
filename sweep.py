import os
import sys
import json
import argparse

from os import path

class Sweeper(object):
  def __init__(self):
    parser = argparse.ArgumentParser(description='', usage='')
    parser.add_argument('command', type=str, help='')
    args = parser.parse_args(sys.argv[1:2])
    if not hasattr(self, args.command):
      print('Unrecognized command:', args.command)
      parser.print_help()
      exit(1)
    getattr(self, args.command)()

  def clean(self):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-p', '--path', type=str, required=False)
    parser.add_argument('--add', '-a', action='store_true', help='Adds the specified path to the list of saved roots.')
    args = parser.parse_args(sys.argv[2:])

    if not args.path:
      print('Sweeping all roots...')
    else:
      if (args.add):
        print('Adding root to list.')
      print('Sweeping directory...')

  def dirs(self):
    parser = argparse.ArgumentParser(description='', usage='')
    parser.add_argument('-p', '--path', type=str, required=False, help='The path to the root directory.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', action='store_true', help='Adds the specified path to the list of saved root directories.')
    group.add_argument('-r', '--remove', action='store_true', help='Removes the specified path from the list of saved root directories.')
    group.add_argument('-c', '--clear', action='store_true', help='Clears the list of saved root directories.')
    group.add_argument('-l', '--list', action='store_true', help='Displays a list of saved root directories.')
    args = parser.parse_args(sys.argv[2:])

    if(args.add):
      if(not args.path):
        print('Path not specified.')
        parser.print_help()
        exit(1)

      if (not path.exists(args.path)):
        print('Cannot add directory: it does not exist.')
        exit(1)

      # add directory to list of roots
    elif(args.remove):
      if (not args.path):
        print('Path not specified.')
        parser.print_help()
        exit(1)
      
      if (not path.exists(args.path)):
        print('Directory does not exist.')
        parser.print_help()
        exit(1)
      
      # remove directory from list of roots
    elif(args.clear):
      # clear the list of roots
      print ('Clearing roots...')
      
    else:
      print ('Roots:')

  def temps(self):
    parser = argparse.ArgumentParser(description='', usage='')
    parser.add_argument('-n', '--name', type=str, required=False, help='')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', action='store_true', help='')
    group.add_argument('-r', '--remove', action='store_true', help='')
    group.add_argument('-c', '--clear', action='store_true', help='')
    group.add_argument('-l', '--list', action='store_true', help='')
    args = parser.parse_args(sys.argv[2:])



if __name__ == '__main__':
  Sweeper()