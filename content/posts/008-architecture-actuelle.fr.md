---
title: Mon architecture actuelle, ou l’art de retirer des choses
description: Après 287 jours de silence, cinq caractères manquants expliquent ma page 404. Je retire deux outils et tout fonctionne enfin.
topic: Journal
date: 2026-11-06
---

*Épisode 3/3. Avant : [le Raspberry Pi abandonné](/blog/005-raspberry-arm-contre-x86/), puis [la valse des docker compose](/blog/006-proxmox-docker-guacamole/).*

19 novembre 2025 : dernier commit. 2 septembre 2026 : le suivant. Entre les deux, 287 jours sans rien. Quand je rouvre le dossier, les conteneurs tournent toujours, et Guacamole affiche toujours sa page 404.

## Ce qui a tout relancé

Entre-temps, j’ai pris un abonnement Claude et installé Claude Code dans VS Code. Il travaille directement sur mes fichiers et peut les pousser sur Git. Jusque-là, j’essayais de tout faire à la main, ce qui était difficile avec le peu de temps dont je dispose. Avec ChatGPT, je faisais l’intermédiaire : je recopiais les logs dans un sens, puis les corrections dans l’autre. Cette fois, l’outil lit lui-même la configuration et l’historique. Pour ce projet, ça a été un vrai accélérateur.

## Cinq caractères

Le coupable était une configuration Traefik. Je faisais référence à un middleware nommé `authelia-guac`, alors qu’il fallait écrire `authelia-guac@file`. Sans ce suffixe, Traefik cherchait le middleware au mauvais endroit, ne le trouvait pas, et ignorait toute la route.

L’historique montre même le commit précis. Le 19 novembre 2025, la référence était d’abord correcte : `authelia@file`. Quelques commits plus loin, en renommant le middleware, le suffixe a disparu. Le projet s’est arrêté le jour même, pour dix mois.

Cinq caractères. 80 commits.

En reprenant l’architecture à froid, le constat était plus gênant : Authelia n’apportait presque rien. Un portail d’authentification centralisé se justifie avec plusieurs applications et plusieurs utilisateurs. J’avais une application, un utilisateur, et Guacamole gère nativement le mot de passe et le code à usage unique. C’était une couche redondante, et la plus fragile de l’ensemble.

La vraie correction n’était donc pas d’ajouter ces cinq caractères. C’était de retirer des choses.

## Ce que j’ai retiré

- **Traefik**, remplacé par **Caddy**, dont la configuration tient en quelques lignes lisibles et qui gère seul ses certificats HTTPS.
- **Authelia**, remplacé par l’authentification native de Guacamole, avec un code à usage unique.

Six conteneurs sont devenus quatre. Tout ça en une seule soirée, le 2 septembre 2026, après 80 commits l’année précédente.

## Deux mois pour finir le travail

Une fois l’accès réparé, le reste a suivi vite :

| Date | Étape |
|---|---|
| 2 sept. 2026 | Caddy remplace Traefik, Authelia disparaît |
| 5 sept. 2026 | VPN WireGuard dans son propre conteneur |
| 7 sept. 2026 | Mise à jour de Guacamole, surveillance des services |
| 11 sept. 2026 | Mon vieux NAS reprend du service |
| 5 nov. 2026 | Fin d’une passe de sécurisation commencée fin octobre |
| 6 nov. 2026 | Rapport hebdomadaire par mail |

## L’architecture d’aujourd’hui

![Schéma : un navigateur passe par Caddy et Guacamole, mes appareils par le VPN WireGuard, pour rejoindre devbox1 sur le MSI Cubi sous Proxmox](/img/008/architecture-fr.svg){width=820 height=420}

Deux chemins mènent à mon poste de travail :

- **depuis un simple navigateur**, via Caddy et Guacamole ;
- **depuis mes propres appareils**, via un VPN WireGuard.

## Ce que je retiens

Le constat le plus net de toute cette aventure : je voulais avancer sur mes projets personnels, et j’ai passé des mois à construire l’infrastructure censée me le permettre. Reverse proxy, certificats, portail d’authentification, double facteur : à un moment, l’outil est devenu le projet, et j’ai perdu de vue le problème que je voulais résoudre.

C’est un schéma classique, et je le vois régulièrement en entreprise. Un projet démarre pour répondre à un besoin métier précis. Puis la plateforme, l’outillage et l’architecture prennent toute la place, jusqu’à ce que plus personne ne se rappelle la question de départ. Après 15 ans dans la data, c’est précisément ce que je m’efforce d’éviter chez les autres : revenir au besoin, et livrer une solution simple qui fonctionne plutôt qu’une solution parfaite qui n’arrive jamais. Il m’a fallu 80 commits sur mon propre réseau pour m’appliquer ma propre règle.

Ironie de l’histoire : l’offre AWS écartée au départ parce que trop chère m’aurait probablement coûté moins que la machine, ajoutée à toutes les soirées passées à la mettre en place.

Tout n’a pas été perdu pour autant. Ce chantier m’a fait pratiquer la conteneurisation et Docker, peu répandus quand j’ai fait mes études et absents de mon quotidien dans la data. Il m’a aussi remis à jour sur les reverse proxies, les certificats et les réseaux. Ce n’est pas ce que je cherchais, mais c’est un acquis.

Le besoin du départ tenait en une phrase : coder mes projets depuis n’importe où, sans copier mes fichiers d’une machine à l’autre. Il est enfin satisfait. Cet article a d’ailleurs été préparé depuis cette machine, avec Claude Code.

Reste le Raspberry Pi. Il est toujours branché sur mon réseau, sans aucun rôle. Je me surprends régulièrement à lui chercher une utilisation, avant de me rendre compte que je m’égare à nouveau. Après tout, si le Pi n’a rien à faire, ce n’est pas bien grave.
