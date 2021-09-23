import random
l = True
b= []
while l:
    i = random.randint(1, 1000)
    if i == 956:
        l = False

    else:
        for x in b:
            if x == i:
                pass
            else:
                b.append(i)
                print(i)