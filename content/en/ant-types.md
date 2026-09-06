---
title: Ant Types & Stats
description: Soldier ant categories, special ants, stats, and the evolution system in The Ants.
category: Guides
order: 20
updated: 2026-09-06
---

## The 3 soldier ant types

- **Guardian Ant** — front row, tanky/defense-focused
- **Shooter Ant** — back row, high attack but low defense
- **Carrier Ant** — resource-hauling specialist, can also be built defensively

Each type has 10 tiers (T1-T9 as the core range, with T10/T11 above that), unlocked by leveling the matching barracks.

## Full hatchery level table (own-account audit, 2026-07-19)

I recorded my own account's hatchery screens from level 1 through 25, plus promotion tiers 1-10. **The combat power, hatch-count, damage-amplification, and damage-reduction-amplification columns are identical across all three hatcheries** (Guardian / Shooter / Carrier) — only the named ant unlocked at each level differs.

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

*Source: my own account's hatchery screens (measured 2026-07-19, all levels recorded)*

Example unlocks per hatchery (at Lv1 / Lv5 / Lv10 / Lv22) — my account is set to Japanese, so these names are my own tentative translations, not confirmed against the official English client:

| | Lv1 | Lv5 | Lv10 | Lv22 |
|---|---|---|---|---|
| Shooter hatchery | "Ceratia" ant | "Camponotus sp." ant | "Textor" carpenter ant | "Omoserus" big-head ant |
| Guardian hatchery | Rare big-head ant | "Belgio" big-head ant | "Versicolor" leafcutter ant | "Zeraflora" big-head ant |
| Carrier hatchery | "Sebbabus" ant | "Melanogaster" honeypot ant | "Yshi" honeypot ant | "Mimicus" honeypot ant |

## Awakening bonus examples

- Shooter Ant: ATK +10.0% (up to +20.0% at higher rank)
- Carrier Ant: DEF +10.0% (up to +20.0%)
- Guardian Ant: HP +4.0% (up to +8.0%)

The August 17, 2026 update added three more awakening parts to the Maze Store, for Cyphomyrmex Rimosus, the Saharan Silver Ant and Meranoplus Castaneus (in the Japanese client: シフォミルキンアリ／菌斑頭甲, ザサハラ銀アリ／銀光の背甲, メラノハットアリ／ハート腹部).

## Special Ants: rarity and roles

There are **73 special ants** in total. Colour sets both the number of skills and the hatching odds.

| Colour | Skills | Tier | Normal hatch | Advanced hatch | Supreme hatch |
|---|---|---|---|---|---|
| Green | 2-3 | Common | 28.30% | 21.43% | 0% |
| Blue | 4 | Uncommon | 19.59% | 39.84% | 85.23% |
| Purple | 6 | Rare | 0.54% | 6.98% | 10.45% |
| Orange | 8 | Legendary | 0.02% | 0.14% | 3.93% |
| Orange (Lost Island) | 8 | Epic | 0% | 0% | 0.39% |

Orange is 3.93% even on a supreme hatch, and 0.02% on a normal one — roughly one in 5,000. It is not something you chase.

### Combat-type vs Develop-type

- **Combat-type** — deployed in troops, up to **three per troop** once you have the required evolutions
- **Develop-type** — never fights; stationed at a specific structure to boost its output

Each ant then has a combination of two attributes (rarely three) that fixes its role.

**Combat-type attributes**

| Attribute | Meaning | Best placement |
|---|---|---|
| Melee | Attacks at short range (1-3 units) | Front, middle |
| Ranged | Attacks at long range (4-5 units) | Middle, back |
| Support | Attacks that debuff the enemy | Middle |
| Guardian / Shooter / Carrier | Skills only work when the squad is made of that soldier type | With the matching soldier type |
| Universal | Skills work regardless of squad composition | Anywhere |
| Hunt | Skills only work when hunting wild creatures | Anywhere |

**Develop-type attributes**

The first attribute is Gather, Military or Develop; the second fixes the target. Gather pairs with meat, wet soil, sand, plant or honeydew; Military pairs with the Guardian, Shooter or Carrier nest; Develop pairs with trade (Ladybug), healing pools, insects, or the Construction Center.

