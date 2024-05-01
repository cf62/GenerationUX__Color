import os
import re
import sys
import csv
import json
import argparse

#
# Application Main Method
#

def main(appname, argv):

   args = get_args(os.path.basename(appname))
   
   with open(args.input, encoding = 'utf8') as file:
      data = json.load(file)

   with open(args.values, newline = '', encoding = 'utf8') as file:
      values = [row for row in csv.reader(file)]
   
   filename, *targets = values.pop(0)

   os.makedirs(args.output, exist_ok=True)

   for name, *subs in values:
      
      path  = os.path.join(args.output, name) + ".json"
      table = dict(zip(targets, subs))
      
      replaced = traverse_and_replace(data, table)
      
      with open(path, "w", encoding = 'utf8') as file:
         json.dump(replaced, file, indent=2, ensure_ascii=False)

#
# Perform the replacement of values in the data object.
#

def traverse_and_replace(data, subs):
   
   def replacer(match):
      return '#' + subs.get(match[1], match[1])
   
   if isinstance(data, dict):
      return dict([(key, traverse_and_replace(datum, subs)) for key, datum in data.items()])
   elif isinstance(data, list):
      return [traverse_and_replace(datum, subs) for datum in data]
   elif isinstance(data, str):
      return re.sub("#(\w+)", replacer, data)
   else:
      return data

#
# Process the command line arguments.
#

def get_args(appname):

   parser = argparse.ArgumentParser(prog=appname, description='performs color value replacements.')

   parser.add_argument('-i', metavar='<json>'   , dest='input' , help='The input JSON file. Default: 0.json', default=here('0.json'))   
   parser.add_argument('-v', metavar='<values>' , dest='values', help='The values CSV file. Default: values.csv', default=here('values.csv'))   
   parser.add_argument('-o', metavar='<output>' , dest='output', help="The output directory. Default: .", default=here('.'))
   
   return parser.parse_args()

#
# Build a path to this file in the application directory.
#

def here(filename):
  
   base = os.path.dirname(__file__)
   return os.path.join(base, filename)

#
# Script entry point.
#

if __name__ == '__main__':

   main(os.path.basename(sys.argv[0]), sys.argv[1:])
