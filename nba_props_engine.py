#!/usr/bin/env python3
"""
NBA FanDuel Props Analysis Engine
==================================
Fill in player data below, then run:
    python nba_props_engine.py
Output: nba_props_MMDD.html in same directory

DATA YOU NEED TO FILL IN:
  1. GAMES_META        — game info, times, win probabilities
  2. DEF               — defensive rankings per team (pts/reb/ast rank out of 30, pace)
  3. RAW_PLAYERS       — per game: player logs, minutes, role, injury, edges, FD line
"""

import json
from datetime import datetime

TODAY = datetime.now().strftime("%B %d, %Y")
DATE  = datetime.now().strftime("%m%d")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: GAMES
# Fill in each game being played tonight.
# prob_away / prob_home = win probability %
# status = "UPCOMING" | "LIVE Q1" | "LIVE Q2" etc.
# ─────────────────────────────────────────────────────────────────────────────
GAMES_META = [
    {
        "id":        "AWAY_HOME",        # e.g. "OKC_CHI"
        "away":      "AWAY",             # e.g. "OKC"
        "home":      "HOME",             # e.g. "CHI"
        "away_rec":  "00-00",
        "home_rec":  "00-00",
        "time":      "7:00 PM ET",
        "prob_away": 50,
        "prob_home": 50,
        "status":    "UPCOMING",
    },
    # add more games...
]

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: DEFENSIVE RANKINGS
# pts/reb/ast = rank out of 30 (1=best D, 30=worst D)
# Higher rank = worse defense = better for the offensive player
# pace = possessions per 48 min (league avg ~112)
# ─────────────────────────────────────────────────────────────────────────────
DEF = {
    # TEAM ABBR
    "CHI": {"pts": 28, "reb": 26, "ast": 22, "pace": 115.8},
    "SAC": {"pts": 29, "reb": 27, "ast": 25, "pace": 116.2},
    "WAS": {"pts": 30, "reb": 29, "ast": 28, "pace": 116.5},
    "PHI": {"pts": 18, "reb": 12, "ast":  8, "pace": 112.4},
    "ORL": {"pts":  8, "reb": 10, "ast": 12, "pace": 106.2},
    "CLE": {"pts":  5, "reb":  8, "ast":  6, "pace": 105.8},
    "MIA": {"pts": 14, "reb": 16, "ast": 18, "pace": 110.4},
    "TOR": {"pts": 20, "reb": 22, "ast": 19, "pace": 112.8},
    "MIN": {"pts":  4, "reb":  6, "ast":  5, "pace": 108.3},
    "LAL": {"pts": 15, "reb": 17, "ast": 14, "pace": 111.6},
    "BKN": {"pts": 27, "reb": 25, "ast": 26, "pace": 114.2},
    "DAL": {"pts": 24, "reb": 20, "ast": 21, "pace": 111.8},
    "DET": {"pts": 16, "reb": 15, "ast": 17, "pace": 112.0},
    "MEM": {"pts": 23, "reb": 19, "ast": 23, "pace": 113.5},
    "NOP": {"pts": 26, "reb": 24, "ast": 24, "pace": 113.0},
    "NYK": {"pts": 11, "reb": 13, "ast": 15, "pace": 109.6},
    "CHA": {"pts": 22, "reb": 18, "ast": 20, "pace": 113.1},
    "PHX": {"pts": 12, "reb": 14, "ast": 10, "pace": 112.2},
    # add/update more teams as needed
}

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: PLAYER DATA
#
# Organized by game ID (must match GAMES_META "id" above)
# Each player needs:
#
#   name          — full name string
#   team          — team abbreviation
#   opp           — opponent abbreviation (must exist in DEF above)
#   pos           — "PG" | "SG" | "SF" | "PF" | "C"
#   role          — "starter" | "bench"
#   inj           — None | "GTD" | "QUESTIONABLE" | "DOUBTFUL" | "OUT"
#
#   last10_games  — list of 10 dicts, index 0 = MOST RECENT game
#                   each: {"pts": X, "reb": X, "ast": X}
#
#   min_avg       — season average minutes per game
#   min_l10       — average minutes over last 10 games
#                   (if min_l10 >> min_avg → minutes spike signal)
#
#   edges         — how much above average this matchup is for each stat
#                   {"pts": 0.0–4.0, "reb": 0.0–4.0, "ast": 0.0–4.0}
#                   0 = no edge, 4 = huge edge
#                   (derive from DVP data or your own scouting)
#
#   fd_line_cat   — which category to show on the sparkline
#                   "P" | "R" | "A" | "PR" | "PA" | "RA" | "PRA"
#   fd_line       — the actual FanDuel line for that category
#                   (e.g. if FD has "Points Over/Under 24.5" → 24.5)
#
#   note          — one line of context shown on the card
# ─────────────────────────────────────────────────────────────────────────────
RAW_PLAYERS = {

    "AWAY_HOME": [
        {
            "name":  "Player Name",
            "team":  "AWAY",
            "opp":   "HOME",
            "pos":   "PG",
            "role":  "starter",       # "starter" or "bench"
            "inj":   None,            # None, "GTD", "QUESTIONABLE", "DOUBTFUL", "OUT"

            # ── LAST 10 GAMES (index 0 = most recent) ──────────────────────
            "last10_games": [
                {"pts": 28, "reb": 5, "ast": 8},   # game 1 (most recent)
                {"pts": 24, "reb": 4, "ast": 7},   # game 2
                {"pts": 31, "reb": 6, "ast": 9},   # game 3
                {"pts": 22, "reb": 4, "ast": 6},   # game 4
                {"pts": 29, "reb": 5, "ast": 8},   # game 5
                {"pts": 26, "reb": 5, "ast": 7},   # game 6
                {"pts": 30, "reb": 6, "ast": 8},   # game 7
                {"pts": 25, "reb": 4, "ast": 7},   # game 8
                {"pts": 27, "reb": 5, "ast": 8},   # game 9
                {"pts": 28, "reb": 5, "ast": 7},   # game 10 (oldest)
            ],

            # ── MINUTES ────────────────────────────────────────────────────
            "min_avg":  33.0,   # season avg minutes
            "min_l10":  34.2,   # last 10 game avg minutes

            # ── MATCHUP EDGES (0.0 = no edge, 4.0 = huge edge) ────────────
            "edges": {"pts": 2.5, "reb": 0.5, "ast": 1.5},

            # ── FANDUEL LINE ───────────────────────────────────────────────
            "fd_line_cat": "PRA",   # category to chart on sparkline
            "fd_line":     39.5,    # actual FanDuel line

            "note": "One line of context about this player / matchup.",
        },

        # ── Add more players for this game... ──────────────────────────────
    ],

    # ── Add more games... ─────────────────────────────────────────────────────
}


# =============================================================================
# ENGINE — DO NOT EDIT BELOW THIS LINE
# =============================================================================

CATS = ["P", "R", "A", "PR", "PA", "RA", "PRA"]

CAT_META = {
    "P":   {"label": "Points",   "color": "#38bdf8"},
    "R":   {"label": "Rebounds", "color": "#c084fc"},
    "A":   {"label": "Assists",  "color": "#34d399"},
    "PR":  {"label": "Pts+Reb",  "color": "#818cf8"},
    "PA":  {"label": "Pts+Ast",  "color": "#22d3ee"},
    "RA":  {"label": "Reb+Ast",  "color": "#a3e635"},
    "PRA": {"label": "PRA",      "color": "#fb923c"},
}

INJ_PENALTY = {
    "OUT":          -99,
    "DOUBTFUL":      -6,
    "QUESTIONABLE":  -2.5,
    "GTD":           -1.5,
}


