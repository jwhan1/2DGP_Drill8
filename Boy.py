from pico2d import *

def start(e):
    return e[0] == 'START'
def pressA(e):
    return e[0] == 'AUTORUN' and e[1].key == SDLK_a
def time_out(e):
    return e[0] == 'TIME_OUT'
def right_down(e):
    return e[0] == 'KEY_DOWN' and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'KEY_UP' and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'KEY_DOWN' and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'KEY_UP' and e[1].key == SDLK_LEFT
class Idle:
    @staticmethod
    def enter(boy,e):
        if start(e) or right_up(e):
            boy.action = 3
        elif left_up(e):
            boy.action = 2
        elif time_out(e):
            if boy.action == 1:
                boy.action = 3
            elif boy.action == 0:
                boy.action = 2

        boy.start_time = get_time()
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))
    @staticmethod
    def draw(boy):
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Autorun:
    @staticmethod
    def enter(boy,e):
        if pressA(e):
            if boy.dir >= 0:
                boy.action = 1
                boy.dir = -3
            else :
                boy.action = 0
                boy.dir = 3
        boy.frame = 0
        boy.start_time = get_time()
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):#벽을 만나면 방향전환
        boy.frame = (boy.frame + 1) % 8

        if boy.x >= 750:
            boy.dir = 3
            boy.action = 0
        elif boy.x <= 0:
            boy.dir = -3
            boy.action = 1
        #이동
        if boy.action == 1:#오른쪽으로
            boy.x = boy.x + 10
        else:
            boy.x = boy.x - 10
            
        if get_time() - boy.start_time > 5:#5초 후 정지
            print(boy.x)
            boy.state_machine.add_event(('TIME_OUT', 0))


    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy,e):
        boy.action=3

    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(boy.frame*100,300,100,100,3.141592/2, '', boy.x-25,boy.y-25,100,100)

class Run:
    @staticmethod
    def enter(boy,e):
        if right_down(e):
            boy.action = 1#오른쪽으로
            boy.dir = 1
        elif left_down(e):
            boy.action = 0#왼쪽으로
            boy.dir = -1
    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if 0 < boy.x+boy.dir * 5 and boy.x+boy.dir * 5 < 750:
            boy.x += boy.dir * 5
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame*100,boy.action*100,100,100,boy.x,boy.y)

class StateMachine:
    def __init__(self,o):
        self.o = o#자기와 연결된 객체
        self.event_que=[] #발생한 이벤트 담기

    def start(self, start_state):
        # 현재 상태를 시작 상태로 만듬.
        self.cur_state = start_state # Run
        self.cur_state.enter(self.o,('START', 0))
   
    def add_event(self,event):
        self.event_que.append(event)#상태머신용 이벤트 추가
        
    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        # 현재 상태 업데이트
        self.cur_state.do(self.o) 
        #이벤트 발생 시 상태 변환
        if self.event_que:
            e = self.event_que.pop(0)#이벤트가 있으면 리스트의 첫번째 요소 꺼냄
            
            for check_event, next_state, in self.transitions[self.cur_state].items():
                
                if check_event(e):
                    print(f'exit from{self.cur_state}')
                    self.cur_state.exit(self.o,e)
                    self.cur_state = next_state
                    print(f'enter to{self.cur_state}')
                    self.cur_state.enter(self.o,e)

    def draw(self):
        self.cur_state.draw(self.o)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90 # 위치
        self.frame = 0 # 움직임
        self.dir = 0 # +:오른쪽, -:왼쪽
        self.action = 3 # 움직임

        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체를 위한 상태 머신인지 알려줄 필요

        self.state_machine.start(Idle) # 첫 상태 집어넣기

        #idle에서 time_out이면 sleep으로 sleep에서 space_down이면 idle로
        self.state_machine.set_transitions(
            {
                Idle: {pressA: Autorun, right_down:Run, left_down:Run},
                Run: {right_up:Idle, left_up:Idle},
                Autorun: {time_out: Idle, right_down:Run, left_down:Run}
            })
    def update(self):
        self.state_machine.update()
        self.frame = (self.frame + 1) % 8
    def draw(self):
        self.state_machine.draw()
    def handle_event(self, event):
        #input event
        #state machine event : (이벤트 종류, 큐)
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            self.state_machine.add_event(('AUTORUN', event))
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            self.state_machine.add_event(('KEY_UP', event))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            self.state_machine.add_event(('KEY_DOWN', event))
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            self.state_machine.add_event(('KEY_UP', event))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            self.state_machine.add_event(('KEY_DOWN', event))

        pass
    def start(self):
        pass
    def state(self):
        pass
