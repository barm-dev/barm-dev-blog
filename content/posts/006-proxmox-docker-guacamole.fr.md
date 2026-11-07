---
title: Proxmox, Docker, Guacamole, et la valse des docker compose
description: Deux jours pour poser le socle, deux semaines pour exposer Guacamole proprement. Puis une couche de sécurité de trop l’a rendu inaccessible.
topic: Journal
date: 2025-11-19
---

*Épisode 2/3. Récit reconstitué après coup à partir de mon historique Git et de mes conversations avec ChatGPT de l’époque. Épisode précédent : [pourquoi j’ai abandonné le Raspberry Pi](/blog/005-raspberry-arm-contre-x86/).*

Le MSI Cubi est arrivé avec son processeur x86, ses 16 Go de RAM et son SSD. Je n’ai pas attendu longtemps : le serveur a été installé le 26 septembre 2025, à 1 h 20 du matin.

## Un hyperviseur plutôt qu’un serveur

Plutôt que d’installer Linux directement sur la machine, j’ai choisi **Proxmox**, un hyperviseur, pour séparer les rôles dans des machines virtuelles :

- `infra1`, un Ubuntu avec Docker, pour les services ;
- `devbox1`, un Windows 11, le poste de travail.

Une erreur côté infrastructure ne touche pas le poste de travail, et inversement. C’est le même principe que la séparation des environnements dans un projet data.

`infra1` existait quelques heures plus tard, et Docker tournait dès le 27 septembre. En deux jours, le socle était en place.

## Exposer un service, la vraie difficulté

Fin septembre, j’ajoute **Guacamole**, la passerelle d’accès distant, et **Traefik** devant, comme reverse proxy, pour l’exposer en HTTPS.

Le réseau et la sécurité ne sont pas mon domaine : je viens de la data. J’ai donc choisi de me faire guider par ChatGPT. Le mode opératoire était simple : je lui transmettais logs et fichiers de configuration, il proposait une piste, je l’appliquais et je validais. J’ai conservé ces échanges. Croisés avec l’historique Git, ils permettent de reconstituer le chantier étape par étape.

### Le certificat qui ne venait pas

2 octobre. Premier jalon : le tableau de bord de Traefik en HTTPS. Le navigateur refuse le certificat : Traefik sert son certificat autosigné par défaut, et aucune demande ne part vers Let’s Encrypt. Aucune erreur dans les logs.

Diagnostic : la route du tableau de bord ne déclarait pas de résolveur de certificat (`tls.certResolver`). Sans cette déclaration, Traefik n’a aucune raison d’en demander un.

Les logs d’accès montraient autre chose : moins d’une minute après l’ouverture des ports 80 et 443, des scanners inconnus interrogeaient déjà la machine. Tout service exposé est sondé immédiatement. Cela a cadré la suite du projet.

### Quatre jours de 504

9 octobre. Les conteneurs tournent, mais chaque requête vers Guacamole se termine par un « 504 Gateway Timeout » après trente secondes.

J’ai procédé par élimination. Le ping entre Traefik et Guacamole passe. Un `curl` lancé depuis un conteneur du même réseau obtient une réponse correcte. Le service fonctionne donc, et la panne se situe dans le routage de Traefik. Il m’a fallu quatre jours et une série de commits explicites pour la localiser :

```
docker compose new try
docker compose fix new try
one more try
traefik stupid typo fix
try1
try2
try3
Revert "try3"
```

La cause : Guacamole était rattaché à deux réseaux Docker, un réseau partagé avec Traefik et un réseau privé vers sa base de données. Traefik retenait l’adresse IP du réseau privé, qu’il ne pouvait pas joindre. L’étiquette `traefik.docker.network` permet de lui imposer le bon réseau.

La solution est venue d’un fil de forum, pas de ChatGPT, le 13 octobre au soir. Je l’ai photographié pour obtenir de ChatGPT un exemple adapté à ma configuration.

![Réponse d’un forum : ajouter l’étiquette traefik.docker.network](/img/006/forum-traefik.jpg){width=900 height=426}

Le correctif est committé une minute plus tard. Guacamole répond depuis l’extérieur.

## Ça marche, et c’est là que le risque commence

Le soir même, ma question suivante porte sur la sécurité : « Ça m’inquiète, Guacamole exposé sur le web, qui donne accès à mes VM. »

Guacamole n’était protégé que par un identifiant et un mot de passe, alors qu’il donne accès à toutes les machines qu’il dessert. Une seule couche de protection pour un point d’entrée de ce niveau, ce n’était pas acceptable.

Entre-temps, le 26 octobre, je crée `devbox1`, la VM Windows : l’environnement de développement dédié que j’envisageais depuis août, et la raison d’être du nouveau serveur. L’installateur ne détecte aucun disque : Windows n’embarque pas les pilotes VirtIO des disques virtuels de Proxmox, qu’il faut charger depuis une seconde image.

![Installation de Windows 11 : aucun disque détecté](/img/006/windows-aucun-disque.jpg){width=900 height=691}

Le 1er novembre, j’étudie les options pour renforcer l’accès, dont Pocket ID, un fournisseur d’identité par clé d’accès. Je retiendrai finalement Authelia.

## Deuxième round : Authelia

Mi-novembre, j’ajoute **Authelia**, un portail d’authentification placé devant Guacamole, avec mot de passe et code à usage unique (TOTP). L’architecture est élégante sur le papier, mais elle porte l’ensemble à six conteneurs.

C’est là que la méthode a montré ses limites. Les configurations proposées par ChatGPT correspondaient à une version antérieure d’Authelia : clés dépréciées, options inexistantes, syntaxe de hachage des mots de passe modifiée. Chaque proposition se heurtait à une erreur de validation au démarrage.

Une fois l’accès établi, Authelia exigeait un code envoyé par e-mail pour enregistrer le second facteur, alors qu’aucun serveur d’envoi n’était configuré. Les pistes proposées tournaient autour de l’ajout d’un serveur SMTP. J’ai dû recadrer : l’objectif était précisément de se passer de l’e-mail. Après plusieurs itérations, une configuration TOTP seule a fonctionné.

Le 19 novembre, la double authentification est opérationnelle. Je place Authelia devant Guacamole, j’ajuste encore la configuration, puis dernier commit :

```
la valse des docker compose
```

Ce sera le dernier tout court. Pas parce que tout fonctionnait : la fin d’année est arrivée, et je n’ai plus eu de temps personnel à y consacrer. Les conteneurs tournaient sur `infra1`, mais depuis l’extérieur, Guacamole renvoyait une page 404.

Bilan : 80 commits en sept semaines. Mi-octobre, Guacamole fonctionnait. Un mois plus tard, la couche de sécurité ajoutée l’avait rendu inaccessible.

## Ce que je retiens

- Installer une brique et faire fonctionner un ensemble sont deux métiers différents.
- Chaque brique ajoutée multiplie les points de défaillance. La sécurité n’échappe pas à la règle.
- Se faire guider par une IA hors de son domaine fonctionne, à condition de confronter ses réponses à la documentation de la version installée. Sans accès aux fichiers ni aux versions, elle répond avec assurance pour une autre.
- Quand les messages de commit deviennent `try1`, `try2`, `try3`, ce n’est plus un commit qu’il faut, c’est une pause.

La pause a duré 287 jours.

**La suite :** [Mon architecture actuelle, ou l’art de retirer des choses](/blog/008-architecture-actuelle/)
