import pickle
import os
import copy as cp
import time

class helper():
    def __init__(self, path) -> None:
        self.path = path
        if os.path.getsize(self.path) != 0:
            with open(self.path, "rb") as f:
                self.data = pickle.load(f)
                self.init_data = cp.deepcopy(self.data)
                
        else:
            self.data = {}
        self.stack = []
    
    def insert(self, pointer, address, direct):
        self.stack.append(cp.deepcopy(self.data))
        if pointer not in self.data.keys():
            self.data[pointer] = (address, direct)

    def shift(self, offset, pointers):
        self.stack.append(cp.deepcopy(self.data))
        for pointer in pointers:
            self.data[pointer] = (self.data[pointer][0] - offset, self.data[pointer][1] - offset)

    def change_address(self, new_address, pointer):
        self.stack.append(cp.deepcopy(self.data))
        self.data[pointer] = (new_address, self.data[pointer][1])
        

    def change_direct(self, new_direct, pointer):
        self.stack.append(cp.deepcopy(self.data))
        self.data[pointer] = (self.data[pointer][0], new_direct)

    def delete_pointer(self, pointer):
        self.stack.append(cp.deepcopy(self.data))
        del self.data[pointer]

    def get_log(self):
        path = time.ctime().split(' ')
        path = "".join(path)
        path = path.split(':')
        path = "".join(path)
        with open("./%s.txt"%(path), 'w') as f:
            init_data_buffer = []   
            data_buffer = []         
            for key in self.init_data.keys():
                init_data_buffer.append(str(key) + '  ' + str(hex(self.init_data[key][0])) + '  ' + str(hex(self.init_data[key][1])))
            f.write(str(init_data_buffer) + '\n')
            for data in self.stack:
                stack_data_buffer = []
                for key in data.keys():
                    stack_data_buffer.append(str(key) + '  ' + str(hex(data[key][0])) + '  ' + str(hex(data[key][1])))
                f.write(str(stack_data_buffer) + '\n')
            for key in self.data.keys():
                data_buffer.append(str(key) + '  ' + str(hex(self.data[key][0])) + '  ' + str(hex(self.data[key][1])))
            f.write(str(data_buffer))
    def undo(self):
        self.data = self.stack.pop()

    def save_data(self):
        with open(self.path, "wb") as f:
            pickle.dump(self.data, f)
