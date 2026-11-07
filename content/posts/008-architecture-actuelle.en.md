---
title: My current architecture, or the art of removing things
description: After 287 days of silence, five missing characters explain my 404 page. I remove two tools and everything finally works.
topic: Journal
date: 2026-11-06
---

*Episode 3/3. Before this: [the abandoned Raspberry Pi](/en/blog/005-raspberry-arm-contre-x86/), then [the docker compose waltz](/en/blog/006-proxmox-docker-guacamole/).*

19 November 2025: last commit. 2 September 2026: the next one. In between, 287 days of nothing. When I reopened the project, the containers were still running, and Guacamole was still showing its 404 page.

## What got it moving again

In the meantime, I took a Claude subscription and installed Claude Code in VS Code. It works directly on my files and can push them to Git. Until then, I had been trying to do everything by hand, which was hard with the little time I have. With ChatGPT, I was the go-between: copying logs one way, then fixes the other way. This time, the tool reads the configuration and the history itself. For this project, it was a real accelerator.

## Five characters

The culprit was a Traefik configuration. I was referring to a middleware called `authelia-guac`, when I should have written `authelia-guac@file`. Without that suffix, Traefik looked for the middleware in the wrong place, didn’t find it, and ignored the whole route.

The history even shows the exact commit. On 19 November 2025, the reference was correct at first: `authelia@file`. A few commits later, while renaming the middleware, the suffix disappeared. The project stopped that same day, for ten months.

Five characters. 80 commits.

Looking at the architecture with fresh eyes, the conclusion was more awkward: Authelia added almost nothing. A central authentication portal makes sense with several applications and several users. I had one application, one user, and Guacamole handles the password and one-time code natively. It was a redundant layer, and the most fragile one in the stack.

So the real fix wasn’t adding those five characters. It was removing things.

## What I removed

- **Traefik**, replaced by **Caddy**, whose configuration fits in a few readable lines and which handles its HTTPS certificates on its own.
- **Authelia**, replaced by Guacamole’s native authentication with a one-time code.

Six containers became four. All of it in a single evening, on 2 September 2026, after 80 commits the year before.

## Two months to finish the job

Once access was fixed, the rest followed quickly:

| Date | Step |
|---|---|
| 2 Sep 2026 | Caddy replaces Traefik, Authelia goes away |
| 5 Sep 2026 | WireGuard VPN in its own container |
| 7 Sep 2026 | Guacamole update, service monitoring |
| 11 Sep 2026 | My old NAS is back in service |
| 5 Nov 2026 | End of a security pass started in late October |
| 6 Nov 2026 | Weekly report by email |

## Today’s architecture

![Diagram: a browser goes through Caddy and Guacamole, my devices through the WireGuard VPN, to reach devbox1 on the MSI Cubi running Proxmox](/img/008/architecture-en.svg){width=820 height=420}

Two paths lead to my workstation:

- **from a plain browser**, through Caddy and Guacamole;
- **from my own devices**, through a WireGuard VPN.

## What I took away

The clearest lesson from this whole adventure: I wanted to make progress on my personal projects, and I spent months building the infrastructure that was supposed to let me do so. Reverse proxy, certificates, authentication portal, second factor: at some point, the tool became the project, and I lost sight of the problem I wanted to solve.

It’s a classic pattern, and I see it regularly in companies. A project starts to answer a specific business need. Then the platform, the tooling and the architecture take up all the room, until nobody remembers the original question. After 15 years in data, that’s exactly what I try to help others avoid: go back to the need, and deliver a simple solution that works rather than a perfect one that never arrives. It took 80 commits on my own network for me to follow my own rule.

The irony: the AWS offering I ruled out at the start for being too expensive would probably have cost me less than the machine, plus all the evenings spent setting it up.

Not everything was lost, though. This project made me practise containerisation and Docker, which were not widespread when I studied and are absent from my day-to-day work in data. It also refreshed my knowledge of reverse proxies, certificates and networking. Not what I was after, but a real gain.

The original need fit in one sentence: code my projects from anywhere, without copying files from one machine to another. It is finally met. This post was actually prepared on that very machine, with Claude Code.

That leaves the Raspberry Pi. It’s still plugged into my network, with no role at all. I regularly catch myself looking for a use for it, before realising I’m drifting off again. After all, if the Pi has nothing to do, it’s not a big deal.
