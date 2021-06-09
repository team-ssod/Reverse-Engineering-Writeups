#!/usr/bin/env python3



file_handle = open("trace.txt","r")
file_read = file_handle.read().strip().split("\n")
count = 0
counter = 0
while(counter <= 60):
    for i in file_read:
        if('cmp al, bl' in i):
            count+=1
        elif('dec rdx' in i):
            print(count-1)
            count = 0
            counter+=1
file_handle.close()
