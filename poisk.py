words = [['','','','','','','','','','','','','','','',],
           ['','','','','','','','','','','','','','','',],
           ['','','','','','','','','','','','','','','',],
           ['','','','','','','','','','','','','','','',],
           ['','','','','','','о','','к','','','','','','',],
           ['','','','','','','т','и','р','а','н','','','','',],
           ['','','','','','','в','','е','','','','','','',],
           ['','','','','а','н','е','к','д','о','т','','','','',],
           ['','','','','','','т','','о','','','','','','',],
           ['','','','','','','','','','','','','','','',],
           ['','','','','','','','','','','','','','','',],
           ['','','','','','','','','','','','','','','',],
           ['','','','','','','','','','','','','','','',],
           ['','','','','','','','','','','','','','','',],
           ['','','','','','','','','','','','','','','',]]
newkoord = [[4,6],[4,8],[4,9],[4,10]]
newletters = ['б','т','о','н']
#движение по оси x = 1
#движение по оси y = 2
def prov(words,x,y,napr,newkoord):
    flag = 0
    if (napr == 2) and (y != 14) :
        if (y != 0):
            if (words[y-1][x] == '') and (words[y+1][x] != ''):
                flag = 1
        else:
            if (words[y+1][x] != ''):
                flag = 1
    if (napr == 1) and (x != 14):
        if (x != 0):
            if (words[y][x-1] == '') and (words[y][x+1] != ''):
                flag = 1
        else:
            if (words[y][x+1] != ''):
                flag = 1
    if (flag == 1):
        return(schit(words,x,y,napr,newkoord))
    else:
        return(['',0])

def schit(words,x,y,napr,newkoord):
    s = ''
    newword = 0
    if (napr == 2):
        a=1
        while (a != 0):
            koord = [x,y]
            if (koord in newkoord):
                newword = 1
            s = s + words[y][x]
            if (y == 14):
                a = 0
            else:
                if (words[y+1][x] == ''):
                    a = 0
            y = y + 1
    else:
        a=1
        while (a != 0):
            koord = [x,y]
            if (koord in newkoord):
                newword = 1
            s = s + words[y][x]
            if (x == 14):
                a = 0
            else:
                if (words[y][x+1] == ''):
                    a = 0
            x = x + 1
    return([s,newword])
def pasteletters(words, newkoord, newletters):
    for i in range(len(newkoord)):
        words[newkoord[i][1]][newkoord[i][0]] = newletters[i]
    return(words)
                

def serch(words, newkoord, newletters):
    words = pasteletters(words, newkoord, newletters)
    for i in range(len(words)):
        for j in range(len(words[i])):
            if (words[i][j] != ''):
                slx = prov(words,j,i,1,newkoord)
                sly = prov(words,j,i,2,newkoord)
                if (slx[1] == 1):
                    slx[0] = slx[0] + 'new'
                if (sly[1] == 1):
                    sly[0] = sly[0] + 'new'
                if (slx[0] != ''):
                    print(slx[0])
                if (sly[0] != ''):
                    print(sly[0])
            
