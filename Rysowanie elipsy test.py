import matplotlib.pyplot as plt
import numpy as np

def putPixel(x,y,cx,cy,data,kolor=20):
    data[y+cy,x+cx] = kolor
    data[-y+cy,x+cx] = kolor
    data[y+cy,-x+cx] = kolor
    data[-y+cy,-x+cx] = kolor

def elipse(n, m, O, a, b, fill = 1):

    kolor_linii=20
    kolor_tla=230
    
    if max(kolor_linii,kolor_tla)-min(kolor_linii,kolor_tla) < 5:
        data=np.zeros((m,n,3), dtype=np.uint8) #n-os_x m-os_y
        data.fill(0)
        print('Kolor linii i tła powinien bardziej się różnić')
        return data
    

    # ustalam bezpieczny obszar rysowania
    # dla funkcji wypełniającej figurę
    obszar_rysowania=[O[0]-a-2, O[0]+a+2, O[1]-b-2, O[1]+b+2]

    data=np.zeros((m,n,3), dtype=np.uint8) #n-os_x m-os_y
    data.fill(kolor_tla)

    cx,cy= O
    a22=2*a*a
    b22=2*b*b

    # Ustalam granice rysowania figury na odległość 1 piksela od krawędzi
    # dla wartości wykraczających zostaje zwracana czarna tablica
    # zakres obszaru dla tabliczy 100x100 
    # zaczyna się od indeksu 0 i kończy na indeksie 99,
    # a więc dozwolony punkt centrum dla przykładowej elipsy a=20 b=10, to:
    # O=([21-78],[11-88]).

    if (O[0]-a < 1) or (O[0]+a > n-2) or (O[1]-b < 1) or (O[1]+b > m-2):
        data=np.zeros((m,n,3), dtype=np.uint8) #n-os_x m-os_y
        data.fill(0)
        print('Przekroczono granice rysowania')
        return data
    
    #Segment 1. elipsy o poczwórnej symetrii
    x=a
    y=0
    dx=(b**2)*(1-(2*a))
    dy=a**2
    Error=0
    PunktKoncowyX=b22*a
    PunktKoncowyY=0

    while (PunktKoncowyX >= PunktKoncowyY):
        putPixel(x,y,cx,cy,data,kolor_linii)
        y+=1
        PunktKoncowyY+=a22
        Error+=dy
        dy+=a22
        if ((2*Error + dx) > 0):
            x-=1
            PunktKoncowyX-=b22
            Error+=dx
            dx+=b22

    #Segment 2. elipsy o poczwórnej symetrii
    x=0
    y=b
    dx=b*b
    dy=(a**2)*(1-(2*b))
    Error=0

    PunktKoncowyX=0
    PunktKoncowyY=a22*b

    while (PunktKoncowyX <= PunktKoncowyY):
        putPixel(x,y,cx,cy,data,kolor_linii)
        x+=1
        PunktKoncowyX+=b22
        Error+=dx
        dx+=b22
        if ((2*Error+dy)>0):
            y-=1
            PunktKoncowyY-=a22
            Error+=dy
            dy+=a22

    if fill:
        wypelnij(data,obszar_rysowania,kolor_linii,kolor_tla)

    return data

def wypelnij(data,obszar,kolor_linii=20,kolor_tla=240):

    x,y = obszar[0],obszar[2]


    while x < obszar[1]:
        start,end,switch,tlo_po_linii,y=0,0,0,0,0
        lista_start,lista_end=[],[]


        while y < obszar[3]:
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
            
        if len(lista_start)>0:
            for idx in range(len(lista_start)):
                for i in range(lista_start[idx],lista_end[idx]):
                    data[i,x] = kolor_linii
        x+=1
    return data