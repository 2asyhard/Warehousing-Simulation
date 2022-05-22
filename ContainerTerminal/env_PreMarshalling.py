
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


    def initialize_action_list(self):
        # make action list
        for i in range(self.columns):
            for j in range(self.columns):
                if i != j:
                    self.action_list.append([i, j])
                self.valid_action_list[i, j] = -1


    def move_container(self, in_action):
        out_stack = in_action[0]
        in_stack = in_action[1]
        for i in range(self.rows):
            if self.state[i, out_stack] != 0:
                target_container = self.state[i, out_stack]
                self.state[i, out_stack] = 0
                break
        for i in range(self.rows):
            if self.state[-i-1, in_stack] == 0:
                self.state[-i-1, in_stack] = target_container
                break


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
                elif stack_sizes[i] == self.rows:
                    self.valid_action_list[i, j] = False
                # else, it's valid
                else:
                    self.valid_action_list[i, j] = True


    def check_terminal_state(self):
        for i in range(self.columns):
            for j in range(self.rows - 1):
                if self.state[j, i] > self.state[j + 1, i]:
                    return False
        return True


class play_pre_marshalling:
    def __init__(self, initial_state):
        self.env = Pre_marshalling_env(initial_state)
        self.step = 0
        self.finished = False


    def input_action(self):
        '''
        print available actions
        input from stack num
        input to stack num

        '''
        pass


    def execute_action(self):
        pass


    def check_action_validity(self):
        '''
        check validity of action
        if invalid reinput action
        if valid execute action
        :return:
        '''
        pass


    def display_state(self):
        '''
        display changed state after executing action
        :return:
        '''
        pass


    def start(self):
        pass



