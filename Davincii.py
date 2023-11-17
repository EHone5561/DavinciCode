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
        for _ in range(0, select_white):
            Code_w, Computer_hand = receive_Code(Code_w, Computer_hand)
    if select_white < 4: #예외 처리
        for _ in range(0, 4 - select_white):
            Code_b, Computer_hand = receive_Code(Code_b, Computer_hand)
    return (Code_b, Code_w, Computer_hand)

def Player_Start(Code_b, Code_w, Player_hand): #플레이어가 게임을 시작하기 전 패를 가져오는 메소드입니다.
    try: #플레이어의 입력을 받으므로 예외처리
        select_black = int(input("몇 개의 검은 색 패를 가져가시겠습니까? (최대 4개):"))
        assert (0 <= select_black <= 4)
        if select_black > 0:
            for _ in range(0, select_black):
                Code_b, Player_hand = receive_Code(Code_b, Player_hand)
        if select_black < 4:
            for _ in range(0, 4 - select_black):
                Code_w, Player_hand = receive_Code(Code_w, Player_hand)

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

def receive_Code(Code, receiver): #임의의 패산에서 하나의 패를 receiver에게 전달하는 메소드입니다.
    receiver.append(Code[0])
    Code = Code[1:]
    return (Code, receiver) #남은 패산과 추가된 손패

def sort_Code(Code): # 컴퓨터나 플레이어가 패를 가져온 후 올바른 순서로 정렬하기 위한 메소드입니다.
    Code.sort(key = lambda x: (x[-1].isdigit(), int(x[:-1]) if x[:-1].isdigit() else float('inf'), x))
    return Code

def find_Player_Joker(Code, joker_info): #플레이어가 가져온 패가 조커인 경우를 확인하고 조커를  배치하는 메소드입니다. 
    joker = False
    black = False
    if Code[-1][0] == 'J': #조커는 한 번에 두 개 들어오지 않는다.
        print('조커 발견')
        joker = True
        if Code[-1][1] == 'b':
            black = True
    if joker:
        try:
            act = int(input("조커를 둘 위치를 선택하세요 (맨 앞을 0부터):"))
            assert (0 <= act <= (len(Code) + 1))
        except (ValueError):
            print("정확한 위치를 입력해주세요.")
            return find_Player_Joker()
        except (AssertionError):
            print("올바른 위치가 아닙니다. 다시 입력해주세요.")
            return find_Player_Joker()
        if act == len(Code):
            act -= 1
        if black:
            Code.insert(act, 'jb')
            joker_info.append('jb')
            joker_info.append(act)
        else:
            Code.insert(act, 'jw')
            joker_info.append('jw')
            joker_info.append(act)
        Code = Code[:-1]
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
            Code.insert(act, 'jb')
            joker_info.append('jb')
            joker_info.append(act)
        else:
            Code.insert(act, 'jw')
            joker_info.append('jw')
            joker_info.append(act)
        Code = Code[:-1]
    return (Code, joker_info)

def delete_joker(Code, joker_info): #이미 배열한 조커가 마지막에도 오는 문제를 해결하기위해 만든 메소드였다. 신경쓰지 말 것
    if len(joker_info) != []:
        if Code[-1] == 'jb':
            Code = Code[:-1]
        elif Code[-1] == 'jw':
            Code = Code[:-1]
        else:
            pass
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

def draw_phase_player(Code_b, Code_w, joker_info, receiver): #플레이어가 드로우하는 페이즈로 관련 메소드들을 순서에 따라 배치해놓은 메소드입니다.
    if receiver[-1] == 'jb':
        receiver = receiver[:-1]
    elif receiver[-1] == 'jw':
        receiver = receiver[:-1]
    else:
        pass
    if (len(Code_b) == 0) and (len(Code_w) == 0):
        print("더 이상 가져올 수 있는 패가 없어 과정을 생략합니다.")
    else:
        while(True):
            print(f"검은색 패 수 : {len(Code_b)}, 흰색 패 수 {len(Code_w)}")
            act = input("무슨 색 패를 뽑으시겠습니까?(b or w): ")
            if act in ['B', 'b']:
                if (len(Code_b) == 0):
                    print("해당 색의 패가 부족하여 다른 색의 패를 드로우 하였습니다.")
                    Code_w, receiver = receive_Code(Code_w, receiver)
                    break
                else:
                    Code_b, receiver = receive_Code(Code_b, receiver)
                    break
            elif act in ['W','w']:
                if (len(Code_w) == 0):
                    print("해당 색의 패가 부족하여 다른 색의 패를 드로우 하였습니다.")
                    Code_b, receiver = receive_Code(Code_b, receiver)
                    break
                else:
                    Code_w, receiver = receive_Code(Code_w, receiver)
                    break
            else:
                print("제대로 입력해주세요(b or w)")
    receiver = sort_Code(receiver)
    receiver, joker_info = find_Player_Joker(receiver, joker_info)
    receiver, joker_info = delete_joker(receiver, joker_info)
    receiver = sort_Code(receiver)
    if joker_info != []:
        receiver, joker_info = sort_Joker(receiver, joker_info)
    else:
        pass
    return (Code_b, Code_w, joker_info, receiver)

