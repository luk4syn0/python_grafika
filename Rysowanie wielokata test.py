import matplotlib.pyplot as plt
import numpy as np
import math

def odleglosc_punktu_od_prostej(x, y, A, B, C):
    odleglosc = abs(A * x + B * y + C) / math.sqrt(A**2 + B**2)
    return odleglosc

def LiniaA(P1,P2,data,rozmiar_x,rozmiar_y,kolor_linii):
    # Można użyć tej funkcji do rysowania linii aa, dla niewypełnionej figury
    # i daje to pewne efekty
    xp,yp = P1
    xk,yk = P2
    

    A = yk-yp
    B = xp-xk
    C = xk*yp-xp*yk
    y=yp
    for x in range(min(xp,xk),max(xp,xk)+1,1):
        if (x>=rozmiar_x or y>=rozmiar_y):
            break
        else:
            for y in range(min(yp,yk),max(yp,yk)+1):
                d=odleglosc_punktu_od_prostej(x,y,A,B,C)
                if d<1:
                    data[y,x]=kolor_linii
                      
    
    return data


def Linia(P1,P2,data,kolor_linii):
    # Druga wersja rysowania linii - bresenham, cienka, bardziej ostra na końcach.
    # Momentami dziwnie postrzępiona.
    x1, y1 = P1
    x2, y2 = P2

    dlugosc_linii = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
    dx = (x2 - x1) / dlugosc_linii
    dy = (y2 - y1) / dlugosc_linii

    for i in range(dlugosc_linii + 1):
        x = int(x1 + i * dx)
        y = int(y1 + i * dy)
        # print(x,y)
        # data[x][y] = 0
        data[y,x]=kolor_linii
    return data

def LiniaB(P1,P2,data,kolor_linii):  

    # Najlepiej wyglądająca linia w porównaniu do poprzednich,
    # Ale ten kod... przynajmniej w miarę działa :)

    xp,yp = P1
    xk,yk = P2

    if abs(yk-yp)==0 and abs(xk-xp)==0:
        print("if")
        data[xp,xk] = kolor_linii
        
    elif abs(yk-yp)>abs(xk-xp):
        
        if yp>yk:
            o=yp
            yp=yk
            yk=o
            
            o=xp
            xp=xk
            xk=o
        
        a = (xk-xp)/(yk-yp)
        # print(a)
        # print("elif")
        for y in range(yp,yk+1,1):
            
            x = xp + a*(y-yp)
            # print(f'{x},{y}')
            if (x>=100 or y>=100):
                break
            else:
                data[int(round(y)),int(round(x))] = kolor_linii

    else:  
        if xp>xk:
            o=xp
            xp=xk
            xk=o
            
            o=yp
            yp=yk
            yk=o
             
        a = (yk-yp)/(xk-xp)
        
        for x in range(xp,xk+1,1):
            y = yp + a*(x-xp)
            if (x>=100 or y>=100):
                break
            else:
                data[int(round(y)),int(round(x))] = kolor_linii

    return data

def wypelnij(data,kolor_linii=20,kolor_tla=240):
    x,y = 0,0
    while x < len(data[0]):
        start,end,switch,tlo_po_linii,y=0,0,0,0,0
        lista_start,lista_end=[],[]


        while y < len(data[1]):

            # Wypelnianie figury tym sposobem działa tylko w przypadku gdy mamy
            # parzystą ilość wystąpień koloru linii przerwanego
            # wystąpieniami koloru tła.

            # Prymitywne, w swoim zamyśle oraz bierze pod uwage całą przestrzeń a nie
            # tylko wybrany wycinek gdzie znajduje się figura jak w następnej wersji.

            # Problem pojawia się dla figur przecinających się, ale
            # tematem tego zadania jest pozbycie się w ogólności wystąpień
            # tego typu.

            # Kilka założeń:
            # Switch to wyznacznik wystąpienia koloru linii, na
            # początku równoznaczny z początkiem obszaru figury start.
            # Rozpoznawany w warunku elif oraz zmieniany gdy natrafimy w
            # Końcu na kolor tła. Zmieniany jest wtedy parametr
            # tlo_po_linii, a oznacza on wejście do wnętrze figury.
            # Na koniec sprawdzamy czy nie nastąpiło ponowne wystąpienie
            # linii i w rezultacie wyjście poza nią. Oznaczamy to jako end.

            if data[y,x][0] != kolor_tla:
                switch=1
                if tlo_po_linii==0:
                    start=y

            elif switch==1 and data[y,x][0] == kolor_tla: 
                tlo_po_linii+=1
                switch=0


            if tlo_po_linii==2:

                end=y-1
                lista_start.append(start)
                lista_end.append(end)
                tlo_po_linii=0
                switch=0
            
            

            y+=1

        #Pozostałość po próbie rozważenia figury przecinającej się. Ale działa :)  
            
        if len(lista_start)>0:
            # print(f'start {lista_start}')
            # print(f'end {lista_end}')
            for idx in range(len(lista_start)):
                for i in range(lista_start[idx],lista_end[idx]):
                    data[i,x] = kolor_linii
        x+=1
    return data

