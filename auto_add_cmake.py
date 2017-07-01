#! /usr/bin/python3
import os

file_names = [ name for name in os.listdir() if name.endswith(('.h', '.cpp'))]
file_names = ' '.join(file_names)

name_list = open('name_list', 'w')
name_list.write(file_names)



