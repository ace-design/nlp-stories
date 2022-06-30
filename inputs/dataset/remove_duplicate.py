file = open("inputs\\dataset\\g27-culrepo.txt")
lines = file.readlines()
print("start")
for i in range(len(lines)):
    check = lines[0].strip()
    del lines[0]
    for j in range(len(lines)):
        if check == lines[j].strip():
            print(check)
            break
print("done")