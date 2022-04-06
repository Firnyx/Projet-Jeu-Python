# Projet-Jeu-Python pour Parcoursup

- Le but du jeu est simple :  vous devez empêcher les éclairs arrivant de tous les côtés d'atteindre le personnage (l'invocateur) situé au centre en les détruisant avec la sphère
- Vous pouvez contrôler la sphère en tant que joueur avec les touches Z,Q,S,D (haut, gauche, bas, droite)

Attention à ne pas entrer en collison avec le personnage ou ce sera une fin de partie !

Détails sur le projet :

- nécessite évidemment d'avoir python d'installé, ainsi que le module pygame
- réalisé avec l'IDE Pycharm
- Le personnage ainsi que ses animations ont été importés; j'ai dessiné la sphère, le fond et les éclairs à l'aide du logiciel Krita.

Dans ce programme, j'ai utilisé de la trigonométrie et des vecteurs pour créer un fonctionnement des éclairs qui soit convenable.

Tout d'abord, un cercle trigonométrique (l.113 à l.118) a été utilisé pour générer aléatoirement et de manière optimale les projectiles (éclairs):
- un timer (l.97 et l.98) va déclencher le processus toutes les x périodes de temps, ici tous les 920 ticks;
- la variable r correspond à la taille du rayon (entre 500 et 600 ), la méthode randint permet d'ajouter de l'aléatoire à leur apparition, plutôt qu'une         longeur toujours fixe
    - theta correspond au périmètre du cercle, détermine la position où va apparaître l'objet, en degré
    - theta_rad convertit la variable précédente en radiant, car python calcule le cos et le sin dans cette unité
    - ainsi on calcule des positions x et y avec ces valeurs (l.117 et 118), on ajoute 420 à x et 341 à y pour que le cercle virtuel soit centré sur le             personnage, on obtient donc des positions (arrondies) avec l'aide du cosinus et du sinus)
Ces positions sont  ensuite attribuées à un rectangle (image éclair) qui est stockée dans une liste
Cette liste contient tous les rectangles éclairs (nommés 'ennemi' dans le code), avec l'information de leur position. Elle  va s'auto référer (l.148) à l'aide d'une fonction, pour créer une boucle.
La fonction mouvement_projectile
