import pygame, sys, time
from random import randint
import math

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('Images/sphere_anim1.png').convert_alpha()
        self.image_base = pygame.image.load('Images/sphere_anim1.png').convert_alpha()
        self.rect = self.image.get_rect(center = (200,130))
        self.x = 200
        self.y = 130
        self.angle = 0
        # animation
        sphere_anim1 = pygame.image.load('Images/sphere_anim1.png').convert_alpha()
        sphere_anim2 = pygame.image.load('Images/sphere_anim2.png').convert_alpha()
        sphere_anim3 = pygame.image.load('Images/sphere_anim3.png').convert_alpha()
        self.index_animation = 0
        self.sphere_images = [sphere_anim1, sphere_anim2, sphere_anim3]


    def contrôles_joueur(self):
        self.touche = pygame.key.get_pressed()
        if self.touche[pygame.K_z] :
            self.y -= 5
        if self.touche[pygame.K_s] :
            self.y += 5
        if self.touche[pygame.K_q]:
            self.x -= 5
        if self.touche[pygame.K_d]:
            self.x += 5


    def animation(self):
        self.index_animation += 0.1
        if self.index_animation >= 2 : self.index_animation = 0
        self.image_base = self.sphere_images[int(self.index_animation)]


    def rotation(self):
        self.image = pygame.transform.rotate(self.image_base, self.angle)
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.angle -= 1

    def update(self):
        self.contrôles_joueur()
        self.animation()
        self.rotation()



