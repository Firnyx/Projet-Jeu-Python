import pygame, sys, time
from random import randint
import math



def score_éliminations():
    score = texte.render(f'Score: {enmi_tués}',False, "Black")
    score_rect = score.get_rect( center = (150,60))
    screen.blit(score, score_rect)

def score_temps():
    temps = int(pygame.time.get_ticks() / 1000) - temps_global
    return temps

def mouvement_projectile(liste_projectile):

    if liste_projectile :
        for projectile_rect in liste_projectile:
            vecteur_ProjectPerso = (420 - projectile_rect.x), (341 - projectile_rect.y)
            norme_vecteur_ProjectPerso = math.sqrt((420 - projectile_rect.x)**2 + (341 - projectile_rect.y)**2)
            Vect_projectile = vecteur_ProjectPerso[0] / norme_vecteur_ProjectPerso, vecteur_ProjectPerso[1] / norme_vecteur_ProjectPerso

            projectile_rect.x += round(Vect_projectile[0])*2
            projectile_rect.y += round(Vect_projectile[1])*2


            screen.blit(ennemi, projectile_rect)

        return liste_projectile

    else : return []

def collisions_gameOver(perso, projectiles):
    if projectiles:
        for projectile_rect in projectiles:
            if perso.colliderect(projectile_rect): return False
    return True

def collisions_Joueur_Proj(joueur, projectiles):
    if projectiles:
        for projectile_rect in projectiles:
            if joueur.colliderect(projectile_rect):
                projectiles.remove(projectile_rect)
                global enmi_tués
                enmi_tués += 1

def perso_animation():
    global index_perso, indicateur_chgmt_image, surf_perso
    indicateur_chgmt_image += 0.1
    index_perso = indicateur_chgmt_image

    if int(index_perso) >= len(perso_invoc)-1: index_perso = len(perso_invoc)-1
    if indicateur_chgmt_image >= 28:
        index_perso = 0
        indicateur_chgmt_image = 0
    surf_perso = perso_invoc[int(index_perso)]




pygame.init()
screen = pygame.display.set_mode((900,700))                          # afficher et définir la taille de la fenêtre (largeur, hauteur)
pygame.display.set_caption('Invocateur')                             # afficher le nom du jeu sur la barre de la fenêtre
clock = pygame.time.Clock()                                          # variable qui stocke le temps => permet de définir le taux de rafraichissement avec la dernière ligne du code (l.180)


jeu_actif = True
enmi_tués = 0
durée_jeu = 0
temps_global = 0
score_GameOver = 0
projectile_rect_liste = []

# charge les images et les textes qui apparaîtront sur l'écran
ennemi = pygame.image.load('Images/proj_foudre.png').convert_alpha()
arrière_plan = pygame.image.load('Images/Arrière_plan.png').convert()
texte = pygame.font.Font(None, 60)
texte_gameOver = pygame.font.Font(None, 60)
surface_txt_gameOver = texte.render("appuyez sur Espace pour recommencer", False, "brown")
sphere_joueur = pygame.image.load('Images/sphere.png').convert_alpha()
joueur_rect = sphere_joueur.get_rect(center = (100,130))

# charge les images de l'animation du personnage (voir détails sur ReadMe)
perso_invoc1 = pygame.image.load('Images/perso_standing1.png').convert_alpha()
perso_invoc2 = pygame.image.load('Images/perso_standing2.png').convert_alpha()
perso_invoc3 = pygame.image.load('Images/perso_standing3.png').convert_alpha()
perso_invoc4a = pygame.image.load('Images/perso_standing4.png').convert_alpha()
indicateur_chgmt_image = 0
index_perso = 0
perso_invoc = [perso_invoc1, perso_invoc2, perso_invoc3, perso_invoc4a,]
surf_perso = perso_invoc[index_perso]
perso_rect = surf_perso.get_rect(midbottom = (420, 395))


# timer
projectile_timer = pygame.USEREVENT + 1
pygame.time.set_timer(projectile_timer,920)




while True :
    for event in pygame.event.get():                            # les événements du jeu, tels que les actions du joueur et le timer
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and jeu_actif == False:  # permet de recommencer une partie en appuyant sur espace, et de remettre le compteur du score à 0
            jeu_actif = True                # variable qui définit  si le jeu est actif (True) ou non (False)
            enmi_tués = 0

        if event.type == projectile_timer:
            r = randint(500, 600)
            theta = randint(0, 360)
            theta_rad = theta * (math.pi / 180)
            x = int(420 + (r * math.cos(theta_rad)))
            y = int(341 + (r * -math.sin(theta_rad)))       # avec pygame, y "descend" quand il est positif, ainsi j'ai ajouté un - pour que cela corresponde au sens horraire du cercle (pas nécessaire)

            projectile_rect_liste.append(ennemi.get_rect(center=(x, y)))


    if jeu_actif == True :            # boucle de la fenêtre de jeu principale

        # affichage des images
        perso_animation()

        screen.blit(arrière_plan,(0,0))
        screen.blit(sphere_joueur, joueur_rect)
        screen.blit(surf_perso, perso_rect)

        score_éliminations()
        durée_jeu = score_temps()

        # contrôles du joueur
        touche = pygame.key.get_pressed()
        if touche[pygame.K_z] :
            joueur_rect.y -= 5
        if touche[pygame.K_s] :
            joueur_rect.y += 5
        if touche[pygame.K_q]:
            joueur_rect.x -= 5
        if touche[pygame.K_d]:
            joueur_rect.x += 5


        # boucle mouvements projectiles
        projectile_rect_liste = mouvement_projectile(projectile_rect_liste)

        # collisions
        jeu_actif = collisions_gameOver(perso_rect,projectile_rect_liste,)
        collisions_Joueur_Proj(joueur_rect, projectile_rect_liste)
        if joueur_rect.colliderect(perso_rect):
            joueur_rect.x = 100
            joueur_rect.y = 130
            jeu_actif = False


    else :                                                                              # boucle menu 'Game Over'

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

        projectile_rect_liste.clear()        # effacer tous les éclairs restant lors du Game Over



    pygame.display.update()
    clock.tick(60)                                    # ne dois pas s'actualiser plus de 60 fois par seconde ( limite à 60 FPS)