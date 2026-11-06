---
title: Problèmes de baie serveur
description: Quand de simples soucis mécaniques ralentissent mes projets
topic: Journal
date: 2025-09-01
hero: /img/003/hero.jpg
---

Parfois, le plus petit accroc mécanique peut faire dérailler un projet technique. Ce week-end, je me suis attaqué à l’un d’eux, qui attendait depuis plus d’un an…

Comme je le disais dans mon article précédent, je prévois d’héberger une machine virtuelle Linux sur mon réseau domestique.
Mon idée actuelle est d’utiliser mon vieux Raspberry Pi 3. Je ne suis pas sûr que ça marche : il ne sera peut-être pas assez puissant.
Dans tous les cas, je devais lui trouver une place où le brancher sur une prise réseau.
C’est là que je suis retombé sur un « projet en attente » vieux d’un an… 😨

## La baie serveur

Il y a un an, j’ai commencé à installer une baie serveur à la maison.
J’ai acheté une baie murale 19" 6U et un bon switch.

![Nouvelle baie Dexlan](/img/003/rack.jpg){width=250 height=217}

J’ai tout monté avec soin, caché les câbles et organisé le tout du mieux possible.
Tout était prêt, il ne restait qu’à poser la porte vitrée, et là, terrible constat…

![Impossible de fermer la baie](/img/003/impossible-to-close-server-rack.gif){width=180 height=320}

Impossible de fermer la porte à cause des câbles réseau.

## Reculer les deux montants verticaux

La solution consistait à reculer les deux montants verticaux sur lesquels sont fixés tous les composants (switch, panneau de brassage, multiprise, etc.).
Mais je suis tombé sur un autre problème : les vis du côté gauche de la baie étaient bloquées par le tableau électrique (j’ai oublié de prendre des photos).
J’ai finalement dû décrocher la baie du mur, reculer les montants et la remonter.

![Montants verticaux de la baie](/img/003/move-vertical-bars.gif){width=180 height=320}

## Résultat final

La baie est maintenant en place.
Avec assez d’espace pour le Raspberry Pi et mon NAS.

![Résultat final de la baie](/img/003/rack-final.jpg){width=400 height=533}

Maintenant que la baie est enfin en place, je peux passer aux tests du Raspberry Pi. Espérons qu’il soit assez puissant !

## Liens utiles

- Merci à l’article de [reseau-vdi.fr](https://reseau-vdi.fr/coffret-de-communication-pas-chere-baie-de-brassage-19/), qui m’a permis de bien préparer ce projet.
