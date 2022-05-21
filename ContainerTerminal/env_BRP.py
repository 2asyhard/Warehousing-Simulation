from copy import deepcopy
import numpy as np


class BRP_env:
    def __init__(self, initial_state):
        self.columns = len(initial_state[0])
        self.rows = len(initial_state)
        self.state = initial_state
        self.action_size = self.columns*(self.columns-1)
        self.decreased_number = 0
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
        out_stack = in_action[1]
        in_stack = in_action[2]
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


    def check_releasable_container(self):
        '''
        if releasable container exists in
        '''
        min_container_num = float('inf')
        for column in range(self.columns):
            for row in range(self.rows):
                if self.state[row][column] != 0:
                    min_container_num = min(min_container_num, self.state[row][column])

        found = False
        container_info = [-1,-1,-1] # [row, column, container number]
        for column in range(self.columns):
            for row in range(self.rows):
                if self.state[row][column] != 0:
                    if self.state[row][column] == min_container_num:
                        found = True
                        container_info = [row, column, self.state[row][column]]
                        #self.state[row][column] = 0
                    break
            if found:
                break

        return found, container_info


    def check_terminal_state(self):
        if np.count_nonzero(self.state) > 0:
            return False
        return True


    def decrease_container_num_by_1(self):
        for column in range(self.columns):
            for row in range(self.rows):
                if self.state[row][column] != 0:
                    self.state[row][column] -= 1
        self.decreased_number += 1


    def get_display_state(self):
        '''
        when container is released and most imminent container number is bigger than 1,
        each number of containers can be decreased so most imminent containers number can be 1

        [[0,0,0],               [[0,0,0],
        [1,2,3],   released->   [0,2,3],    +    [1]
        [4,5,6]]                [4,5,6]]

        display 1               display 2
        [[0,0,0],               [[0,0,0],
        [0,2,3],       or       [0,1,2],
        [4,5,6]]                [3,4,5]]

        display 2 can have advantage when using neural network for training
        '''
        display_state = deepcopy(self.state)
        for row in range(self.rows):
            for col in range(self.columns):
                if display_state[row][col] > 0:
                    display_state[row][col] += self.decreased_number
        return display_state


class play_BRP:
    def __init__(self, initial_state):
        self.env = BRP_env(initial_state)





