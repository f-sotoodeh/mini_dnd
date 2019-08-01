from random import randint
import _pickle as pickle
import conf

class Board:
    def __init__(self, spec):
        self.size = spec.get('size')
        self.door = spec.get('door')
        self.medic = spec.get('medic')
        self.walls = spec.get('walls')

    def draw(self, creatures):
        o = {i.position: i.name for i in creatures}
        o.update({w: '#' for w in self.walls})
        o.update({self.door: '^'})
        o.update({self.medic: '+'})

        print(' _'*self.size[1])
        for r in range(self.size[0]):
            print('|', end='')
            for c in range(self.size[1]):
                o.get((r,c),'_')
                print(o.get((r,c),'_'), end='|')
            print()


class Player:
    def __init__(self, spec):
        self.name = spec.get('name')
        self.position = spec.get('position')
        self.health = spec.get('health')
        self.ear = spec.get('ear')
        self.noise = spec.get('noise')
        self.speed = spec.get('speed')
    

class Dragon:
    def __init__(self, spec):
        self.name = '&'
        self.position = spec.get('position')
        self.health = spec.get('health')
        

class Game:
    def __init__(self):
        self.board = Board(conf.board)
        self.player = Player(conf.player)
        self.dragon = Dragon(conf.dragon)
        self.scope = [self.player,]
        self.play()

    def distance(self, x, y):
        return abs(self.dragon.position[0]-x) + abs(self.dragon.position[1]-y)

    def dragon_fire(self, x, y):
        self.player.health -= 1
        if not self.player.health:
            self.finish(False)

    def check(self, x, y):
        if x == self.board.door[0] and y == self.board.door[1]:
            self.finish(True)

        if x == self.board.medic[0] and y == self.board.medic[1]:
            self.player.health = conf.player.get('health')
            self.board.medic = (-1, -1)

        if self.distance(x, y) < self.player.noise:
            self.dragon_fire(x, y)

        if self.distance(x, y) < self.player.ear:
            self.scope.append(self.dragon)
        elif self.dragon in self.scope:
            self.scope.remove(self.dragon)


    def move(self, p):
        x = self.player.position[0] + p[0]
        y = self.player.position[1] + p[1]
        self.check(x, y)
        
        x = 0 if x < 0 else x
        x = self.board.size[0]-1 if x >= self.board.size[0] else x
        y = 0 if y < 0 else y
        y = self.board.size[1]-1 if y >= self.board.size[1] else y
        self.player.position = (x, y)

    def finish(self, res):
        if res:
            print('YOU WON :)')
        else:
            print('YOU LOSE :(')
        exit()

    def play(self):
        while True:
            self.board.draw(self.scope)
            {
                'U': lambda: self.move((-1, 0)),
                'L': lambda: self.move((0, -1)),
                'D': lambda: self.move((1, 0)),
                'R': lambda: self.move((0, 1)),
                'Q': lambda: self.quit(),
            }.get(input(':').upper(), lambda:None)()

    def quit(self):
        exit()



def new_game():
    g = Game()


def load_game():
    pass



def main():
    hlp = '''press
    U : up
    D : down
    L : left
    R : right
    Q : quit
    '''
    msg = '''Press
    ? : help
    N : start a new game
    L : load a saved game
    Q : quit
    \r'''
    {
        '?': lambda: print(hlp),
        'N': new_game,
        'L': load_game,
        'Q': exit,
    }.get(input(msg).upper(), lambda:print('-_-'))()

if __name__ == '__main__':
    main()