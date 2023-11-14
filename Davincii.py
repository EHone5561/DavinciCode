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



def shuffle_Code(Code): # @parameter Code(list): 섞이지 않은 패산
    import random
    random.shuffle(Code)
    return Code #섞인 패산 

def receive_Code(Code, receiver): # @parameter Code(list): 패산
    receiver.append(Code[0])
    Code = Code[1:]
    return (Code, receiver) #남은 패산과 추가된 손패

def main():
    Code_b, Code_w = make_Code()
    Code_b, Code_w, Player_hand, Computer_hand = make_hand(Code_b, Code_w)
    Code = shuffle_Code(make_CodeDummy(Code_b, Code_w))
    print(Code)
    print()
    print("플레이어의 손 패: ", Player_hand)
    print()
    print("컴퓨터의 손 패: ", Computer_hand)

main()
