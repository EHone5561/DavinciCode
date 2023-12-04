import random

#-------------------------------------------------------------------------------------------------------------------------
import time
def make_Code(): #패산을 생성 혹은 초기화하는 메소드입니다.
    Code_b = [f"{i}b" for i in range(12)] #패산 생성 (검은 색) # n + w (n: 숫자, b:색깔(black)) 
    Code_w = [f"{i}w" for i in range(12)] #패산 생성 (하얀 색)# n + w (n: 숫자, w:색깔(white)) 
    return (Code_b, Code_w)

def make_hand(Code_b, Code_w): #게임 시작전 기본 패를 분배하는 메소드입니다.
    Computer_hand = [] 
    Player_hand = []
    Code_b = shuffle_Code(Code_b) #각 색깔의 패산을 셔플하는 단계
    Code_w = shuffle_Code(Code_w) 
    Code_b, Code_w, Computer_hand = Computer_Start(Code_b, Code_w, Computer_hand) #Computer가 패를 선택하여 가져오기
    print(f"컴퓨터가 4개의 임의의 패를 가져갔습니다.")
    Code_b, Code_w, Player_hand = Player_Start(Code_b, Code_w, Player_hand) #Player가 패를 선택하여 가져오기
    print("당신은 4개의 패를 손에 집었습니다.")
    return (Code_b, Code_w, Player_hand, Computer_hand)

def add_joker(Code_b, Code_w): #패 분배가 끝나고 조커를 삽입하는 메소드입니다.
    Code_b.append("Jb") #검은색 조커 추가
    Code_w.append("Jw") #하얀색 조커 추가
    return (Code_b, Code_w)

def Computer_Start(Code_b, Code_w, Computer_hand): ######인공지능###### #컴퓨터가 게임을 시작하기 전 패를 가져오는 메소드입니다.
    import random
    select_white = random.randint(0,4) #임시 #뽑은 하얀 색 패의 수의 수를 random.randint로 구현해놓았습니다. 그러나 이는 인공지능을 사용하여 더욱 효율적으로 결정되어야 합니다.
    if select_white > 0: #예외 처리
        for _ in range(0, select_white): #dummy(list) 쓰이지 않지만 argument를 충족하기 위해 임시로 넣음
            dummy, Code_w, Computer_hand = receive_Code([], Code_w, Computer_hand)
    if select_white < 4: #예외 처리
        for _ in range(0, 4 - select_white):
            dummy, Code_b, Computer_hand = receive_Code([], Code_b, Computer_hand)
    return (Code_b, Code_w, Computer_hand)

def Player_Start(Code_b, Code_w, Player_hand): #플레이어가 게임을 시작하기 전 패를 가져오는 메소드입니다.
    try: #플레이어의 입력을 받으므로 예외처리
        select_black = int(input("몇 개의 검은 색 패를 가져가시겠습니까? (최대 4개):"))
        assert (0 <= select_black <= 4)
        if select_black > 0:
            for _ in range(0, select_black):
                dummy, Code_b, Player_hand = receive_Code([], Code_b, Player_hand)
        if select_black < 4:
            for _ in range(0, 4 - select_black):
                dummy, Code_w, Player_hand = receive_Code([], Code_w, Player_hand)

    except(ValueError):
        print("정확한 값을 입력해주세요.")
        Code_b, Code_w, Player_hand = Player_Start(Code_b, Code_w, Player_hand)

    except(AssertionError):
        print("범위 안의 숫자를 입력해주세요.")
        Code_b, Code_w, Player_hand = Player_Start(Code_b, Code_w, Player_hand)
    return (Code_b, Code_w, Player_hand)



def shuffle_Code(Code): #가져온 코드(list)를 셔플하는 메소드입니다.
    import random
    random.shuffle(Code)
    return Code #섞인 패산 

def receive_Code(draw, Code, receiver): #임의의 패산에서 하나의 패를 receiver에게 전달하는 메소드입니다.
    receiver.append(Code[0])
    if Code[0] == "Jw":
        draw = ['jw']
    elif Code[0] == "Jb":
        draw = ['jb']
    else:
        draw.append(Code[0])
    Code = Code[1:]
    return (draw, Code, receiver) #남은 패산과 추가된 손패