def iloczyn_wektorowy(X, Y, Z):
    x1, y1 = Z[0] - X[0], Z[1] - X[1]
    x2, y2 = Y[0] - X[0], Y[1] - X[1]
    return x1 * y2 - x2 * y1

def sprawdz(X, Y, Z):
    return (min(X[0], Y[0]) <= Z[0] <= max(X[0], Y[0])
            and min(X[1], Y[1]) <= Z[1] <= max(X[1], Y[1]))

def czy_przecinaja(A, B, C, D):
    
    #Algorytm z pomocą artykułu na algorytm.edu.pl
    v1 = iloczyn_wektorowy(C, D, A)
    v2 = iloczyn_wektorowy(C, D, B)
    v3 = iloczyn_wektorowy(A, B, C)
    v4 = iloczyn_wektorowy(A, B, D)

    if ((v1 > 0 and v2 < 0 or v1 < 0 and v2 > 0)
        and (v3 > 0 and v4 < 0 or v3 < 0 and v4 > 0)):
        return True

    if v1 == 0 and sprawdz(C, D, A):
        return True
    if v2 == 0 and sprawdz(C, D, B):
        return True
    if v3 == 0 and sprawdz(A, B, C):
        return True
    if v4 == 0 and sprawdz(A, B, D):
        return True
    return False
                

def quadrilateral(m,n,P1,P2,P3,P4,fill=1):

    # Na początek sprawdzamy czy przeciwległe odcinki się przecinają
    # Aby wykryć nieprawidłowość w budowie czworokąta

    if ((P1[0] < 0 or P1[1] < 0) or (P1[0] >= n or P1[1] >= m) or
        (P2[0] < 0 or P2[1] < 0) or (P2[0] >= n or P2[1] >= m) or
        (P3[0] < 0 or P3[1] < 0) or (P3[0] >= n or P3[1] >= m) or
        (P4[0] < 0 or P4[1] < 0) or (P4[0] >= n or P4[1] >= m)):
        data=np.zeros((m,n,3), dtype=np.uint8)
        data.fill(0)
        print('Podaj linie które znajdują się w obszarze rysowania')
        return data
    

    if czy_przecinaja(P1,P2,P3,P4) or czy_przecinaja(P2,P3,P1,P4):
        data=np.zeros((m,n,3), dtype=np.uint8)
        data.fill(0)
        return data
    
    kolor_linii = 30
    kolor_tla = 210
    
    if max(kolor_linii,kolor_tla)-min(kolor_linii,kolor_tla) < 5:
        data=np.zeros((m,n,3), dtype=np.uint8) #n-os_x m-os_y
        data.fill(0)
        print('Kolor linii i tła powinien bardziej się różnić')
        return data

    data=np.zeros((m,n,3), dtype=np.uint8)
    data.fill(kolor_tla)

    # x1, y1 = P1
    # x2, y2 = P2
    # x3, y3 = P3
    # x4, y4 = P4

    lista_wierzcholkow=[P1,P2,P3,P4]

    for idx_wierzcholek in range(len(lista_wierzcholkow)-1):
        # print(lista_wierzcholkow[idx_wierzcholek])
        # LiniaA(lista_wierzcholkow[idx_wierzcholek],lista_wierzcholkow[idx_wierzcholek+1],data,m,n,kolor_linii)
        # Linia(lista_wierzcholkow[idx_wierzcholek],lista_wierzcholkow[idx_wierzcholek+1],data,kolor_linii)
        LiniaB(lista_wierzcholkow[idx_wierzcholek],lista_wierzcholkow[idx_wierzcholek+1],data,kolor_linii)
    # LiniaA(lista_wierzcholkow[-1],lista_wierzcholkow[0],data,m,n,kolor_linii)
    # Linia(lista_wierzcholkow[-1],lista_wierzcholkow[0],data,kolor_linii)
    LiniaB(lista_wierzcholkow[-1],lista_wierzcholkow[0],data,kolor_linii)

    if fill==1:
        wypelnij(data,kolor_linii,kolor_tla)

    return data