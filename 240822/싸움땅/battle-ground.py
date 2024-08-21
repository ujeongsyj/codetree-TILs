N,M,K = map(int, input().split())
v = [[[] for _ in range(N + 1)] for _ in range(N + 1)] #총 보드
for i in range(1, N+1):
    values = map(int, input().split())
    for j, value in enumerate(values, start=1):
        if value != 0:
            v[i][j].append(value)


p_loc = [(0,0) for _ in range(M+1)]
p_dir = [0]*(M+1)
p_gun = [0]*(M+1)
init_power = [0]*(M+1)
point = [0]*(M+1)
dy = [-1,0,1,0]
dx = [0,1,0,-1]

for i in range(1,M+1):
    pr,pc,p_dir[i],init_power[i] = map(int,input().split())
    p_loc[i] = (pr,pc)

def player_move(m):
    pr,pc = p_loc[m]
    d = p_dir[m]
    nr = pr + dy[d]
    nc = pc + dx[d]
    if nr<1 or nr>N or nc<1 or nc>N:
        if d == 0: d=2
        elif d==1: d=3
        elif d==3: d=1
        else: d=0
        p_dir[m] = d
    nr = pr + dy[d]
    nc = pc + dx[d]
    p_loc[m] = (nr,nc)

def get_gun(m,v):
    max_gun = max(v)
    if p_gun[m] == 0:
        p_gun[m] = max_gun
        v.remove(max_gun)
    else:
        if p_gun[m]<max_gun:
            v.append(p_gun[m])
            p_gun[m] = max_gun
            v.remove(max_gun)


def fight(other, m):
    global point
    other_power = init_power[other]+p_gun[other]
    m_power = init_power[m]+p_gun[m]
    if other_power > m_power or (other_power==m_power and init_power[other]>init_power[m]):
        winner = other
        loser = m
        p = other_power - m_power
    else:
        winner = m
        loser = other
        p = m_power - other_power


    return winner, loser,p

def loser_move(loser):
    pr, pc = p_loc[loser]
    d = p_dir[loser]

    while True:
        nr = pr + dy[d % 4]
        nc = pc + dx[d % 4]
        if 1 <= nr <= N and 1 <= nc <= N and p_loc.count((nr, nc)) == 0:
            break
        d+=1


    p_dir[loser] = d % 4
    p_loc[loser] = (nr,nc)
    if len(v[nr][nc]) != 0:
        get_gun(loser, v[nr][nc])


for k in range(K):
    #move
    for m in range(1,M+1):
        # 한칸 이동
        player_move(m)
        r,c = p_loc[m]
        other_player = 0
        # 다른 플레이어 검사
        for i in range(1,M+1):
            if i == m:
                continue
            if p_loc[i] == p_loc[m]:
                other_player = i

        if other_player == 0:
            if len(v[r][c]) != 0 :
                get_gun(m,v[r][c])
        else:
            winner, loser,p = fight(other_player,m)
            point[winner] += p #이긴사람 포인트 획득
            # 진사람 총 내려놓고 이동
            lr,lc = p_loc[loser]
            if p_gun[loser] != 0:
                v[lr][lc].append(p_gun[loser])
            p_gun[loser] = 0
            loser_move(loser)
            #이긴사람 총획득
            wr,wc = p_loc[winner]
            if len(v[wr][wc]) != 0:
                get_gun(winner,v[wr][wc])

for i in range(1,M+1):
    print(point[i], end=" ")