def combo(g, cat):
    """Calculate combined stat value for a game dict and category string."""
    v = 0
    if "P" in cat: v += g["pts"]
    if "R" in cat: v += g["reb"]
    if "A" in cat: v += g["ast"]
    return v


def analyze(game_id, p, all_teammates):
    """
    Analyze a single player and return a scored result dict.
    all_teammates = list of all player dicts in the same game (for injury cascades)
    """
    games  = p["last10_games"]
    opp    = p["opp"]
    edges  = p["edges"]
    role   = p.get("role", "starter")
    pos    = p.get("pos", "SF")
    inj    = p.get("inj")
    dc     = DEF.get(opp, {"pts": 15, "reb": 15, "ast": 15, "pace": 111})

    # ── Compute L10 stats (PRIMARY METRIC) ───────────────────────────────────
    l10_combos = {c: round(sum(combo(g, c) for g in games) / 10, 1) for c in CATS}
    l10_lows   = {c: min(combo(g, c) for g in games) for c in CATS}   # TRUE floor
    l10_highs  = {c: max(combo(g, c) for g in games) for c in CATS}
    last_combos= {c: combo(games[0], c) for c in CATS}

    l10_pra    = l10_combos["PRA"]
    last1_pra  = last_combos["PRA"]
    last2_pra  = combo(games[1], "PRA") if len(games) >= 2 else last1_pra
    avg_last2  = (last1_pra + last2_pra) / 2

    # Sparkline: oldest → newest for the target category
    tcat   = p.get("fd_line_cat", "PRA")
    fd_line= p.get("fd_line", l10_combos[tcat])
    spark  = [combo(g, tcat) for g in reversed(games)]

    score  = 0.0
    flags  = []

    # ── 1. INJURY ─────────────────────────────────────────────────────────────
    if inj:
        score += INJ_PENALTY.get(inj, -2)
        flags.append(f"[WARN] {inj} — verify status before betting")

    # ── 2. TEAMMATE INJURY CASCADE ────────────────────────────────────────────
    teammate_out = False
    for mate in all_teammates:
        if mate["name"] == p["name"] or mate["team"] != p["team"]:
            continue
        if mate.get("role") == "starter" and mate.get("inj") in ("OUT", "DOUBTFUL"):
            teammate_out = True
            if role == "bench":
                score += 2.5
                flags.append(f"[UP] {mate['name']} {mate['inj']} — likely starting, major minutes bump")
            elif role == "starter":
                score += 0.8
                flags.append(f"[UP] {mate['name']} {mate['inj']} — extra usage expected")
        elif mate.get("role") == "starter" and mate.get("inj") == "GTD":
            # Returning starter = negative for bench players who benefited
            if role == "bench":
                score -= 2.0
                flags.append(f"[WARN] {mate['name']} GTD — if active, minutes/usage likely reduced")
            elif role == "starter":
                score -= 0.5
                flags.append(f"[WARN] {mate['name']} GTD — monitor status")

    # ── 3. MINUTES SIGNAL ────────────────────────────────────────────────────
    min_diff = p["min_l10"] - p["min_avg"]
    if role == "bench" and min_diff > 3:
        score += 2.5
        flags.append(f"[UP] BENCH VALUE: {p['min_avg']}→{p['min_l10']} min L10 — books still pricing at bench level")
    elif min_diff > 1.5:
        score += 0.8
        flags.append(f"[UP] Minutes trending up ({p['min_avg']}→{p['min_l10']} L10)")
    elif min_diff < -2:
        score -= 0.8
        flags.append(f"[DOWN] Minutes down ({p['min_avg']}→{p['min_l10']} L10)")

    # ── 4. BOUNCE-BACK / FADE (last 1 AND last 2 games vs L10 avg) ───────────
    if last1_pra < l10_pra * 0.78 and last2_pra < l10_pra * 0.78:
        # Both last 2 games well below avg — strongest signal
        score += 1.5
        flags.append(f"[BB][BB] STRONG bounce-back: last 2 games both cold ({last1_pra}/{last2_pra} PRA vs {l10_pra} avg)")

    elif last1_pra < l10_pra * 0.78:
        # Last game only below avg
        score += 0.75
        flags.append(f"[BB] Bounce-back: {last1_pra} PRA last game vs {l10_pra} L10 avg (-{l10_pra - last1_pra:.1f})")

    elif avg_last2 < l10_pra * 0.85:
        # Average of last 2 is soft even if neither alone qualifies
        score += 0.4
        flags.append(f"[BB] Soft bounce-back: avg last 2 ({avg_last2:.1f}) below L10 avg ({l10_pra})")

    elif last1_pra > l10_pra * 1.25 and last2_pra > l10_pra * 1.25:
        # Both last 2 games way above avg — strong fade
        score -= 1.25
        flags.append(f"[DOWN][DOWN] STRONG fade: last 2 games both hot ({last1_pra}/{last2_pra} PRA vs {l10_pra} avg)")

    elif last1_pra > l10_pra * 1.25:
        # Last game only above avg
        score -= 0.6
        flags.append(f"[DOWN] Fade: {last1_pra} PRA last game above {l10_pra} L10 avg (+{last1_pra - l10_pra:.1f})")

    # ── 4b. Suppress bounce-back if cold games explained by teammate injury ──
    # If a teammate was recently OUT and player was cold, don't double-count
    if teammate_out:
        # Suppress bounce-back — cold games were likely due to reduced role
        # when teammate was out, not a true regression signal
        pass  # teammate_out flag used to contextualize, not suppress entirely

    # ── 5. MATCHUP EDGES ─────────────────────────────────────────────────────
    if dc["pts"] >= 22 and edges.get("pts", 0) >= 1.5:
        score += 1.5
        flags.append(f"🎯 {opp} #{dc['pts']} worst pts D — {edges['pts']:.1f} edge")
    if dc["reb"] >= 22 and edges.get("reb", 0) >= 1.5:
        score += 1.5
        flags.append(f"[NBA] {opp} #{dc['reb']} worst reb D — {edges['reb']:.1f} edge")
    if dc["ast"] >= 20 and edges.get("ast", 0) >= 1.5:
        score += 1.2
        flags.append(f"🤝 {opp} #{dc['ast']} worst ast D — {edges['ast']:.1f} edge")

    # ── 6. PACE BONUS ────────────────────────────────────────────────────────
    if dc["pace"] >= 114:
        score += 1.5
        flags.append(f"[PACE] High pace game ({dc['pace']} pace) — more possessions")

    # ── 7. CATEGORY TARGETING ────────────────────────────────────────────────
    # Use POSITIONAL DVP to determine which stat the defense is vulnerable to
    # e.g. team allows rank 28 pts to PGs but rank 3 ast -> target P not A
    pos_key = pos if pos in ("PG","SG","SF","PF","C") else "SF"

    def pos_dvp_rank(stat):
        key = f"{pos_key}_{stat}"
        return dc.get(key, dc.get(stat, 15))

    def rank_to_edge(rank):
        if rank >= 25: return 2.5
        if rank >= 20: return 1.5
        if rank >= 15: return 0.5
        if rank >= 10: return -0.5
        if rank >= 5:  return -1.5
        return -2.5

    # Blend positional DVP edge with BettingPros edges
    edge_p = (edges.get("pts", 0) + rank_to_edge(pos_dvp_rank("pts"))) / 2
    edge_r = (edges.get("reb", 0) + rank_to_edge(pos_dvp_rank("reb"))) / 2
    edge_a = (edges.get("ast", 0) + rank_to_edge(pos_dvp_rank("ast"))) / 2

    cat_scores = {}
    for cat in CATS:
        n = len(cat)
        raw = 0.0
        if "P" in cat: raw += edge_p
        if "R" in cat: raw += edge_r
        if "A" in cat: raw += edge_a
        # Normalize by components so PRA can't win just by accumulating
        s = raw / n
        # Floor safety: consistency of this combo over L10
        if l10_combos[cat] > 0:
            s += (l10_lows[cat] / l10_combos[cat]) * 1.2
        # Small bonus for single-stat (cleaner line)
        if n == 1:
            s += 0.3
        cat_scores[cat] = round(s, 2)

    best_cat = max(cat_scores, key=cat_scores.get)

    # Flag strong positional mismatches
    pos_edges = [("pts", pos_dvp_rank("pts")), ("reb", pos_dvp_rank("reb")), ("ast", pos_dvp_rank("ast"))]
    top_stat, top_rank = max(pos_edges, key=lambda x: x[1])
    if top_rank >= 24:
        stat_label = {"pts": "Points", "reb": "Rebounds", "ast": "Assists"}[top_stat]
        flags.append(f"[UP] {opp} rank {top_rank}/30 vs {pos_key} {stat_label} — positional mismatch")

    # ── FINAL OUTPUT ─────────────────────────────────────────────────────────
    direction  = "OVER" if score >= 0 else "FADE"
    conf       = "HIGH" if abs(score) >= 5 else ("MED" if abs(score) >= 3 else "LOW")
    floor_pct  = round(l10_lows[tcat] / l10_combos[tcat] * 100) if l10_combos[tcat] > 0 else 0

    # L10 averages for pts/reb/ast individually (computed from game logs)
    l10_avg_pts = round(sum(g["pts"] for g in games) / 10, 1)
    l10_avg_reb = round(sum(g["reb"] for g in games) / 10, 1)
    l10_avg_ast = round(sum(g["ast"] for g in games) / 10, 1)

    return {
        "name":         p["name"],
        "team":         p["team"],
        "opp":          p["opp"],
        "game_id":      game_id,
        "pos":          p["pos"],
        "role":         role,
        "inj":          inj,
        "score":        round(score, 1),
        "direction":    direction,
        "conf":         conf,
        "target_cat":   best_cat,
        "cat_scores":   cat_scores,
        "fd_line_cat":  tcat,
        "fd_line":      fd_line,
        "edges":        edges,
        # L10 is the primary metric
        "l10_avg":      {"pts": l10_avg_pts, "reb": l10_avg_reb, "ast": l10_avg_ast},
        "l10_pra":      l10_pra,
        "l10_combos":   l10_combos,
        "l10_lows":     l10_lows,    # TRUE minimums from actual game logs
        "l10_highs":    l10_highs,
        "last_game":    games[0],
        "last_combos":  last_combos,
        "last2_pra":    last2_pra,
        "min_avg":      p["min_avg"],
        "min_l10":      p["min_l10"],
        "spark":        spark,        # oldest → newest, for target category
        "floor_pct":    floor_pct,
        "flags":        flags,
        "notes":        p.get("note", ""),
    }


