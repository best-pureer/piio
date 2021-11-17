#coding:utf-8
import webbrowser
import tkinter
import wiringpi
pins = []
io_state = [0]*40

pins_to_Wiring = [
    -3, -5,
    8, -5,
    9, -1,
    7, 15,
    -1, 16,
    0, 1,
    2, -1,
    3, 4,
    -1, 5,
    12, -1,
    13, 6,
    14, 10,
    -1, 11,
    30, 31,
    21, -1,
    22, 26,
    23, -1,
    24, 27,
    25, 28,
    -1, 29,
]

pins_to_BCM = [
    -3, -5,
    2, -5,
    3, -1,
    4, 14,
    -1, 15,
    17, 18,
    27, -1,
    22, 23,
    -1, 24,
    10, -1,
    9, 25,
    11, 8,
    -1, 7,
    0, 1,
    5, -1,
    6, 12,
    13, -1,
    19, 16,
    26, 20,
    -1, 21,
]

pins_to_PHY = [
    -3, -5,
    8, -5,
    9, -1,
    7, 15,
    -1, 16,
    0, 1,
    2, -1,
    3, 4,
    -1, 5,
    12, -1,
    13, 6,
    14, 10,
    -1, 11,
    30, 31,
    21, -1,
    22, 26,
    23, -1,
    24, 27,
    25, 28,
    -1, 29,
]

pins_to_func = [
    -3, -5,
    'SDA1', -5,
    'SCL1', -1,
    7, 'TXD',
    -1, 'RXD',
    0, 1,
    2, -1,
    3, 4,
    -1, 5,
    'MOSI', -1,
    'MISO', 6,
    'SCLK', 'CE0',
    -1, 'CE1',
    'SDA0', 'SCL0',
    21, -1,
    22, 26,
    23, -1,
    24, 27,
    25, 28,
    -1, 29,
]

pins_map = [pins_to_Wiring, pins_to_BCM, pins_to_PHY, pins_to_func]

colors = ['#D9D6C3', '#E0861A']

face_state = 0
direction = 2


def fresh_io_state():
    for i in range(40):
        if pins_to_Wiring[i] >= 0:
            io_state[i] = wiringpi.digitalRead(pins_to_Wiring[i])
            pins[i]['bg'] = colors[io_state[i]]


def fresh_io_map(pin_type):
    for i in range(40):
        if pins_to_Wiring[i] >= 0:
            pins[i]['text'] = pins_map[pin_type][i]


def reverse_pin(num):
    wiringpi.digitalWrite(pins_to_Wiring[num], 1-io_state[num])
    print('1-io_state[num]:'+str(1-io_state[num]))
    io_state[num] = wiringpi.digitalRead(pins_to_Wiring[num])
    print('read io_state[num]:'+str(io_state[num]))
    pins[num]['bg'] = colors[io_state[num]]


location = [[0] * 2 for i in range(40)]
rel_location = [[0] * 2 for i in range(40)]


