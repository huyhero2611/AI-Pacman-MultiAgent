# AI-Pacman-MultiAgent

### 1. Reflex Agent - evaluation Function
- nếu kết thúc => return
```
if successorGameState.isWin():
  return 1000000
```
- tìm khoáng cách gần nhần của food so với pacman:
```
closestFood = min([manhattanDistance(newPos, food) for food in newFood.asList()])
```
- nếu ghost không sợ và khoảng cách so với pacman < 2 => không đi theo hướng đó:
```
for ghost in newGhostStates:
  if ghost.scaredTimer == 0 and manhattanDistance(ghost.getPosition(), newPos) < 2: 
    return -1000000
```
- trả về hàm đánh giá, score + 1 / closestFood (vì càng gần và nghịch đảo thì hàm đánh giá càng cao)
```
return successorGameState.getScore() + 1.0 / closestFood
```
### 2. Minimax Agent
- viết 1 hàm tìm kiếm theo minimax với đầu vào là gamesState và turn(turn++ mỗi khi 1 agent đi 1 bước)
- tạo 1 mảng evalutions các giá trị của node con của node đó bằng cách để quy hàm search:
```
evals = [self.minimax_search(gameState.generateSuccessor(agentIndex, action), turn + 1) for action in actions]
```
- nếu đến turn ghost trả về min, pacman trả về max với mảng đánh giá
```
if agentIndex > 0:
  return min(evals)
return max(evals)
```
### 3. Alpha Beta
- tương tự minimax
- thêm alpha, beta vào hàm saarch:
```
def alphabeta_search(self, gameState, turn, alpha, beta):
```
- áp dụng mã giả thuật toán alpha beta:
```
for action in actions:
  successor = gameState.generateSuccessor(agentIndex, action)
  if (agentIndex > 0): # min value
    v = min(v, self.alphabeta_search(successor, turn + 1, alpha, beta))
    if v < alpha:
      return v
    beta = min(beta, v)
  else:
    v = max(v, self.alphabeta_search(successor, turn + 1, alpha, beta))
    if v > beta:
      return v
    alpha = max(alpha, v)
return v
```
### 4. Expectimax:
- tương tự minimax (chỉ thay nếu turn ghost thì lấy trung bình của hàm đánh giá)
```
if agentIndex > 0:
  return sum(evals) * 1.0 / len(evals) 
return max(evals)
```
### 5. Evaluation function
- xét hàm đánh giá với 3 giá trị: pacman gần thức ăn (closestFood), ghosts có khoảng cách < 3 so với ghost(cover_me) và những con ma đang không sợ (scare_me)
```
closestFood = min(manhattanDistance(pacmanPosition, food) for food in foods.asList())
cover_me = sum([(manhattanDistance(pacmanPosition, ghost.getPosition()) < 3) for ghost in ghostStates])
scare_me = sum([(ghost.scaredTimer == 0) for ghost in ghostStates])
```
- hàm đánh giá (chọn ngẫu nhiên):
```
return currentGameState.getScore() * 10.0 + 1.0 / closestFood + 1.0 * cover_me + 1.0 / (scare_me + 0.01)
```



      