class Personnage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # charge les images de l'animation du personnage
        perso_invoc1 = pygame.image.load('Images/perso_standing1.png').convert_alpha()
        perso_invoc2 = pygame.image.load('Images/perso_standing2.png').convert_alpha()
        perso_invoc3 = pygame.image.load('Images/perso_standing3.png').convert_alpha()
        perso_invoc4 = pygame.image.load('Images/perso_standing4.png').convert_alpha()
        self.indicateur_chgmt_image = 0
        self.index_animation = 0
        self.perso_invoc = [perso_invoc1, perso_invoc2, perso_invoc3, perso_invoc4, ]
        self.image = pygame.image.load('Images/perso_standing1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (420, 395))

    def perso_animation(self):  # lorsque la variable indicateur_chgmt_image est égale à 1, 2, 3 et 4 le personnage change d'image; on la fait monter jusqu'à 28 pour créer un délais entre chaque animation
        self.indicateur_chgmt_image += 0.1
        self.index_animation = self.indicateur_chgmt_image
        if int(self.index_animation) >= len(self.perso_invoc) - 1: self.index_animation = len(self.perso_invoc) - 1
        if self.indicateur_chgmt_image >= 28:
            self.index_animation = 0
            self.indicateur_chgmt_image = 0

        self.image = self.perso_invoc[int(self.index_animation)]

    def update(self):
        self.perso_animation()



class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Images/proj_foudre.png').convert_alpha()

        r = randint(500, 600)
        theta = randint(0, 360)   
        theta_rad = theta * (math.pi / 180)
        x = int(420 + (r * math.cos(theta_rad)))
        y = int(341 + (r * -math.sin(theta_rad)))
        self.image = pygame.transform.rotate(self.image, (theta - 90))      # pivote l'image de l'éclair  pour qu'elle pointe vers le personnage au centre de l'écran, quelle que soit sa position
        self.rect = self.image.get_rect(center=(x, y))

    def mouvement_projectile(self):
        vecteur_ProjectPerso = (420 - self.rect.x), (341 - self.rect.y)
        norme_vecteur_ProjectPerso = math.sqrt((420 - self.rect.x) ** 2 + (341 - self.rect.y) ** 2)
        Vect_projectile = vecteur_ProjectPerso[0] / norme_vecteur_ProjectPerso, vecteur_ProjectPerso[1] / norme_vecteur_ProjectPerso

        self.rect.x += round(Vect_projectile[0]) * 2
        self.rect.y += round(Vect_projectile[1]) * 2

    def update(self):
        self.mouvement_projectile()




def score_éliminations():                               # créé l'image qui montre le score lorsque le jeu est actif
    score = texte.render(f'Score: {enmi_tués}',False, "Black")
    score_rect = score.get_rect( center = (150,60))
    screen.blit(score, score_rect)

def score_temps():                                      # détermine le temps de jeu
    temps = int(pygame.time.get_ticks() / 1000) - temps_global
    return temps

def collisions_sprites():                               # détecte les collisions entre les éclairs, le joueur et le personnage => si la valeur retournée est False, le jeu s'arrête
    if pygame.sprite.spritecollide(personnage.sprite, projectile, False):
        projectile.empty()                              # vide les instances de la classe Projectile => quand le jeu se relance tous les éclairs auront disparu
        return False
    elif pygame.sprite.spritecollide(joueur.sprite, projectile, True):
        global enmi_tués
        enmi_tués += 1
        return True
    elif pygame.sprite.spritecollide(joueur.sprite, personnage, False):
        joueur.empty()
        joueur.add(Joueur())
        projectile.empty()
        return False
    else : return True



pygame.init()
screen = pygame.display.set_mode((900,700))      # afficher et définir la taille de la fenêtre (largeur, hauteur)
pygame.display.set_caption('Invocateur')         # afficher le nom du jeu sur la barre de la fenêtre
clock = pygame.time.Clock()                      # variable qui stocke le temps => permet de définir le taux de rafraichissement avec la dernière ligne du code (l.189)

jeu_actif = True                                 # variable qui définit  si le jeu est actif (True) ou non (False)
enmi_tués = 0
durée_jeu = 0
temps_global = 0
score_GameOver = 0


# Groupes => on sépare le personnage du joueur et des éclairs pour détecter par la suite les collisions entre chaque groupe
joueur = pygame.sprite.GroupSingle()
joueur.add(Joueur())

personnage = pygame.sprite.GroupSingle()
personnage.add(Personnage())

projectile = pygame.sprite.Group()


arrière_plan = pygame.image.load('Images/Arrière_plan.png').convert()
texte = pygame.font.Font(None, 60)
texte_gameOver = pygame.font.Font(None, 60)
surface_txt_gameOver = texte.render("appuyez sur Espace pour recommencer", False, "brown")


# timer
projectile_timer = pygame.USEREVENT + 1
pygame.time.set_timer(projectile_timer, 920)

while True :
    for event in pygame.event.get():                    # les événements du jeu, tels que les actions du joueur et le timer
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and jeu_actif == False:  # permet de recommencer une partie en appuyant sur espace, et de remettre le compteur du score à 0
            jeu_actif = True
            enmi_tués = 0

        if event.type == projectile_timer and jeu_actif == True:
            projectile.add(Projectile())                    # chaque fois que le timer se déclenche, une nouvelle instance de la classe Projectile se crée


    if jeu_actif == True :            # boucle de la fenêtre de jeu principale
        screen.blit(arrière_plan,(0,0))
        score_éliminations()
        durée_jeu = score_temps()


        joueur.draw(screen)
        joueur.update()

        personnage.draw(screen)
        personnage.update()

        projectile.draw(screen)
        projectile.update()
        
        # collisions
        jeu_actif = collisions_sprites()

    else :                             # boucle menu 'Game Over'
        screen.fill((63,34,4))
        screen.blit(surface_txt_gameOver, (65, 500))

        temps_global = int(pygame.time.get_ticks() / 1000)
        txt_durée_jeu = texte.render(f'Vous avez survécu pendant {durée_jeu} secondes', False, ("Black"))
        durée_jeu_rect = txt_durée_jeu.get_rect(center=(450, 60))
        screen.blit(txt_durée_jeu, durée_jeu_rect)

        # afficher le score final
        score_GameOver = enmi_tués
        score_GO_image = texte.render(f'Score: {score_GameOver}', False, "Black")
        score_GO_rect = score_GO_image.get_rect(midleft =(50, 130))
        screen.blit(score_GO_image, score_GO_rect)


    pygame.display.update()
    clock.tick(60)                                    # ne dois pas s'actualiser plus de 60 fois par seconde ( limite à 60 FPS)
