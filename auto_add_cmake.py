#! /usr/bin/python3
import os

file_names = os.listdir()
file_names = ' '.join(file_names)

name_list = open('name_list', 'w')
name_list.write(file_names)



