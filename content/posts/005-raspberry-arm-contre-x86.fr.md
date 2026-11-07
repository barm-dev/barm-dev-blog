---
title: Raspberry Pi et Docker, quand le processeur tranche
description: Une image Docker publiée pour amd64 seulement met fin à l’expérience Raspberry Pi. Le vrai sujet était ailleurs : le besoin dépassait le matériel.
topic: Journal
date: 2025-09-23
---

*Épisode 1/3. Récit reconstitué après coup à partir de mon historique Git, et daté du jour des faits.*

On s’était quittés sur une carte SD morte et la promesse de faire enfin avancer ce Raspberry Pi 3B. J’ai racheté une carte SD et je l’ai mise dans le Pi. Avant de raconter la suite, un retour sur le besoin, parce que c’est lui qui a guidé chaque décision.

## Le besoin

Je développe mes projets personnels dans des créneaux dispersés : dans le train, depuis une chambre d’hôtel en vacances, et à la maison sur deux PC différents. Git synchronise le code, mais pas l’environnement : outils, versions, configuration. Chaque changement de poste coûtait du temps, et les fichiers finissaient copiés un peu partout.

Je voulais donc un environnement de développement unique, toujours au même endroit, accessible depuis n’importe quel appareil.

## Les options

La première idée était de le louer en ligne. J’avais regardé une offre AWS de ce type : elle ne correspondait pas vraiment à mon usage, et le coût grimpait vite pour une utilisation régulière.

Restait à l’héberger moi-même. Deux options se dessinaient :

- une machine virtuelle Linux qui tournerait sur le Pi ;
- le Pi en simple passerelle, avec [Apache Guacamole](https://guacamole.apache.org/), pour ouvrir depuis un navigateur une session sur une autre machine du réseau local, mon PC de bureau par exemple.

Pourquoi Guacamole plutôt qu’un VPN et une connexion RDP classique ? Parce qu’il ne demande rien d’autre qu’un navigateur. J’utilise parfois des ordinateurs sur lesquels je ne peux pas installer de client VPN, ou sur lesquels je n’ai pas envie de saisir mes identifiants habituels : le PC de mes parents ou de ma belle-famille, par exemple.

J’ai commencé par la seconde option, la plus légère : Guacamole sous Docker sur le Pi.

Le 16 septembre 2025 au soir, j’écris un premier `docker-compose.yml` : Guacamole, son démon `guacd`, qui assure les connexions, et une base MySQL, qui stocke utilisateurs et connexions. Au lancement, Docker refuse.

## Le blocage n’est pas venu d’où je l’attendais

Je m’attendais à buter sur la puissance : 1 Go de RAM, c’est peu. Le vrai bloqueur a été l’architecture du processeur.

Le Pi utilise un processeur **ARM**, je le savais. Ce que je n’avais pas vérifié, c’est que toutes les images Docker ne sont pas publiées pour tous les types de processeurs. Une image embarque des programmes compilés pour un jeu d’instructions précis : si le manifeste ne propose pas de variante `arm64`, il n’y a rien à exécuter. C’était le cas de `mysql:8.0-bookworm`, publiée pour `amd64` uniquement :

```
no matching manifest for linux/arm64/v8 in the manifest list entries
```

## La décision

Pour le seul rôle de passerelle, les contournements existaient : une autre image, une autre base de données, une compilation maison. Mais ce blocage a surtout rendu visible une question que j’aurais dû poser plus tôt : le matériel tenait-il la suite ?

La passerelle seule laissait l’environnement de développement sur mon PC de bureau, qui devait rester allumé et disponible. L’autre option, une machine virtuelle dédiée, n’était pas réaliste sur le Pi : avec 1 Go de RAM et un processeur ARM, il pouvait au mieux servir de passerelle, jamais d’hôte. Contourner le problème aurait seulement retardé la décision.

Sept jours plus tard, le 23 septembre 2025, je commandais une machine x86, capable d’héberger à la fois la passerelle et l’environnement de développement.

| Composant | Prix (CHF) |
|---|---:|
| MSI Cubi N ADL S-225BEU, Intel N100 | 109.00 |
| Crucial SO-DIMM DDR4 3200 MHz, 16 Go | 53.90 |
| WD Blue SN5000 NVMe, 1 To | 59.90 |
| **Total** | **222.80** |

![MSI Cubi N ADL, un mini-PC Intel N100](/img/005/msi-cubi-n100.jpg){width=480 height=344}

*Le MSI Cubi N ADL. Image : MSI.*

## Avant, après

| | Raspberry Pi 3B | MSI Cubi N100 |
|---|---|---|
| Processeur | ARM 64 bits (Cortex-A53) | x86-64 (Intel N100) |
| Cœurs | 4 | 4 |
| RAM | 1 Go | 16 Go |
| Stockage | Carte microSD | SSD NVMe 1 To |

## Ce que je retiens

- Vérifier pour quels processeurs une image est publiée (`amd64`, `arm64`…) avant de la retenir. Docker Hub l’affiche pour chaque tag.
- Partir du besoin, pas du matériel disponible. Réutiliser un Pi qui traînait était tentant, mais ce n’était pas une exigence.
- Un blocage technique est parfois un bon signal pour réévaluer le choix de départ, plutôt qu’un problème à contourner.

Il restait à installer tout ça. Ce ne fut pas si rapide.

**La suite :** [Proxmox, Docker, Guacamole, et la valse des docker compose](/blog/006-proxmox-docker-guacamole/)