def draw_phase_computer(Code_b, Code_w, joker_info, receiver): ######인공지능#######
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
                    Code_w, receiver = receive_Code(Code_w, receiver)
                    print("컴퓨터는 하얀색 패를 하나 가져갔습니다.")
                    break
                else:
                    Code_b, receiver = receive_Code(Code_b, receiver)
                    print("컴퓨터는 검은색 패를 하나 가져갔습니다.")
                    break
            elif act == 1:
                if (len(Code_w) == 0):
                    Code_b, receiver = receive_Code(Code_b, receiver)
                    print("컴퓨터는 검은색 패를 하나 가져갔습니다.")
                    break
                else:
                    Code_w, receiver = receive_Code(Code_w, receiver)
                    print("컴퓨터는 하얀색 패를 하나 가져갔습니다.")
                    break
            else:
                print("오류 발생 (시스템 종료)")
                exit()
    receiver = sort_Code(receiver)
    receiver, joker_info = find_Computer_Joker(receiver, joker_info)
    receiver, joker_info = delete_joker(receiver, joker_info)
    receiver = sort_Code(receiver)
    if joker_info != []:
        receiver, joker_info = sort_Joker(receiver, joker_info)
    else:
        pass
    return (Code_b, Code_w, joker_info, receiver)


def main(): #게임을 구성하는 메소드입니다.
    import time
    ############## 사전 준비 페이즈 ##############
    Code_b, Code_w = make_Code()
    Code_b, Code_w, Player_hand, Computer_hand = make_hand(Code_b, Code_w)
    Code_b, Code_w = add_joker(Code_b, Code_w)
    Code_b = shuffle_Code(Code_b)
    Code_w = shuffle_Code(Code_w)
    joker_info_computer = []
    joker_info_player = []
    ############## 사전 준비 페이즈 ##############

    print()
    print("플레이어의 손 패: ", sort_Code(Player_hand))
    print()
    print("컴퓨터의 손 패: ", sort_Code(Computer_hand)) #제대로 드로우하고 있는 확인하는 구문입니다. 게임과는 무관 

    ############## 게임 실행 페이즈 ##############
    while True:
        print()
        print("플레이어의 차례입니다.")
        print()
        time.sleep(1)
        Code_b, Code_w, joker_info_player, Player_hand = draw_phase_player(Code_b, Code_w, joker_info_player, Player_hand)
        print("플레이어의 손 패: ", Player_hand)
        time.sleep(2)
        print()
        print("컴퓨터의 차례입니다.")
        print()
        time.sleep(1)
        Code_b, Code_w, joker_info_computer, Computer_hand = draw_phase_computer(Code_b, Code_w, joker_info_computer, Computer_hand)
        print("컴퓨터의 손 패: ", Computer_hand) #일단 오류 없는지 확인하기 위한 출력, 본래에는 컴퓨터의 패 공개 여부에 따라 구현해야함.
        time.sleep(2)
    ############## 게임 실행 페이즈 ##############
main()
#일단 문제점을 적어두었다.

#첫 째, 조커를 마지막에서 인식해서 플레이어가 원하는 위치로 끼워넣기가 가능하다. 그러나 마지막에 있는 조커가 사라지지 않고 한 번 뒤에 사라진다. < 해결 필요

#둘 째, 플레이어의 드로우 페이즈에서 조커를 인식하는 것을 구현해 두었지만, 플레이어는 색깔과 남아있는 패의 수를 출력받아
#원하는 색깔의 패를 출력할 수 있도록 구현해야한다. << 해결 완료 Code_b 와 Code_w를 따로 둔다.

#향후 업데이트 필요