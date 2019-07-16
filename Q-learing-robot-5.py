
# coding: utf-8

# In[1]:

from itertools import product as selfcrossjoin
import numpy as np
Qtable = {}


#分两次更新Q表，当落子没有占满棋盘时，当落子占满棋盘


# In[ ]:




# In[ ]:

#利用itertools 笛卡尔生成器生成 Q表，并初始化Q值为全部0
#因为9个位置，每个位置有3种可能组合0,1,2。期盘有9个格子 因此排列组合的可能性有 3^9=19683种组合
x=0
for i in selfcrossjoin([0,1,2], repeat = 25):
     Qtable.update({i : 0})
     x=x+1
#输出的初始Q表类似下面的样子：
#25代表棋盘5*5=25 
'''{(1, 2, 1, 2, 2, 2, 0, 1, 0): 0, (1, 2, 1, 1, 2, 0, 1, 2, 0): 0......}'''
print('Q表中的状态一共有',x)
#print(Qtable)


# In[ ]:

def get_R_and_Win(state): #返回R值以及判断胜利
     #print('get_R_and_Win传入的state为',state)
     board = [(0,1,2,3,4), (5,6,7,8,9), (10,11,12,13,14),(15,16,17,18,19), (20,21,22,23,24), (0,5,10,15,20),(1,6,11,16,21), 
              (2,7,12,17,22),(3,8,13,18,23),(4,9,14,19,24),(0,6,12,18,24),(4,8,12,16,20)]
     for (p1, p2, p3,p4,p5) in board:
         if (state[p1] != 0):
             if (state[p1] == state[p2] == state[p3]==state[p4]==state[p5]):
                 return 1
     return 0


# In[ ]:

#  返回一个随机位置,传入参数为期盘，Q表，和玩家
def get_a_move(board, P_Qtable, gamer): # return random position in space board
    #print('get_a_move传入的board为' ,board,'gamer是',gamer)
    stage_var = []
    for i in range(len(board)):
         #判断期盘是否有子,如果没有子就送入stage_var，作为候选位置
         if (board[i] == 0):
             stage_var.append(i)
             #print('get_a_move stage_var append 现在为：',stage_var)
    length = len(stage_var)
    returnpoistion=stage_var[np.random.randint(0, length)]
    #print('get_a_move返回的可用的候选落子位置为',returnpoistion)
    return (returnpoistion)


# In[ ]:

# 在当前状态下。 下一个状态的Q值

##############################################

# 完成返回Q值函数定义

##############################################

def getnextQvalue(board, P_Qtable, gamer): #返回当前状态下 如果选择选择所有可能动作进入下一个可能所有状态，的所有Q值
    
    if (0 in board):
        
        Qvalue = []
        
        for i in range(len(board)):
            if (board[i]== 0):
                stage_var = board[:]
                stage_var[i] = gamer
                
                temp_tuple = tuple(stage_var)
                
                Qvalue.append(P_Qtable[temp_tuple])
        return Qvalue
    else :
        return [0]


# In[1]:


def upd_pre_state_Q(length, Qtable,state,alpha=0.2,gamma=0.7):
    preState = state[:]

    while (length > 0):

        preState[p[length]] = 0

                                                           
                                                           
        Qtable[tuple(preState)] = Qtable[tuple(preState)] + alpha *(gamma * Qtable[tuple(state)] - Qtable[tuple(preState)])
        state = preState[:]

        length =length - 1

    return 0


# In[2]:

def AI_Play_Move(board, P_Qtable): #计算最大Q值对应的位置
    temp_Q=-10000
    ai_move = 0
 
    for i in range(len(board)):
        stage_var = board[:]        
        if (board[i] == 0):
            
            stage_var[i] = 1
            
            if (P_Qtable[tuple(stage_var)] > temp_Q):
               
                temp_Q = P_Qtable[tuple(stage_var)]
                ai_move = i
    #print('当前的i=',ai_move,'是Q最大作为落子点返回')            
    return ai_move


# In[ ]:




# In[ ]:

def train(iteration=2000,alpha=0.2,gamma=0.7):
    episode = 0
    while (episode < iteration):
    #while (episode < 50):
        episode += 1

        state = [0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        global p
        p = []
        turn = 1
        while ( 0 in state):
            position = get_a_move(state, Qtable, turn) # 返回期盘的随机位置
            
            p.append(position)           
            
            state[position] = turn
            
            if(get_R_and_Win(state) == 1 ):
                if (turn == 1):
                    Qtable[tuple(state)] = 1
                    
                elif(turn == 2):
                    Qtable[tuple(state)] = -1
                    
                break
            elif(turn == 1):
                turn = 2

            else:  #turn == 2
                turn = 1
                #'设置玩家=1再次计算更新Q值,下一个状态应该是1也就是AI落子，我们希望选择的动作具有最大的Q值')
                t = getnextQvalue(state,Qtable, turn) #q-value
                future_score = (gamma * max(t) - Qtable[tuple(state)]) #q-value
                Qtable[tuple(state)] = Qtable[tuple(state)] + alpha * future_score #q-value
        length = len(p) -1

        upd_pre_state_Q(length, Qtable, state,alpha,gamma)
        
train()


# In[ ]:

board = [0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
instruct_board = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
print('*********棋盘落子位置说明************')

print(instruct_board[0:4])
print(instruct_board[5:9])
print(instruct_board[10:14])
print(instruct_board[15:19])
print(instruct_board[20:24])

print('**************对局开始*****************')

print(board[0:4])
print(board[5:9])
print(board[10:14])
print(board[15:19])
print(board[20:24])
while (0 in board):  
    postion = AI_Play_Move(board, Qtable)
    board[postion] = 1#在选择的棋盘位置填入1
    print('AI落子现在棋盘为:')
    print(board[0:4])
    print(board[5:9])
    print(board[10:14])
    print(board[15:19])
    print(board[20:24])
    
    if (get_R_and_Win(board) == 1): #检查是否胜利
        print ('人工智能获得胜利')
        break
    userposition = int(input("输入你的位置"))
    board[userposition] = 2 #在用户输入的位置填入2
    print(board[0:4])
    print(board[5:9])
    print(board[10:14])
    print(board[15:19])
    print(board[20:24])
    if (get_R_and_Win(board) == 1):
        print ('你获得了胜利')
        break


# In[ ]:



