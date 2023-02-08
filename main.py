import pygame, sys
import random

FPS = 45

pygame.init()
screen_size = (600,600)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

class Balle:

    balles = []

    def __init__(self, position: list[float] , velocity: list[float], acceleration: list[float], rebound_coeff: list[float], radius: int, color: tuple[int], len_file: int) -> None:
        """
        initialise une balle
        à la fin de la fonction, la balle est ajouté à la fin de la variable de classe balles (list)

        Args:
            position (list[float]): 
                list contenant la position x et y du centre de la balle
                x et y sont de type float mais peuvent être int
            velocity (list[float]): 
                list contenant la vitesse de base de la balle x et y
                en 1s la position balle auras augmenté de x et y
                x et y sont de type float mais peuvent être int
            acceleration (list[float]): 
                list contenant l'accélération de la balle x et y
                en 1s la velocity de la balle auras augmenté de x et y
                x et y sont de type float mais peuvent être int
            rebound_coeff (list[float]): 
                list de coefficient de rebondissement de la balle x et y
                1 pour un rebont constant, <1 pour réduire la vitesse à chaque rebond, >1 pour augmenter la vitesse à chaque rebond
                x et y sont de type float mais peuvent être int
            radius (int): 
                le rayon de la balle en pixel
            color (tuple[int]): 
                un tuple (r,g,b) pour la couleur de la balle
        """
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.rebound_coeff = rebound_coeff
        self.radius = radius
        self.color = color
        self.len_file = len_file
        self.file = [position.copy()]
        Balle.balles.append(self)
    
    def affichage(self):
        """
        dessine le cercle sur l'écran
        """
        for i in self.file:
            pygame.draw.circle(screen, self.color, i, self.radius)
    
    def update(self, dt: int) -> None:
        """
        cette fonction est appeller à chaque frame.
        elle ajoute à la velocity l'acceleration multiplier par le temps entre les fram en seconde
        puis elle ajoute à la position la velocity multiplier par le temps entre les frame en seconde
        (multiplier par le temps en seconde permet d'avoir un déplacement constant peut importe le combre de frame)
        la fonction check ensuite les collision puis corrige la position des balles qui cerais sortie de l'écran

        Args:
            dt(int): temps entre chaque frame en ms
        """
        dt /= 1000
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.file.append(self.position.copy())
        if len(self.file) > self.len_file:
            del self.file[0]
        self.collision_detecion()
        self.correction_pos()
    
    def collision_detection_x(self) -> bool:
        """
        check si la bale sort de l'écran en x
        return True si la balle est en dehore de l'éran en x sinon False

        :return: True if the ball touches or goes beyond the left or right edges of the screen, and false otherwise
        """
        return self.position[0] - self.radius <= 0 or self.position[0] + self.radius >= screen_size[0]
    
    def collision_detection_y(self) -> bool:
        """
        check si la bale sort de l'écran en y
        return True si la balle est en dehore de l'éran en y sinon False

        :return: True if the ball hits the top or bottom of the screen, false otherwise
        """
        return self.position[1] - self.radius <= 0 or self.position[1] + self.radius >= screen_size[1]
    
    def collision_detecion(self) -> None:
        """
        The collision_detecion function checks if the ball has collided with any of the walls. 
        If it has, then it reverses its direction. réduit ou augmente aussi la vitesse en fonction de rebound_coeff
        """
        if self.collision_detection_x():
            self.velocity[0] *= - self.rebound_coeff[0]
        if self.collision_detection_y():
            self.velocity[1] *= - self.rebound_coeff[1]
    
    def correction_pos(self) -> None:
        """
        corrige la position de la balle si elle sort de l'écran 
        ex : si elle sort de 1 pixel à gauche du bord de l'éran, elle seras remis à 1 pixel à droite du bord de l'écran
        """
        if self.position[0] - self.radius < 0: 
            self.position[0] = 2 * self.radius - self.position[0]
            self.file.append(self.position.copy())
            if len(self.file) > self.len_file:
                del self.file[0]
        elif self.position[0] + self.radius > screen_size[0]: 
            self.position[0] = screen_size[0] - self.radius - ((self.position[0] + self.radius) - screen_size[0])
            self.file.append(self.position.copy())
            if len(self.file) > self.len_file:
                del self.file[0]
        if self.position[1] - self.radius < 0: 
            self.position[1] = 2 * self.radius - self.position[1]
            self.file.append(self.position.copy())
            if len(self.file) > self.len_file:
                del self.file[0]
        elif self.position[1] + self.radius > screen_size[1]: 
            self.position[1] = screen_size[1] - self.radius - ((self.position[1] + self.radius) - screen_size[1])
            self.file.append(self.position.copy())
            if len(self.file) > self.len_file:
                del self.file[0]

#Balle([150.0, 300.0], [-400.0, 0.0], [0.0, 1000.0], [1.0, 1.0], 50, (255, 255, 100))
#Balle([450.0, 300.0], [1000.0, -1000.0], [0.0, 1000.0], [1.0, 1.0], 50, (255, 100, 255))
#Balle([300.0, 300.0], [150.0, 500.0], [0.0, 1000.0], [1.0, 1.0], 50, (255, 100, 100))
#Balle([300.0, 300.0], [200.0, 200.0], [0.0, 500.0], [1.0, 1.0], 30, (100, 100, 255))
#Balle([300.0, 300.0], [500.0, 150.0], [0.0, 250.0], [1.0, 1.0], 10, (100, 255, 100))
Balle([screen_size[0]/2, screen_size[1]/2], [-500.0, 300.0], [-500.0, 500.0], [1, 1], 10, (255,0,0), 500)
Balle([screen_size[0]/2, screen_size[1]/2], [500.0, -300.0], [500.0, -500.0], [1, 1], 10, (0,255,255), 500)
r = random.randint
r2 = random.uniform
for i in range(0):
    Balle([r(100, screen_size[0] - 100), r(100, screen_size[1] - 100)], [r(-500, 500), r(-500, 500)], [r(-5000, 5000), r(-5000, 5000)], [1, 1], r(1,100), (r(0,255), r(0,255), r(0, 255)), 500)

def main():
    """
    The main function of the program.
    """
    while True:
        screen.fill((0,0,0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        for balle in Balle.balles:
            for _ in range(0,clock.get_time()*1, 1):
                balle.update(1)
            balle.affichage()

        pygame.display.flip()
        clock.tick(FPS)
        print(clock.get_fps())

if __name__ == "__main__":
    main()