# ── RUN ANALYSIS ─────────────────────────────────────────────────────────────
all_picks  = {}
all_flat   = []

for game_id, players in RAW_PLAYERS.items():

    # ── PLAYER ELIGIBILITY FILTERS ────────────────────────────────────────────
    def is_eligible(p):
        games = p.get("last10_games", [])
        # Must have at least 5 games with actual stats (pts+reb+ast > 0)
        games_played = sum(1 for g in games if (g.get("pts",0) + g.get("reb",0) + g.get("ast",0)) > 0)
        if games_played < 5:
            return False
        # Use min_avg (season average) and min_l10 (L10 average) for minutes check
        # Both must be >= 15 to filter out garbage time players
        if p.get("min_avg", 0) < 15 and p.get("min_l10", 0) < 15:
            return False
        return True

    # ── BENCH PLAYER RULES ────────────────────────────────────────────────────
    # Only include bench if a starter on their team is OUT/DOUBTFUL
    # Max 2 bench players per team (top 2 by min_avg)
    teams_with_star_out = set()
    for p in players:
        if p.get("role") == "starter" and p.get("inj") in ("OUT", "DOUBTFUL"):
            teams_with_star_out.add(p["team"])

    # Pick top 2 bench players per team by min_avg
    bench_by_team = {}
    for p in players:
        if p.get("role") == "bench" and p["team"] in teams_with_star_out and is_eligible(p):
            team = p["team"]
            bench_by_team.setdefault(team, []).append(p)
    # Sort each team's bench by min_avg desc, keep top 2
    allowed_bench = set()
    for team, bench_players in bench_by_team.items():
        bench_players.sort(key=lambda x: x.get("min_avg", 0), reverse=True)
        for p in bench_players[:2]:
            allowed_bench.add(p["name"])

    # Apply all filters
    filtered = []
    for p in players:
        if p.get("role") == "bench":
            if p["name"] not in allowed_bench:
                continue
        else:
            # Starters still need eligibility check
            if not is_eligible(p):
                continue
        filtered.append(p)

    results = [analyze(game_id, p, players) for p in filtered]
    results.sort(key=lambda x: x["score"], reverse=True)
    all_picks[game_id] = results
    all_flat.extend(results)

all_flat.sort(key=lambda x: x["score"], reverse=True)

total_games   = len(all_picks)
total_players = len(all_flat)
total_overs   = sum(1 for p in all_flat if p["direction"] == "OVER")
total_fades   = sum(1 for p in all_flat if p["direction"] == "FADE")
total_high    = sum(1 for p in all_flat if p["conf"] == "HIGH")

print(f"[DONE] Analysis complete: {total_games} games, {total_players} players")
print(f"   Overs: {total_overs}  Fades: {total_fades}  HIGH conf: {total_high}")


# =============================================================================
# HTML RENDERER
# =============================================================================

def build_html():
    CAT_META_JS  = json.dumps(CAT_META)
    GAMES_JS     = json.dumps(GAMES_META)
    PICKS_JS     = json.dumps(all_picks)
    ALL_JS       = json.dumps(all_flat)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trust Me Bro Props · {TODAY}</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{
  --bg:#05070f;--s1:#080c18;--s2:#0d1220;--s3:#111828;
  --b1:#18203a;--b2:#1e2840;
  --green:#22c55e;--red:#f43f5e;--yellow:#fbbf24;--orange:#fb923c;
  --blue:#38bdf8;--purple:#c084fc;
  --txt:#dde8f8;--m1:#2a3c60;--m2:#4a6090;
  --bebas:"Bebas Neue",sans-serif;
  --mono:"IBM Plex Mono",monospace;
  --body:"Outfit",sans-serif;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--txt);font-family:var(--body);min-height:100vh;overflow-x:hidden}}
body::before{{content:"";position:fixed;inset:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.025) 2px,rgba(0,0,0,.025) 4px);
  pointer-events:none;z-index:9999}}

