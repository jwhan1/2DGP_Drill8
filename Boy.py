from pico2d import load_image, get_time

def start(e):
    return e[0] == 'START'
def pressA(e):
    return e[0] == 'AUTORUN' and e[1].type == 'a'
def time_out(e):
    return e[0] == 'TIME_OUT'

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3

        self.image = load_image('Labs/Lecture10_Character_Controller_1/animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체를 위한 상태 머신인지 알려줄 필요

        self.state_machine.start(Idle) # 첫 상태 집어넣기

        #idle에서 time_out이면 sleep으로 sleep에서 space_down이면 idle로
        self.state_machine.set_transitions(
            {
                Idle: {pressA: Autorun},
                Autorun: {time_out: Idle}
                })
    def update(self):
        self.state_machine.update()
        self.frame = (self.frame + 1) % 8
    def draw(self):
        self.state_machine.draw()
    def handle_event(self, event):
        #input event
        #state machine event : (이벤트 종류, 큐)
        self.state_machine.add_event(('INPUT', event))
        pass
    def start(self):
        pass
    def state(self):
        pass

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
            e = self.event_que.pop[0]#리스트의 첫번째 요소 꺼냄
            for check_event, next_state, in self.transitions(self.cur_state.items()):
                if check_event(e):
                    print(f'exit from{self.cur_state}')
                    self.cur_state.exit(self.o)
                    self.cur_state = next_state
                    print(f'enter to{self.cur_state}')
                    self.cur_state.enter(self.o)

class Idle:
    @staticmethod
    def enter(boy,e):
        boy.action = 3
        boy.frame = 0
        boy.dir = 0
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
    pass