# barm-dev-blog

Source of [blog.barm.dev](https://blog.barm.dev). No framework: Markdown files,
one HTML template, one stylesheet and a small Python script. French is served
at the root, English under `/en/`.

```
content/posts/   articles, NNN-slug.fr.md and NNN-slug.en.md
content/pages/   about, roadmap
content/drafts/  not published
templates/       base.html
static/          CSS, fonts, images, copied as is
build.py         writes everything to dist/; interface text is at the top
```

## Local preview

```powershell
py -3.12 -m pip install --user -r requirements.txt   # once
py -3.12 build.py --serve                            # http://localhost:4321
```

Re-run the second command after editing a file.

## New post

Create `content/posts/005-my-slug.fr.md`, and the same name in `.en.md` if you
translate it. A post can exist in one language only: the language button then
leads to the other language's home page.

```markdown
---
title: Mon titre
description: Une ligne pour la liste et le flux RSS
topic: Data
date: 2026-11-06
hero: /img/005/hero.png
---

Texte en Markdown. Images : ![Texte alternatif](/img/005/photo.jpg){width=400 height=300}
```

Add `draft: true` to the header to hide a post from the site; `build.py --drafts`
shows hidden posts in the local preview. A hidden post is still readable on GitHub
if it is committed: list it in `.gitignore` to keep it local.

`hero` is optional and works best at 900×200. Push to `master` and Vercel builds it.
