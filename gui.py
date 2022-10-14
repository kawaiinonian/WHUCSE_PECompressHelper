import tkinter as tk
from helper import helper
from functools import partial
import tkinter.messagebox as msgbox

root = tk.Tk()
root.title("武带信安PE作业helper ^-^")
root.geometry("1000x600")
root.iconbitmap('./icon.ico')

input_string = tk.StringVar()
input_name = tk.StringVar()
input_address = tk.StringVar()
input_direct = tk.StringVar()

def shift_window():
    def apply_shift():
        offset = input_string.get()
        offset = int(offset, base=16)
        h.shift(offset, h.data.keys())
        table_update()
        top.destroy()
    top = tk.Toplevel()
    top.title("shift")
    top.geometry("300x100+100+100")
    offset_label = tk.Label(top, text='offset:')
    offset_entry = tk.Entry(top, textvariable=input_string)
    apply_button = tk.Button(top, text="确认", command=apply_shift)
    offset_label.pack()
    offset_entry.pack()
    apply_button.pack()    

def change_address_window(name):
    def apply_address_change(name):
        val = input_string.get()
        val = int(val, base=16)
        h.change_address(val, name)
        table_update()
        top.destroy()
    top = tk.Toplevel()
    top.title("change address for " + name)
    top.geometry("300x100+100+100")
    new_address_label = tk.Label(top, text='new address:')
    new_address_entry = tk.Entry(top, textvariable=input_string)
    apply_button = tk.Button(top, text="确认", command=lambda: apply_address_change(name))
    new_address_label.pack()
    new_address_entry.pack()
    apply_button.pack()
    
def change_direct_window(name):
    def apply_direct_change(name):
        val = input_string.get()
        val = int(val, base=16)
        h.change_direct(val, name)
        table_update()
        top.destroy()
    top = tk.Toplevel()
    top.title("change direct for " + name)
    top.geometry("300x100+100+100")
    new_address_label = tk.Label(top, text='new direct:')
    new_address_entry = tk.Entry(top, textvariable=input_string)
    apply_button = tk.Button(top, text="确认", command=lambda: apply_direct_change(name))
    new_address_label.pack()
    new_address_entry.pack()
    apply_button.pack()

def insert_window():
    def apply_insert():
        name = input_name.get()
        address = input_address.get()
        address = int(address, base=16)
        direct = input_direct.get()
        direct = int(direct, base=16)
        h.insert(name, address, direct)
        frame = tk.Frame(frame_root)
        table_labels.append(tk.Label(frame, text=str(name) + '\t\t' + '0x%X\t\t0x%X'%(address, direct)))
        table_labels[-1].pack(padx='10px', side=tk.LEFT, anchor='nw')
        tk.Button(frame, text='修改指针', width=10, height=1, command=partial(change_direct_window, name)).pack(padx='10px', side=tk.RIGHT, anchor='nw')
        tk.Button(frame, text='修改地址', width=10, height=1, command=partial(change_address_window, name)).pack(padx='10px', side=tk.RIGHT, anchor='nw')
        tk.Button(frame, text='删除', width=5, height=1, command=partial(delete_data, name)).pack(padx='10px', side=tk.RIGHT, anchor='nw')
        frame.pack(fill=tk.X, side=tk.TOP, anchor='n')
        frames[name] = frame
        top.destroy()
    top = tk.Toplevel()
    top.title("insert a new pointer")
    top.geometry("600x100+100+100")
    frame_entries = tk.Frame(top)
    frame_label = tk.Frame(top)
    tk.Label(frame_label, text="name\t\taddress\t\tdirect").pack(side = tk.LEFT)
    frame_label.pack(side=tk.TOP)
    tk.Entry(frame_entries, textvariable=input_name).pack(side=tk.LEFT)
    tk.Entry(frame_entries, textvariable=input_address).pack(side=tk.LEFT)
    tk.Entry(frame_entries, textvariable=input_direct).pack(side=tk.LEFT)
    frame_entries.pack(side=tk.TOP)
    apply_button = tk.Button(top, text="确认", command=apply_insert)
    apply_button.pack()

def undo_apply():
    h.undo()
    table_update()

def save_apply():
    h.save_data()
    msgbox.showwarning("保存", "保存还就那个成昆")
    
def delete_data(name):
    result = msgbox.askokcancel("删除", "小老板想好了删")
    if result:
        frames[name].destroy()
        h.delete_pointer(pointer=name)
        del frames[name]

def window_init():
    for key in h.data.keys():
        frame = tk.Frame(frame_root)
        table_labels.append(tk.Label(frame, text=str(key) + '\t\t' + '0x%X\t\t0x%X'%(h.data[key][0], h.data[key][1])))
        table_labels[-1].pack(padx='10px', side=tk.LEFT, anchor='nw')
        tk.Button(frame, text='修改指针', width=10, height=1, command=partial(change_direct_window, key)).pack(padx='10px', side=tk.RIGHT, anchor='nw')
        tk.Button(frame, text='修改地址', width=10, height=1, command=partial(change_address_window, key)).pack(padx='10px', side=tk.RIGHT, anchor='nw')
        tk.Button(frame, text='删除', width=5, height=1, command=partial(delete_data, key)).pack(padx='10px', side=tk.RIGHT, anchor='nw')
        frame.pack(fill=tk.X, side=tk.TOP, anchor='n')
        frames[key] = frame

def table_update():
    for i, key in enumerate(h.data.keys()):
        table_labels[i].config(text = str(key) + '\t\t' + '0x%X\t\t0x%X'%(h.data[key][0], h.data[key][1]))

def generate_log():
    h.get_log()

h = helper('./dict.pkl')
frame_root = tk.Frame(root)
frame_root.pack()
frame_title = tk.Frame(frame_root)
tk.Label(frame_title, text="name\t\t\taddress\t\tdirect").pack(padx='10px', side=tk.LEFT, anchor='nw')
tk.Button(frame_title, text='偏移', width=5, height=1, command=shift_window).pack(padx='10px', side=tk.RIGHT, anchor='nw')
tk.Button(frame_title, text='撤回', width=5, height=1, command=undo_apply).pack(padx='10px', side=tk.RIGHT, anchor='nw')
tk.Button(frame_title, text='保存', width=5, height=1, command=save_apply).pack(padx='10px', side=tk.RIGHT, anchor='nw')
tk.Button(frame_title, text='插入', width=5, height=1, command=insert_window).pack(padx='10px', side=tk.RIGHT, anchor='nw')
tk.Button(frame_root, text='生成日志', width=10, height=1, command=generate_log).pack(padx='10px', side=tk.BOTTOM, anchor='nw')
frame_title.pack(fill=tk.X, side=tk.TOP, anchor='n')
frames = {}
table_labels = []

window_init()
root.mainloop()