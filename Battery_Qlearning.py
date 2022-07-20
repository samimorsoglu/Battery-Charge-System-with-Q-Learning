import numpy as np
import pandas as pd
import time


np.random.seed(2)
testing=0

N_STATES = 101
ACTIONS = ['decharge','charge']

EPSILON = 0.9
ALPHA = 0.1 # ogrenme orani
GAMMA = 0.9 # discount factor

MAX_EPISODES = 50
FRESH_TIME = 0


def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))), columns=actions)
    return table


def choose_action(state, q_table):
    state_actions = q_table.iloc[state, :]
    # print(state_actions)
    if (np.random.uniform() > EPSILON) or ( state_actions==0).all():
        action_name = np.random.choice(ACTIONS)
    else:
        action_name = state_actions.idxmax()
    print(" Action name : ", action_name)
    return action_name


def get_env_feedback(S, A):
   if A=='charge':
       if S<30:
           
           if S == N_STATES-71:
               S_ = 'optimum charge value'
               R = 100
           elif S== N_STATES-1:
               S_ = S - 2
               R = -10
           elif 30-S > 30-(S+1):    
               S_ = S + 1
               R = 10
           else :
               S_ = S + 1
               R = 0
               
       else:
            
            if S == N_STATES-71:
               S_ = 'optimum charge value'
               R = 100
            elif S== N_STATES-1:
               S_ = S - 2
               R = -10
            elif S-30 < (S+1)-30:    
               S_ = S + 1
               R = -10
            else :
               S_ = S + 1
               R = 0       
   else:
         R = 0
         if S<30:
           
           if S == N_STATES-71:
               S_ = 'optimum charge value'
               R = 100
           elif S== N_STATES-100:
               S_ = S + 2
               R = -1
           elif 30-S < 30-(S-1):    
               S_ = S - 1
               R = -10
           else :
               S_ = S - 1
               R = 0
               
         else:
            
            if S == N_STATES-71:
               S_ = 'optimum charge value'
               R = 100
            elif S== N_STATES-100:
               S_ = S + 2
               R = -1
            elif S-30 > (S-1)-30:    
               S_ = S - 1
               R = 10
            else :
               S_ = S - 1
               R = 0  
           
   return S_, R 


def update_env(S, episode, step_counter):
    env_list = ['X']*(N_STATES)
    if S == 'optimum charge value':
        interaction = 'Episode is %s tatal_steps = %s' % (episode+1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                            ', end='')
    else:
        print('\r{%s}'%S)
        env_list[S] = 'O'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)


def rl():
    q_table = build_q_table(N_STATES, ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = np.random.randint(0,100)
        is_terminal = False
        update_env(S, episode, step_counter)
        while not is_terminal:
            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A)
            q_predict = q_table.loc[S, A]
            if S_ != 'optimum charge value':
                q_target = R + GAMMA * q_table.iloc[S_, :].max()
            else:
                q_target = R
                is_terminal = True
            q_table.loc[S, A] += ALPHA * (q_target - q_predict)
            S = S_
            update_env(S, episode, step_counter+1)
    return q_table


if __name__ == "__main__":
    q_table = rl()
    print('\r\nQ_Table:\n')
    print(q_table)
    df = pd.DataFrame(q_table, columns = ['decharge', 'charge'])
    df.to_excel('Battery_Charge_Report.xlsx', sheet_name='Q_table')
    while True:
        testing = input("Please enter the current value of battery charge :") 
        x=int(testing)
        if(x >=0 and x <= 30 or x==30):
            while x >=0 and x <= 30 or x==30:
                if(q_table.iat [x,0]<q_table.iat [x,1]):
                    print("Charge Value=%s You need a Charge"%x)
                    time.sleep(1)
                    x=x+1
                elif(x==30):
                    print("Charge Value=%s You are on Optimum Charge Point"%x)
                    x=102
                else:
                    print("Charge Value=%s You need a DeCharge"%x)
                    x=x+1
                    time.sleep(1)
                continue
        elif(x >=30 and x <= 100 or x==30): 
            while x >=30 and x <= 100 or x==30:
                if(q_table.iat [x,0]<q_table.iat [x,1]):
                    print("Charge Value=%s You need a Charge"%x)
                    time.sleep(1)
                    x=x-1
                elif(x==30):
                    print("Charge Value=%s You are on Optimum Charge Point"%x)
                    x=102
                else:
                    print("Charge Value=%s You need a DeCharge"%x)
                    x=x-1
                    time.sleep(1)
                continue
        else:
            break 
            
        