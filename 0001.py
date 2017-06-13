#! /usr/bin/python3

import  random

collection = set()

while len(collection) < 200:
    collection.add(random.randint(1000, 9999))

with open('coupon_code', 'w') as f:
    for num in collection:
        f.write(str(num) + '\n')


