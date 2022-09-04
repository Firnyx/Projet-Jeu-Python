# Projet-Jeu-Python 

- Le but du jeu est simple :  vous devez empêcher les éclairs arrivant de tous les côtés d'atteindre le personnage (l'invocateur) situé au centre en les détruisant avec la sphère
- Vous pouvez contrôler la sphère en tant que joueur avec les touches Z, Q, S, D (haut, gauche, bas, droite)

Attention à ne pas entrer en collison avec le personnage ou la partie prendra fin !

Détails sur le projet :

- Pour lancer le jeu : exécuter le script python3 Pygame.py dans le dossier Jeu_Pygame
- nécessite évidemment d'avoir python d'installé, ainsi que le module pygame
- réalisé avec l'IDE Pycharm
- Le personnage ainsi que ses animations ont été importés; j'ai dessiné la sphère, le fond et l'éclair à l'aide du logiciel Krita.

Dans ce programme, j'ai utilisé de la trigonométrie et des vecteurs pour créer un fonctionnement des éclairs qui soit convenable.

Tout d'abord, un cercle trigonométrique (l.87 à l.93) a été utilisé pour générer aléatoirement et de manière optimale les projectiles (éclairs):
- un timer (l.164 et l.165) va déclencher le processus toutes les x périodes de temps, ici tous les 920 ticks;
- la variable r correspond à la taille du rayon (entre 500 et 600 pixels), la méthode randint permet d'ajouter de l'aléatoire dans leur apparition, plutôt qu'une longeur toujours fixe
- theta correspond au périmètre du cercle, détermine la position où va apparaître l'objet, en degré
- theta_rad convertit la variable précédente en radiant, car python calcule le cos et le sin dans cette unité
- ainsi on calcule des positions x et y avec ces valeurs (l.90 et 91), on ajoute 420 à x et 341 à y pour que le cercle virtuel soit centré sur le             personnage, on obtient donc des positions (arrondies) avec l'aide du cosinus et du sinus

Ces positions sont  ensuite attribuées au rectangle de la classe Projectile (image éclair).
La fonction mouvement_projectile (l.95) permet de calculer le déplacement des rectangles avec des vecteurs :

- vecteur_ProjectPerso calcule le vecteur éclair - Personnage 
- norme_vecteur_ProjectPerso comme son nom l'indique calcule la longueur qui sépare ces deux points 
- Si l'on en restait là les éclairs se téléporteraient directement sur le centre, pour éviter cela on utilise la variable Vect_projectile qui divise le vecteur par sa norme, ainsi on obtient un déplacement de 1, dans la bonne direction et le bon sens
- on assimile les nouvelles coordonnées calculées au rectangle avec self.rect.x et self.rect.y
- J'ai utilisé la fonction round() pour que les coordonnées soit arrondies selon les règles mathématiques, c'est à dire que si la partie décimale est égale ou  supérieure à 0.5 on arrondit au-dessus, ce que ne fait pas la fonction int()
- La valeur est multiplié par par deux, pour augmenter la difficulté

Si vous voulez en savoir plus sur les fonctions créés ainsi que sur le code en général, quelque notes ont été rédigées directement sur celui-ci.


