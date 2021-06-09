#!/usr/bin/env python3


file_handle = open("trace.txt","r")
file_read = file_handle.read().strip().split("\n")
address_list = []
address_list2 = []
for i in file_read:
    if(i[:8] not in address_list):
        address_list.append(i[:8])
for i in address_list:
    address_list2.append(int(i,16))
address_list2.sort()
count = 0
for i in address_list2:
    for j in file_read:
        if(hex(i) == j[:8]):
            count+=file_read.count(j)
            print(j)
            break
file_handle.close()