def sort_Code(Code): # 컴퓨터나 플레이어가 패를 가져온 후 올바른 순서로 정렬하기 위한 메소드입니다.
    Code.sort(key = lambda x: (x[-1].isdigit(), int(x[:-1]) if x[:-1].isdigit() else float('inf'), x))
    return Code

def find_Player_Joker(Code, joker_info): #플레이어가 가져온 패가 조커인 경우를 확인하고 조커를  배치하는 메소드입니다. 
    joker = False
    black = False
    if Code[-1] in ['jb']:
        Code = Code[:-1]
    if Code[-1] in ['jw']:
        Code = Code[:-1]
    if Code[-1][0] == 'J': #조커는 한 번에 두 개 들어오지 않는다.
        print('조커 발견')
        joker = True
        if Code[-1][1] == 'b':
            black = True
        Code = Code[:-1]
    if joker:
        try:
            print(Code)
            print()
            act = int(input("조커를 둘 위치를 선택하세요 (맨 앞을 0부터):"))
            assert (0 <= act <= (len(Code) + 1))
        except (ValueError):
            print("정확한 위치를 입력해주세요.")
            return find_Player_Joker()
        except (AssertionError):
            print("올바른 위치가 아닙니다. 다시 입력해주세요.")
            return find_Player_Joker()
        if black:
            Code.insert(act, 'jb')
            joker_info.append('jb')
            joker_info.append(act)
        else:
            Code.insert(act, 'jw')
            joker_info.append('jw')
            joker_info.append(act)
    return (Code, joker_info)

def find_Computer_Joker(Code, joker_info): ######인공지능###### #컴퓨터가 가져온 패가 조커인 경우를 확인하고  조커를 배치하는 메소드입니다.
    joker = False                           #컴퓨터가 조커를 뽑고 배치하는 경우를 random.randint로 구현해놓았습니다. 그러나 이는 인공지능을 사용하여 더욱 효율적으로 배치되어야 합니다.
    black = False
    if Code[-1][0] == 'J':
        joker = True
        if Code[-1][1] == 'b':
            black = True
    if joker:
        import random
        act = random.randint(0,len(Code))
        if act == len(Code):
            act -= 1
        if black:
            joker_info.append('jb')
            joker_info.append(act)
        else:
            joker_info.append('jw')
            joker_info.append(act)
        Code = Code[:-1]
    return (Code, joker_info)

def delete_joker(Code, joker_info): #이미 배열한 조커가 마지막에도 오는 문제를 해결하기위해 만든 메소드였다. 신경쓰지 말 것
    if 'jw' in Code:
        Code.remove('jw')
    if 'jb' in Code:
        Code.remove('jb')
    return (Code, joker_info)

def sort_Joker(Code, joker_info): #패를 정렬하고 맨 뒤에 온 조커를 joker_info에 있는 조커의 정보에 따라 재배치하는 메소드입니다.
    if len(joker_info) == 2:
        Code.insert(joker_info[1], joker_info[0])
    elif (len(joker_info) == 4):
        Code.insert(joker_info[1], joker_info[0])
        Code.insert(joker_info[3], joker_info[2])
    else:
        pass
    return (Code, joker_info)

def draw_phase_player(draw, Code_b, Code_w, joker_info, receiver): #플레이어가 드로우하는 페이즈로 관련 메소드들을 순서에 따라 배치해놓은 메소드입니다.
    if (len(Code_b) == 0) and (len(Code_w) == 0):
        print("더 이상 가져올 수 있는 패가 없어 과정을 생략합니다.")
    else:
        while(True):
            print("--------------------------------------------------------------------")
            print(f"검은색 패 수 : {len(Code_b)}, 흰색 패 수 {len(Code_w)}")
            print()
            act = input("무슨 색 패를 뽑으시겠습니까?(b or w): ")
            print("--------------------------------------------------------------------")
            if act in ['B', 'b']:
                if (len(Code_b) == 0):
                    print("해당 색의 패가 부족하여 다른 색의 패를 드로우 하였습니다.")
                    draw, Code_w, receiver = receive_Code(draw, Code_w, receiver)
                    break
                else:
                    draw, Code_b, receiver = receive_Code(draw, Code_b, receiver)
                    break
            elif act in ['W','w']:
                if (len(Code_w) == 0):
                    print("해당 색의 패가 부족하여 다른 색의 패를 드로우 하였습니다.")
                    draw, Code_b, receiver = receive_Code(draw, Code_b, receiver)
                    break
                else:
                    draw, Code_w, receiver = receive_Code(draw, Code_w, receiver)
                    break
            else:
                print("제대로 입력해주세요(b or w)")
    receiver = sort_Code(receiver)
    receiver, joker_info = find_Player_Joker(receiver, joker_info)
    receiver, joker_info = delete_joker(receiver, joker_info)
    if joker_info != []:
        receiver, joker_info = sort_Joker(receiver, joker_info)
    else:
        pass
    return (draw, Code_b, Code_w, joker_info, receiver)

