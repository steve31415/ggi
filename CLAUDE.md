# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Website for the Golden Gate Institute for AI (GGI), a non-profit AI think tank. Hosted on Vercel at:
- Main site: goldengateinstitute.org
- Conference site: thecurve.goldengateinstitute.org (The Curve AI conference)

## Commands

```bash
npm run dev       # Start dev server with Turbopack (port 3000)
npm run build     # Build for production
npm run lint      # ESLint
```

## Architecture

**Framework**: Next.js 15 with App Router, React 19, TypeScript, Tailwind CSS v4

### Route Groups

Two separate visual experiences share some components:
- `app/(main)/` - Main GGI website (classic theme, serif typography)
- `app/(the-curve)/thecurve/` - Conference microsite (teal theme, different branding)

**Domain Routing** (`middleware.ts`): Requests to `thecurve.*` subdomains are rewritten to `/thecurve/*` paths internally.

### Content System

**Blog Posts** (`posts/*.mdx`):
- YAML front matter (title, subtitle, authors, date) + Markdown body
- Rendered via `app/(main)/[slug]/page.tsx`
- Parsed with `gray-matter`

**Reports** (`mdx-pages/*.mdx`):
- Longer-form content (cybersecurity reports)
- Rendered via `app/(main)/cyber-security-report/[slug]/page.tsx`

**Configuration Data** (`utils/constants.ts`):
- Team members, external URLs, Typeform IDs
- Edit this file to update team roster or form integrations

### Themes

CSS theme classes applied to sections (defined in `globals.css`):
- `theme-classic` - main site default
- `theme-sand` - blog posts
- `theme-teal` - home hero
- `theme-the-curve` - conference site

### Key Components

- `components/post-content.tsx` - Markdown renderer (remaps h1→h3, h2→h4, handles tables)
- `components/nav-bar.tsx` - Main responsive navigation
- `components/blocks.tsx` - Layout primitives (Row, Col)
- `app/(the-curve)/thecurve/speakers.tsx` - Speaker data for The Curve

## Adding Content

**New blog post**: Create `posts/your-slug.mdx` with front matter:
```yaml
---
title: "Post Title"
subtitle: "Optional"
authors: "Name"
date: "YYYY-MM-DD"
---
```

**New team member**: Add to `TEAM_MEMBERS` array in `utils/constants.ts`, place photo in `public/team/`

## External Services

- **Typeform**: Event registration and announcements (IDs in `constants.ts`)
- **Airtable**: The Curve application/recommendation forms
- **Fillout**: Session proposal forms
