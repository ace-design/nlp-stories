file = open("C:\\Users\\sathu\\nlp-stories\\inputs\\dataset\\g13-planningpoker.txt")
lines = file.readlines()
print("start")
for i in range(len(lines)):
    check = lines[0]
    del lines[0]
    for j in range(len(lines)):
        if check == lines[j]:
            print(check)
            break
print("done")