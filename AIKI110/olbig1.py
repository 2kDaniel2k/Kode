with open("/aiki110/oblig01/problem.txt", "r") as fil:
        
        liste = []
        for linje in fil:
                liste.extend(linje.strip().split())
        
        bevegelser = {
        N: (0, 1),
        NE: (1, 1),
        E: (1, 0),
        SE: (1, -1),
        S: (0, -1),
        SW: (-1, -1),
        W: (-1, 0),
        NW: (-1, 1),
}

        x = int(liste[0])
        y = int(liste[1])
        orientering = [(x, y)]




        for element in liste[2:]:
                if element in bevegelser:
                        dx, dy = bevegelser[retning]
                        ny_x = orientering[0][0] + dx
                        ny_y = orientering[0][1] + dy
                
                        if 0 <= ny_x <= 7 and 0 <= ny_y <= 7:
                                orientering.append((ny_x, ny_y))
         
                                resultat = orientering[-1]
                                
                                print(resultat)