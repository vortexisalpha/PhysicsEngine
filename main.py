import math 
import pygame
from pygame.locals import *
from random import randint
import sys
pygame.init()

class Engine:

    def __init__(self):        
        self.clock = pygame.time.Clock()

        (self.width, self.height) = (800, 800)
        self.screen = pygame.display.set_mode((self.width, self.height))
        background_colour=(255,255,255)
        self.screen.fill(background_colour)  

        self.circle_list = []   
        self.pendulum_list = []  

        #slider variables
        self.x_scroll1 = 10
        self.x_scroll2 = 10

        self.bar_y = 200

        self.bottom = Bottom(self.screen)

    def draw_circle(self):
        newCircle = Circle(self.screen,2)
        return newCircle
    
    def draw_pendulum(self, length , velocity):
        newPendulum = Pendulum(self.screen,length,velocity)
        return newPendulum
    

    def doCircle(self):
        #Run the circle on mous click and append the circle to the list 'circle_list'
        self.circle_list.append(self.draw_circle()) 
        self.created_circle = True

    def doPendulum(self, length, velocity):
        self.pendulum_list.append(self.draw_pendulum(length, velocity))
        self.created_pendulum = True

    #creates the slider on the left
    def slider (self, x,y,width,height,action=None):
        #gets mouse position
        cur = pygame.mouse.get_pos()
        #gets the type of mouse click
        click = pygame.mouse.get_pressed()
        if x + width > cur[0]> x and y + height + 12 > cur[1]> y -12:
            pygame.draw.rect(self.screen, (255,255,255),(x,y,width,height))
            if click[0] == 1 and action != None:
                if action =='scroll1':
                    self.x_scroll1 = cur[0]
                if action =='scroll2':
                    self.x_scroll2 = cur[0]
        else:
            pygame.draw.rect(self.screen,(255,255,255),(x,y,width,height))

    def initialise(self):
        self.running = True
        self.created_pendulum = False
        self.created_circle = False


        length,velocity = 300, 0.05

        while self.running:
            background_colour=(138, 45, 104)
            self.screen.fill(background_colour)
            self.bottomBar = self.bottom.drawBottom()

            #create the text for the velocity slider
            font_color=(0,0,0)
            font_obj=pygame.font.Font("Roboto-Regular.ttf",16)
            velocity_string = 'Velocity: ' + str(self.x_scroll1/1000*60)[:3]
            text_obj=font_obj.render(velocity_string,True,font_color)
            self.screen.blit(text_obj,(10,160))

            #create the velocity slider
            self.slider(10,self.bar_y, 75,2,action='scroll1')
            pygame.draw.rect(self.screen, (255,255,255), [self.x_scroll1-5, self.bar_y-12,10,24])

            
            #x_scroll1 gives an output with range of 81-11
            #we want max velocity range to be around 0.1- 0.01 so we can make this 0.081-0.011 by dividing by 1000
            velocity = self.x_scroll1/1000

            #create the text for the length slider
            font_color=(0,0,0)
            font_obj=pygame.font.Font("Roboto-Regular.ttf",16)
            length_string = 'Length: ' + str((self.x_scroll2-5)*10)
            text_obj=font_obj.render(length_string,True,font_color)
            self.screen.blit(text_obj,(10,260))
            

            #create the length slider
            self.slider(10,self.bar_y+100, 75,2,action='scroll2')
            pygame.draw.rect(self.screen, (255,255,255), [self.x_scroll2-5, self.bar_y+100-12,10,24])
            
            #x_scroll1 gives an output with range of 81-11
            #we want max velocity range to be around 600- 50 so we can make this timsing by 10
            length = (self.x_scroll2-5)*10

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0] > 90: #On mouse click
                    type_of_click = pygame.mouse.get_pressed()
                    if type_of_click[0] == True:
                        self.doPendulum(length, velocity)
                        self.created_pendulum = True
                    if type_of_click[2] == True:
                        self.doCircle()
                        self.created_circle = True
                    

            #animate the circle using the class function that is in the circle class
            if self.created_circle == True:
                for i in range(len(self.circle_list)):
                    self.circle_list[i].animate()

            #do the same thing for the pendulum
            if self.created_pendulum == True:
                for i in range(len(self.pendulum_list)):
                    self.pendulum_list[i].animate()

            pygame.display.update()
            self.clock.tick(60)

