---
title: Faire revivre mon Raspberry Pi 3B
description: De Jessie à Bookworm (avec une carte SD morte en chemin)
topic: Journal
date: 2025-09-05
hero: /img/004/hero.png
---

## En bref

J’ai voulu mettre à jour mon vieux Raspberry Pi 3B, découvert qu’il tournait encore sous Raspbian Jessie (2015 !), installé Bookworm Lite, activé SSH, puis je me suis heurté à un mur quand la carte SD a lâché pendant la mise à jour.
Prochaine étape : réinstaller Raspberry Pi OS sur un disque externe pour éviter de futurs problèmes de stockage.

---

## La surprise : Jessie en 2025 ?

J’espérais une mise à jour rapide : activer SSH et c’est parti. Mais bien sûr, rien ne s’est passé comme prévu.

Il s’avère que le système installé était **Raspbian Jessie**, sorti en 2015 et mis à jour pour la dernière fois en 2017. **Quoi ?!** Honnêtement, je pensais l’avoir utilisé plus récemment. Le temps passe vite 😅

---

## Installer le dernier Raspberry Pi OS

Je suis allé sur la page officielle [Raspberry Pi Operating Systems](https://www.raspberrypi.com/software/) pour un environnement léger.
Je veux économiser autant d’espace et de CPU que possible pour Docker (ou d’autres services légers).

---

## Utiliser Raspberry Pi Imager

- J’ai formaté la carte SD (32 Go > FAT32).
- J’ai dû changer de port USB : apparemment, Raspberry Pi Imager [n’aime pas l’USB 3](http://reddit.com/r/rasberrypi/comments/13bmqsh/error_writing_to_storage/).
- J’ai inséré la carte SD, démarré le Pi… et SSH a fonctionné ! Victoire ! 👑

![Capture d’écran de Pi Imager](/img/004/pi-imager.png){width=679 height=475}

---

## Mise à jour rapide du système… ou pas

J’ai lancé les commandes habituelles :
```cmd
sudo apt-get update
sudo apt-get upgrade
```
Mais alors… échec de la mise à jour 😱
```
dpkg: error processing archive ... Input/output error
dpkg: error while cleaning up: unable to securely remove ... Input/output error
```
Même sudo a cessé de fonctionner :
```
/usr/bin/sudo: Input/output error
```

---

## Diagnostic : carte SD mourante
Après quelques recherches, il semble que la carte SD soit en train de mourir. Je vais devoir en acheter une nouvelle, et la prochaine fois, j’installerai le système sur un disque externe pour éviter ces problèmes de lecture et d’écriture.

Cette vidéo pourrait bien me sauver la vie :
[Boot Raspberry Pi from USB](https://www.youtube.com/watch?v=NDcI9HZPRaQ&t=81s)

---

## Leçons apprises
- Toujours vérifier la version de son système : le temps passe vite !
- Les cartes SD s’usent. Préférer un stockage externe pour la fiabilité.
- Raspberry Pi Imager a ses bizarreries (problèmes avec l’USB 3).
- SSH peut être activé directement dans Imager : super pratique.

---

## Et ensuite ?
Réinstaller Raspberry Pi OS sur un disque externe.
La suite au prochain article, peut-être que cette fois j’avancerai 🤪
