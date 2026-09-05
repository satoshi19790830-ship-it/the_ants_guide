---
title: Ant Types & Stats
description: Soldier ant categories, special ants, stats, and the evolution system in The Ants.
category: Guides
order: 20
updated: 2026-07-19
---

## The 3 soldier ant types

- **Guardian Ant** — front row, tanky/defense-focused
- **Shooter Ant** — back row, high attack but low defense
- **Carrier Ant** — resource-hauling specialist, can also be built defensively

Each type has 10 tiers (T1-T9 as the core range, with T10/T11 above that), unlocked by leveling the matching barracks.

<div class="source-note">
Sources: <a href="https://the-ants-underground-kingdom.fandom.com/wiki/Shooter_Ant">Fandom Wiki: Shooter Ant</a>, <a href="https://the-ants-underground-kingdom.fandom.com/wiki/Guardian_Ant">Guardian Ant</a> (community wiki)
</div>

## Full hatchery level table (own-account audit, 2026-07-19)

We recorded our own account's hatchery screens from level 1 through 25, plus promotion tiers 1-10. **The combat power, hatch-count, damage-amplification, and damage-reduction-amplification columns are identical across all three hatcheries** (Guardian / Shooter / Carrier) — only the named ant unlocked at each level differs.

| Lv | Combat Power | Hatch Count | Dmg Amp | Dmg Reduction Amp |
|---|---|---|---|---|
| 1 | 56 | 0 | 0% | 0% |
| 5 | 81 | 100 | 0% | 0% |
| 10 | 426 | 300 | 0% | 0% |
| 15 | 2.0K | 500 | 0% | 0% |
| 20 | 9.9K | 650 | 0% | 0% |
| 22 | 18.1K | 700 | 0% | 0% |
| 25 | 44.8K | 850 | 0% | 0% |
| Promo 1 | 51.5K | 865 | 5.0% | 5.0% |
| Promo 5 | 78.4K | 915 | 25.0% | 25.0% |
| Promo 8 | 98.6K | 950 | 40.0% | 40.0% |
| Promo 10 | 112.0K | 975 | 50.0% | 50.0% |

Damage amp/reduction stays at 0% all the way through level 25, then climbs **+5% per promotion tier**, capping at +50% at promotion 10. This "damage amp / reduction amp" pair is part of the multiplicative layer discussed in [Verifying the Damage Formula](damage-calculation.html).

<div class="source-note">
Source: our own account's hatchery screens (measured 2026-07-19, all levels recorded)
</div>

Example unlocks per hatchery (at Lv1 / Lv5 / Lv10 / Lv22) — our account is set to Japanese, so these names are our own tentative translations, not confirmed against the official English client:

| | Lv1 | Lv5 | Lv10 | Lv22 |
|---|---|---|---|---|
| Shooter hatchery | "Ceratia" ant | "Camponotus sp." ant | "Textor" carpenter ant | "Omoserus" big-head ant |
| Guardian hatchery | Rare big-head ant | "Belgio" big-head ant | "Versicolor" leafcutter ant | "Zeraflora" big-head ant |
| Carrier hatchery | "Sebbabus" ant | "Melanogaster" honeypot ant | "Yshi" honeypot ant | "Mimicus" honeypot ant |

## Awakening bonus examples

- Shooter Ant: ATK +10.0% (up to +20.0% at higher rank)
- Carrier Ant: DEF +10.0% (up to +20.0%)
- Guardian Ant: HP +4.0% (up to +8.0%)

<div class="source-note">
Source: <a href="https://the-ants-underground-kingdom.fandom.com/wiki/Awakening">Fandom Wiki: Awakening</a>
</div>

## Special Ants: rarity and roles

| Rank | Color | Skill count |
|---|---|---|
| Highest | Orange | 8 |
| High | Purple | 6 |
| Mid | Blue | 4 |
| Low | Green | 2 |

Special ants split into "war type" and "develop type," with war type further divided into melee, ranged, support, military, auxiliary, and gathering roles. Only orange-rank war-type special ants can use the "Star Up" system after unlocking skill 6, pushing skill level past the normal cap of 10.

<div class="source-note">
Source: <a href="https://zhuanlan.zhihu.com/p/625725052">Zhihu: Special Ant progression guide</a> (Chinese-language player guide)
</div>

> Tier lists ranking special ants by strength are common on Chinese community sites, but they change frequently with balance updates, so we don't publish a fixed ranking here — check current guide sites for the latest.

### Skill damage follows "base%(+special ant Lv × coefficient%)"

Auditing dozens of special-ant skill tooltips on our own account, nearly every active skill states its damage using the same pattern: "base damage% (+special ant level × a per-skill coefficient%)" — coefficients vary by skill (1%, 2%, 0.25%, and others). In other words, leveling up a special ant continuously increases the skill's own damage %. See [Verifying the Damage Formula](damage-calculation.html) for details.

Stat screens for special ants leading troops also show a "Special Ant Skill ATK / Skill DEF (while leading)" stat — meaning the stats of the soldier ants you deploy also feed back into the special ant's own skill power.

## Evolution system (Evolution Fungi)

There are 21+ "evolution trees," each boosting a specific aspect of your colony (combat, resources, movement speed, etc.). Researching them consumes resources and time.

<div class="source-note">
Source: <a href="https://the-ants-underground-kingdom.fandom.com/wiki/Evolution_Fungi">Fandom Wiki: Evolution Fungi</a>
</div>

## How stats affect combat

How ATK and DEF actually translate into damage is not officially documented. We're verifying this with real data — see [Verifying the Damage Formula](damage-calculation.html).
