# someetimes some folders don't exist in a sequence
# for example, in folders from 5450 to 5550, folders 5422, 5438, and 5447 don't exsit
# that means i need make a list of them to iterate through in main.py
# so i just use this file for whenever i have to do that

nums = []

for i in range(5450, 5550):
    if i == 5422 or i == 5438 or i == 5447:
        continue
    nums.append(i)

print(nums)