class Circle:
    def __init__(self,screen,mass):
        self.radius = 20
        self.screen = screen
        self.mass = mass*1000
        self.circle = self.create_circle()
        self.velocity = 0
        self.force = 0
        self.acceleration = 9.8*10
        self.elastic_coefficient = 0.4
        self.cross_section = 3.14*self.radius*self.radius
        self.positionX = pygame.mouse.get_pos()[0]
        self.positionY = pygame.mouse.get_pos()[1]
        self.initialY = pygame.mouse.get_pos()[1]
        
    def create_circle(self):
        self.random_colour = (randint(0,255), randint(0,255), randint(0,255))
        return pygame.draw.circle(self.screen, self.random_colour ,pygame.mouse.get_pos(),self.radius,0 )

    def animate(self):
        #get verticle distance between bottom box and circle
        distance = self.positionY- 725
        #if falling
        
        bounced = False

        if distance <0 and bounced==False:
            self.force += self.acceleration*self.mass/60
            '''
            self.air_resistance = 0
            if self.force > 1:
                self.air_resistance = (0.5)*0.02*(self.velocity)*(self.velocity)*self.cross_section/60
            self.force -= self.air_resistance/60
            '''
            self.velocity += (self.force/self.mass)
            self.positionY += self.velocity/60
        #if hits the bottom    
        elif distance >=0:
            bounced=True
            self.force = -self.acceleration*self.mass/60
            self.velocity = -self.velocity*self.elastic_coefficient
            self.positionY += self.velocity/60      
        elif distance <0:
            self.force += self.acceleration*self.mass/60
           
            self.velocity += 100
            self.positionY += self.velocity/60

        return pygame.draw.circle(self.screen, self.random_colour ,[self.positionX,self.positionY],self.radius,0 )

class Bottom: 
    def __init__(self, screen):
        self.width = 800
        self.height = 50
        self.color = (90,90,90)
        self.screen = screen
    
    def drawBottom(self):
        return pygame.draw.rect(self.screen, self.color, pygame.Rect(0,800-self.height,self.width, self.height))
        
class Pendulum:
    def __init__(self, screen,length,velocity):
        #T=2pi*rootlength/g
        self.speed_constant = velocity
        self.pivotX = pygame.mouse.get_pos()[0]
        self.pivotY = pygame.mouse.get_pos()[1]
        self.screen=screen
        self.length = length
        self.theta = 45
        self.endPointX = self.pivotX + math.sin(self.theta)*self.length
        self.endPointY = self.pivotY + math.cos(self.theta)*self.length
        self.counter=0
        self.multiplyer = -1
        self.radius = 20
        self.pendulum = self.create_pendulum()
        self.angular_velocity = 0.2
        self.gravity = 0.1
        

    def create_pendulum(self):
        self.random_colour = (randint(0,255), randint(0,255), randint(0,255))
        self.line = pygame.draw.aaline( self.screen, (0,0,0), (self.pivotX , self.pivotY), (self.endPointX , self.endPointY))
        self.circle = pygame.draw.circle(self.screen, self.random_colour ,(self.endPointX , self.endPointY),self.radius,0 )
        
    def animate(self):
        self.force = self.gravity * math.sin(self.theta) 
        self.angular_acceleration = -self.force
        
        self.angular_velocity += self.angular_acceleration
        self.theta += self.angular_velocity*self.speed_constant

        self.endPointX = self.pivotX + math.sin(self.theta)*self.length
        self.endPointY = self.pivotY + math.cos(self.theta)*self.length
        self.line = pygame.draw.aaline( self.screen, (0,0,0), (self.pivotX , self.pivotY), (self.endPointX , self.endPointY))
        self.circle = pygame.draw.circle(self.screen, self.random_colour ,(self.endPointX , self.endPointY),self.radius,0 )
        
    

    

newEngine = Engine()
newEngine.initialise()