### Star-Up and skill upgrade costs

Star-Up — raising skills past the normal level 10 cap — is available **only to Orange combat-type ants**, and only after their 6th skill is unlocked.

Skill levels are raised with Spores:

| To level | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| Spores | 20 | 30 | 45 | 60 | 90 | 130 | 200 | 270 | 400 |

That is 1,245 spores to take one skill from level 1 to 10. The back half is steep, so concentrating on one ant beats spreading spores across several.

### Special ants you cannot hatch (25)

These 25 never drop from "Hatch Special Ants" and must be obtained another way, such as fragment synthesis.

Myrmarachne Formicaria, Myrmecotypus Rettenmeyeri, Pheidole Neitneri, Lathy Sniffer, Ghost Ant, Proatta, White Velvet, Brown Rogue, Dark Hercules, Golden Venom, Banshee Panda, Amber Glider, Giant Destructor, Flat Shield, Acid Ant, Urchin Ant, Crimson Healer, Red Foot, Green Head, Yellow Spider, Strober, Texas Turtle, Bright Blue Ant, Strobe Ant, Atta Leafcutter

A few Green and Blue ants carry two second attributes: Black Stripe (Carrier/Shooter), Northern Sugar (Guardian/Carrier), Black Shield (Guardian/Shooter) and Black Fire (Guardian/Carrier). The Green Slender Ant and Brown Glider have only one attribute, Universal, which lets them be used as either combat-type or develop-type.
> Tier lists ranking special ants by strength are common on Chinese community sites, but they change frequently with balance updates, so I don't publish a fixed ranking here — check current guide sites for the latest.

### Skill damage follows "base% (+special ant Lv × coefficient%)"

Auditing dozens of special-ant skill tooltips on my own account, nearly every active skill states its damage using the same pattern: "base damage% (+special ant level × a per-skill coefficient%)" — coefficients vary by skill (1%, 2%, 0.25%, and others). In other words, leveling up a special ant continuously increases the skill's own damage %. See [Verifying the Damage Formula](damage-calculation.html) for details.

Stat screens for special ants leading troops also show a "Special Ant Skill ATK / Skill DEF (while leading)" stat — meaning the stats of the soldier ants you deploy also feed back into the special ant's own skill power.

## Evolution system (Evolution Fungi)

There are 21+ "evolution trees," each boosting a specific aspect of your colony (combat, resources, movement speed, etc.). Researching them consumes resources and time.

The August 3, 2026 update lowered the development resource cost of the Mutation System, Soldiers Reform, the Amp System and Special Ant Evolution, so these are cheaper to push than older guides suggest.

## How stats affect combat

How ATK and DEF actually translate into damage is not officially documented. I'm verifying this with real data — see [Verifying the Damage Formula](damage-calculation.html).

## Sources

External sources used for this page. Figures measured on my own account are noted inline where they appear.

- <a href="https://the-ants-underground-kingdom.fandom.com/wiki/Special_Ants">Fandom: The Ants Underground Kingdom Wiki, "Special Ants"</a> — total count, per-colour skill counts and hatching odds, the combat/develop attribute system, Star-Up conditions, spore costs, and the 25 non-hatchable ants. Community wiki (CC BY-SA)

- Sources: <a href="https://the-ants-underground-kingdom.fandom.com/wiki/Shooter_Ant">Fandom Wiki: Shooter Ant</a>, <a href="https://the-ants-underground-kingdom.fandom.com/wiki/Guardian_Ant">Guardian Ant</a> (community wiki)
- Source: <a href="https://the-ants-underground-kingdom.fandom.com/wiki/Awakening">Fandom Wiki: Awakening</a>
- Source: <a href="https://zhuanlan.zhihu.com/p/625725052">Zhihu: Special Ant progression guide</a> (Chinese-language player guide)
- Source: <a href="https://the-ants-underground-kingdom.fandom.com/wiki/Evolution_Fungi">Fandom Wiki: Evolution Fungi</a>
