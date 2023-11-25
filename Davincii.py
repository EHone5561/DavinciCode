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
    draw.append(Code[0])
    Code = Code[1:]
    return (draw, Code, receiver) #남은 패산과 추가된 손패

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

def draw_phase_player(draw, Code_b, Code_w, joker_info, receiver): #플레이어가 드로우하는 페이즈로 관련 메소드들을 순서에 따라 배치해놓은 메소드입니다.
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
    receiver = sort_Code(receiver)
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
        draw = False
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
    receiver = sort_Code(receiver)
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

def view_hand_player(Player_hand, Computer_hand, reveal_info_computer):
    print("상대의 손패: ", encrypt_Code(Computer_hand, reveal_info_computer))
    print()
    print()
    print("플레이어의 손 패: ", Player_hand)
    ###### 암호화된 컴퓨터의 손패를 보여준다. ######
def find_code_in_reveal(Code, reveal):
    if (Code in reveal):
        return True
    else:
        return False

def reason_phase_player(draw, Player_hand, Computer_hand, reveal_list_player, reveal_list_computer, Game_over):
    while(True):
        print()
        while(True):
            try:
                idx = int(input("맞출 상대의 패의 번호를 선택해주세요(왼쪽부터 0): "))
                if 0 <= idx <= (len(Computer_hand) - 1):
                    break
            except(ValueError):
                print("위치 번호를 정확하게 입력해주세요.")
        while(True):
            try:
                print()
                value = input("상대의 패를 예측해주세요(ex: 3b, 7w, jb)):")
                assert (value[-1] in ['b', 'B', 'w', 'W']) #마지막 글자가 색깔과 관련되어 있는 지를 확인합니다.
                if (len(value) == 2): #일의 자리 숫자인 경우를 확인합니다.

                    if (value[0]).isdigit():
                        if (0 <= int(value[0]) <= 9):
                            pass
                        else:
                            raise AssertionError
                    else:  
                        if value[0] in ['J', 'j']:
                            pass
                        else:
                            raise AssertionError
                elif (len(value) == 3): #십의 자리 숫자인 경우를 확인합니다.
                    assert(int(value[0]) == 1)
                    assert(0 <= int(value[1]) <= 1)
                break
            except(ValueError):
                print("정확하게 입력해주세요.")
            except(AssertionError):
                print("숫자 + 색깔의 형식으로 다시 입력해주세요.")
        if (value[0] in (['j', 'J'] + [f"{i}" for i in range(12)])):
            if value == Computer_hand[idx]:
                print("--------------------------------------------------------------------")
                print("정답입니다!")
                print(f"상대의 패 {Computer_hand[idx]} 를 공개합니다.")
                print("--------------------------------------------------------------------")
                reveal_list_computer.append(Computer_hand[idx])
                print()
                if len(reveal_list_computer) != len(Computer_hand):
                    act = input("더 맞추시겠습니까? (y n) ")
                    if act in ['Y', 'y']:
                        print("한 번 더 추리를 시작합니다.")
                    elif act in ['N', 'n']:
                        print("추리를 종료합니다.")
                        break
                    else:
                        print("입력 오류입니다. 추리를 종료합니다.")
                        break
                else:
                    break
            else:
                print("--------------------------------------------------------------------")
                print("오답입니다...")
                if draw != []:
                    for i, elem in enumerate(Player_hand):
                        if elem == draw[0]:
                            print(f"아까 드로우했던 패 {elem} 를 공개합니다.")
                            reveal_list_player.append(Player_hand[i])
                        else:
                            pass
                else:
                    pass
                print("--------------------------------------------------------------------")
                
                print("추리를 종료합니다.")
                break
        else:
            print("입력 오류입니다. 다시 입력해주세요.")
    if len(reveal_list_computer) == len(Computer_hand):
        print("--------------------------------------------------------------------")
        print("상대방의 모든 패가 공개되었습니다. 당신의 승리입니다.")
        exit(0)
        print("--------------------------------------------------------------------")
        Game_Over = True
    elif len(reveal_list_player) == len(Player_hand):
        print("--------------------------------------------------------------------")
        print("플레이어의 모든 패가 공개되었습니다. 당신의 패배입니다.")
        exit(0)
        print("--------------------------------------------------------------------")
        Game_Over = True
    else:
        pass
    return (Player_hand, Computer_hand, reveal_list_player, reveal_list_computer, Game_over)

