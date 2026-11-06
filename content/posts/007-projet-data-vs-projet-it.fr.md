---
title: Non ! Un projet data ne se gère pas comme un projet IT
description: Mettre en place un dashboard, ce n’est pas développer une application. Un exemple vécu, à quatre jours d’une visite de la direction générale.
topic: Data
date: 2026-04-16
---

Non ! Un projet analytique (data, BI, DWH, …) ne peut être géré comme un projet IT opérationnel (ERP, CRM, applicatif, …). Même s’ils partagent de nombreuses similitudes, mettre en place un dashboard ce n’est pas développer une application pour mobile ou migrer une application métier. L’un doit s’adapter à tout l’existant technique, aux processus internes, à la stratégie de l’entreprise, aux décisions politiques, l’autre impose une certaine structure à l’entreprise, apporte ses concepts et force les utilisateurs à penser dans son modèle.

Pour moi il n’y a aucun doute là-dessus, c’est viscéral, je le sais. C’est sans doute grâce à la somme de mes 15 ans d’expériences passées, de tous les projets que j’ai livrés, mais étonnamment, lorsqu’une question précise m’est posée, qu’on tente de transposer des concepts « applicatifs » sur un projet « data », cela devient difficile de donner une réponse claire et structurée.

À titre d’exemple, j’ai dû affronter ce problème il y a quelques semaines. Suite à une réorg dans une entreprise du secteur pharmaceutique, l’organisation commerciale d’un pays avait complètement changé : on passait alors d’une sales line unique à deux sales lines distinctes, chacune répartie par indication médicale. L’impact sur les dashboards était clair, l’ensemble des produits commercialisés sans distinction d’indication devait maintenant être clairement différencié. Une dimension supplémentaire, un niveau de granularité supplémentaire ; business as usual ! Une nouvelle feature a été ajoutée au backlog, elle sera déployée avec la prochaine release. C’était sans compter l’aspect politique… pour la visite de la direction générale prévue la semaine suivant la réorg, il nous a été demandé de clairement afficher cette distinction afin de justifier, de manière chiffrée, les bénéfices de ces changements, at any cost ! Développer et déployer une telle feature en suivant le processus classique aurait nécessité deux semaines (pour la fast track !). Nous avions quatre jours (week-end inclus) ! Comment expliquer cela aux IT architects, aux PMs, aux process owners du groupe ? Rien, dans un processus de développement standard, ne justifie une telle urgence. « Ce n’est pas un bug fix critique, pourquoi ce niveau d’urgence ? » « Pourquoi n’aviez-vous pas prévu cette feature plus tôt ? ». Il a alors fallu prendre une grande respiration, et se lancer dans de longs mails de justification…

C’est pourquoi j’ai décidé de mettre tout ça à plat, de prendre le temps de lister ces différences, de développer des explications claires et de donner une réponse structurée pour chaque cas.

Dans les semaines à venir, je posterai des articles sur ces sujets ! Si cela vous parle, vous intéresse, si vous souhaitez en discuter, n’hésitez pas à prendre contact avec moi, je suis curieux de savoir si je suis le seul à rencontrer ces difficultés !