def draw_phase_computer(draw, Code_b, Code_w, joker_info, receiver): ######인공지능#######
    if receiver[-1] == 'jb':                                  #컴퓨터가 드로우하는 페이즈로 관련 메소드들을 순서에 따라 배치해놓은 메소드입니다.
        receiver = receiver[:-1]                              #컴퓨터가 드로우할 색깔의 패를 결정하는 과정을 random.randint로 구현하였습니다. 그러나 이는 인공지능을 사용하여 효율적으로 결정되어야합니다.
    elif receiver[-1] == 'jw':
        receiver = receiver[:-1]
    else:
        pass
    if (len(Code_b) == 0) and (len(Code_w) == 0):
        print("더 이상 가져올 수 있는 패가 없어 과정을 생략합니다.")
    else:
        while(True):
            import random
            act = random.randint(0,1)
            if act == 0:
                if (len(Code_b) == 0):
                    draw, Code_w, receiver = receive_Code(draw, Code_w, receiver)
                    print("컴퓨터는 하얀색 패를 하나 가져갔습니다.")
                    break
                else:
                    draw, Code_b, receiver = receive_Code(draw, Code_b, receiver)
                    print("컴퓨터는 검은색 패를 하나 가져갔습니다.")
                    break
            elif act == 1:
                if (len(Code_w) == 0):
                    draw, Code_b, receiver = receive_Code(draw, Code_b, receiver)
                    print("컴퓨터는 검은색 패를 하나 가져갔습니다.")
                    break
                else:
                    draw, Code_w, receiver = receive_Code(draw, Code_w, receiver)
                    print("컴퓨터는 하얀색 패를 하나 가져갔습니다.")
                    break
            else:
                print("오류 발생 (시스템 종료)")
                exit()
    receiver = sort_Code(receiver)
    receiver, joker_info = find_Computer_Joker(receiver, joker_info)
    receiver, joker_info = delete_joker(receiver, joker_info)
    #receiver = sort_Code(receiver)
    if joker_info != []:
        receiver, joker_info = sort_Joker(receiver, joker_info)
    else:
        pass
    return (draw, Code_b, Code_w, joker_info, receiver)

def encrypt_Code(Code, Reveal_list): #Reveal_list(정답이 맞춰졌거나, 틀렸을 시에 공개되는 패의 정보를 담고 있음)를 참조하여 컴퓨터 혹은 플레이어의 코드를 암호화함
    encrypted_Code = []
    for elem in Code:
        if elem in Reveal_list:
            encrypted_Code.append(elem)
        else:
            if elem[-1] == 'b':
                encrypted_Code.append('▣ b')
            elif elem[-1] == 'w':
                encrypted_Code.append('▣ w')
            else:
                print("디버깅용  > 오류 발생")
                exit(0)
    return encrypted_Code
def view_hand_player(Player_hand, Computer_hand, reveal_info_computer, reveal_info_player):
    print()
    print("--------------------------------------------------------------------")
    print("상대의 손패:", encrypt_Code(Computer_hand, reveal_info_computer))
    print()
    print("당신의 손패: [", end = " ")
    for card in Player_hand:
        if card in reveal_info_player:
            print(card + "*,", end = " ")
        else:
            print(card+",", end = " ")
    print("]")