def get_location(phy_pin_num):
    global direction
    global face_state
    weight = 36
    height = 27
    x = 0
    y = 0
    if direction == 0:
        x = weight*(phy_pin_num % 2)
        y = height*(phy_pin_num//2)
    elif direction == 1:
        x = weight*(phy_pin_num // 2)
        y = height*(phy_pin_num % 2)
        y = y+500
    elif direction == 2:
        x = weight*(phy_pin_num % 2)
        x = x+630
        y = height*(phy_pin_num//2)
    else:
        x = weight*(phy_pin_num // 2)
        y = height*(phy_pin_num % 2)

    return x, y


pins_width = 2
pins_height = 1


def gen_button(w, i, s=''):
    if s != '':
        if s == 'GND':
            pins.append(tkinter.Button(
                w, text=s, width=pins_width, height=pins_height, bg='#121a2a', fg='#f6f5ec'))
        if s == '3.3V':
            pins.append(tkinter.Button(
                w, text=s, width=pins_width, height=pins_height, bg='#f05b72', fg='#f6f5ec'))
        if s == '5V':
            pins.append(tkinter.Button(
                w, text=s, width=pins_width, height=pins_height, bg='#ed1941', fg='#f6f5ec'))
    else:
        pins.append(tkinter.Button(w, text=str(
            pins_to_Wiring[i]), width=pins_width, height=pins_height, command=lambda: reverse_pin(i)))
    x = get_location(i)[0]
    y = get_location(i)[1]
    pins[i].place(x=x, y=y)
    location[i][0] = x
    location[i][1] = y
    rel_location[i][0] = x
    rel_location[i][1] = y

wiringpi.wiringPiSetup()
w = tkinter.Tk()
w_x = 770
w_y = 600
w.geometry(str(w_x)+"x"+str(w_y))


for i in range(40):
    if pins_to_Wiring[i] == -1:
        gen_button(w, i, 'GND')
    elif pins_to_Wiring[i] == -3:
        gen_button(w, i, '3.3V')
    elif pins_to_Wiring[i] == -5:
        gen_button(w, i, '5V')
    else:
        gen_button(w, i)


face_name = ['UP', 'BOTTOM']
face_color = ['#2a5caa', '#64492b']
face = tkinter.Button(w, text="THIS IS UP SIDE", fg='#f6f5ec',
                      bg='#2a5caa')


def fresh_io_face():
    global face_state
    face_state = 1-face_state
    face['text'] = 'THIS IS '+face_name[face_state]+' SIDE'
    face['bg'] = face_color[face_state]
    for i in range(20):
        x = rel_location[2*i][0]
        y = rel_location[2*i][1]
        pins[2*i].place(x=rel_location[2*i+1][0],
                        y=rel_location[2*i+1][1])
        pins[2*i+1].place(x=x,
                          y=y)
        rel_location[2*i][0] = rel_location[2*i+1][0]
        rel_location[2*i][1] = rel_location[2*i+1][1]
        rel_location[2*i+1][0] = x
        rel_location[2*i+1][1] = y
        _x = location[2*i][0]
        _y = location[2*i][1]
        location[2*i][0] = location[2*i+1][0]
        location[2*i][1] = location[2*i+1][1]
        location[2*i+1][0] = _x
        location[2*i+1][1] = _y

face['command'] = fresh_io_face
face.place(x=w_x/2.7, y=200)

fresh = tkinter.Button(w, text="fresh io", bg='#1d953f',
                       command=fresh_io_state)
fresh.place(x=w_x/2.7, y=250)
fresh_io_state()

def go_to_web():
    webbrowser.open("pureer.cn")


web = tkinter.Button(w, text="WEB:pureer.cn", command=go_to_web)
web.place(x=20, y=560)


def go_to_git():
    webbrowser.open("github.com/best-pureer/piio.git")


git = tkinter.Button(
    w, text="GIT:github.com/best-pureer/piio.git", command=go_to_git)
git.place(x=180, y=560)

pin_type = tkinter.IntVar()
r0 = tkinter.Radiobutton(w, variable=pin_type, value=0,
                         text="Wiring", command=lambda: fresh_io_map(0))
r1 = tkinter.Radiobutton(w, variable=pin_type, value=1,
                         text="BCM", command=lambda: fresh_io_map(1))
r2 = tkinter.Radiobutton(w, variable=pin_type, value=2,
                         text="PHY", command=lambda: fresh_io_map(2))
r3 = tkinter.Radiobutton(w, variable=pin_type, value=3,
                         text="func", command=lambda: fresh_io_map(3))
pin_type.set(0)
r0.place(x=w_x/3.3, y=300)
r1.place(x=w_x/3.3+w_x*0.13, y=300)
r2.place(x=w_x/3.3+w_x*0.24, y=300)
r3.place(x=w_x/3.3+w_x*0.33, y=300)


def rotate(act):
    global direction
    direction += act
    if(direction < 0):
        direction = 3
    if(direction > 3):
        direction = 0
    for i in range(40):
        x = location[i][0]-270-35
        y = location[i][1]-280-35
        _x = -act*y+270+35
        y = act*x+280+35
        x = _x
        if direction == 0:
            pins[i].place(x=x+56, y=y-116)
            rel_location[i][0] = x+56
            rel_location[i][1] = y-116
        elif direction == 1:
            pins[i].place(x=x+10+11*(i//2), y=y-10+55)
            rel_location[i][0] = x+10+11*(i//2)
            rel_location[i][1] = y-10+55
        elif direction == 2:
            pins[i].place(x=x+20, y=y)
            rel_location[i][0] = x+20
            rel_location[i][1] = y
        elif direction == 3:
            pins[i].place(x=x+105-11*(i//2), y=y-170)
            rel_location[i][0] = x+105-11*(i//2)
            rel_location[i][1] = y-170

        location[i][0] = x
        location[i][1] = y


l_rotate = tkinter.Button(w, text="-90°",
                          bg='#1d953f', command=lambda: rotate(-1))
r_rotate = tkinter.Button(w, text="+90°",
                          bg='#1d953f', command=lambda: rotate(1))
l_rotate.place(x=w_x/2.7, y=350)
r_rotate.place(x=w_x/2.1, y=350)


w.mainloop()
