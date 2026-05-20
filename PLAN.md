# Personal Weekly Newsletter — Plan

## Context

You want a recurring personal newsletter covering **tech, AI, global economics, and US stocks**. You're new to Claude routines, so the plan is structured as an **incremental MVP**: nail the content first by hand, then automate it with a routine, then add email delivery. That way each step is verifiable on its own and you learn the routines primitive without it being a black box.

**Constraints you set:**
- Free to run (no paid SaaS subscriptions)
- Both file archive + emailed to `antsamudio99@gmail.com`
- Medium depth: 3–5 stories per section, paragraph + "why it matters"
- Daily cadence temporarily for testing, then Thursday mornings
- Sources via WebSearch + WebFetch

**Cost honesty:** "Claude routines" (scheduled remote agents) run on Anthropic infrastructure and consume your existing Claude usage allowance. If you're on a paid Claude plan, daily runs are fine. If you're on the free tier, watch your usage — we'll switch to weekly Thursdays before this matters.

---

## Architecture (one-page mental model)

```
┌──────────────────────────────────────────────────────────┐
│  Claude Routine (scheduled remote agent)                 │
│  Schedule: daily at first → weekly Thursday 7am later    │
│                                                          │
│  1. Read newsletter-prompt.md (the master instructions)  │
│  2. WebSearch each of 4 sections for last 24h / 7d       │
│  3. WebFetch top headlines for context                   │
│  4. Compose markdown digest using template               │
│  5. Save to archive/YYYY-MM-DD.md                        │
│  6. POST to Resend API → email lands in inbox            │
└──────────────────────────────────────────────────────────┘
```

**Why Resend for email:** free tier is 3,000 emails/month + 100/day — generous for personal use. One HTTP POST with an API key, works inside the routine sandbox without OAuth dance (Gmail SMTP would need an App Password and SMTP libs, more friction).

---

## Project structure (to be created)

```
NewsLetter/
├── README.md                  # how-to-run, schedule, troubleshooting
├── newsletter-prompt.md       # the master prompt the routine executes
├── template.md                # the output structure (sections, headings)
├── archive/                   # one .md file per issue, dated
│   └── .gitkeep
└── .env.example               # documents RESEND_API_KEY env var (no secrets in repo)
```

No code files — the whole pipeline is a Claude routine reading the prompt and using built-in tools. Keeps it simple and free.

---

## Newsletter content structure (template.md)

```markdown
# Weekly Brief — {{date}} (Week {{week-num}})

> Coverage window: {{start}} → {{end}}

## 📰 Tech
For each of 3–5 stories:
- **Headline** — [source name](direct article URL)
- 2–3 sentence summary
- *Why it matters:* one line on stakes / who's affected

**Sources used this section:**
- [Outlet 1](url) — what they covered
- [Outlet 2](url) — what they covered

## 🤖 AI
Same structure as Tech. Bias toward: model releases, frontier-lab news,
notable research, regulation/policy moves, major product launches.
End with **Sources used** list.

## 🌍 Global Economics
Same structure. Bias toward: central bank decisions, GDP/inflation
prints, trade/tariff news, major currency moves, geopolitical risk.
End with **Sources used** list.

## 📈 US Stocks
- **Index recap:** S&P 500, Nasdaq, Dow — week's % change + level (cite source)
- **Notable movers:** 3–5 single-stock or sector stories with context + link
- **Looking ahead:** earnings/Fed/data on next week's calendar
End with **Sources used** list.

---
**Every story carries a link. Every section ends with a Sources list.** No claim without a source — if it can't be sourced, drop it.

---
*Generated {{timestamp}} by Claude routine.*
```

---

## Build phases

### Phase 1 — Draft & manually test the prompt (today)

1. Create `template.md` with the structure above.
2. Create `newsletter-prompt.md` containing:
   - Role/persona (concise newsletter editor)
   - Per-section instructions with source quality guidance (e.g. tech → TechCrunch / The Verge / Ars / Hacker News; econ → Reuters / FT / Bloomberg; stocks → CNBC / WSJ / MarketWatch)
   - Explicit "use WebSearch with current-year query, then WebFetch top 2–3 for accuracy" workflow
   - Tone rules ("concise, no fluff, no hype, no emoji except section headers")
   - Output: write the file to `archive/YYYY-MM-DD.md`
