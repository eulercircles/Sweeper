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
      print('Unrecognized command')
      parser.print_help()
      exit(1)
    getattr(self, args.command)()

  def clean(self):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--root', '-r', required=False)
    parser.add_argument('--add', '-a', required=False)
    args = parser.parse_args(sys.argv[2:])

    if not args.root: # no root argument
      print('Sweeping all roots...')
    else:
      if (args.add):
        print('Adding root to list.')
      print('Sweeping roots...')

  def roots(self):
    parser = argparse.ArgumentParser(description='', usage='')
    parser.add_argument('--path', '-p', required=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--add', '-a', required=False)
    group.add_argument('--remove', '-r', required=False)
    group.add_argument('--clear', '-c', required=False)
    args = parser.parse_args(sys.argv[2:])

    if(args.add):
      if(not args.path):
        print('Path not specified.')
        parser.print_help()
        exit(1)

      if (not path.exists(args.path)):
        print('Directory does not exist.')
        parser.print_help()
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
      # list the roots
      print ('Roots:')
  
  def temps(self):
    parser = argparse.ArgumentParser(description='', usage='')
    parser.add_argument('--name', '-n', required=False)

if __name__ == '__main__':
  Sweeper()