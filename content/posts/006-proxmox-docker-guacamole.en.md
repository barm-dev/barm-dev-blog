---
title: Proxmox, Docker, Guacamole, and the docker compose waltz
description: Two days to lay the foundation, two weeks to expose Guacamole properly. Then one security layer too many made it unreachable.
topic: Journal
date: 2025-11-19
---

*Episode 2/3. Reconstructed afterwards from my Git history and my ChatGPT conversations from the time. Previous episode: [why I gave up on the Raspberry Pi](/en/blog/005-raspberry-arm-contre-x86/).*

The MSI Cubi arrived with its x86 processor, 16 GB of RAM and SSD. I didn’t wait long: the server was installed on 26 September 2025, at 1:20 in the morning.

## A hypervisor rather than a server

Rather than installing Linux directly on the machine, I chose **Proxmox**, a hypervisor, to separate roles into virtual machines:

- `infra1`, an Ubuntu box with Docker, for the services;
- `devbox1`, a Windows 11 machine, the workstation.

A mistake on the infrastructure side doesn’t touch the workstation, and vice versa. It’s the same principle as separating environments in a data project.

`infra1` existed a few hours later, and Docker was running by 27 September. In two days, the foundation was in place.

## Exposing a service, the real difficulty

At the end of September, I add **Guacamole**, the remote access gateway, with **Traefik** in front of it as a reverse proxy, to expose it over HTTPS.

Networking and security aren’t my field: I come from data. So I chose to let ChatGPT guide me. The process was simple: I passed it logs and configuration files, it suggested a lead, I applied it and checked the result. I kept those exchanges. Cross-referenced with the Git history, they let me reconstruct the work step by step.

### The certificate that never came

2 October. First milestone: Traefik’s dashboard over HTTPS. The browser rejects the certificate: Traefik serves its default self-signed one, and no request ever goes to Let’s Encrypt. No error in the logs.

Diagnosis: the dashboard route declared no certificate resolver (`tls.certResolver`). Without that declaration, Traefik has no reason to request one.

The access logs showed something else: less than a minute after ports 80 and 443 were opened, unknown scanners were already probing the machine. Any exposed service gets probed immediately. That framed the rest of the project.

### Four days of 504

9 October. The containers are running, but every request to Guacamole ends with a “504 Gateway Timeout” after thirty seconds.

I worked by elimination. Ping between Traefik and Guacamole works. A `curl` from a container on the same network gets a proper answer. So the service works, and the fault lies in Traefik’s routing. It took four days and a series of very explicit commits to pin it down:

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

The cause: Guacamole was attached to two Docker networks, one shared with Traefik and a private one for its database. Traefik picked the IP address on the private network, which it couldn’t reach. The `traefik.docker.network` label forces it onto the right one.

The answer came from a forum thread, not from ChatGPT, on the evening of 13 October. I took a photo of it to get ChatGPT to produce an example matching my setup.

![Forum answer: add the traefik.docker.network label](/img/006/forum-traefik.jpg){width=900 height=426}

The fix was committed one minute later. Guacamole answered from outside.

## It works, and that’s where the risk begins

That same evening, my next question was about security: “It worries me, Guacamole exposed on the web, giving access to my VMs.”

Guacamole was protected only by a username and a password, while it gives access to every machine behind it. A single layer of protection for an entry point of that level wasn’t acceptable.

Meanwhile, on 26 October, I create `devbox1`, the Windows VM: the dedicated development environment I had been considering since August, and the reason for the new server. The installer detects no disk: Windows doesn’t ship the VirtIO drivers for Proxmox’s virtual disks, which have to be loaded from a second image.

![Windows 11 setup: no disk detected](/img/006/windows-aucun-disque.jpg){width=900 height=691}

On 1 November, I look at options to harden access, including Pocket ID, a passkey-based identity provider. I end up choosing Authelia.

## Round two: Authelia

In mid-November, I add **Authelia**, an authentication portal in front of Guacamole, with a password and a one-time code (TOTP). The architecture is elegant on paper, but it brings the total to six containers.

This is where the method showed its limits. The configurations ChatGPT suggested matched an older version of Authelia: deprecated keys, options that didn’t exist, a changed password hashing syntax. Every suggestion ran into a validation error at start-up.

Once access was working, Authelia required a code sent by email to register the second factor, and no mail server was configured. The suggested fixes revolved around adding an SMTP server. I had to reframe: the whole point was to do without email. After several iterations, a TOTP-only configuration worked.

On 19 November, two-factor authentication is up and running. I put Authelia in front of Guacamole, adjust the configuration again, then the last commit:

```
la valse des docker compose
```

(“the docker compose waltz”.) It would be the last one, full stop. Not because everything worked: the end of the year came, and I had no personal time left for it. The containers were running on `infra1`, but from outside, Guacamole returned a 404 page.

The result: 80 commits in seven weeks. In mid-October, Guacamole worked. A month later, the added security layer had made it unreachable.

## What I took away

- Installing a piece and making a whole system work are two different jobs.
- Every piece you add multiplies the points of failure. Security is no exception.
- Letting an AI guide you outside your field works, provided you check its answers against the documentation of the installed version. Without access to files or versions, it answers confidently for another one.
- When your commit messages become `try1`, `try2`, `try3`, you don’t need another commit, you need a break.

The break lasted 287 days.

**Next:** [My current architecture, or the art of removing things](/en/blog/008-architecture-actuelle/)
