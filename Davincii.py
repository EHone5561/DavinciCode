def make_Code(): #패산을 생성 혹은 초기화하는 메소드입니다.
    Code_b = [f"{i}b" for i in range(12)] #패산 생성 (검은 색) # n + w (n: 숫자, b:색깔(black)) 
    Code_w = [f"{i}w" for i in range(12)] #패산 생성 (하얀 색)# n + w (n: 숫자, w:색깔(white)) 
    return (Code_b, Code_w) # @variable Code(list) 색깔 별 패산

def make_hand(Code_b, Code_w): #게임 시작전 기본 패를 분배합니다.
    Computer_hand = [] 
    Player_hand = []
    Code_b = shuffle_Code(Code_b) #검은색 패산을 셔플하는 단계
    Code_w = shuffle_Code(Code_w) #하얀색 패산을 셔플하는 단계
    ###################################################
    Code_b, Code_w, Computer_hand = Computer_Start(Code_b, Code_w, Computer_hand) #Computer가 패를 선택하여 가져오기
    print(f"컴퓨터가 4개의 임의의 패를 가져갔습니다.")
    ###################################################
    Code_b, Code_w, Player_hand = Player_Start(Code_b, Code_w, Player_hand) #Player가 패를 선택하여 가져오기
    print("당신은 4개의 패를 손에 집었습니다.")
    return (Code_b, Code_w, Player_hand, Computer_hand)

def make_CodeDummy(Code_b, Code_w): #게임 시작 패 분배가 끝난 후 패 산을 만드는 메소드입니다.
    Code = Code_b + Code_w
    Code.append("Jb") #검은색 조커 추가
    Code.append("Jw") #하얀색 조커 추가
    return Code

def Computer_Start(Code_b, Code_w, Computer_hand):
    import random
    select_white = random.randint(0,4) #임시 #뽑은 하얀 색 패의 수
    if select_white > 0: #예외 처리
        for _ in range(0, select_white):
            Code_w, Computer_hand = receive_Code(Code_w, Computer_hand)
    if select_white < 4: #예외 처리
        for _ in range(0, 4 - select_white):
            Code_b, Computer_hand = receive_Code(Code_b, Computer_hand)
    return (Code_b, Code_w, Computer_hand)

def Player_Start(Code_b, Code_w, Player_hand):
    try:
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



def shuffle_Code(Code): # @param Code(list): 섞이지 않은 패산
    import random
    random.shuffle(Code)
    return Code #섞인 패산 

def receive_Code(Code, receiver): # @param Code(list): 패산
    receiver.append(Code[0])
    Code = Code[1:]
    return (Code, receiver) #남은 패산과 추가된 손패

def sort_Code(Code):
    Code.sort(key = lambda x: (x[-1].isdigit(), int(x[:-1]) if x[:-1].isdigit() else float('inf'), x))
    return Code

def find_Player_Joker(Code, joker_info): #조커는 한 번에 두 개 들어오지 않는다.
    joker = False
    black = False
    if Code[-1][0] == 'J':
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
            Code.insert(act, 'jb') ################################################
            joker_info.append('jb')
            joker_info.append(act)
        else:
            Code.insert(act, 'jw') ##############################################
            joker_info.append('jw')
            joker_info.append(act)
        Code = Code[:-1]
    return (Code, joker_info)
def delete_joker(Code, joker_info):
    if len(joker_info) != []:
        if Code[-1] == 'jb':
            Code = Code[:-1]
        elif Code[-1] == 'jw':
            Code = Code[:-1]
        else:
            pass
    return (Code, joker_info)
def sort_Joker(Code, joker_info): #조커의 위치를 매개변수로 받아 다시 입력하기
    if len(joker_info) == 2:
        
        Code.insert(joker_info[1], joker_info[0])
    elif (len(joker_info) == 4):
        Code.insert(joker_info[1], joker_info[0])
        Code.insert(joker_info[3], joker_info[2])
    else:
        pass
    return (Code, joker_info)

def draw_phase_player(Code, joker_info, receiver):
    if receiver[-1] == 'jb':
        receiver = receiver[:-1]
    elif receiver[-1] == 'jw':
        receiver = receiver[:-1]
    else:
        pass
    Code, receiver = receive_Code(Code, receiver)
    receiver = sort_Code(receiver)
    receiver, joker_info = find_Player_Joker(receiver, joker_info)
    receiver, joker_info = delete_joker(receiver, joker_info)
    receiver = sort_Code(receiver)
    if joker_info != []:
        receiver, joker_info = sort_Joker(receiver, joker_info)
    else:
        pass
    return (Code, joker_info, receiver)


def main():
    Code_b, Code_w = make_Code()
    Code_b, Code_w, Player_hand, Computer_hand = make_hand(Code_b, Code_w)
    Code = shuffle_Code(make_CodeDummy(Code_b, Code_w))
    joker_info_computer = []
    joker_info_player = []
    print(Code)
    print()
    print("플레이어의 손 패: ", sort_Code(Player_hand))
    print()
    print("컴퓨터의 손 패: ", sort_Code(Computer_hand))
    while True:
        Code, joker_info_player, Player_hand = draw_phase_player(Code, joker_info_player, Player_hand)
        print("플레이어의 손 패: ", Player_hand)
        import time
        time.sleep(5)
        # Code, joker_info_computer, Computer_hand = draw_phase_computer(Code, )


main()
#일단 문제점을 적어두었다.
#첫 째, 조커를 마지막에서 인식해서 플레이어가 원하는 위치로 끼워넣기가 가능하다. 그러나 마지막에 있는 조커가 사라지지 않고 한 번 뒤에 사라진다.
#둘 째, 플레이어의 드로우 페이즈에서 조커를 인식하는 것을 구현해 두었지만, 플레이어는 색깔과 남아있는 패의 수를 출력받아
#원하는 색깔의 패를 출력할 수 있도록 구현해야한다.
#향후 업데이트 필요