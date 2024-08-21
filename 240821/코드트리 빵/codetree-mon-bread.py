from collections import deque

'''
s1, s2, s3: 편의점
p1, p2, p3: 사람좌표
time
while True:
    if s1==p1 and s2==p2 and s3==p3:
        break
    
    #1.사람 최단거리 이동
    #2.편의점 도착
    #3.베이스캠프로 들어가기
'''


N, M = map(int, input().split())
arr = [[0]*(N+1) for _ in range(N+1)]
for i in range(1,N+1):
    arr[i][1:] = map(int,input().split())

p = [(0, 0) for _ in range(M+1)]
s = [(0,0)]*(M+1)

for i in range(1,M+1):
    s[i] = tuple(map(int, input().split()))
time = 0
arrive = set()
found_basement = set()

def bfs(i,j,m):
    q = deque()
    sr, sc = s[m]
    q.append((i,j))
    visited = [[0]*(N+1) for _ in range(N+1)]
    visited[i][j] = 1
    min_dist = 0
    while q:
        pr,pc = q.popleft()
        min_dist+=1
        if pr == sr and pc == sc:
            return visited[pr][pc]-1
        for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            nr = pr + dy
            nc = pc + dx
            if 1<=nr<=N and 1<=nc<=N and arr[nr][nc] != -1 and visited[nr][nc] ==0:
                visited[nr][nc] = visited[pr][pc]+1
                q.append((nr,nc))


    return 100


def move(m):
    pr, pc = p[m]  # 현재 위치
    sr, sc = s[m]  # 목표 위치

    # BFS로 sr, sc까지의 최단 거리 계산
    q = deque()
    q.append((sr, sc))
    distance = [[-1] * (N + 1) for _ in range(N + 1)]
    distance[sr][sc] = 0

    while q:
        cr, cc = q.popleft()
        for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            nr = cr + dy
            nc = cc + dx
            if 1 <= nr <= N and 1 <= nc <= N and arr[nr][nc] != -1 and distance[nr][nc] == -1:
                distance[nr][nc] = distance[cr][cc] + 1
                q.append((nr, nc))

    # pr, pc에서 sr, sc까지의 최단 거리로 한 칸 이동
    best_move = (pr, pc)
    min_dist = float('inf')

    for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        nr = pr + dy
        nc = pc + dx
        if 1 <= nr <= N and 1 <= nc <= N and arr[nr][nc] != -1:
            if distance[nr][nc] != -1 and distance[nr][nc] < min_dist:
                min_dist = distance[nr][nc]
                best_move = (nr, nc)

    return best_move



def find_basecamp(m):
    min_dist=100
    min_r = 0
    min_c = 0
    for i in range(1,N+1):
        for j in range(1,N+1):
            if arr[i][j] != 1:
                continue
            if arr[i][j] == -1:
                continue
            bfs_dist = bfs(i,j,m)
            if bfs_dist  < min_dist or (bfs_dist  == min_dist and i<min_r) or \
                (bfs_dist  == min_dist and i==min_r and j <min_c ):
                min_r = i
                min_c = j
                min_dist = bfs_dist

    return (min_r,min_c)





while True:
    if len(arrive) == M:
        break
    time += 1
    for m in range(1, M+1):

        #3번 베이스먼트 찾기
        if time<m:
            continue
        if m in arrive:
            continue
        if p[m] == (0,0):
            br,bc = find_basecamp(m)
            found_basement.add(m)
            #arr[br][bc] = -1
            p[m] = (br,bc)
            continue
        else:
            p[m] = move(m)
    for m in range(1, M+1):
        pr, pc = p[m]
        #1,2번 편의점으로 이동
        if m in found_basement:
            arr[pr][pc] = -1  # 베이스먼트 도착
            found_basement.remove(m)
        if p[m] == s[m]:
            arr[pr][pc] = -1  # 편의점 도착
            arrive.add(m)
            continue

 
print(time)