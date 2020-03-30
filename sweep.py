
import yaml
import argparse

from os import path, scandir, listdir, rmdir
from shutil import rmtree
from sys import argv
from termcolor import colored, cprint

class Sweeper(object):
  def __init__(self):
    parser = argparse.ArgumentParser(description='', usage='''sweep.py <command> [<args>]
Commands:
  clean: Clean one or multiple directories of junk
  dirs: Modify saved directories
  junk: Modify saved junk types''')
    parser.add_argument('command', type=str, help='')
    args = parser.parse_args(argv[1:2])

    if (not hasattr(self, args.command)) or (str(args.command).startswith('__')):
      self.__printError("Unrecognized command: " + "'" + str(args.command) + "'")
      parser.print_help()
      exit(1)
      
    self.__loadConfig()
    getattr(self, args.command)()

  def clean(self):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-p', '--path', type=str, required=False)
    parser.add_argument('--add', '-a', action='store_true', help="Adds the specified path to the list of saved roots.")
    args = parser.parse_args(argv[2:])

    # Handle full clean
    if not args.path:
      for dir in self.__config['directories']:
        self.__sweepDirectory(dir)
    
    # Handle specified path
    else:
      if (args.add):
        self.__addDirectory(str(args.path))
      self.__printInfo('Sweeping directory...')

  def dirs(self):
    parser = argparse.ArgumentParser(description='Accesses list of saved root directories.', usage='')
    parser.add_argument('-p', '--path', type=str, required=False, help='The path to the root directory.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', action='store_true', help='Adds the specified path to the list of saved root directories.')
    group.add_argument('-r', '--remove', action='store_true', help='Removes the specified path from the list of saved root directories.')
    group.add_argument('-c', '--clear', action='store_true', help='Clears the list of saved root directories.')
    group.add_argument('-l', '--list', action='store_true', help='Displays a list of saved root directories.')
    args = parser.parse_args(argv[2:])

    if(args.add):
      if(not str(args.path)):
        self.__printError('Path not specified.')
        parser.print_help()
        exit(1)
      if (self.__addDirectory(str(args.path))): exit(0)
      else: exit(1)
    
    elif(args.remove):
      if (not args.path):
        self.__printError("Please specify a path to a directory.")
        parser.print_help()
        exit(1)
      if (self.__removeDirectory(str(args.path))): exit(0)
      else: exit(1)
    
    # Clear the list of directories
    elif(args.clear):
      if (self.__clearDirectories()): exit(0)
      else: exit(1)
      
    else:
      if (len(self.__config['directories']) == 0):
        self.__printWarn("No saved directories. It's a good idea to save directories. Saving directories saves work.")
      else:
        self.__printInfo("Saved directories:")
        for directory in self.__config['directories']:
          cprint("\t" + "'" + directory + "'", 'blue')

  def junk(self):
    parser = argparse.ArgumentParser(description='Accesses list of saved junk subdirectories and filetypes', usage='')
    parser.add_argument('-n', '--name', type=str, required=False, help='')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', action='store_true', help='')
    group.add_argument('-r', '--remove', action='store_true', help='')
    group.add_argument('-c', '--clear', action='store_true', help='')
    group.add_argument('-l', '--list', action='store_true', help='')
    args = parser.parse_args(argv[2:])

    # Add junk type
    if (args.add):
      if (not str(args.name)):
        self.__printError("Junk type not specified.")
        parser.print_help()
        exit(1)
      if (self.__addJunkType(str(args.name))):
        exit(0)
    
    # Remove junk type
    elif (args.remove):
      if str(args.name) in self.__config['junkTypes']:
        self.__config['junkTypes'].remove(str(args.name))
        self.__saveConfig()
        self.__printSuccess('Removed junk type from list.')
    
    # Clear junk types
    elif (args.clear):
      self.__config['junkTypes'].clear()
      self.__saveConfig()
      self.__printSuccess('Cleared junk types.')
    
    # List junk types
    else:
      if (len(self.__config['junkTypes']) == 0):
        self.__printWarn("No saved junk types. It's a good idea to save junk types. Saving junk types saves work.")
      else:
        self.__printInfo("Saved junk types:")
        for junkType in self.__config['junkTypes']:
          cprint("\t" + "'" + junkType + "'", 'blue')

  def __sweepDirectory(self, dirPath):
    self.__printInfo("Attempting to clean " + "'" + str(dirPath) + "':")
    if (not path.exists(str(dirPath))):
      self.__printError("Directory does not exist.")
      return False

    junkDirectories = self.__getSubdirectories(str(dirPath))   
    if (len(junkDirectories) == 0):
      self.__printSuccess("\tIt looks like everything's already clean.")
    else:
      cleaned = 0
      for junkDirectory in junkDirectories:
        try:
          rmtree(junkDirectory)
          cleaned += 1
          self.__printInfo("\tDeleted " + junkDirectory)
        except PermissionError as error:
          self.__printError(error)
      self.__printSuccess("Cleaned " + str(cleaned) + " junk directories.")
    return True

  def __loadConfig(self):
    if (path.exists('config.yml')):
      with open('config.yml', 'r') as file:
        self.__config = yaml.safe_load(file)
    else:
      self.__config = {'directories': [], 'junkTypes': []}

  def __saveConfig(self):
    with open('config.yml', 'w') as file:
      yaml.dump(self.__config, file)

  def __getSubdirectories(self, directory):
    results = []
    entries = scandir(directory)
    for entry in entries:
      # handle directories
      if (entry.is_dir()):
        if (entry.name in self.__config['junkTypes']):
          results.append(str(entry.path))
        else:
          results.extend(self.__getSubdirectories(str(entry.path)))
      
      # handle files
    return results

  def __addDirectory(self, dirPath):
    if (not path.exists(dirPath)):
      self.__printError("Cannot add directory. Directory does not exist.")
      return False
    elif (not dirPath in self.__config['directories']):
      self.__config['directories'].append(dirPath)
      self.__saveConfig()
      self.__printSuccess("Directory added to list.")
      return True
  
  def __removeDirectory(self, dirPath):
    if (str(dirPath) in self.__config['directories']):
      self.__config['directories'].remove(str(dirPath))
      self.__saveConfig()
      self.__printSuccess("Directory removed from list.")
      return True
  
  def __clearDirectories(self):
    self.__config['directories'].clear()
    self.__saveConfig()
    self.__printSuccess('List of saved directories cleared.')
    return True
  
  def __addJunkType(self, name):
    if (not str(name)):
      self.__printDebug("Invalid junk type.")
      return False
    if (str(name) not in self.__config['junkTypes']):
      self.__config['junkTypes'].append(str(name))
      self.__saveConfig()
      self.__printSuccess("Added junk type to list.")
      return True
    else:
      self.__printInfo("Junk type already saved.")
      return True
  
  def __removeJunkType(self, name):
    raise NotImplementedError
  
  def __clearJunkTypes(self):
    raise NotImplementedError

  def __printError(self, error):
    cprint(str(error), 'red', attrs=['bold'])
  
  def __printInfo(self, info):
    cprint(str(info), 'white')
  
  def __printWarn(self, warning):
    cprint(str(warning), 'yellow', attrs=['bold'])
  
  def __printSuccess(self, result):
    cprint(str(result), 'green', attrs=['bold'])

  def __printDebug(self, message):
    cprint("[DEBUG]: " + str(message), 'yellow', 'on_cyan')

if __name__ == '__main__':
  Sweeper()