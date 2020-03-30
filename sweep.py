import os
import sys
import yaml
import argparse

from os import path

class Sweeper(object):
  def __init__(self):
    parser = argparse.ArgumentParser(description='', usage='sweep.py <command> [<args>]')
    parser.add_argument('command', type=str, help='')
    args = parser.parse_args(sys.argv[1:2])

    if (not hasattr(self, args.command)) or (str(args.command).startswith('__')):
      print('Unrecognized command:', args.command)
      parser.print_help()
      exit(1)
      
    self.__loadConfig()
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
      if(not str(args.path)):
        print('Path not specified.')
        parser.print_help()
        exit(1)
      if (not path.exists(args.path)):
        print('Cannot add directory: it does not exist.')
        exit(1)
      if (str(args.path) not in self.__config['directories']):
        self.__config['directories'].append(args.path)
        self.__saveConfig()
    
    elif(args.remove):
      if (not args.path):
        print('Path not specified.')
        parser.print_help()
        exit(1)
      if (str(args.path) in self.__config['directories']):
        self.__config['directories'].remove(str(args.path))
        print('Removed directory.')
    
    # Clear the list of directories
    elif(args.clear):
      self.__config['directories'].clear()
      self.__saveConfig()
      print('Directories cleared.')
      
    else:
      for dir in self.__config['directories']:
        print(dir)

  def junk(self):
    parser = argparse.ArgumentParser(description='', usage='')
    parser.add_argument('-n', '--name', type=str, required=False, help='')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', action='store_true', help='')
    group.add_argument('-r', '--remove', action='store_true', help='')
    group.add_argument('-c', '--clear', action='store_true', help='')
    group.add_argument('-l', '--list', action='store_true', help='')
    args = parser.parse_args(sys.argv[2:])

    if (args.add):
      self.__config['junkTypes'].append(args.name)
      self.__saveConfig()
      print('Added junk type.')
    
    elif (args.remove):
      if str(args.name) in self.__config['junkTypes']:
        self.__config['junkTypes'].remove(str(args.name))
        print('Removed junk type.')
        self.__saveConfig()
    
    elif (args.clear):
      self.__config['junkTypes'].clear()
      self.__saveConfig()
      print('Cleared junk types.')
    
    else:
      for junkType in self.__config['junkTypes']:
        print(junkType)

  def __loadConfig(self):
    if (path.exists('config.yml')):
      with open('config.yml', 'r') as file:
        self.__config = yaml.safe_load(file)
    else:
      self.__config = {'directories': [], 'junkTypes': []}

  def __saveConfig(self):
    with open('config.yml', 'w') as file:
      yaml.dump(self.__config, file)

if __name__ == '__main__':
  Sweeper()