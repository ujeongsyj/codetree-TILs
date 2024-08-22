import copy

N,M,K,C = map(int, input().split())
tree = [[0]*(N+1) for _ in range(N+1)]
for i in range(1,N+1):
    tree[i][1:] = map(int, input().split())

grow = [[(0,0) for _ in range(N+1)] for _ in range(N+1)]



herbicide = [[0]*(N+1) for _ in range(N+1)]
kill_tree_cnt = 0


#인접나무 수 세기 + 정보 저장
def count(r,c):
    tree_cnt = 0
    breed_tree_cnt = 0
    for (dy,dx) in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr = r + dy
        nc = c + dx
        if 1<=nr<=N and 1<=nc<=N and tree[nr][nc] > 0:
            tree_cnt += 1
        if 1 <= nr <= N and 1 <= nc <= N and tree[nr][nc] == 0 and herbicide[nr][nc] == 0:
            breed_tree_cnt += 1
    return tree_cnt,breed_tree_cnt

#번식
def breed(i,j,new_tree_cnt,new_tree):
    for (dy,dx) in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr = i + dy
        nc = j + dx
        if 1 <= nr <= N and 1 <= nc <= N and tree[nr][nc] == 0 and herbicide[nr][nc] == 0:
            new_tree[nr][nc] += new_tree_cnt
    return new_tree


def find_most_kill():
    max_kill = 0
    max_r = 0
    max_c = 0
    for i in range(1,N+1):
        for j in range(1,N+1):
            kill_cnt = 0
            kill_cnt+=tree[i][j]
            if tree[i][j] <= 0:
                continue
            for (dy,dx) in [(-1,-1),(-1,1),(1,1),(1,-1)]:
                for k in range(1,K+1):
                    nr = i + k*dy
                    nc = j + k*dx
                    if nr>N or nr<1 or nc>N or nc<1:
                        break
                    if tree[nr][nc] == -1 or tree[nr][nc] ==0:
                        break
                    kill_cnt += tree[nr][nc]
            if kill_cnt>max_kill or (kill_cnt == max_kill and i<max_r) or \
                    (kill_cnt == max_kill and i == max_r and j < max_c):
                max_kill = kill_cnt
                max_r,max_c = i,j
    return max_r, max_c

def kill_tree(r,c):
    global kill_tree_cnt
    kill_tree_cnt += tree[r][c]
    tree[r][c] = 0
    for (dy, dx) in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
        for k in range(1, K + 1):
            nr = r + k * dy
            nc = c + k * dx
            if nr > N or nr < 1 or nc > N or nc < 1:
                break
            if tree[nr][nc] == -1 or tree[nr][nc] == 0:
                break
            kill_tree_cnt += tree[nr][nc]
            tree[nr][nc] = 0


for m in range(1,M+1):
    kill = [[0] * (N + 1) for _ in range(N + 1)]
    cnt = [[0] * (N + 1) for _ in range(N + 1)]
    breed_tree = [[0] * (N + 1) for _ in range(N + 1)]
    #1.나무성장
    for i in range(1,N+1):
        for j in range(1,N+1):
            if tree[i][j] > 0:
                cnt[i][j],breed_tree[i][j] = count(i,j)
                tree[i][j] += cnt[i][j]

    new_tree = copy.deepcopy(tree)
    #2.번식
    for i in range(1,N+1):
        for j in range(1,N+1):
            if tree[i][j] > 0:
                if breed_tree[i][j] != 0:
                    new_tree_cnt = tree[i][j] // breed_tree[i][j]
                    new_tree = breed(i,j,new_tree_cnt,new_tree)
    tree = new_tree

    #3.박멸할 칸 지정
    r,c = find_most_kill()

    # 제초제 뿌리는 년수 감소
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if herbicide[i][j] != 0:
                herbicide[i][j] -= 1
    #제초제 뿌리기
    herbicide[r][c] = C
    for (dy, dx) in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
        for k in range(1, K + 1):
            nr = r + k * dy
            nc = c + k * dx
            if nr > N or nr < 1 or nc > N or nc < 1:
                break
            if tree[nr][nc] == -1 or tree[nr][nc] == 0:
                herbicide[nr][nc] = C
                break
            herbicide[nr][nc]=C
    #박멸
    kill_tree(r,c)



print(kill_tree_cnt)