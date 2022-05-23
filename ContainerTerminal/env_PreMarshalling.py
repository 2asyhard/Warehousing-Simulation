
class Pre_marshalling_env:
    def __init__(self, initial_state):
        self.columns = len(initial_state[0])
        self.rows = len(initial_state)
        self.state = initial_state
        self.action_size = self.columns*(self.columns-1)
        self.action_list = [] # [[from stack, to stack], [], ... ]
        self.valid_action_list = dict() # self.valid_action_list[from stack, to stack] : bool
        self.initialize_action_list()
        self.get_valid_action_list()
        self.done = False
        self.check_terminal_state()


    def initialize_action_list(self):
        # make action list
        for i in range(self.columns):
            for j in range(self.columns):
                if i != j:
                    self.action_list.append([i, j])
                self.valid_action_list[i, j] = False


    def move_container(self, from_stack, to_stack):
        # if not self.valid_action_list[from_stack, to_stack]:
        #     print(f'Moving container from stack{from_stack} to stack{to_stack} is impossible')
        for i in range(self.rows):
            if self.state[i][from_stack] != 0:
                target_container = self.state[i][from_stack]
                self.state[i][from_stack] = 0
                break
        for i in range(self.rows):
            if self.state[-i-1][to_stack] == 0:
                self.state[-i-1][to_stack] = target_container
                break
        self.get_valid_action_list()
        self.check_terminal_state()


    def get_valid_action_list(self):
        # get possible action and impossible action
        stack_sizes = []
        for i in range(self.columns):
            tmp_stack_size = 0
            for j in range(self.rows):
                if self.state[j][i] != 0:
                    tmp_stack_size += 1
            stack_sizes.append(tmp_stack_size)

        for i in range(len(stack_sizes)): # from stack
            for j in range(len(stack_sizes)): # to stack
                # if from stack and to stack is same, continue
                if i == j:
                    continue
                # if from stack has no container, action is invalid
                if stack_sizes[i] == 0:
                    self.valid_action_list[i, j] = False
                # if to stack has maximum containers, action is invalid
                elif stack_sizes[j] == len(self.state):
                    self.valid_action_list[i, j] = False
                # else, it's valid
                else:
                    self.valid_action_list[i, j] = True


    def check_terminal_state(self):
        for i in range(self.columns):
            for j in range(self.rows - 1):
                if self.state[j][i] > self.state[j + 1][i]:
                    self.done = False
                    return
        self.done = True


    def get_top_container_num(self, stack):
        top_container = 0
        for i in range(self.rows):
            if self.state[i][stack] != 0:
                top_container = self.state[i][stack]
                break
        return top_container



class play_pre_marshalling:
    def __init__(self, initial_state):
        self.env = Pre_marshalling_env(initial_state)
        self.num_stacks = len(self.env.state[0])
        self.step = 0
        self.max_step = 100
        self.done = self.env.done
        self.selected_action = [-1, -1]


    def input_action(self):
        '''
        print available actions
        input from stack num
        input to stack num
        '''
        while True:
            from_stack = input(f"Enter from stack(1 ~ {self.num_stacks}): ")
            to_stack = input(f"Enter to stack(1 ~ {self.num_stacks}): ")
            if self.check_action_validity(from_stack, to_stack):
                from_stack, to_stack = int(from_stack) - 1, int(to_stack) - 1
                if self.env.valid_action_list[from_stack, to_stack]:
                    break
                else:
                    print(f"Moving container from stack {from_stack+1} to stack{to_stack+1} is in valid")
                    print(f"Please selected different stacks")

        return from_stack, to_stack


    def check_action_validity(self, from_stack, to_stack):
        '''
        check validity of action
        if invalid reinput action
        if valid execute action
        '''
        try:
            from_stack = int(from_stack)
            to_stack = int(to_stack)
        except:
            print("Please enter number")
            return False
        if 1<=from_stack<=self.num_stacks:
            if 1<=to_stack<=self.num_stacks and from_stack != to_stack:
                return True
            else:
                print(f"To stack number must be one of the following: {list(set(range(1, self.num_stacks+1)) - set([from_stack]))}")
        else:
            print(f"From stack number must be one of the following: {list(set(range(1, self.num_stacks+1)))}")

        return False


    def execute_action(self, from_stack, to_stack):
        container_num = self.env.get_top_container_num(from_stack)
        print(f'Move container {container_num}, from stack {from_stack+1} to stack {to_stack+1}')
        print()
        self.env.move_container(from_stack, to_stack)
        self.done = self.env.done


    def display_state(self):
        '''
        display changed state after executing action
        '''
        if self.step == 0:
            print('Initial state')
        if self.done:
            print('Terminal state')
        print(f"Step: {self.step}")
        for row in self.env.state:
            print(row)
        print('-'*60)


    def start(self):
        state_history = [self.env.state]
        while self.step < self.max_step:
            from_stack, to_stack = self.input_action()
            self.execute_action(from_stack, to_stack)
            self.step += 1
            self.display_state()
            state_history.append(self.env.state)
            if self.done:
                print('Terminal state reached')
                break

        print('State History')
        for state in state_history:
            for row in state:
                print(row)
            print('-'*20)

