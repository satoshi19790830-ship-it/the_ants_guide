---
title: Verifying the Damage Formula
description: The Ants doesn't publish its damage formula. We're reverse-engineering it from player-submitted data.
category: Research Project
order: 30
updated: 2026-07-19
---

**Bottom line: The Ants has never published an official damage formula.** This is a shared premise across the Japanese, English, and Chinese-speaking communities. This page summarizes what's already been pieced together, and runs a data-driven project to reverse-engineer the formula from real combat data.

## Approach

1. Collect (ATK, DEF, actual damage dealt) triples from players — see [Contribute Your Data](data-collection.html)
2. Fit several common damage-formula candidates (below) against the collected data and compare statistical fit
3. Publish whichever formula fits best as a "current best guess," updating as more data comes in

Our analysis pipeline (`scripts/analyze_damage.py`) has been tested against synthetic data. Results will be posted here once enough real submissions come in.

## Candidate formulas

| Model | Formula shape | Notes |
|---|---|---|
| Attack/defense ratio | damage = k × ATK² / (ATK + DEF) | Very common pattern in mobile RPGs |
| Power-law | damage = k × ATK^p / DEF^q | Allows ATK and DEF to have different weights |
| Difference | damage = k × (ATK − DEF) | Simple subtractive model |
| Linear | damage = a×ATK + b×DEF + c | Baseline for comparison |

As the account audit below shows, final damage is very likely a product of three layers: this base ATK-vs-DEF formula × skill% (+special ant Lv × coefficient%) × (1 + attacker's damage-amplification% − defender's damage-reduction-amplification%). What we're trying to isolate here is that innermost ATK-vs-DEF layer.

## What auditing our own account revealed (2026-07-19, first-party data)

As a step above community speculation, we systematically screenshotted our own account's skill tooltips and stat screens — 407 screenshots — and transcribed all of them. This surfaced quantitative mechanics the game actually states in its own text.

### Finding 1: skill damage is literally written as "base%(+special ant Lv × coefficient%)"

Nearly every special ant combat skill states its damage in this exact form:

> Example: "Poison Spread" (Silver Honeypot Ant) — current: **114%(+special ant Lv × 2%)** to all enemy rows; Max Lv: **260%(+special ant Lv × 2%)**
> Example: "Mandible Bite" (Giant Jaw) — **300%(+special ant Lv × 1%)**
> Example: "Brutal Counter" (Bison Ant) — **130%(+special ant Lv × 0.25%)**

So each skill's damage multiplier is "that skill's base %" plus "special ant level × a per-skill coefficient" (1%, 2%, 0.25%, 0.1%, and more, depending on the skill). This confirms that the "120% / 240% / 480%"-style stepped percentages the Chinese community had noticed were actually a continuous, level-dependent formula in disguise.

### Finding 2: a separate "damage amplification / reduction amplification" layer exists

Beyond the skill %, stat screens explicitly show "Damage Amplification" (attacker-side) and "Damage Reduction Amplification" (defender-side) percentages, which stack from hatchery promotion levels, treasures, and evolution amplifiers. Across the full hatchery level table, each promotion tier adds +5% to both, up to +50% at promotion tier 10. Final damage therefore likely has at least a two-layer multiplicative structure: skill% × (1 + attacker's amp% − defender's reduction%).

### Finding 3: combat speed (turn order) varies hugely — in the hundreds up to 900+

Our own account's invasion squads showed combat speed values ranging from 772 to 952. This confirms, with concrete numbers, the community's qualitative sense that going first swings outcomes significantly.

### Finding 4: buffs stack additively within the same stat category (confirmed from real combat logs)

A second batch of 115 screenshots included actual "Neutral Creature Report" combat logs. Against the same fixed target (a level 1 Marmot with 0% buffs) using the same squad, we captured 17 farming runs, and the breakdown tooltips on each stat revealed exactly how each stat is assembled:

> Example: "Damage Amplification: 66.00%" breaks down as Evolution 20.00% + Neutral Creature 5.00% + Building 41.00% = 66.00%
> Example: "Combat Speed: 952" breaks down as Evolution Meteorite 140 + Evolution 470 + Neutral Creature 140 + Cell 30 + Gene 50 + Bacteria 50 + Fungus 50 + Troop Modification 2 + VIP 20 = 952

A striking number of systems (evolution, neutral creatures, buildings, cells, genes, bacteria, fungi, troop modification, treasures, VIP, awakening, and more) each add their own bonus to the same stat, and **within a single stat category, they simply sum** — not multiply.

