import copy
import sys
from collections import deque
N,M = map(int,input().split())
sr,sc,er,ec = map(int,input().split())
war = []
alive = [1] * (M)

#이거 빠르게 하는 법 찾아보기
lst = list(map(int, input().split()))
for i in range(0,2*M,2):
    war.append((lst[i],lst[i+1]))

#상하좌우
dy = [-1,1,0,0]
dx = [0,0,-1,1]

arr = list(list(map(int,input().split()))for _ in range(N))

def s_shortest_dist(sr,sc,er,ec):
    p = [(sr,sc)]
    q = deque([(sr, sc, p)])
    while q:
        r,c,path = q.popleft()
        if (r,c) == (er,ec):
            return path
        for d in range(4):
            nr,nc = r+dy[d],c+dx[d]
            if 0<=nr<N and 0<=nc<N and arr[nr][nc]==0 and (nr,nc) not in path:
                new_path = path[:]
                new_path.append((nr, nc))
                q.append((nr, nc, new_path))
    return 0

def cnt_war(dir,sr,sc):
    stone_loc = [[0] * N for _ in range(N)]
    visited = [[0] * N for _ in range(N)] #메두사 시선
    # 메두사가 돌 만들기
    if dir == 0:
        l_dir = (-1, -1)
        r_dir = (-1, 1)
    elif dir == 1:
        l_dir = (1, -1)
        r_dir = (1, 1)
    elif dir == 2:
        l_dir = (1, -1)
        r_dir = (-1, -1)
    elif dir == 3:
        l_dir = (-1, 1)
        r_dir = (1, 1)

    q = deque()
    q.append((sr,sc))
    visited[sr][sc] = 1
    while q:
        r,c = q.popleft()
        for i in range(len(war)):
            if war[i] == (r,c) and alive[i] == 1:
                stone_loc[r][c] = 1

        for y, x in [(dy[dir], dx[dir]), l_dir, r_dir]:
            nr, nc = r + y, c + x
            if 0 <= nr < N and 0 <= nc < N and visited[nr][nc] == 0:
                visited[nr][nc] = 1
                q.append((nr, nc))

    # stone_loc, visited에서 숨은 전사 제거
    new_visited = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if stone_loc[i][j] == 1:
                if dir == 0:
                    # 축 기준 왼쪽
                    if j < sc:
                        dir_lst = [(dy[dir], dx[dir]), l_dir]
                    # 같은 축
                    elif j == sc:
                        dir_lst = [(dy[dir], dx[dir])]
                    # 축 기준 오른쪾
                    else:
                        dir_lst = [(dy[dir], dx[dir]), r_dir]
                elif dir == 1:
                    if j < sc:
                        dir_lst = [(dy[dir], dx[dir]), l_dir]
                    elif j == sc:
                        dir_lst = [(dy[dir], dx[dir])]
                    else:
                        dir_lst = [(dy[dir], dx[dir]), r_dir]
                elif dir == 2:
                    if i > sr:
                        dir_lst = [(dy[dir], dx[dir]), l_dir]
                    elif i == sr:
                        dir_lst = [(dy[dir], dx[dir])]
                    else:
                        dir_lst = [(dy[dir], dx[dir]), r_dir]
                elif dir == 3:
                    if i < sr:
                        dir_lst = [(dy[dir], dx[dir]), l_dir]
                    elif i == sr:
                        dir_lst = [(dy[dir], dx[dir])]
                    else:
                        dir_lst = [(dy[dir], dx[dir]), r_dir]
                dq = deque()
                dq.append((i,j))
                new_visited[i][j] = 1
                while dq:
                    r,c = dq.popleft()
                    for y, x in dir_lst:
                        nr, nc = r + y, c + x
                        if (0 <= nr < N and 0 <= nc < N and new_visited[nr][nc] == 0) \
                            or (0 <= nr < N and 0 <= nc < N and stone_loc[nr][nc] == 1):
                            new_visited[nr][nc] = 1
                            dq.append((nr, nc))
                            if stone_loc[nr][nc] == 1:
                                stone_loc[nr][nc] = 0
    #최종 메두사 시선
    for i in range(N):
        for j in range(N):
            if visited[i][j] == 1:
                if new_visited[i][j] == 1:
                    visited[i][j] = 0

    for i in range(N):
        for j in range(N):
            if stone_loc[i][j] == 1:
                visited[i][j] = 1

    visited[sr][sc] = 0

    # stone된 돌 수 세기
    cnt = 0
    for i in range(len(war)):
        r,c = war[i][0],war[i][1]
        if stone_loc[r][c] == 1 and alive[i] == 1:
            cnt += 1
    return visited, cnt, stone_loc

def cal_distance(sr,sc,er,ec):
    dist = abs(sr-er) + abs(sc-ec)
    return dist

#1.메두사 최단거리 찾기
path = s_shortest_dist(sr,sc,er,ec)
if path == 0:
    print(-1)
else:
    #print(path)
    #1. 메두사 이동
    for i in range(1,len(path)):
        sr,sc = path[i]
        for j in range(len(war)):
            if (war[j][0],war[j][1]) == (sr,sc):
                alive[j] = 0
        #마지막일때
        if i == len(path)-1:
            print(0)
            break
        # 2. 메두사 시선
        dir = 0 #메두사 시선
        cnt_w = 0
        dist = [0] * (M)
        attack_cnt = 0
        for d in range(4):
            watch, c, stone = cnt_war(d, sr, sc)
            if c > cnt_w:
                cnt_w = c
                dir = d
                stone_loc = stone
                m_watch = watch
        #print(cnt_w, dir, stone_loc, m_watch)
        # 3. 전사 이동 상하좌우
        for i in range(len(war)):
            wr,wc = war[i]
            if stone_loc[wr][wc] == 0 and alive[i] == 1:
                cur_dist = cal_distance(wr,wc,sr,sc)
                for d in range(4):
                    nr,nc = wr+dy[d],wc+dx[d]
                    if 0<=nr<N and 0<=nc<N and m_watch[nr][nc]==0:
                        new_dist = cal_distance(nr,nc,sr,sc)
                        if new_dist < cur_dist:
                            war[i] = (nr,nc)
                            dist[i] += 1
                            # 4.전사공격
                            if war[i] == (sr,sc):
                                attack_cnt +=1
                                alive[i] = 0
                            break
        #3. 좌우상하
        for i in range(len(war)):
            wr,wc = war[i]
            if stone_loc[wr][wc] == 0 and alive[i] == 1:
                cur_dist = cal_distance(wr,wc,sr,sc)
                for ddy,ddx in [(0,-1),(0,1),(-1,0),(1,0)]:
                    nr,nc = wr+ddy,wc+ddx
                    if 0<=nr<N and 0<=nc<N and m_watch[nr][nc]==0:
                        new_dist = cal_distance(nr,nc,sr,sc)
                        if new_dist < cur_dist:
                            war[i] = (nr,nc)
                            dist[i] += 1
                            # 4.전사공격
                            if war[i] == (sr,sc):
                                attack_cnt +=1
                                alive[i] = 0
                            break
        # 출력
        total_war_dist = sum(dist)
        print(total_war_dist, cnt_w, attack_cnt)
