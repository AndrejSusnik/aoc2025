import itertools
from functools import cache

file = 'input'
# file = 'example'

@cache
def get_joltage(buttons, state):
    if buttons == ():
        return state

    return get_joltage(buttons[1:], press_button(buttons[0], state))

def press_button(button, state):
        t = list(state)
        for idx in button:
            t[idx] = state[idx] + 1
        
        return tuple(t) 

class Machine:
    def __init__(self, light_configuration, availabe_buttons, joltage_requirement):
        self.final_configuration = list(map(lambda x: x == '#', light_configuration[1:-1]))
        self.available_buttons = tuple(map(lambda x: tuple(map(int, x[1:-1].split(','))), availabe_buttons))
        self.joltage_requirement =  tuple(map(int, joltage_requirement[1:-1].split(",") ))

    def press_button_p1(self, button, initial_config):
        for idx in button:
            initial_config[idx] = not initial_config[idx]
        
        return initial_config

    def press_button_p2(self, button, initial_config):
        for idx in button:
            initial_config[idx] = initial_config[idx] + 1
        
        return initial_config

    def get_min_button_presses_p1(self):
        presses = 1
        while True:
            all_combinations = self.get_combinations_of_len_n(presses)
            for c in all_combinations:
                initial_config = [False] * len(self.final_configuration)
                for r in c:
                    initial_config = self.press_button_p1(r, initial_config)
                if initial_config == self.final_configuration:
                    return presses
            presses += 1

    def get_min_button_presses_p2(self):
        pass

    def get_combinations_of_len_n(self, n):
        return itertools.combinations_with_replacement(self.available_buttons, n)

    def get_combinations_of_len_p2(self, n):
        return itertools.combinations_with_replacement(range(len(self.available_buttons)), n)

data = open(file).readlines()

machines = []
for machine_str in data:
    machine_desc = machine_str.split()

    machines.append(Machine(machine_desc[0], machine_desc[1:-1], machine_desc[-1]))

print(f"Part 1: {sum(map(lambda x: x.get_min_button_presses_p1(), machines))}")
print(f"Part 2: {sum(map(lambda x: x.get_min_button_presses_p2(), machines))}")