def reason_phase_player(Computer_hand):
    print()
    while(True):
        try:
            idx = int(input("맞출 상대의 패의 번호를 선택해주세요(왼쪽부터 0): "))
            if 0 <= idx <= (len(Computer_hand)) - 1:
                break
        except(ValueError):
            print("위치 번호를 정확하게 입력해주세요.")
    while(True):
        try:
            print()
            value = input("상대의 패를 예측해주세요(ex: 3b, 7w, jb)):")
            if(value in ('jb', 'jw')):
                break
            assert (value[-1] in ['b', 'B', 'w', 'W']) #마지막 글자가 색깔과 관련되어 있는 지를 확인합니다.
            if (len(value) == 2): #일의 자리 숫자인 경우를 확인합니다.
                assert((0 <= int(value[0]) <= 9) or (value[0] in ['j', 'J']))
            elif (len(value) == 3): #십의 자리 숫자인 경우를 확인합니다.
                assert(int(value[0]) == 1)
                assert(0 <= int(value[1]) <= 1)
            break
        except(ValueError):
            print("정확하게 입력해주세요.")
        except(AssertionError):
            print("숫자 + 색깔의 형식으로 다시 입력해주세요.")
    return idx, value


#--------------------------------------------------------------------------------------------------------------
from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

class GameOfDavinci(TwoPlayerGame):
    def __init__(self, players):
        self.Debugging = False
        self.players = players
        self.current_player = 1   #1은 HumanPlayer, 2는 AIplayer를 의미한다. 1부터 게임을 시작한다. 인덱스 저장 위치를 가리키는 용도로 주로 사용했다.

        self.Code_b, self.Code_w = make_Code()
        self.Code_b, self.Code_w, self.Player_hand, self.Computer_hand = make_hand(self.Code_b, self.Code_w)
        self.Code_b, self.Code_w = add_joker(self.Code_b, self.Code_w)
        self.Code_b = shuffle_Code(self.Code_b)
        self.Code_w = shuffle_Code(self.Code_w)
        self.Code_b = self.Code_b[:-1]
        self.Code_w = self.Code_w[:-1]
        self.joker_info_computer = []
        self.joker_info_player = []
        self.reveal_info_player = []
        self.reveal_info_computer = []
        self.wronganswers = [[],[],[]] #틀린 시도를 기록해두고, possible_moves에서 빼는 용도로 기획했었다.

        #self.card_deck = self.Code_b + self.Code_w

        self.gameboard = [[], sort_Code(self.Player_hand), sort_Code(self.Computer_hand)] # 1번 인덱스에 Humanplayer의 카드패를, 2번 인덱스에 AI의 카드패를 저장한다. 0번 인덱스는 그냥 위치 맞춤 용이다.
        self.draw = [[],[],[]] #1번 인덱스에 HumanPlayer의 draw정보를, 2번 인덱스에 AIplayer의 draw정보를 저장한다. 0번 인덱스는 그냥 위치맞춤용이다.


        
        self.card_candidate = [[], [f"{i}b" for i in range(12)] + [f"{i}w" for i in range(12)] + ['jb', 'jw'] ,[f"{i}b" for i in range(12)] + [f"{i}w" for i in range(12)] + ['jb', 'jw']]
        #1번 인덱스에선 AI플레이어 입장에서 Human플레이어의 패에 대한 후보패, 2번 인덱스에는 Human플레이어 입장에서 AI플레이어의 패에 대한 후보패를를 저장해놓았다. 
        self.unrevealed_index = [[],[i for i in range(len(self.gameboard[1]))], [j for j in range(len(self.gameboard[2]))]]
        self.revealed_idx_list = []

        for card in self.gameboard[2]:
            if card in self.card_candidate[1]:
                self.card_candidate[1].remove(card)
        
        for card in self.gameboard[1]:
            if card in self.card_candidate[2]:
                self.card_candidate[2].remove(card)
    
    
    def possible_moves(self): #가능한 움직임들의 리스트를 전달하는 클래스이다.


        output = []
        #일단 모든 가능한 (인덱스, 카드) 조합을 output담아서 리턴하는 방식을 사용했다.
        for i in self.unrevealed_index[self.opponent_index]:
            for card in self.card_candidate[self.opponent_index]:
                if(self.gameboard[self.opponent_index][i][-1] == card[-1]):
                    output.append([i, card])
            
        for content in self.wronganswers[self.current_player]:
            if content in output:
                output.remove(content)

        if(self.current_player==2):  #현재 플레이어가 AI일경우에만 작동
            self.revealed_idx_list = [idx for idx in (range(len(self.gameboard[1]))) if idx not in self.unrevealed_index[1]]

            for idx in self.revealed_idx_list:    #특정 위치 이전의 카드의 후보군에서 밝혀진 카드의 숫자보다 낮은 카드는 제거한다.
                if(not self.gameboard[1][idx][:-1].isdigit()):
                    continue
                for i in range(idx+1,len(self.gameboard[1])):
                    idx_list = [j[0] for j in output]
                    if(i not in idx_list):
                        continue
                    min_idx = idx_list.index(i)
                    for card in output[min_idx:] :
                        if(card[1][:-1].isdigit() and int(card[1][:-1]) < int(self.gameboard[1][idx][:-1])):
                            if(card in output):
                                output.remove(card)


        return output
    
        
    
    def make_move(self, move): #움직임을 만드는 클래스이다. AI가 움직임을 결정하기까지 Negamax의 깊이 인수에 비례하여 꽤 많이 반복된다. 근데 입력할때 [0, '1w']대충 이런식으로 입력해야한다. 안그러면 입력 단계가 계속 반복됨.
                                #move는 [인덱스, 카드]로 구성된다.
                                #         
        answer = self.gameboard[self.opponent_index][move[0]] #self.opponent_index는 현재 진행중인 (Human or AI)플레이어의 반대 플레이어의 번호를 말한다.
        #태원이의 코드의 Computer_hand[idx]가 여기선 self.gameboard[self.opponent_index][move[0]]과 동일함


        if(answer == move[1]):
            #print("--------------------------------------------------------------------")
            #print("정답입니다!")
            if(self.current_player==2): #AIplayer일때
                if(answer in self.card_candidate[self.opponent_index]):
                    self.card_candidate[self.opponent_index].remove(answer) #밝혀졌으므로 후보군에서 제외한다.

            if(self.current_player == 1):  #현재 플레이어가 HumanPlayer일경우
                self.reveal_info_computer.append(answer)
                
                #print(f"상대 AI의 패 {self.gameboard[self.opponent_index][move[0]]} 를 공개합니다.")
                #print("--------------------------------------------------------------------")
            else: #현재 플레이어가 AI플레이어일경우
                self.reveal_info_player.append(answer)
                '''
                print(f"당신의 패 {self.gameboard[self.opponent_index][move[0]]} 를 공개합니다.")
                print("--------------------------------------------------------------------")
                '''
            
  
            #print(self.gameboard)
        else:
            if(self.current_player==2):
                self.wronganswers[self.current_player].append(move)
            #print("--------------------------------------------------------------------")
            #print("오답입니다...")
            
            if self.draw[self.current_player] != []:
                for i, elem in enumerate(self.gameboard[self.current_player]):

                    if elem == self.draw[self.current_player][-1]:
                        #print(f"아까 드로우했던 패 {elem} 를 공개합니다.")
                        if(self.current_player == 1):
                            self.reveal_info_player.append(elem)
                        else:
                            self.reveal_info_computer.append(elem)
                        if(self.current_player==1):
                            if(elem in self.card_candidate[self.current_player]):
                                self.card_candidate[self.current_player].remove(elem)
                        #print("AI플레이어가 예측할 수 있는 당신 패의 후보 인덱스 : ", self.card_candidate[self.opponent_index])

                    else:


                        pass
            else:
                pass
            #print("--------------------------------------------------------------------")
        #print(move)
            
        
    def loss_condition(self):
        if(self.current_player==1):
            return len(self.reveal_info_player) == len(self.gameboard[1])
        else:
            return len(self.reveal_info_computer) == len(self.gameboard[2])
        
    def is_over(self): #게임이 끝나는 조건을 정의하는 클래스이다. 가능한 움직임이 없거나 모든 카드가 다 밝혀졌을 경우를 끝나는 조건으로 정의했다.
        
        
        return (self.possible_moves == [] or self.loss_condition())
    
    def show_lose(self):
        if len(self.reveal_info_computer) == len(self.gameboard[2]) or self.possible_moves == []:
            print("--------------------------------------------------------------------")
            print("상대방의 모든 패가 공개되었습니다. 당신의 승리입니다.")
            print("--------------------------------------------------------------------")
        
        elif len(self.reveal_info_player) == len(self.gameboard[1]) or self.possible_moves == []:
            print("--------------------------------------------------------------------")
            print("플레이어의 모든 패가 공개되었습니다. 당신의 패배입니다.")
            print("--------------------------------------------------------------------")
            exit(0)
        else:
            pass
        
    

    def show(self): #Human_Player와 AI_Player의 패를 보여주는 클래스이다.
        view_hand_player(self.gameboard[1], self.gameboard[2], self.reveal_info_computer, self.reveal_info_player)
        print()
        if(self.Debugging):
            print('AI_HandViewer : ', end = '')
            for card in self.gameboard[2]:   #드러난 카드는 카드 뒤에 *기호를 붙이도록 작성된 코드이다.

                
                    print(card, end = "  ")
            
        
        print()
        print()
        
        #print("상대편의 남아있는 인덱스", game.unrevealed_index[game.opponent_index]) #제대로 동작하는지 확인용
    
    
    def scoring(self):
        return -100 if self.loss_condition() else 0




