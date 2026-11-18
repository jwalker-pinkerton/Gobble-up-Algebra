import math
W,H=24,26
def build():
    g=[['.']*W for _ in range(H)]
    cx=11.5; fy=15.0
    for r in range(H):
        for c in range(W):
            dx=c-cx; dy=(r-fy)*1.05
            d=math.hypot(dx,dy)
            if r<=17 and d<=12.0:
                g[r][c]='R' if d>9.3 else ('O' if d>6.6 else 'Y')
    for r in range(H):
        for c in range(W):
            if ((c-cx)/5.2)**2+((r-15.5)/5.6)**2<=1: g[r][c]='B'
            if ((c-cx)/2.6)**2+((r-17.0)/3.0)**2<=1: g[r][c]='T'
    for r in range(H):
        for c in range(W):
            if ((c-cx)/3.0)**2+((r-5.0)/2.4)**2<=1: g[r][c]='B'
            if 7<=r<=11 and 10<=c<=13: g[r][c]='B'
    g[4][10]='K'; g[4][13]='K'
    g[6][11]='O'; g[6][12]='O'
    g[7][12]='R'; g[8][12]='R'; g[9][12]='R'
    for (r,c) in [(21,9),(22,9),(22,8),(22,10),(21,14),(22,14),(22,13),(22,15)]:
        g[r][c]='O'
    # pumpkins
    for (r,a,b) in [(20,1,4),(21,0,5),(22,1,4),(20,19,22),(21,18,23),(22,19,22)]:
        for c in range(a,b+1): g[r][c]='O'
    g[19][2]='G'; g[19][20]='G'
    for r in (23,24,25):
        for c in range(W): g[r][c]='G'
    return g
COL={'.':'#ffffff','R':'#c0392b','O':'#e67e22','Y':'#f4d03f','B':'#6e3b1e','T':'#d2a679','K':'#111111','G':'#3f8f3a'}
if __name__=='__main__':
    g=build()
    print('\n'.join(''.join(x) for x in g))
    from collections import Counter
    print(Counter(ch for row in g for ch in row))
    from PIL import Image
    im=Image.new('RGB',(W*20,H*20))
    for r in range(H):
        for c in range(W):
            for y in range(20):
                for x in range(20):
                    im.putpixel((c*20+x,r*20+y),tuple(int(COL[g[r][c]][i:i+2],16) for i in (1,3,5)))
    im.save('preview.png')