def reason_phase_computer(draw, Player_hand, Computer_hand, reveal_list_player, reveal_list_computer, Game_Over): ####### 인공지능 #######
    import random
    import time
    ###########################################################
    encrypted_code = encrypt_Code(Player_hand, reveal_list_player) #인공지능이 변수 encrypted_code를 입력받아 판단하도록 설계해야한다.
    ###########################################################
    while(True):
        print()
        idx = random.randint(0, len(Player_hand) - 1)
        value = '3b'
        if (value[0] in (['j'] + [f"{i}" for i in range(12)])):
            if value == Player_hand[idx]:
                print("--------------------------------------------------------------------")
                print("상대가 정답을 맞췄습니다")
                time.sleep(1)
                print(f"플레이어의 패 {Player_hand[idx]} 를 공개합니다.")
                print("--------------------------------------------------------------------")
                time.sleep(1)
                reveal_list_player.append(Player_hand[idx])
                if len(reveal_list_player) != len(Player_hand):
                    act = 'n' ##### 일단 컴퓨터는 재 추리를 하지 않도록 코드를 짰다.
                    if act in ['Y', 'y']:
                        print("상대는 한 번 더 추리를 시작합니다.")
                    elif act in ['N', 'n']:
                        print("상대가 추리를 종료합니다.")
                        break
                    else:
                        print("Value 오류")
                        break
                else:
                    break
            else:
                print("--------------------------------------------------------------------")
                print("상대가 정답을 맞추지 못하였습니다. ")
                time.sleep(1)
                if draw != []:
                    for i, elem in enumerate(Computer_hand):
                        if elem == draw[0]:
                            print(f"상대가 드로우했던 패 {elem} 를 공개합니다.")
                            reveal_list_computer.append(Computer_hand[i])
                        else:
                            pass
                else:
                    pass
                print("--------------------------------------------------------------------")
                time.sleep(1)
                
                print("추리를 종료합니다.")
                break
        else:
            print("입력 오류입니다. 다시 입력해주세요.")
    if len(reveal_list_computer) == len(Computer_hand):
        print("--------------------------------------------------------------------")
        print("컴퓨터의 모든 패가 공개되었습니다. 당신의 승리입니다.")
        exit(0)
        print("--------------------------------------------------------------------")
        Game_Over = True
    elif len(reveal_list_player) == len(Player_hand):
        print("--------------------------------------------------------------------")
        print("플레이어의 모든 패가 공개되었습니다. 당신의 패배입니다.")
        exit(0)
        print("--------------------------------------------------------------------")
        Game_Over = True
    else:
        pass
    return (Player_hand, Computer_hand, reveal_list_player, reveal_list_computer, Game_Over)




            
def main(): #게임을 구성하는 메소드입니다.
    import time
    ############## 사전 준비 페이즈 ##############
    print("--------------------------------------------------------------------")
    print("곧 게임을 시작합니다.")
    print("--------------------------------------------------------------------")
    time.sleep(1)
    Game_Over = False #게임이 종료되었는 지 관한 boolean 변수
    Code_b, Code_w = make_Code()
    Code_b, Code_w, Player_hand, Computer_hand = make_hand(Code_b, Code_w)
    Code_b, Code_w = add_joker(Code_b, Code_w)
    Code_b = shuffle_Code(Code_b)
    Code_w = shuffle_Code(Code_w)
    joker_info_computer = []
    joker_info_player = []
    reveal_info_player = []
    reveal_info_computer = []
    ############## 사전 준비 페이즈 ##############
    print("--------------------------------------------------------------------")
    print("게임이 시작되었습니다.")
    print()
    print("플레이어의 손 패: ", sort_Code(Player_hand))
    print()
    print("컴퓨터의 손 패: ", sort_Code(Computer_hand)) #제대로 드로우하고 있는 확인하는 구문입니다. 게임과는 무관 (디버깅용)
    print("--------------------------------------------------------------------")
    ############## 게임 실행 페이즈 ##############
    while not Game_Over:
        draw_player = []
        print("--------------------------------------------------------------------")
        print()
        print("플레이어의 차례입니다.")
        print()
        print("--------------------------------------------------------------------")
        time.sleep(1)
        draw_player, Code_b, Code_w, joker_info_player, Player_hand = draw_phase_player(draw_player, Code_b, Code_w, joker_info_player, Player_hand)
        view_hand_player(Player_hand, Computer_hand, reveal_info_computer)
        ###### 정답 추리 페이즈 #######
        Player_hand, Computer_hand, reveal_info_player, reveal_info_computer, Game_Over = reason_phase_player(draw_player, Player_hand, Computer_hand, reveal_info_player, reveal_info_computer, Game_Over)
        if Game_Over:
            print("게임이 종료되었습니다.")
            break
        else:
            pass
        ###### 정답 추리 페이즈 #######
        time.sleep(2)
        draw_computer = []
        print("--------------------------------------------------------------------")
        print()
        print("컴퓨터의 차례입니다.")
        print()
        print("--------------------------------------------------------------------")
        time.sleep(1)
        draw_computer, Code_b, Code_w, joker_info_computer, Computer_hand = draw_phase_computer(draw_computer, Code_b, Code_w, joker_info_computer, Computer_hand)
        ###### 정답 추리 페이즈 #######
        Player_hand, Computer_hand, reveal_list_player, reveal_list_computer, Game_Over = reason_phase_computer(draw_computer, Player_hand, Computer_hand, reveal_info_player, reveal_info_computer, Game_Over)
        if Game_Over:
            print("게임이 종료되었습니다.")
            break
        else:
            pass
        ###### 정답 추리 페이즈 #######
        time.sleep(2)
    ############## 게임 실행 페이즈 ##############
main()