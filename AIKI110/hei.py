
hei = 10

def primtall(hei):
    liste = [2]
    for i in range(3, hei + 1):
        var = False
        for j in liste:
            if i % j == 0:
                var = True
        if not var:
            liste.append(i)
    print(liste)

    hade = len(liste)
    print(f"{hade} primtall som er mindre enn 10")

primtall(hei)