/* HEADER */
header{{position:relative;padding:14px 24px 12px;border-bottom:1px solid var(--b1);
  display:flex;align-items:center;justify-content:space-between;
  background:linear-gradient(135deg,#09122a,var(--bg) 55%);overflow:hidden}}
header::after{{content:"";position:absolute;bottom:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--orange) 25%,var(--blue) 75%,transparent)}}
.logo{{font-family:var(--bebas);font-size:2rem;letter-spacing:3px;line-height:1;
  background:linear-gradient(135deg,#fff 30%,var(--orange));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.logo-sub{{font-family:var(--mono);font-size:.5rem;color:var(--m2);letter-spacing:3px;margin-top:3px}}
.hdr-r{{display:flex;flex-direction:column;align-items:flex-end;gap:3px}}
.live-badge{{font-family:var(--mono);font-size:.52rem;letter-spacing:2px;color:var(--green);
  border:1px solid var(--green);border-radius:3px;padding:2px 7px;display:flex;align-items:center;gap:4px}}
.live-dot{{width:5px;height:5px;background:var(--green);border-radius:50%;animation:pulse 1.4s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.4;transform:scale(.8)}}}}
.hdr-date{{font-family:var(--mono);font-size:.52rem;color:var(--m1)}}

/* TABS */
.tab-bar{{background:var(--s1);border-bottom:1px solid var(--b1);overflow-x:auto;scrollbar-width:none}}
.tab-bar::-webkit-scrollbar{{display:none}}
.tab-list{{display:flex;padding:0 6px;min-width:max-content}}
.tab{{position:relative;padding:10px 14px 8px;cursor:pointer;
  border-bottom:2px solid transparent;transition:all .15s;white-space:nowrap;user-select:none}}
.tab:hover{{background:rgba(255,255,255,.03)}}
.tab.active{{border-bottom-color:var(--orange)}}
.tab-label{{font-family:var(--bebas);font-size:.95rem;letter-spacing:1px;color:var(--txt);transition:color .15s}}
.tab.active .tab-label{{color:var(--orange)}}
.tab-meta{{font-family:var(--mono);font-size:.44rem;color:var(--m2);letter-spacing:.5px;margin-top:2px}}
.tab-badge{{font-family:var(--mono);font-size:.42rem;
  background:var(--b2);color:var(--m2);border-radius:20px;padding:1px 5px;margin-left:4px}}
.tab.active .tab-badge{{background:var(--orange);color:#000}}
.tab-live{{font-family:var(--mono);font-size:.4rem;color:var(--green);letter-spacing:1px;margin-top:1px}}

/* PANELS */
.panel{{display:none;animation:fadeIn .2s ease}}
.panel.active{{display:block}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:translateY(0)}}}}

/* SUMMARY */
.sum-wrap{{max-width:1200px;margin:0 auto;padding:18px 16px 60px}}
.sum-hdr{{display:flex;align-items:flex-start;gap:12px;margin-bottom:18px;
  padding-bottom:14px;border-bottom:1px solid var(--b1)}}
.sum-title{{font-family:var(--bebas);font-size:1.9rem;letter-spacing:2px;line-height:1}}
.sum-sub{{font-family:var(--mono);font-size:.52rem;color:var(--m2);margin-top:3px}}
.sum-kpis{{display:flex;gap:20px;margin-left:auto;flex-shrink:0}}
.kpi{{text-align:center}}
.kpi-v{{font-family:var(--bebas);font-size:1.6rem;line-height:1}}
.kpi-l{{font-family:var(--mono);font-size:.42rem;color:var(--m2);letter-spacing:1px;margin-top:1px;text-transform:uppercase}}

.sum-table-wrap{{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:20px}}.sum-table{{background:var(--s1);border:1px solid var(--b1);border-radius:10px;overflow:hidden;min-width:580px}}
.sum-thead{{display:grid;
  grid-template-columns:32px 1fr 80px 60px 56px 72px 100px;
  gap:8px;padding:7px 12px;background:var(--s2);border-bottom:1px solid var(--b2)}}
.sth{{font-family:var(--mono);font-size:.44rem;letter-spacing:1.5px;color:var(--m2);text-transform:uppercase}}
.sth.c{{text-align:center}}.sth.r{{text-align:right}}

.sum-row{{display:grid;
  grid-template-columns:32px 1fr 80px 60px 56px 72px 100px;
  align-items:center;gap:8px;padding:8px 12px;
  border-bottom:1px solid var(--b1);border-left:3px solid transparent;
  transition:background .13s;cursor:default;
  animation:rowIn .25s ease both}}
@keyframes rowIn{{from{{opacity:0;transform:translateX(-6px)}}to{{opacity:1;transform:translateX(0)}}}}
.sum-row:hover{{background:var(--s2)}}
.sr-rank{{font-family:var(--bebas);font-size:1rem;color:var(--m1)}}
.sr-name{{font-family:var(--bebas);font-size:1.05rem;letter-spacing:.5px;line-height:1}}
.sr-meta{{font-family:var(--mono);font-size:.44rem;color:var(--m2);margin-top:1px}}
.sr-game{{font-family:var(--mono);font-size:.54rem;color:var(--m2);text-align:center}}
.sr-score{{font-family:var(--bebas);font-size:1.35rem;text-align:right;line-height:1}}
.sr-dir{{font-family:var(--mono);font-size:.5rem;letter-spacing:1.5px;font-weight:600;text-align:center}}
.cat-chip{{font-family:var(--mono);font-size:.58rem;font-weight:600;letter-spacing:1px;
  border-radius:4px;padding:2px 7px;border:1px solid}}

/* GAME PANEL */
.game-wrap{{max-width:1280px;margin:0 auto;padding:16px 14px 60px}}
.game-hdr{{display:flex;align-items:center;gap:14px;padding:12px 16px;
  margin-bottom:14px;background:var(--s1);border:1px solid var(--b1);
  border-radius:10px;position:relative;overflow:hidden}}
.game-hdr::before{{content:"";position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--orange),var(--blue))}}
.gh-team{{font-family:var(--bebas);font-size:1.8rem;letter-spacing:2px;line-height:1}}
.gh-rec{{font-family:var(--mono);font-size:.48rem;color:var(--m2);margin-top:2px}}
.gh-mid{{flex:1;text-align:center}}
.gh-at{{font-family:var(--bebas);font-size:.85rem;color:var(--m2)}}
.gh-time{{font-family:var(--bebas);font-size:1.05rem;letter-spacing:2px;color:var(--orange)}}
.gh-prob{{font-family:var(--mono);font-size:.5rem;color:var(--m2);margin-top:2px;letter-spacing:1px}}
.gh-live{{font-family:var(--mono);font-size:.48rem;color:var(--green);margin-top:2px;letter-spacing:1px}}

/* LINEUP BAR */
.lineup-bar{{background:var(--s2);border:1px solid var(--b1);border-radius:8px;
  padding:10px 14px;margin-bottom:14px}}
.lineup-title{{font-family:var(--mono);font-size:.46rem;letter-spacing:2px;
  color:var(--m2);text-transform:uppercase;margin-bottom:8px}}
.lineup-teams{{display:flex;gap:20px;flex-wrap:wrap}}
.lineup-team{{flex:1;min-width:200px}}
.lineup-team-lbl{{font-family:var(--bebas);font-size:.8rem;letter-spacing:1px;
  color:var(--m2);margin-bottom:5px}}
.lineup-pills{{display:flex;gap:4px;flex-wrap:wrap}}
.lpill{{font-family:var(--mono);font-size:.52rem;border:1px solid var(--b2);
  border-radius:4px;padding:2px 7px;display:flex;align-items:center;gap:3px}}