3. **Run the prompt manually once in this session** to see the output. Iterate on the prompt until you like the result. This is the most important step — the routine just repeats this prompt automatically, so quality here = quality forever.

### Phase 2 — Wrap as daily routine (after Phase 1 looks good)

Use the `schedule` skill / `mcp__scheduled-tasks__create_scheduled_task` to register a routine:

- **Cron:** `7 8 * * *` (8:07 am daily — off-minute on purpose; many users pick `0 8` and the fleet stacks at the same instant)
- **Prompt:** "Run the newsletter generation as defined in `newsletter-prompt.md`. Today's date is {{auto-injected by routine}}."
- Let it run for **3–5 days**. Read the outputs. Adjust the prompt as needed (e.g. tighten word counts, change source priorities, fix tone).

### Phase 3 — Add email delivery

**About your question "do I need to sign in as antsamudio99@gmail.com?":**
You don't sign into Gmail differently — Resend is a separate service. But the Resend free tier has one gotcha: **without a verified domain, Resend only lets you send to the email address you signed up with**. So:

- **Sign up for Resend using `antsamudio99@gmail.com`** (not your other one). That makes it the verified recipient automatically.
- You don't need to do anything in Gmail itself — emails just arrive in that inbox.
- If you later want to send to *both* your addresses or to others, you'd verify a domain you own (free, but requires DNS access).

**Steps:**
1. Go to `resend.com`, sign up with `antsamudio99@gmail.com`.
2. From the dashboard → API Keys → create one. Copy it (shown once).
3. Add `RESEND_API_KEY` to the routine's secrets (the scheduled-tasks MCP supports env-var injection; if not, paste the key into the routine prompt as a last resort — fine for a single personal recipient).
4. Append to `newsletter-prompt.md`: after writing the file, POST to `https://api.resend.com/emails` with `from: "Newsletter <onboarding@resend.dev>"`, `to: "antsamudio99@gmail.com"`, `subject: "Weekly Brief — {{date}}"`, and the markdown body (Resend renders it).
5. Trigger one manual run, confirm the email lands at `antsamudio99@gmail.com` within ~1 minute.

### Phase 4 — Switch to weekly Thursday mornings

Once you trust the output, update the routine's cron from `7 8 * * *` to `7 8 * * 4` (Thursdays at 8:07 am). Adjust the prompt to cover **the last 7 days** instead of 24 hours. Done.

---

## Critical files & their roles

| File | Role | Created in |
|------|------|------------|
| `newsletter-prompt.md` | Master prompt the routine executes verbatim | Phase 1 |
| `template.md` | Output structure reference | Phase 1 |
| `archive/*.md` | One file per issue, dated | Phase 1 (first manual run) |
| `README.md` | How-to-run, schedule, how to pause | Phase 1 |
| `.env.example` | Documents the `RESEND_API_KEY` slot | Phase 3 |

No external libraries, no build step, no servers. The routine + Claude's built-in WebSearch/WebFetch + Resend's REST API = the whole stack.

---

## Verification plan

**Phase 1 verification:** Run the prompt manually in this session. Check that
- All 4 sections are populated
- Each story has a working source link (spot-check 2)
- Word counts feel "medium depth" (3–5 stories × ~80 words = ~300–400 words/section)
- No hallucinated numbers in the stocks section (cross-check the index closes)

**Phase 2 verification:** After 3 daily runs, read all 3 outputs. They should feel non-repetitive, source-diverse, and useful. If two days reuse the same lead story, tighten the de-dup instruction.

**Phase 3 verification:** Trigger one manual routine run; confirm email arrives at `antsamudio99@gmail.com` within 2 minutes and renders cleanly on mobile + desktop.

**Phase 4 verification:** First Thursday run lands at ~8:07am, covers 7 days, no double-firing.

---

## Open question for you before we start building

Resend email needs you to make a free Resend account using `antsamudio99@gmail.com` (that's the gotcha — sign up with the address you want emails delivered to, otherwise their free tier won't deliver to it). About 2 minutes of setup. If you'd rather skip email entirely for now and just have the routine save the markdown file, we can defer Phase 3 indefinitely. I'll ask after you approve the plan.
