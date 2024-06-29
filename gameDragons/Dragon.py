import pygame
from gameDragons import red
 
class Dragon:
    def __init__(self,coordsInicio=[96,32], bodyDragon=[[96, 32], [64, 32], [32, 32]], directionInicio="RIGHT", direction_blocks=['RIGHT','RIGHT','RIGHT'], color = 'red'):
        #body block = 32px x 32px -> grid layout
        
        self.body = bodyDragon
        self.position = coordsInicio
        self.direction = directionInicio    #RIGHT, UP, LEFT, DOWN
        self.last_direction = self.direction    #ultima direção que o dragao andou
        self.direction_blocks = direction_blocks    #: RIGHT, UP, LEFT, DOWN, c1, c2, c3, c4 
        self.color = color
        self.eatState = False

    def change_direction(self,direction:str):
        #Verificando direção atual para mudar somente em casos válidos
        #Atualizando o valor de direction_blocks do pescoço para fazer a curva
        if direction == 'UP' and self.last_direction != 'DOWN' and self.last_direction != 'UP':
            self.direction = 'UP'

            if(self.last_direction == 'RIGHT'):     #adiciona a direção de uma curva
                self.direction_blocks[0] = 'c4'
            elif(self.last_direction == 'LEFT'):
                self.direction_blocks[0] = 'c3'
                
        elif direction == 'DOWN' and self.last_direction != 'UP' and self.last_direction != 'DOWN':
            self.direction = 'DOWN'
            
            if(self.last_direction == 'RIGHT'):     #adiciona a direção de uma curva
                self.direction_blocks[0] = 'c2'
            elif(self.last_direction == 'LEFT'):
                self.direction_blocks[0] = 'c1'

        elif direction == 'LEFT' and self.last_direction != 'RIGHT' and self.last_direction != 'LEFT':
            self.direction = 'LEFT'
            
            if(self.last_direction == 'UP'):        #adiciona a direção de uma curva
                self.direction_blocks[0] = 'c2'
            elif(self.last_direction == 'DOWN'):
                self.direction_blocks[0] = 'c4'

        elif direction == 'RIGHT' and self.last_direction != 'LEFT' and self.last_direction != 'RIGHT':
            self.direction = 'RIGHT'
            
            if(self.last_direction == 'UP'):        #adiciona a direção de uma curva
                self.direction_blocks[0] = 'c1'
            elif(self.last_direction == 'DOWN'):
                self.direction_blocks[0] = 'c3'

    def move(self):
        if self.direction == 'UP':
            self.position[1] -= 32  #posição y
        if self.direction == 'DOWN':
            self.position[1] += 32  #posição y
        if self.direction == 'LEFT':
            self.position[0] -= 32  #posição x
        if self.direction == 'RIGHT':
            self.position[0] += 32 #posição x

        self.last_direction = self.direction
    
    def eat(self,foodPosition):
        if self.position == foodPosition:
            self.direction_blocks.insert(0,self.direction)      #adiciona mais uma direção de um bloco (cabeça)
            self.eatState = True
        else:
            self.eatState = False
            self.body.pop()

        return self.eatState
    
    def update(self,display_size, other_dragon):
        self.move()
        self.body.insert(0, list(self.position))
        
        if(not self.eatState):
            for index in range(len(self.direction_blocks)-1,-1,-1):     #atualizando a direção dos blocos
                self.direction_blocks[index] = self.direction_blocks[index-1]

        self.direction_blocks[0] = self.direction                   #atualizando a direção da cabeça
        #print(self.direction_blocks)
        
        # Game Over conditions

        # Getting out of bounds
        if self.position[0] < 0 or self.position[0] > display_size[0]-32:
            print("Para fora da tela")
            return True
        if self.position[1] < 0 or self.position[1] > display_size[1]-32:
            print("Para fora da tela")
            return True

        # Touching the snake body
        for block in self.body[1:]:
            if self.position == block:
                print("Tocou no seu corpo")
                return True
        
        if other_dragon != None:
            for block in other_dragon.body:
                if self.position == block:
                    print("Tocou no outro corpo")
                    return True
            
        return False    #tudo ok

    def draw_dragon(self, display, surf):
        if self.color == 'blue':
            for index, pos in enumerate(self.body):  # desenhando bloco a bloco de acordo com suas direções
                if index == 0:
                    match self.direction_blocks[0]:
                        case 'DOWN': display.window.blit(surf.blue_dragon_sprites['head']['DOWN'], pos)
                        case 'RIGHT': display.window.blit(surf.blue_dragon_sprites['head']['RIGHT'], pos)
                        case 'UP': display.window.blit(surf.blue_dragon_sprites['head']['UP'], pos)
                        case 'LEFT': display.window.blit(surf.blue_dragon_sprites['head']['LEFT'], pos)
                elif index < len(self.body) - 1:
                    match self.direction_blocks[index]:
                        case 'DOWN': display.window.blit(surf.blue_dragon_sprites['body']['DOWN'], pos)
                        case 'RIGHT': display.window.blit(surf.blue_dragon_sprites['body']['RIGHT'], pos)
                        case 'UP': display.window.blit(surf.blue_dragon_sprites['body']['UP'], pos)
                        case 'LEFT': display.window.blit(surf.blue_dragon_sprites['body']['LEFT'], pos)
                        case 'c1': display.window.blit(surf.blue_dragon_sprites['bodyC']['C1'], pos)
                        case 'c2': display.window.blit(surf.blue_dragon_sprites['bodyC']['C2'], pos)
                        case 'c3': display.window.blit(surf.blue_dragon_sprites['bodyC']['C3'], pos)
                        case 'c4': display.window.blit(surf.blue_dragon_sprites['bodyC']['C4'], pos)
                else:
                    match self.direction_blocks[index]:  # tail
                        case 'DOWN': tail = surf.blue_dragon_sprites['tail']['DOWN']
                        case 'RIGHT': tail = surf.blue_dragon_sprites['tail']['RIGHT']
                        case 'UP': tail = surf.blue_dragon_sprites['tail']['UP']
                        case 'LEFT': tail = surf.blue_dragon_sprites['tail']['LEFT']
                        case 'c1':
                            if self.body[-2][0] == self.body[-1][0] + 32:
                                tail = surf.blue_dragon_sprites['tail']['RIGHT']
                            else:
                                tail = surf.blue_dragon_sprites['tail']['DOWN']
                        case 'c2':
                            if self.body[-2][0] == self.body[-1][0] - 32:
                                tail = surf.blue_dragon_sprites['tail']['LEFT']
                            else:
                                tail = surf.blue_dragon_sprites['tail']['DOWN']
                        case 'c3':
                            if self.body[-2][0] == self.body[-1][0] + 32:
                                tail = surf.blue_dragon_sprites['tail']['RIGHT']
                            else:
                                tail = surf.blue_dragon_sprites['tail']['UP']
                        case 'c4':
                            if self.body[-2][0] == self.body[-1][0] - 32:
                                tail = surf.blue_dragon_sprites['tail']['LEFT']
                            else:
                                tail = surf.blue_dragon_sprites['tail']['UP']

                    display.window.blit(tail, pos)
        else:
            for index, pos in enumerate(self.body):  # desenhando bloco a bloco de acordo com suas direções
                if index == 0:
                    match self.direction_blocks[0]:
                        case 'DOWN': display.window.blit(surf.red_dragon_sprites['head']['DOWN'], pos)
                        case 'RIGHT': display.window.blit(surf.red_dragon_sprites['head']['RIGHT'], pos)
                        case 'UP': display.window.blit(surf.red_dragon_sprites['head']['UP'], pos)
                        case 'LEFT': display.window.blit(surf.red_dragon_sprites['head']['LEFT'], pos)
                elif index < len(self.body) - 1:
                    match self.direction_blocks[index]:
                        case 'DOWN': display.window.blit(surf.red_dragon_sprites['body']['DOWN'], pos)
                        case 'RIGHT': display.window.blit(surf.red_dragon_sprites['body']['RIGHT'], pos)
                        case 'UP': display.window.blit(surf.red_dragon_sprites['body']['UP'], pos)
                        case 'LEFT': display.window.blit(surf.red_dragon_sprites['body']['LEFT'], pos)
                        case 'c1': display.window.blit(surf.red_dragon_sprites['bodyC']['C1'], pos)
                        case 'c2': display.window.blit(surf.red_dragon_sprites['bodyC']['C2'], pos)
                        case 'c3': display.window.blit(surf.red_dragon_sprites['bodyC']['C3'], pos)
                        case 'c4': display.window.blit(surf.red_dragon_sprites['bodyC']['C4'], pos)
                else:
                    match self.direction_blocks[index]:  # tail
                        case 'DOWN': tail = surf.red_dragon_sprites['tail']['DOWN']
                        case 'RIGHT': tail = surf.red_dragon_sprites['tail']['RIGHT']
                        case 'UP': tail = surf.red_dragon_sprites['tail']['UP']
                        case 'LEFT': tail = surf.red_dragon_sprites['tail']['LEFT']
                        case 'c1':
                            if self.body[-2][0] == self.body[-1][0] + 32:
                                tail = surf.red_dragon_sprites['tail']['RIGHT']
                            else:
                                tail = surf.red_dragon_sprites['tail']['DOWN']
                        case 'c2':
                            if self.body[-2][0] == self.body[-1][0] - 32:
                                tail = surf.red_dragon_sprites['tail']['LEFT']
                            else:
                                tail = surf.red_dragon_sprites['tail']['DOWN']
                        case 'c3':
                            if self.body[-2][0] == self.body[-1][0] + 32:
                                tail = surf.red_dragon_sprites['tail']['RIGHT']
                            else:
                                tail = surf.red_dragon_sprites['tail']['UP']
                        case 'c4':
                            if self.body[-2][0] == self.body[-1][0] - 32:
                                tail = surf.red_dragon_sprites['tail']['LEFT']
                            else:
                                tail = surf.red_dragon_sprites['tail']['UP']

                    display.window.blit(tail, pos)

    def to_dict(self):
        return {
            'body': [{'x': block[0], 'y': block[1]} for block in self.body],
            'position': self.position,
            'direction': self.direction,
            'last_direction': self.last_direction,
            'direction_blocks': self.direction_blocks,
            'eatState': self.eatState
        }