.lpill.starter{{color:var(--txt);border-color:var(--b2)}}
.lpill.bench{{color:var(--m2);border-style:dashed}}
.lpill.gtd{{color:var(--yellow);border-color:#fbbf2450}}
.lpill.out{{color:var(--red);border-color:#f43f5e50}}
.lp-pos{{font-size:.4rem;color:var(--m1);background:var(--b1);padding:1px 3px;border-radius:2px}}
.lp-min{{font-size:.44rem;color:var(--m1)}}

/* CONTROLS */
.ctrl-bar{{display:flex;align-items:center;gap:5px;margin-bottom:12px;flex-wrap:wrap}}
.ctrl-lbl{{font-family:var(--mono);font-size:.45rem;letter-spacing:1.5px;color:var(--m2);text-transform:uppercase}}
.ctrl-btn{{font-family:var(--mono);font-size:.48rem;letter-spacing:1px;border:1px solid var(--b2);
  border-radius:4px;padding:3px 8px;cursor:pointer;background:transparent;color:var(--m2);transition:all .13s}}
.ctrl-btn:hover,.ctrl-btn.on{{border-color:var(--orange);color:var(--orange);background:rgba(251,146,60,.06)}}
.ctrl-sep{{width:1px;height:14px;background:var(--b1);margin:0 2px}}
.ctrl-r{{margin-left:auto;font-family:var(--mono);font-size:.46rem;color:var(--m2)}}

/* PLAYER GRID */
.pgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:10px}}

/* PLAYER CARD */
.pcard{{background:var(--s1);border:1px solid var(--b1);border-radius:11px;
  padding:12px 13px 10px;position:relative;overflow:hidden;
  transition:transform .12s,box-shadow .12s;
  animation:cardIn .3s ease both}}
@keyframes cardIn{{from{{opacity:0;transform:translateY(7px)}}to{{opacity:1;transform:translateY(0)}}}}
.pcard:hover{{transform:translateY(-2px);box-shadow:0 12px 36px rgba(0,0,0,.6)}}
.pcard-bar{{position:absolute;top:0;left:0;width:3px;height:100%;border-radius:3px 0 0 3px}}

.inj-banner{{font-family:var(--mono);font-size:.52rem;letter-spacing:1px;
  border:1px solid;border-radius:4px;padding:3px 8px;margin-bottom:7px}}

/* CARD TOP */
.ct{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px}}
.ct-l{{flex:1}}
.ct-badges{{display:flex;gap:3px;flex-wrap:wrap;align-items:center;margin-bottom:3px}}
.b-dir{{font-family:var(--mono);font-size:.48rem;letter-spacing:2px;font-weight:600;
  border:1px solid;border-radius:3px;padding:2px 6px}}
.b-role{{font-family:var(--mono);font-size:.44rem;letter-spacing:1px;
  color:var(--yellow);border:1px solid #fbbf2440;border-radius:3px;padding:1px 5px}}
.b-inj{{font-family:var(--mono);font-size:.44rem;letter-spacing:1px;
  border:1px solid;border-radius:3px;padding:1px 5px}}
.pname{{font-family:var(--bebas);font-size:1.3rem;letter-spacing:.5px;line-height:1}}
.psub{{font-family:var(--mono);font-size:.52rem;color:var(--m2);margin-top:2px}}
.ct-r{{text-align:right;flex-shrink:0;padding-left:8px}}
.score-n{{font-family:var(--bebas);font-size:1.85rem;line-height:1;margin-bottom:2px}}
.conf-b{{font-family:var(--mono);font-size:.46rem;letter-spacing:1.5px;
  border:1px solid;border-radius:3px;padding:2px 5px;display:inline-block}}
.min-b{{font-family:var(--mono);font-size:.48rem;margin-top:4px}}

/* CAT CHIPS */
.cat-row{{display:flex;align-items:center;gap:3px;margin-bottom:7px;flex-wrap:wrap}}
.cat-lbl{{font-family:var(--mono);font-size:.42rem;letter-spacing:2px;
  color:var(--m1);text-transform:uppercase;margin-right:2px}}
.chip{{font-family:var(--mono);font-size:.52rem;font-weight:600;letter-spacing:1px;
  border-radius:4px;padding:2px 5px;border:1px solid;transition:opacity .13s;cursor:default}}
.chip.best{{font-size:.6rem}}

/* TARGET BOX */
.tbox{{border:1px solid;border-radius:7px;padding:7px 9px;margin-bottom:7px}}
.tbox-lbl{{font-family:var(--mono);font-size:.5rem;letter-spacing:1px;
  display:block;margin-bottom:5px;font-weight:600}}
.tbox-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:3px}}
.tg{{text-align:center;background:rgba(0,0,0,.2);border-radius:4px;padding:4px 2px}}
.tg-v{{font-family:var(--mono);font-size:.8rem;font-weight:600;line-height:1}}
.tg-k{{font-family:var(--mono);font-size:.38rem;color:var(--m2);
  margin-top:2px;letter-spacing:.5px;text-transform:uppercase}}

/* SPARKLINE */
.spark-wrap{{margin-bottom:7px}}
.spark-lbl{{font-family:var(--mono);font-size:.42rem;letter-spacing:1.5px;
  color:var(--m1);text-transform:uppercase;margin-bottom:4px;
  display:flex;justify-content:space-between;align-items:center}}
.spark-chart{{position:relative;height:32px;display:flex;
  align-items:flex-end;gap:2px;padding-top:4px}}
.sp-bar{{flex:1;border-radius:2px 2px 0 0;min-height:3px;position:relative;z-index:1}}
.sp-line{{position:absolute;left:0;right:0;height:1.5px;
  background:rgba(255,255,255,.22);pointer-events:none;z-index:2}}
.spark-leg{{display:flex;gap:8px;font-family:var(--mono);
  font-size:.4rem;color:var(--m1);margin-top:3px;align-items:center}}
.sl-dot{{width:6px;height:4px;border-radius:1px;display:inline-block}}

/* STAT COMPARE: L10 (primary) vs Season (reference) */
.stat-cmp{{display:flex;align-items:center;gap:6px;margin-bottom:6px;
  background:var(--s2);border:1px solid var(--b1);border-radius:6px;padding:7px 9px}}
.sc-col{{flex:1}}
.sc-col.r{{text-align:right}}
.sc-lbl{{font-family:var(--mono);font-size:.4rem;letter-spacing:1.5px;
  color:var(--m1);text-transform:uppercase;margin-bottom:3px}}
.sc-vals{{display:flex;gap:4px;font-family:var(--mono);font-size:.56rem;color:var(--m2);flex-wrap:wrap}}
.sc-col.r .sc-vals{{justify-content:flex-end}}
.sc-pra{{font-family:var(--bebas);font-size:.95rem;line-height:1;margin-top:2px}}
.sc-arr{{font-family:var(--mono);font-size:.62rem;font-weight:600;text-align:center;flex-shrink:0}}

/* EDGE BARS */
.edge-box{{width:88px;flex-shrink:0;background:var(--s2);
  border:1px solid var(--b1);border-radius:6px;padding:6px 8px}}
.eb-title{{font-family:var(--mono);font-size:.38rem;letter-spacing:1.5px;
  color:var(--m1);text-transform:uppercase;margin-bottom:4px}}
.eb-row{{display:flex;align-items:center;gap:3px;margin-bottom:3px}}
.eb-l{{font-family:var(--mono);font-size:.42rem;color:var(--m1);width:18px}}
.eb-track{{flex:1;height:3px;background:var(--b1);border-radius:2px;overflow:hidden}}
.eb-fill{{height:100%;border-radius:2px}}
.eb-val{{font-family:var(--mono);font-size:.44rem;width:18px;text-align:right}}

/* LAST GAME ROW */
.lg-row{{display:flex;align-items:center;gap:4px;flex-wrap:wrap;
  font-family:var(--mono);font-size:.58rem;margin-bottom:6px}}
.lg-tag{{font-size:.4rem;letter-spacing:1.5px;color:var(--m1);text-transform:uppercase;
  border:1px solid var(--b2);border-radius:3px;padding:2px 5px;margin-right:2px}}
.lg-v{{color:var(--m2)}}.lg-s{{color:var(--b2)}}.lg-hot{{font-weight:600}}

/* SIGNALS */
.sigs{{list-style:none;display:flex;flex-direction:column;gap:2px;margin-bottom:6px}}
.sigs li{{font-family:var(--mono);font-size:.56rem;color:#3a5a88;line-height:1.4}}
.note{{font-family:var(--body);font-size:.62rem;color:var(--m2);
  border-left:2px solid var(--b2);padding-left:6px;line-height:1.5;font-weight:300}}

.disc{{text-align:center;font-family:var(--mono);font-size:.5rem;
  color:var(--m1);padding:18px 0 8px;line-height:2;border-top:1px solid var(--b1)}}
</style>
</head>
<body>

<header>
  <div>
    <div class="logo">Trust Me Bro Props</div>
    <div class="logo-sub" id="slug">{TODAY} · {total_games} Games · {total_players} Players</div>
  </div>
  <div class="hdr-r">
    <div class="live-badge"><span class="live-dot"></span>LIVE</div>
    <div class="hdr-date" id="clk"></div>
  </div>
</header>

<div class="tab-bar"><div class="tab-list" id="tabs"></div></div>
<div id="panels"></div>

<script>
const CAT   = {CAT_META_JS};
const GAMES = {GAMES_JS};
const PICKS = {PICKS_JS};
const ALL   = {ALL_JS};
const INJ_C = {{GTD:"#fbbf24",QUESTIONABLE:"#fbbf24",DOUBTFUL:"#f43f5e",OUT:"#f43f5e"}};

// Clock
(function tick(){{
  document.getElementById("clk").textContent =
    new Date().toLocaleTimeString("en-US",{{hour:"numeric",minute:"2-digit",hour12:true}})+" ET";
  setTimeout(tick, 1000);
}})();

// ── helpers ──────────────────────────────────────────────────────────────────
function esc(s){{ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;"); }}

function sparkHTML(vals, fdLine, color) {{
  if (!vals || !vals.length) return "";
  const mn = Math.min(...vals, fdLine * 0.88);
  const mx = Math.max(...vals, fdLine * 1.05);
  const rng = mx - mn || 1;
  const linePct = ((fdLine - mn) / rng * 100).toFixed(1);
  const overs = vals.filter(v => v >= fdLine).length;
  const bars = vals.map((v, i) => {{
    const h = Math.max(3, Math.round((v - mn) / rng * 27));
    const isO = v >= fdLine;
    const op = (0.4 + (i / (vals.length - 1)) * 0.6).toFixed(2);
    return "<div class='sp-bar' style='height:" + h + "px;opacity:" + op +
           ";background:" + (isO ? "var(--green)" : "var(--red)") +
           "' title='" + v + "'></div>";
  }}).join("");
  return "<div class='spark-wrap'>" +
    "<div class='spark-lbl'><span>L10 vs Line</span>" +
    "<span style='color:" + color + "'>" + overs + "/10 over " + fdLine + "</span></div>" +
    "<div class='spark-chart'>" + bars +
    "<div class='sp-line' style='bottom:calc(" + linePct + "% + 1px)'></div></div>" +
    "<div class='spark-leg'>" +
    "<span><span class='sl-dot' style='background:var(--green)'></span> Over (" + overs + ")</span>" +
    "<span><span class='sl-dot' style='background:var(--red)'></span> Under (" + (10 - overs) + ")</span>" +
    "<span style='margin-left:auto;color:var(--m2)'>Line: " + fdLine + "</span>" +
    "</div></div>";
}}

function edgeBarsHTML(edges) {{
  return [["PTS","pts","#38bdf8"],["REB","reb","#c084fc"],["AST","ast","#34d399"]].map(([l,k,c]) => {{
    const v = edges[k] || 0;
    const pct = Math.min(100, Math.round(v / 4 * 100));
    const ac = v >= 1.2 ? c : "#1e2c48";
    return "<div class='eb-row'><span class='eb-l'>" + l + "</span>" +
           "<div class='eb-track'><div class='eb-fill' style='width:" + pct + "%;background:" + c + "'></div></div>" +
           "<span class='eb-val' style='color:" + ac + "'>" + v.toFixed(1) + "</span></div>";
  }}).join("");
}}

function catChipsHTML(catScores, best) {{
  return Object.entries(catScores)
    .sort((a,b) => b[1] - a[1])
    .map(([cat, sc]) => {{
      const m = CAT[cat], isB = cat === best;
      const op = isB ? 1 : sc > 2 ? 0.45 : 0.16;
      const bw = isB ? 2 : 1;
      return "<span class='chip" + (isB ? " best" : "") + "' style='color:" + m.color +
             ";border:" + bw + "px solid " + m.color + (isB ? "" : "30") +
             ";background:" + (isB ? m.color + "14" : "transparent") +
             ";opacity:" + op + "' title='" + m.label + ": " + sc.toFixed(1) + "'>" + cat + "</span>";
    }}).join("");
}}

function pcardHTML(p, i) {{
  const isO = p.direction === "OVER";
  const inj = p.inj;
  let bc = isO ? "#22c55e" : "#f43f5e";
  if (inj) bc = INJ_C[inj] || "#fbbf24";
  const cc = {{HIGH:"#22c55e", MED:"#fbbf24", LOW:"#6b7280"}}[p.conf];
  const cat = p.target_cat, m = CAT[cat];
  const l10 = p.l10_avg, lg = p.last_game;
  const l10c = p.l10_combos, l10l = p.l10_lows, lastc = p.last_combos;
  const cv = l10c[cat], cvl = l10l[cat], cvlast = lastc[cat];
  const fp = cv > 0 ? Math.round(cvl / cv * 100) : 0;
  const fpc = fp >= 75 ? "#22c55e" : fp >= 60 ? "#fbbf24" : "#f43f5e";
  const lc = cvlast < cv * 0.82 ? "#f43f5e" : cvlast > cv * 1.1 ? "#22c55e" : "#6b7280";

  // L10 vs season trend arrow
  const l10pra = p.l10_pra;
  const spra = p.l10_avg.pts + p.l10_avg.reb + p.l10_avg.ast; // approx season from l10
  const diff = l10pra - (p.l10_combos.PRA);  // just show L10 PRA vs itself for now
  const minDiff = p.min_l10 - p.min_avg;
  const mc = minDiff > 1.5 ? "#22c55e" : minDiff < -2 ? "#f43f5e" : "#6b7280";
  const delay = (i * 0.05).toFixed(2) + "s";

  const injBanner = inj
    ? "<div class='inj-banner' style='color:" + bc + ";border-color:" + bc + "30;background:" + bc + "0a'>[WARN] " + inj + " — verify status before betting</div>"
    : "";
  const roleBadge = p.role === "bench"
    ? "<span class='b-role'>BENCH</span>" : "";
  const injBadge = inj
    ? "<span class='b-inj' style='color:" + bc + ";border-color:" + bc + "40'>" + inj + "</span>" : "";
  const flags = p.flags.map(f => "<li>" + esc(f) + "</li>").join("");

  return "<div class='pcard' style='animation-delay:" + delay + "'>" +
    "<div class='pcard-bar' style='background:" + bc + "'></div>" +
    injBanner +
    "<div class='ct'><div class='ct-l'>" +
      "<div class='ct-badges'>" +
        "<span class='b-dir' style='color:" + bc + ";border-color:" + bc + "'>" + p.direction + "</span>" +
        roleBadge + injBadge +
      "</div>" +
      "<div class='pname'>" + esc(p.name) + "</div>" +
      "<div class='psub'>" + p.pos + " · <b>" + p.team + "</b> vs " + p.opp + "</div>" +
    "</div><div class='ct-r'>" +
      "<div class='score-n' style='color:" + bc + "'>" + (p.score > 0 ? "+" : "") + p.score.toFixed(1) + "</div>" +
      "<div class='conf-b' style='color:" + cc + ";border-color:" + cc + "'>" + p.conf + "</div>" +
      "<div class='min-b' style='color:" + mc + "'>" + p.min_avg + "→" + p.min_l10 + " min</div>" +
    "</div></div>" +
    "<div class='cat-row'><span class='cat-lbl'>Bet</span>" + catChipsHTML(p.cat_scores, cat) + "</div>" +
    "<div class='tbox' style='border-color:" + m.color + "20;background:" + m.color + "07'>" +
      "<span class='tbox-lbl' style='color:" + m.color + "'>🎯 " + cat + " — " + m.label + "</span>" +
      "<div class='tbox-grid'>" +
        "<div class='tg'><div class='tg-v'>" + cv.toFixed(1) + "</div><div class='tg-k'>L10 Avg</div></div>" +
        "<div class='tg'><div class='tg-v' style='color:#f43f5e'>" + cvl + "</div><div class='tg-k'>L10 Low ✓</div></div>" +
        "<div class='tg'><div class='tg-v' style='color:" + lc + "'>" + cvlast + "</div><div class='tg-k'>Last Game</div></div>" +
        "<div class='tg'><div class='tg-v' style='color:" + fpc + "'>" + fp + "%</div><div class='tg-k'>Floor Safety</div></div>" +
      "</div>" +
    "</div>" +
    sparkHTML(p.spark, p.fd_line, m.color) +
    "<div style='display:flex;gap:6px;margin-bottom:6px'>" +
      "<div class='stat-cmp' style='flex:1'>" +
        "<div class='sc-col'><div class='sc-lbl'>L10 Avg (Primary)</div>" +
          "<div class='sc-vals'><span>" + l10.pts + "p</span><span>" + l10.reb + "r</span><span>" + l10.ast + "a</span></div>" +
          "<div class='sc-pra'>" + l10pra + " PRA</div>" +
        "</div>" +
      "</div>" +
      "<div class='edge-box'><div class='eb-title'>Matchup Edge</div>" + edgeBarsHTML(p.edges) + "</div>" +
    "</div>" +
    "<div class='lg-row'>" +
      "<span class='lg-tag'>Last Game</span>" +
      "<span class='lg-v'>" + lg.pts + "pts</span><span class='lg-s'>/</span>" +
      "<span class='lg-v'>" + lg.reb + "reb</span><span class='lg-s'>/</span>" +
      "<span class='lg-v'>" + lg.ast + "ast</span><span class='lg-s'>/</span>" +
      "<span class='lg-hot' style='color:" + (lastc.PRA < l10pra * 0.78 ? "#f43f5e" : "#6b7280") + "'>" + lastc.PRA + " PRA</span>" +
    "</div>" +
    (flags ? "<ul class='sigs'>" + flags + "</ul>" : "") +
    "<div class='note'>" + esc(p.notes) + "</div>" +
    "</div>";
}}

function sumRowHTML(p, rank) {{
  const isO = p.direction === "OVER", inj = p.inj;
  let bc = isO ? "#22c55e" : "#f43f5e";
  if (inj) bc = INJ_C[inj] || "#fbbf24";
  const cc = {{HIGH:"#22c55e", MED:"#fbbf24", LOW:"#6b7280"}}[p.conf];
  const cat = p.target_cat, m = CAT[cat];
  const vals = p.spark || [], fdLine = p.fd_line;
  const mn = Math.min(...vals, fdLine * 0.88);
  const mx = Math.max(...vals, fdLine * 1.05);
  const rng = mx - mn || 1;
  const linePct = ((fdLine - mn) / rng * 100).toFixed(1);
  const overs = vals.filter(v => v >= fdLine).length;
  const miniSpark = vals.map((v, i) => {{
    const h = Math.max(3, Math.round((v - mn) / rng * 24));
    const isO2 = v >= fdLine;
    const op = (0.4 + (i / (vals.length - 1)) * 0.6).toFixed(2);
    return "<div style='width:7px;height:" + h + "px;background:" + (isO2 ? "var(--green)" : "var(--red)") +
           ";opacity:" + op + ";border-radius:2px 2px 0 0;flex-shrink:0' title='" + v + "'></div>";
  }}).join("");
  const g = GAMES.find(g2 => g2.id === p.game_id) || {{}};
  const gameLabel = g.away ? g.away + "@" + g.home : p.team + " vs " + p.opp;
  const roleTag = p.role === "bench"
    ? "<span style='font-size:.4rem;color:#fbbf24;border:1px solid #fbbf2440;border-radius:2px;padding:1px 3px;margin-left:3px'>B</span>" : "";
  const injTag = inj
    ? "<span style='font-size:.4rem;color:" + bc + ";border:1px solid " + bc + "40;border-radius:2px;padding:1px 3px;margin-left:3px'>" + inj + "</span>" : "";
  const delay = (rank * 0.025).toFixed(2) + "s";

  return "<div class='sum-row' style='animation-delay:" + delay + ";border-left-color:" + bc + "'>" +
    "<div class='sr-rank' style='color:" + bc + "'>" + (rank + 1) + "</div>" +
    "<div><div class='sr-name'>" + esc(p.name) + roleTag + injTag + "</div>" +
      "<div class='sr-meta'>" + p.pos + " · " + p.team + " vs " + p.opp + " · " + p.min_avg + "→" + p.min_l10 + "min</div></div>" +
    "<div class='sr-game'>" + gameLabel + "</div>" +
    "<div class='sr-score' style='color:" + bc + "'>" + (p.score > 0 ? "+" : "") + p.score.toFixed(1) + "</div>" +
    "<div class='sr-dir' style='color:" + bc + "'>" + p.direction + "</div>" +
    "<div style='text-align:center'><span class='cat-chip' style='color:" + m.color + ";border-color:" + m.color + "30;background:" + m.color + "0e'>" + cat + "</span></div>" +
    "<div style='display:flex;align-items:flex-end;gap:2px;height:26px;position:relative'>" +
      miniSpark +
      "<div style='position:absolute;left:0;right:0;height:1.5px;background:rgba(255,255,255,.2);bottom:calc(" + linePct + "% + 1px)'></div>" +
    "</div>" +
    "</div>";
}}

function lineupHTML(players, teamAbbr) {{
  const tp = players.filter(p => p.team === teamAbbr);
  if (!tp.length) return "";
  const pills = tp.map(p => {{
    let cls = "lpill " + (p.role === "bench" ? "bench" : "starter");
    if (p.inj === "GTD" || p.inj === "QUESTIONABLE") cls = "lpill gtd";
    if (p.inj === "OUT" || p.inj === "DOUBTFUL") cls = "lpill out";
    const injTag = p.inj ? "<span style='font-size:.38rem'>" + p.inj + "</span>" : "";
    return "<span class='" + cls + "'>" +
      "<span class='lp-pos'>" + p.pos + "</span>" +
      esc(p.name.split(" ").pop()) + injTag +
      "<span class='lp-min'>" + p.min_l10 + "m</span></span>";
  }}).join("");
  return "<div class='lineup-team'><div class='lineup-team-lbl'>" + teamAbbr + "</div>" +
         "<div class='lineup-pills'>" + pills + "</div></div>";
}}

function buildGamePanel(g) {{
  const pl = PICKS[g.id] || [];
  const overs = pl.filter(p => p.direction === "OVER").length;
  const fades = pl.filter(p => p.direction === "FADE").length;
  const liveHTML = g.status && g.status !== "UPCOMING"
    ? "<div class='gh-live'>● " + g.status + "</div>" : "";
  return "<div class='game-hdr'>" +
      "<div><div class='gh-team'>" + g.away + "</div><div class='gh-rec'>" + g.away_rec + "</div></div>" +
      "<div class='gh-mid'><div class='gh-at'>@</div><div class='gh-time'>" + g.time + "</div>" +
        "<div class='gh-prob'>" + g.prob_away + "% · " + g.prob_home + "%</div>" + liveHTML + "</div>" +
      "<div style='text-align:right'><div class='gh-team'>" + g.home + "</div><div class='gh-rec'>" + g.home_rec + "</div></div>" +
    "</div>" +
    "<div class='lineup-bar'>" +
      "<div class='lineup-title'>[LIST] Probable Starters & Key Players · Min Trend (Season→L10)</div>" +
      "<div class='lineup-teams'>" + lineupHTML(pl, g.away) + lineupHTML(pl, g.home) + "</div>" +
    "</div>" +
    "<div class='ctrl-bar' id='ctrl-" + g.id + "'>" +
      "<button class='ctrl-btn on' data-gid='" + g.id + "' data-f='all' onclick='filt(this.dataset.gid,this.dataset.f,this)'>All (" + pl.length + ")</button>" +
      "<button class='ctrl-btn' data-gid='" + g.id + "' data-f='over' onclick='filt(this.dataset.gid,this.dataset.f,this)'>Overs (" + overs + ")</button>" +
      "<button class='ctrl-btn' data-gid='" + g.id + "' data-f='fade' onclick='filt(this.dataset.gid,this.dataset.f,this)'>Fades (" + fades + ")</button>" +
      "<div class='ctrl-sep'></div>" +
      "<button class='ctrl-btn on' data-gid='" + g.id + "' data-s='score' onclick='srt(this.dataset.gid,this.dataset.s,this)'>Score</button>" +
      "<button class='ctrl-btn' data-gid='" + g.id + "' data-s='name' onclick='srt(this.dataset.gid,this.dataset.s,this)'>Name</button>" +
      "<span class='ctrl-r'>" + pl.length + " players</span>" +
    "</div>" +
    "<div class='pgrid' id='grid-" + g.id + "'>" + pl.map((p,i) => pcardHTML(p, i)).join("") + "</div>" +
    "<div class='disc'>L10 avg is primary · Floor = true min from game logs · For entertainment only · Gamble responsibly</div>";
}}

function buildSummary() {{
  const overs = ALL.filter(p => p.direction === "OVER").length;
  const fades = ALL.filter(p => p.direction === "FADE").length;
  const high  = ALL.filter(p => p.conf === "HIGH").length;
  const thead = "<div class='sum-thead'>" +
    "<div class='sth'>#</div><div class='sth'>Player</div>" +
    "<div class='sth c'>Game</div><div class='sth r'>Score</div>" +
    "<div class='sth c'>Dir</div><div class='sth c'>Bet</div>" +
    "<div class='sth'>L10 Spark</div></div>";
  const rows = ALL.map((p,i) => sumRowHTML(p, i)).join("");
  return "<div class='sum-wrap'>" +
    "<div class='sum-hdr'><div>" +
      "<div class='sum-title'>🏆 All Players — Ranked</div>" +
      "<div class='sum-sub'>Primary metric: L10 avg · True floor from game logs · Bounce-back uses last 2 games</div>" +
    "</div><div class='sum-kpis'>" +
      "<div class='kpi'><div class='kpi-v' style='color:var(--green)'>" + overs + "</div><div class='kpi-l'>Overs</div></div>" +
      "<div class='kpi'><div class='kpi-v' style='color:var(--red)'>"   + fades + "</div><div class='kpi-l'>Fades</div></div>" +
      "<div class='kpi'><div class='kpi-v' style='color:var(--orange)'>" + high + "</div><div class='kpi-l'>HIGH</div></div>" +
      "<div class='kpi'><div class='kpi-v'>" + ALL.length + "</div><div class='kpi-l'>Total</div></div>" +
    "</div></div>" +
    "<div class='sum-table-wrap'><div class='sum-table'>" + thead + "<div id='sum-rows'>" + rows + "</div></div></div>" +
    "<div class='disc'>Sparklines: oldest→newest · Green bar = over FD line · Red = under · For entertainment only</div>" +
    "</div>";
}}

// ── State & Tab switching ─────────────────────────────────────────────────────
const STATE = {{}};
function filt(gid, dir, btn) {{
  btn.closest("#ctrl-" + gid).querySelectorAll(".ctrl-btn").forEach((b,i) => {{ if(i<3) b.classList.remove("on"); }});
  btn.classList.add("on");
  STATE[gid] = {{...STATE[gid], filter: dir}}; rerender(gid);
}}
function srt(gid, by, btn) {{
  btn.closest("#ctrl-" + gid).querySelectorAll(".ctrl-btn").forEach((b,i) => {{ if(i>=3) b.classList.remove("on"); }});
  btn.classList.add("on");
  STATE[gid] = {{...STATE[gid], sort: by}}; rerender(gid);
}}
function rerender(gid) {{
  const st = STATE[gid] || {{}};
  let pl = [...(PICKS[gid] || [])];
  if (st.filter === "over") pl = pl.filter(p => p.direction === "OVER");
  else if (st.filter === "fade") pl = pl.filter(p => p.direction === "FADE");
  if (st.sort === "name") pl.sort((a,b) => a.name.localeCompare(b.name));
  else pl.sort((a,b) => b.score - a.score);
  document.getElementById("grid-" + gid).innerHTML = pl.map((p,i) => pcardHTML(p,i)).join("");
}}
function switchTab(id) {{
  document.querySelectorAll(".tab").forEach(t => t.classList.toggle("active", t.dataset.tid === id));
  document.querySelectorAll(".panel").forEach(p => p.classList.toggle("active", p.id === "pnl-" + id));
}}

// ── Build DOM ─────────────────────────────────────────────────────────────────
const tabsEl   = document.getElementById("tabs");
const panelsEl = document.getElementById("panels");

// Summary tab
const sumTab = document.createElement("div");
sumTab.className = "tab active"; sumTab.dataset.tid = "summary";
sumTab.innerHTML = "<div class='tab-label'>[LIST] All Players</div>" +
  "<div class='tab-meta'>Ranked · " + ALL.length + " total</div>" +
  "<span class='tab-badge'>" + ALL.length + "</span>";
sumTab.addEventListener("click", () => switchTab("summary"));
tabsEl.appendChild(sumTab);
const sumPanel = document.createElement("div");
sumPanel.className = "panel active"; sumPanel.id = "pnl-summary";
sumPanel.innerHTML = buildSummary();
panelsEl.appendChild(sumPanel);

// Game tabs
GAMES.forEach(g => {{
  const cnt = (PICKS[g.id] || []).length;
  const isLive = g.status && g.status !== "UPCOMING";
  const tab = document.createElement("div");
  tab.className = "tab"; tab.dataset.tid = g.id;
  tab.innerHTML = "<div class='tab-label'>" + g.away + " @ " + g.home + "</div>" +
    "<div class='tab-meta'>" + g.time + "</div>" +
    (isLive ? "<div class='tab-live'>● LIVE</div>" : "") +
    "<span class='tab-badge'>" + cnt + "</span>";
  tab.addEventListener("click", () => switchTab(g.id));
  tabsEl.appendChild(tab);
  const panel = document.createElement("div");
  panel.className = "panel"; panel.id = "pnl-" + g.id;
  const inner = document.createElement("div");
  inner.className = "game-wrap";
  inner.innerHTML = buildGamePanel(g);
  panel.appendChild(inner);
  panelsEl.appendChild(panel);
}});
</script>
</body>
</html>'''


html = build_html()
out  = f"nba_props_{DATE}.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print(f"[OK] Report saved -> {out}  ({len(html)//1024}KB)")
print("   Open in browser: open " + out)
