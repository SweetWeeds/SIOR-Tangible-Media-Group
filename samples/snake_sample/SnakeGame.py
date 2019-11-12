# 스네이크 게임 (Snake Game) v.1.1
# 출처: Snake Game by @TokyoEdTech
# 수정: 오상문 sualchi@daum.net
# 먹을 과일이 5개씩 늘어날 때마다 속도를 빠르게 함
# 그런데 몸통이 길어질수록 처리 시간이 느려져서 큰 효과 없네요.
# 속도 높이려면 게임 구조를 변경해야 할 듯

import os
import turtle
import time
import random

# 변수 선언
level = 1      # 레벨 (추가)
delay = 0.1    # 지연시간
score = 0      # 현재 점수
high_score = 0 # 최고 점수
segments = []  # 뱀 몸통 리스트

# 게임 창 초기화
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("green")
wn.setup(width=600, height=600)
#wn.tracer(0)  // 화면 갱신 중지

# 뱀 머리 초기화
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = "stop"

# 먹이 초기화 
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

# 펜 초기화 (점수 출력용)
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0  Level: 1", align="center", font=("Courier",16,"normal")) 

# 사용자 함수 정의 
def go_up():
    if head.direction != "down":   # 반대 방향 변경 금지
        head.direction = "up"

def go_down():
    if head.direction != "up":    
        head.direction = "down"

def go_left():
    if head.direction != "right":    
        head.direction = "left"

def go_right():
    if head.direction != "left":    
        head.direction = "right"    

# 뱀 이동 
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# 벽이나 자신에게 접촉한 경우 초기화 처리 
def reset():
    global score, delay
    segments.clear()
    score = 0
    delay = 0.1
    level = 1       # 추가
    pen.clear()    
    pen.write("Score: {}  High Score: {}  Level: {}".format(score,high_score,level),align="center",font=("Courier",16,"normal")) # 변경      

# 키보드 값을 처리할 메소드 설정
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
#wn.onkeypress(go_up, "Up")
#wn.onkeypress(go_down, "Down")
#wn.onkeypress(go_left, "Left")
#wn.onkeypress(go_right, "Right")

# 게임 처리 메인 부분
while True:
    wn.update() # 화면 갱신 

    # 벽 충돌 검사 처리
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"        
        # 뱀 몸통 숨김
        for segment in segments:
            segment.goto(1000, 1000)
        # 뱀과 점수  초기화 
        reset()   

    # 먹이를 먹었는지 검사 처리 
    if head.distance(food) < 20:    
        # 먹이를 임의 위치에 새로 놓음(옮김)
        x = random.randint(-270, 270)
        y = random.randint(-270, 270)
        food.goto(x, y) 
        # 뱀 몸통 추가
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)
        # 먹이 먹은 숫자 5개 단위로 레벨 업 
        if len(segments)%5 == 0 and len(segments)!=0:  # 추가
          level += 1     # 레벨 증가 
          delay *= 0.5   # 속도 50% 더 빠르게 (추가)
        # 점수 올리고, 최고 점수보다 높으면 갱신 처리
        score += 10
        if score > high_score:
            high_score = score

        pen.clear() # 점수 문자열 부분 지움   
        pen.write("Score: {}  High Score: {}  Level: {}".format(score,high_score,level),align="center",font=("Courier",16,"normal")) # 변경   

    # 몸통 위치 이동 
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x,y)

    # 0번 몸통을 머리 위치로 이동
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    # 머리 이동 처리      
    move()

    # 머리가 몸통과 접촉했는지 검사 처리 
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
            # 몸통 숨김
            for segment in segments:
                segment.goto(1000, 1000)
            # 초기화
            reset()          
    if delay > 0.013:   # 지연 시간 적을 때는 지연 없음
        time.sleep(delay) # 시간 지연 
wn.mainloop()  

# 종료 