#-------------------------------게임 동작 부분-----------------------------------

############## 사전 준비 페이즈 ##############
print("--------------------------------------------------------------------")
print("곧 게임을 시작합니다.")
print("--------------------------------------------------------------------")
time.sleep(1)
game = GameOfDavinci([Human_Player(),AI_Player(Negamax(4))])

while not game.is_over():
    continued = True
    game.show()
    if game.current_player==1:  # we are assuming player 1 is a Human_Player
        print("--------------------------------------------------------------------")
        print()
        print("플레이어의 차례입니다.")
        print()
        print("--------------------------------------------------------------------")

        game.draw[game.current_player], game.Code_b, game.Code_w, game.joker_info_player, game.gameboard[game.current_player] = draw_phase_player(game.draw[game.current_player], game.Code_b, game.Code_w, game.joker_info_player,game.gameboard[game.current_player] )
        #잘못된 대답 모음집에서 새로운 카드가 넣어진 인덱스를 초기화한다.
        for i, card in enumerate(game.draw[game.current_player]):
            if(card == "Jw"):
                game.draw[game.current_player][i] = "jw"
            elif(card == "Jb"):
                game.draw[game.current_player][i] = "jb"

        if (game.wronganswers[game.opponent_index] != []):
            for wrongmove in game.wronganswers[game.opponent_index]:
                if wrongmove[0] == game.gameboard[game.current_player].index(game.draw[game.current_player][-1]):
                    game.wronganswers[game.opponent_index].remove(wrongmove)
                    if(game.Debugging):
                        print("뽑은 카드 제거")

        #game.gameboard[game.current_player] = sort_Code(game.Player_hand)
        if(game.Code_b!=[] and game.Code_w!=[]):
            print("당신이 뽑은 카드 : ", game.draw[game.current_player][-1])  #뽑은 카드 확인용으로 임시로 작성했다.
        if(game.draw[game.current_player][-1] in game.card_candidate[game.opponent_index]):
            game.card_candidate[game.opponent_index].remove(game.draw[game.current_player][-1])
        game.show()

        poss = game.possible_moves()
        '''
        for index, move in enumerate(poss):
            print("{} : {}".format(index, move)) #possiblemove들을 출력하는듯 하다.
        '''
        
                     
        print("< 주의! 색깔이 다를 경우 동작하지 않음> ")
        idx, value = reason_phase_player(game.Computer_hand)
        move = [idx, value]
        while (move not in poss):
            idx, value = reason_phase_player(game.Computer_hand)
            move = [idx, value]

    else:  # we are assuming player 2 is an AI_Player
        print("--------------------------------------------------------------------")
        print()
        print("컴퓨터의 차례입니다.")
        print()
        print("--------------------------------------------------------------------")
        


        game.draw[game.current_player], game.Code_b, game.Code_w, game.joker_info_computer, game.gameboard[game.current_player]  = draw_phase_computer(game.draw[game.current_player], game.Code_b, game.Code_w, game.joker_info_computer, game.gameboard[game.current_player] )
        
        for i, card in enumerate(game.draw[game.current_player]):
            if(card == "Jw"):
                game.draw[game.current_player][i] = "jw"
            elif(card == "Jb"):
                game.draw[game.current_player][i] = "jb"

        #game.gameboard[game.current_player] = sort_Code(game.Computer_hand)
        #print("컴퓨터가 뽑은 카드 : ", game.draw[game.current_player][-1])
        if(game.draw[game.current_player][-1] in game.card_candidate[game.opponent_index]):
            game.card_candidate[game.opponent_index].remove(game.draw[game.current_player][-1])
        
        
        poss = game.possible_moves()
        if(game.Debugging):
            for index, move in enumerate(poss):
                print("{} : {}".format(index, move)) #possiblemove들을 출력하는듯 하다.

        
        
        move = game.get_move()
        print("AI plays {}".format(move))




    #----------추측 결과 출력 페이지----------
    answer = game.gameboard[game.opponent_index][move[0]]
    if(answer == move[1]):
        print("--------------------------------------------------------------------")
        print("정답입니다!")

        if(game.current_player == 1):  #현재 플레이어가 HumanPlayer일경우
            print(f"상대 AI의 패 {game.gameboard[game.opponent_index][move[0]]} 를 공개합니다.")
            print("--------------------------------------------------------------------")
            '''
            ans = input("더 맞추시겠습니까?(y/n)")
            if(ans=="y"):
                print("한 번 더 추리를 시작합니다.")
                continued = True
            else:
                print("추리를 종료합니다.")
            '''

        else: #현재 플레이어가 AI플레이어일경우
            print(f"당신의 패 {game.gameboard[game.opponent_index][move[0]]} 를 공개합니다.")
            print("--------------------------------------------------------------------")
            

            #print(self.gameboard)
    else:
        print("--------------------------------------------------------------------")
        print("오답입니다...")
            
        if game.draw[game.current_player] != []:
            for i, elem in enumerate(game.gameboard[game.current_player]):
                if elem == game.draw[game.current_player][-1]:
                    if(game.Code_b!=[] and game.Code_w!=[]):
                        print(f"아까 드로우했던 패 {elem} 를 공개합니다.")
                    #print("AI플레이어가 예측할 수 있는 당신 패의 후보 인덱스 : ", self.card_candidate[self.opponent_index])

                else:


                    pass
            else:
                pass
        print("--------------------------------------------------------------------")

    if(game.Debugging):
        print("당신(AI)가 뽑은 카드 리스트", game.draw[game.current_player])
        print("당신의 밝혀진 패의 인덱스", game.revealed_idx_list)
    game.play_move(move)

    #밝혀진 인덱스를 예상 조합에서 제외하기 위해서 작성해봄.
    game.unrevealed_index = [[],[i for i in range(len(game.gameboard[1]))], [j for j in range(len(game.gameboard[2]))]]
    for idx, card in enumerate(game.gameboard[1]):
        if card in game.reveal_info_player:
            game.unrevealed_index[1].remove(idx)

    for idx, card in enumerate(game.gameboard[2]):
        if card in game.reveal_info_computer:
            game.unrevealed_index[2].remove(idx)

    #뽑은 카드를 후보군에서 제외함
    for draw_card in game.draw[game.current_player]:
        if draw_card in game.card_candidate[game.opponent_index]:
            game.card_candidate[game.opponent_index].remove(draw_card)
     #드로우 과정에서 새로운 카드가 발생할 수 있음에 따라 이 아이디어는 수정함.
    '''
    if(game.current_player==2 and (game.Code_b + game.Code_w)==0):
        if(move[1] != answer and move[1] in game.card_candidate[1]):  #만약 내가 예측한 카드가 AI의 나의 카드 패에 대한 후보군에 있다면, 내가 예측한 카드는 나에게 없다고 생각할 수 있으므로 나의 카드 패 후보군에서 예측한 카드를 제외한다.
            game.card_candidate[1].remove(move[1])
    '''



    
    print("com_reveal",game.reveal_info_computer)
    print("player_reveal",game.reveal_info_player)
    
    game.show()
    

    ans = input("게임을 계속 진행하시겠습니까?(y/n)")
    while(ans not in ["y", "n"]):
        ans = input("게임을 계속 진행하시겠습니까?(y/n)") 
    if(ans=="n"):
        print("게임을 종료합니다.")
        exit(0)
game.show_lose()