<div class="source-note">
Source: breakdown tooltips on our own account's combat detail screen (measured 2026-07-19). Raw data archived in <code>data/screenshot_extraction_260719-2.md</code>
</div>

However, this farming log isn't clean enough on its own to isolate the ATK-vs-DEF relationship: against the identical opponent with an identical squad, skill activation counts vary randomly (one special ant's damage alone ranged from 9 to 16 activations), so total damage across runs swung from about 3.47B to 6.6B purely from RNG, not from stat differences.

### What's still unconfirmed

We did find real combat logs, but they're all "farming run totals" aggregating multiple units and multiple skill activations — we still don't have the minimal unit of data we need: one skill activation, the attacker's ATK, the defender's DEF, and that single hit's damage. So the core ATK-vs-DEF relationship itself is still unconfirmed. But findings 1, 2, and 4 sharpen what we need to collect: the [data submission form](data-collection.html) now also asks for the skill name and its level, plus the attacker's damage-amplification% and the defender's damage-reduction-amplification%, so we can control for these known variables and isolate the pure ATK-vs-DEF relationship.

## What the existing community has found (as of July 2026)

### Official forum

There's no thread with an explicit formula, but an October 2022 thread titled "Just not understanding anthill defense" has useful staff/veteran responses:

- A player reported losing a defense with 8M troop power against a raid of 130,000 vs their 100-120 defenders. A reply explained that damage can be "transferred" when the attacker reduces your kill count to zero, hinting at a specific mechanic/item.
- Practical advice: keep resources below the protected threshold, don't station marches outside garrisons.

<div class="source-note">
Source: <a href="https://theantsforum.allstarunion.com/t/just-not-understanding-anthill-defense/12780">Official forum thread</a> (official forum, user experience report — not verified data)
</div>

There are also official/semi-official creator videos specifically about combat math (transcripts still to be done):

<div class="source-note">
See: <a href="https://www.youtube.com/watch?v=3Xh7mjK_XcA">understanding combat math and skill damage</a>, <a href="https://www.youtube.com/watch?v=48bErwFVi04">Tom's Guide To Battle Reports</a>, <a href="https://www.youtube.com/watch?v=u3ZODr0IhPw">how to read a battle report and hill tips</a>
</div>

### Japanese community: win-rate statistics as a research method

The Japanese guide site theants-kokuyo.com uses a method close to ours: instead of guessing a formula, they run 30+ identical matchups and compare win rates.

- Front-row Warden lineup: 35 battles, 21W-14L (60%). Front-row Ohagito lineup: 34 battles, 18W-16L (52%). Breakdowns by opponent formation (SSS, CCC, GGG, etc.) are also published.
- Ordering test between two special ants: Formation A 33 battles 20W-13L (60%) vs Formation B 34 battles 18W-16L (52%).
- Early-game special-ant duels: one recorded example dealt 225,154 total damage across only 6 skill activations, showing damage inflation matters more than activation count early on.

<div class="source-note">
Sources: <a href="https://theants-kokuyo.com/shield-or-silence2/">Warden vs Ohagito win-rate comparison</a>, <a href="https://theants-kokuyo.com/inspection/">turn-order test</a>, <a href="https://theants-kokuyo.com/power-speed/">early-game duel data</a> (player-measured, high sample size)
</div>

### Chinese community: concrete percentages

- A squad containing a special ant reportedly takes 25% less damage from both normal attacks and skills.
- Special ant skill damage multipliers are commonly described in stepped percentages like "120% / 240% / 480%", likely scaling with skill level.
- One report: ~14M damage dealt to a wild "groundhog" boss in a single hit, reaching zone-war tier 9 after about 14 hits.

<div class="source-note">
Source: <a href="https://www.taptap.cn/moment/363595786300163245">TapTap plunder/zone-war guide post</a> (player-measured, Chinese community)
</div>

### Common qualitative findings

No directly contradicting formulas were found — instead, both communities converge on the same qualitative points:

1. **Displayed "Power" and actual combat strength diverge** — high power doesn't guarantee a win, repeatedly noted in both communities
2. **Combat speed (turn order) matters a lot** — going first is widely felt to swing outcomes significantly
3. **Formation (front/mid/back row) combined with skill trigger rate and multiplier** is what actually determines effective damage

## Current status

**Data collection is in progress.** No formula is published yet — please contribute via the [data submission form](data-collection.html) if you have combat logs.
