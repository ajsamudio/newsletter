# Quarterly Source Audit Prompt

You are doing a **source-quality audit** for AJ's personal newsletter. This runs roughly every 90 days. Your job is **not to write a newsletter** — it's to look at the current source lists in `newsletter-prompt.md` and propose edits so they stay fresh.

---

## Why this exists

Source landscapes shift. Outlets get acquired, lose key staff, become paywall-heavy, or shift tone. New high-signal voices show up. AJ explicitly wants this list to evolve every couple of months instead of calcifying around fads. You are that mechanism.

---

## Inputs

1. Read `newsletter-prompt.md` — note the "Starting hints" lines in each of the six sections (Tech, AI, Global Economics, US Stocks, World & General News, The Vibes).
2. Read the last 4–8 issues in `archive/` — note which sources actually got cited, which never did, and whether any cited sources produced thin / clickbait / paywalled content.

---

## What to do

For each section in `newsletter-prompt.md`:

1. **WebSearch** for fresh sources. Suggested queries:
   - `"best {topic} newsletter 2026"`
   - `"top {topic} sources reddit 2026"`
   - `"who covers {topic} well 2026"`
   - `"{topic} substack recommendations 2026"`
2. **WebFetch** a handful of the new candidates to confirm they actually publish substantive content, not just SEO bait.
3. Decide on three buckets per section:
   - **ADD:** new sources to surface in the list.
   - **REMOVE:** listed sources that have clearly dropped in quality, gone paywall-only with no alternatives, or never produce cited content in recent issues.
   - **KEEP:** still solid, no change.

For Reddit lists specifically: also check that the subreddits are still active (recent top posts within last 7 days, not dormant) and on-topic (mod changes can pull a sub off-topic).

---

## Output

Write a single proposal file at `audits/{YYYY-MM-DD}-source-audit.md` with this structure:

```markdown
# Source Audit — {date}

## Tech
- **ADD:** [Source name](url) — why it's worth adding
- **REMOVE:** Old source — why (dropped in quality / paywall / never cited)
- **KEEP:** unchanged

## AI
...same structure...

(repeat for each of the 6 sections)

---

## Suggested diff for newsletter-prompt.md
{Show the exact lines that would change in newsletter-prompt.md if AJ approves — copy/pasteable.}
```

---

## Hard rules

1. **Do not edit `newsletter-prompt.md` directly.** AJ reviews and applies the diff manually.
2. **Justify every change with a real reason** — "fresher", "more active", "X% of recent issues cited zero of their content" — not vibes.
3. **Don't churn for churn's sake.** If a section's list is still working well, the proposal can be "no changes recommended this cycle." That's a valid output.
4. **Cap proposed additions at 2 per section** — keep the lists tight.
5. **Verify every proposed new source by WebFetching at least one recent article** before recommending it.

---

## When done

Print a one-line summary: `"Source audit written to audits/{date}-source-audit.md — {N} sections changed, {N} unchanged."`
