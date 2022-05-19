file = open("C:\\Users\\sathu\\nlp-stories\\sample_inputs\\dataset\\g02-federalspending.txt")
lines = file.readlines()
for i in range(len(lines)):
    check = lines[0]
    del lines[0]
    for j in range(len(lines)):
        if check == lines[j]:
            print(check)
            break
print("done")