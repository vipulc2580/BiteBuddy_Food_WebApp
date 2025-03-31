from datetime import time

length=0
hours_list=[]
for h in range(0, 24):
    for m in range(0, 31, 30):
        length+=1
        hours_list.append((time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')))

print(hours_list)