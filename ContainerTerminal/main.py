from env_PreMarshalling import play_pre_marshalling
from env_BRP import play_BRP


def check_int_str(input_):
    try:
        input_ = int(input_)
    except:
        print('\n**Please type in number only**\n')
        return False
    return True


def check_number_range(input_, start, end):
    num_list = list(range(start, end + 1))
    if input_ in num_list:
        return True
    else:
        print(f'\n**please select number between {start} ~ {end}**\n')
        return False


def select_env():
    print('-' * 40)
    print('||||||||||-Select environment-||||||||||')
    env_dict = {
        1: ('Pre-marshalling', play_pre_marshalling),
        2: ('Block Relocation Problem', play_BRP),
    }
    while True:
        print('-'*40)

        for key, item in env_dict.items():
            print(f"{key}: {item[0]}")

        input_str = input('Environment number: ')
        if check_int_str(input_str):
            selected_env = int(input_str)
        else:
            continue

        if check_number_range(selected_env, 1, len(env_dict)):
            print(f"\n--{env_dict[selected_env][0]} selected--\n")
            break

    return env_dict[selected_env][1]


def select_env_settings():
    print('-' * 40)
    print("||||||||||-Environment setting-||||||||||")
    print('-' * 40)

    # number of stacks
    while True:
        print('Number of stacks(columns) range: 3 ~ 8')
        stacks = input('Select number of stacks: ')

        if check_int_str(stacks):
            stacks = int(stacks)
        else:
            continue

        if check_number_range(stacks, 3, 8):
            print(f'\nNumber of stacks: {stacks}\n')
            break

    # number of tiers
    while True:
        print(f'Number of tiers(rows) range: 3 ~ {stacks}')
        tiers = input('Select number of tiers: ')

        if check_int_str(tiers):
            tiers = int(tiers)
        else:
            continue

        if check_number_range(tiers, 3, stacks):
            print(f'\nNumber of stacks: {tiers}\n')
            break

    return stacks, tiers


def auto_settings(stacks, tiers):
    # stacks와 tiers로 자동으로 초기 상태 생성
    state = [[0]*stacks] + [[tier*stacks+stack for stack in range(1,stacks+1)] for tier in range(tiers-1)][::-1]
    print('Initial state is automatically set as below')
    for tier in state:
        print(tier)
    return state


def main():
    play = select_env()
    stacks, tiers = select_env_settings()
    state = auto_settings(stacks, tiers)
    play = play(state)
    play.start()


if __name__ == '__main__':
    main()