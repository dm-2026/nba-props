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
        "id": "DAL_ORL",
        "away": "DAL",
        "home": "ORL",
        "away_rec": "",
        "home_rec": "",
        "time": "2026-03-06T00:00:00Z",
        "prob_away": 50,
        "prob_home": 50,
        "status": "UPCOMING",
        "ou": 228.5,
        "spread": 8.5
    },
    {
        "id": "UTA_WAS",
        "away": "UTA",
        "home": "WAS",
        "away_rec": "",
        "home_rec": "",
        "time": "2026-03-06T00:00:00Z",
        "prob_away": 50,
        "prob_home": 50,
        "status": "UPCOMING",
        "ou": 243.5,
        "spread": 3.5
    },
    {
        "id": "BKN_MIA",
        "away": "BKN",
        "home": "MIA",
        "away_rec": "",
        "home_rec": "",
        "time": "2026-03-06T00:30:00Z",
        "prob_away": 50,
        "prob_home": 50,
        "status": "UPCOMING",
        "ou": 226.5,
        "spread": 13.5
    },
    {
        "id": "GSW_HOU",
        "away": "GSW",
        "home": "HOU",
        "away_rec": "",
        "home_rec": "",
        "time": "2026-03-06T00:30:00Z",
        "prob_away": 50,
        "prob_home": 50,
        "status": "UPCOMING",
        "ou": 213.5,
        "spread": 8.5
    },
    {
        "id": "TOR_MIN",
        "away": "TOR",
        "home": "MIN",
        "away_rec": "",
        "home_rec": "",
        "time": "2026-03-06T01:00:00Z",
        "prob_away": 50,
        "prob_home": 50,
        "status": "UPCOMING",
        "ou": 226.5,
        "spread": 5.5
    },
    {
        "id": "DET_SAS",
        "away": "DET",
        "home": "SAS",
        "away_rec": "",
        "home_rec": "",
        "time": "2026-03-06T01:00:00Z",
        "prob_away": 50,
        "prob_home": 50,
        "status": "UPCOMING",
        "ou": 228.5,
        "spread": 3.5
    },
    {
        "id": "CHI_PHX",
        "away": "CHI",
        "home": "PHX",
        "away_rec": "",
        "home_rec": "",
        "time": "2026-03-06T02:00:00Z",
        "prob_away": 50,
        "prob_home": 50,
        "status": "UPCOMING",
        "spread": 10.5
    },
    {
        "id": "LAL_DEN",
        "away": "LAL",
        "home": "DEN",
        "away_rec": "",
        "home_rec": "",
        "time": "2026-03-06T03:00:00Z",
        "prob_away": 50,
        "prob_home": 50,
        "status": "UPCOMING",
        "ou": 240.5,
        "spread": 5.5
    },
    {
        "id": "NOP_SAC",
        "away": "NOP",
        "home": "SAC",
        "away_rec": "",
        "home_rec": "",
        "time": "2026-03-06T03:00:00Z",
        "prob_away": 50,
        "prob_home": 50,
        "status": "UPCOMING",
        "ou": 234.5,
        "spread": 5.5
    }
]

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: DEFENSIVE RANKINGS
# pts/reb/ast = rank out of 30 (1=best D, 30=worst D)
# Higher rank = worse defense = better for the offensive player
# pace = possessions per 48 min (league avg ~112)
# ─────────────────────────────────────────────────────────────────────────────
DEF = {
    "OKC": {
        "pace": 112.0,
        "PG_pts": 1,
        "PG_reb": 18,
        "PG_ast": 4,
        "SG_pts": 11,
        "SG_reb": 27,
        "SG_ast": 11,
        "SF_pts": 2,
        "SF_reb": 12,
        "SF_ast": 5,
        "PF_pts": 8,
        "PF_reb": 20,
        "PF_ast": 17,
        "C_pts": 4,
        "C_reb": 23,
        "C_ast": 10,
        "pts": 5,
        "reb": 20,
        "ast": 9
    },
    "BOS": {
        "pace": 112.0,
        "PG_pts": 2,
        "PG_reb": 5,
        "PG_ast": 19,
        "SG_pts": 2,
        "SG_reb": 13,
        "SG_ast": 6,
        "SF_pts": 3,
        "SF_reb": 19,
        "SF_ast": 1,
        "PF_pts": 16,
        "PF_reb": 6,
        "PF_ast": 5,
        "C_pts": 7,
        "C_reb": 3,
        "C_ast": 3,
        "pts": 6,
        "reb": 9,
        "ast": 7
    },
    "BKN": {
        "pace": 112.0,
        "PG_pts": 3,
        "PG_reb": 16,
        "PG_ast": 21,
        "SG_pts": 14,
        "SG_reb": 9,
        "SG_ast": 20,
        "SF_pts": 23,
        "SF_reb": 14,
        "SF_ast": 27,
        "PF_pts": 21,
        "PF_reb": 22,
        "PF_ast": 14,
        "C_pts": 22,
        "C_reb": 7,
        "C_ast": 8,
        "pts": 17,
        "reb": 14,
        "ast": 18
    },
    "HOU": {
        "pace": 112.0,
        "PG_pts": 4,
        "PG_reb": 3,
        "PG_ast": 9,
        "SG_pts": 1,
        "SG_reb": 6,
        "SG_ast": 2,
        "SF_pts": 13,
        "SF_reb": 5,
        "SF_ast": 8,
        "PF_pts": 6,
        "PF_reb": 1,
        "PF_ast": 3,
        "C_pts": 10,
        "C_reb": 2,
        "C_ast": 23,
        "pts": 7,
        "reb": 3,
        "ast": 9
    },
    "PHO": {
        "pace": 112.0,
        "PG_pts": 5,
        "PG_reb": 10,
        "PG_ast": 2,
        "SG_pts": 7,
        "SG_reb": 11,
        "SG_ast": 1,
        "SF_pts": 14,
        "SF_reb": 18,
        "SF_ast": 23,
        "PF_pts": 4,
        "PF_reb": 18,
        "PF_ast": 12,
        "C_pts": 16,
        "C_reb": 20,
        "C_ast": 20,
        "pts": 9,
        "reb": 15,
        "ast": 12
    },
    "NYK": {
        "pace": 112.0,
        "PG_pts": 6,
        "PG_reb": 1,
        "PG_ast": 6,
        "SG_pts": 15,
        "SG_reb": 24,
        "SG_ast": 25,
        "SF_pts": 16,
        "SF_reb": 20,
        "SF_ast": 3,
        "PF_pts": 5,
        "PF_reb": 3,
        "PF_ast": 7,
        "C_pts": 3,
        "C_reb": 9,
        "C_ast": 2,
        "pts": 9,
        "reb": 11,
        "ast": 9
    },
    "DET": {
        "pace": 112.0,
        "PG_pts": 7,
        "PG_reb": 14,
        "PG_ast": 3,
        "SG_pts": 8,
        "SG_reb": 1,
        "SG_ast": 3,
        "SF_pts": 11,
        "SF_reb": 4,
        "SF_ast": 2,
        "PF_pts": 11,
        "PF_reb": 8,
        "PF_ast": 6,
        "C_pts": 2,
        "C_reb": 8,
        "C_ast": 4,
        "pts": 8,
        "reb": 7,
        "ast": 4
    },
    "PHI": {
        "pace": 112.0,
        "PG_pts": 8,
        "PG_reb": 21,
        "PG_ast": 10,
        "SG_pts": 28,
        "SG_reb": 22,
        "SG_ast": 28,
        "SF_pts": 17,
        "SF_reb": 3,
        "SF_ast": 29,
        "PF_pts": 12,
        "PF_reb": 29,
        "PF_ast": 13,
        "C_pts": 18,
        "C_reb": 14,
        "C_ast": 5,
        "pts": 17,
        "reb": 18,
        "ast": 17
    },
    "CHI": {
        "pace": 112.0,
        "PG_pts": 9,
        "PG_reb": 15,
        "PG_ast": 25,
        "SG_pts": 24,
        "SG_reb": 17,
        "SG_ast": 24,
        "SF_pts": 10,
        "SF_reb": 28,
        "SF_ast": 18,
        "PF_pts": 30,
        "PF_reb": 23,
        "PF_ast": 23,
        "C_pts": 25,
        "C_reb": 15,
        "C_ast": 27,
        "pts": 20,
        "reb": 20,
        "ast": 23
    },
    "DEN": {
        "pace": 112.0,
        "PG_pts": 10,
        "PG_reb": 8,
        "PG_ast": 12,
        "SG_pts": 16,
        "SG_reb": 3,
        "SG_ast": 7,
        "SF_pts": 25,
        "SF_reb": 13,
        "SF_ast": 20,
        "PF_pts": 15,
        "PF_reb": 15,
        "PF_ast": 29,
        "C_pts": 19,
        "C_reb": 6,
        "C_ast": 9,
        "pts": 17,
        "reb": 9,
        "ast": 15
    },
    "CHA": {
        "pace": 112.0,
        "PG_pts": 11,
        "PG_reb": 2,
        "PG_ast": 8,
        "SG_pts": 5,
        "SG_reb": 19,
        "SG_ast": 18,
        "SF_pts": 5,
        "SF_reb": 7,
        "SF_ast": 12,
        "PF_pts": 24,
        "PF_reb": 4,
        "PF_ast": 25,
        "C_pts": 9,
        "C_reb": 1,
        "C_ast": 11,
        "pts": 11,
        "reb": 7,
        "ast": 15
    },
    "WAS": {
        "pace": 112.0,
        "PG_pts": 12,
        "PG_reb": 20,
        "PG_ast": 20,
        "SG_pts": 29,
        "SG_reb": 15,
        "SG_ast": 30,
        "SF_pts": 27,
        "SF_reb": 30,
        "SF_ast": 26,
        "PF_pts": 29,
        "PF_reb": 28,
        "PF_ast": 24,
        "C_pts": 29,
        "C_reb": 30,
        "C_ast": 19,
        "pts": 25,
        "reb": 25,
        "ast": 24
    },
    "LAC": {
        "pace": 112.0,
        "PG_pts": 13,
        "PG_reb": 25,
        "PG_ast": 14,
        "SG_pts": 22,
        "SG_reb": 2,
        "SG_ast": 12,
        "SF_pts": 9,
        "SF_reb": 2,
        "SF_ast": 11,
        "PF_pts": 1,
        "PF_reb": 2,
        "PF_ast": 18,
        "C_pts": 13,
        "C_reb": 12,
        "C_ast": 7,
        "pts": 12,
        "reb": 9,
        "ast": 12
    },
    "LAL": {
        "pace": 112.0,
        "PG_pts": 14,
        "PG_reb": 4,
        "PG_ast": 30,
        "SG_pts": 10,
        "SG_reb": 8,
        "SG_ast": 17,
        "SF_pts": 30,
        "SF_reb": 6,
        "SF_ast": 22,
        "PF_pts": 19,
        "PF_reb": 5,
        "PF_ast": 10,
        "C_pts": 1,
        "C_reb": 5,
        "C_ast": 17,
        "pts": 15,
        "reb": 6,
        "ast": 19
    },
    "CLE": {
        "pace": 112.0,
        "PG_pts": 15,
        "PG_reb": 7,
        "PG_ast": 22,
        "SG_pts": 19,
        "SG_reb": 10,
        "SG_ast": 9,
        "SF_pts": 8,
        "SF_reb": 9,
        "SF_ast": 7,
        "PF_pts": 23,
        "PF_reb": 24,
        "PF_ast": 28,
        "C_pts": 11,
        "C_reb": 19,
        "C_ast": 12,
        "pts": 15,
        "reb": 14,
        "ast": 16
    },
    "ATL": {
        "pace": 112.0,
        "PG_pts": 16,
        "PG_reb": 24,
        "PG_ast": 28,
        "SG_pts": 26,
        "SG_reb": 14,
        "SG_ast": 4,
        "SF_pts": 28,
        "SF_reb": 26,
        "SF_ast": 16,
        "PF_pts": 13,
        "PF_reb": 26,
        "PF_ast": 26,
        "C_pts": 20,
        "C_reb": 27,
        "C_ast": 14,
        "pts": 21,
        "reb": 23,
        "ast": 18
    },
    "SAS": {
        "pace": 112.0,
        "PG_pts": 17,
        "PG_reb": 23,
        "PG_ast": 1,
        "SG_pts": 3,
        "SG_reb": 20,
        "SG_ast": 15,
        "SF_pts": 6,
        "SF_reb": 11,
        "SF_ast": 15,
        "PF_pts": 9,
        "PF_reb": 7,
        "PF_ast": 15,
        "C_pts": 14,
        "C_reb": 18,
        "C_ast": 30,
        "pts": 10,
        "reb": 16,
        "ast": 15
    },
    "NOR": {
        "pace": 112.0,
        "PG_pts": 18,
        "PG_reb": 6,
        "PG_ast": 26,
        "SG_pts": 30,
        "SG_reb": 25,
        "SG_ast": 27,
        "SF_pts": 26,
        "SF_reb": 23,
        "SF_ast": 17,
        "PF_pts": 3,
        "PF_reb": 11,
        "PF_ast": 20,
        "C_pts": 23,
        "C_reb": 26,
        "C_ast": 21,
        "pts": 20,
        "reb": 18,
        "ast": 22
    },
    "MIA": {
        "pace": 112.0,
        "PG_pts": 19,
        "PG_reb": 28,
        "PG_ast": 18,
        "SG_pts": 17,
        "SG_reb": 30,
        "SG_ast": 16,
        "SF_pts": 20,
        "SF_reb": 10,
        "SF_ast": 9,
        "PF_pts": 27,
        "PF_reb": 30,
        "PF_ast": 22,
        "C_pts": 12,
        "C_reb": 25,
        "C_ast": 15,
        "pts": 19,
        "reb": 25,
        "ast": 16
    },
    "POR": {
        "pace": 112.0,
        "PG_pts": 20,
        "PG_reb": 12,
        "PG_ast": 13,
        "SG_pts": 18,
        "SG_reb": 12,
        "SG_ast": 14,
        "SF_pts": 22,
        "SF_reb": 27,
        "SF_ast": 21,
        "PF_pts": 14,
        "PF_reb": 9,
        "PF_ast": 21,
        "C_pts": 27,
        "C_reb": 13,
        "C_ast": 18,
        "pts": 20,
        "reb": 15,
        "ast": 17
    },
    "MEM": {
        "pace": 112.0,
        "PG_pts": 21,
        "PG_reb": 13,
        "PG_ast": 11,
        "SG_pts": 25,
        "SG_reb": 21,
        "SG_ast": 23,
        "SF_pts": 19,
        "SF_reb": 25,
        "SF_ast": 25,
        "PF_pts": 25,
        "PF_reb": 21,
        "PF_ast": 19,
        "C_pts": 15,
        "C_reb": 24,
        "C_ast": 26,
        "pts": 21,
        "reb": 21,
        "ast": 21
    },
    "DAL": {
        "pace": 112.0,
        "PG_pts": 22,
        "PG_reb": 30,
        "PG_ast": 24,
        "SG_pts": 6,
        "SG_reb": 29,
        "SG_ast": 5,
        "SF_pts": 7,
        "SF_reb": 21,
        "SF_ast": 28,
        "PF_pts": 20,
        "PF_reb": 14,
        "PF_ast": 4,
        "C_pts": 28,
        "C_reb": 22,
        "C_ast": 28,
        "pts": 17,
        "reb": 23,
        "ast": 18
    },
    "IND": {
        "pace": 112.0,
        "PG_pts": 23,
        "PG_reb": 29,
        "PG_ast": 16,
        "SG_pts": 13,
        "SG_reb": 28,
        "SG_ast": 13,
        "SF_pts": 21,
        "SF_reb": 22,
        "SF_ast": 6,
        "PF_pts": 26,
        "PF_reb": 27,
        "PF_ast": 9,
        "C_pts": 26,
        "C_reb": 21,
        "C_ast": 24,
        "pts": 22,
        "reb": 25,
        "ast": 14
    },
    "MIL": {
        "pace": 112.0,
        "PG_pts": 24,
        "PG_reb": 27,
        "PG_ast": 29,
        "SG_pts": 23,
        "SG_reb": 23,
        "SG_ast": 10,
        "SF_pts": 12,
        "SF_reb": 24,
        "SF_ast": 19,
        "PF_pts": 18,
        "PF_reb": 16,
        "PF_ast": 27,
        "C_pts": 8,
        "C_reb": 11,
        "C_ast": 6,
        "pts": 17,
        "reb": 20,
        "ast": 18
    },
    "MIN": {
        "pace": 112.0,
        "PG_pts": 25,
        "PG_reb": 26,
        "PG_ast": 15,
        "SG_pts": 4,
        "SG_reb": 4,
        "SG_ast": 8,
        "SF_pts": 15,
        "SF_reb": 16,
        "SF_ast": 14,
        "PF_pts": 7,
        "PF_reb": 17,
        "PF_ast": 2,
        "C_pts": 21,
        "C_reb": 4,
        "C_ast": 25,
        "pts": 14,
        "reb": 13,
        "ast": 13
    },
    "TOR": {
        "pace": 112.0,
        "PG_pts": 26,
        "PG_reb": 11,
        "PG_ast": 5,
        "SG_pts": 12,
        "SG_reb": 7,
        "SG_ast": 22,
        "SF_pts": 4,
        "SF_reb": 8,
        "SF_ast": 10,
        "PF_pts": 10,
        "PF_reb": 13,
        "PF_ast": 8,
        "C_pts": 5,
        "C_reb": 16,
        "C_ast": 1,
        "pts": 11,
        "reb": 11,
        "ast": 9
    },
    "GSW": {
        "pace": 112.0,
        "PG_pts": 27,
        "PG_reb": 9,
        "PG_ast": 7,
        "SG_pts": 20,
        "SG_reb": 16,
        "SG_ast": 19,
        "SF_pts": 1,
        "SF_reb": 15,
        "SF_ast": 24,
        "PF_pts": 17,
        "PF_reb": 25,
        "PF_ast": 11,
        "C_pts": 17,
        "C_reb": 29,
        "C_ast": 29,
        "pts": 16,
        "reb": 19,
        "ast": 18
    },
    "SAC": {
        "pace": 112.0,
        "PG_pts": 28,
        "PG_reb": 22,
        "PG_ast": 27,
        "SG_pts": 21,
        "SG_reb": 18,
        "SG_ast": 26,
        "SF_pts": 18,
        "SF_reb": 1,
        "SF_ast": 13,
        "PF_pts": 22,
        "PF_reb": 19,
        "PF_ast": 16,
        "C_pts": 30,
        "C_reb": 28,
        "C_ast": 22,
        "pts": 24,
        "reb": 18,
        "ast": 21
    },
    "ORL": {
        "pace": 112.0,
        "PG_pts": 29,
        "PG_reb": 19,
        "PG_ast": 17,
        "SG_pts": 9,
        "SG_reb": 5,
        "SG_ast": 21,
        "SF_pts": 24,
        "SF_reb": 29,
        "SF_ast": 4,
        "PF_pts": 2,
        "PF_reb": 12,
        "PF_ast": 1,
        "C_pts": 6,
        "C_reb": 10,
        "C_ast": 16,
        "pts": 14,
        "reb": 15,
        "ast": 12
    },
    "UTH": {
        "pace": 112.0,
        "PG_pts": 30,
        "PG_reb": 17,
        "PG_ast": 23,
        "SG_pts": 27,
        "SG_reb": 26,
        "SG_ast": 29,
        "SF_pts": 29,
        "SF_reb": 17,
        "SF_ast": 30,
        "PF_pts": 28,
        "PF_reb": 10,
        "PF_ast": 30,
        "C_pts": 24,
        "C_reb": 17,
        "C_ast": 13,
        "pts": 28,
        "reb": 17,
        "ast": 25
    }
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
    "DAL_ORL": [
        {
            "name": "Max Christie",
            "team": "DAL",
            "opp": "ORL",
            "pos": "SG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 15,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 18,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 8,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 12,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 13,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 1,
                    "ast": 2
                }
            ],
            "min_avg": 28.2,
            "min_l10": 27.2,
            "edges": {
                "pts": 0.2,
                "reb": 0.0,
                "ast": 2.2
            },
            "fd_line_cat": "P",
            "fd_line": 10.5,
            "note": "Usage boost +8% (Flagg OUT) | O/U 228.5"
        },
        {
            "name": "Khris Middleton",
            "team": "DAL",
            "opp": "ORL",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 9,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 2,
                    "ast": 5
                },
                {
                    "pts": 10,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 17,
                    "reb": 8,
                    "ast": 9
                },
                {
                    "pts": 9,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 13,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 15,
                    "reb": 6,
                    "ast": 6
                },
                {
                    "pts": 17,
                    "reb": 3,
                    "ast": 3
                }
            ],
            "min_avg": 22.9,
            "min_l10": 21.3,
            "edges": {
                "pts": 3.0,
                "reb": 3.8,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 11.0,
            "note": "Usage boost +8% (Flagg OUT) | Bounce-back (12 PRA last game vs 18 avg) | ORL #24 vs SF pts | O/U 228.5"
        },
        {
            "name": "Daniel Gafford",
            "team": "DAL",
            "opp": "ORL",
            "pos": "C",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 22,
                    "reb": 8,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 8,
                    "ast": 1
                },
                {
                    "pts": 11,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 4,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 12,
                    "reb": 6,
                    "ast": 0
                },
                {
                    "pts": 18,
                    "reb": 8,
                    "ast": 2
                },
                {
                    "pts": 4,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 5,
                    "reb": 10,
                    "ast": 1
                },
                {
                    "pts": 9,
                    "reb": 16,
                    "ast": 5
                },
                {
                    "pts": 13,
                    "reb": 6,
                    "ast": 0
                }
            ],
            "min_avg": 21.6,
            "min_l10": 21.5,
            "edges": {
                "pts": 0.0,
                "reb": 0.2,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 10.5,
            "note": "Usage boost +8% (Flagg OUT) | O/U 228.5"
        },
        {
            "name": "Naji Marshall",
            "team": "DAL",
            "opp": "ORL",
            "pos": "SF",
            "role": "bench",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 11,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 2,
                    "ast": 5
                },
                {
                    "pts": 24,
                    "reb": 4,
                    "ast": 8
                },
                {
                    "pts": 9,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 23,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 8
                },
                {
                    "pts": 8,
                    "reb": 8,
                    "ast": 3
                },
                {
                    "pts": 15,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 40,
                    "reb": 7,
                    "ast": 1
                }
            ],
            "min_avg": 27.8,
            "min_l10": 32.9,
            "edges": {
                "pts": 3.0,
                "reb": 3.8,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 14.5,
            "note": "Usage boost +4% (Flagg OUT) | Bounce-back (16 PRA last game vs 23 avg) | Minutes trending up (27.8->32.9) | ORL #24 vs SF pts | O/U 228.5"
        },
        {
            "name": "Caleb Martin",
            "team": "DAL",
            "opp": "ORL",
            "pos": "PF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 8,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 8,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 7,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 5,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 1,
                    "ast": 2
                }
            ],
            "min_avg": 27.1,
            "min_l10": 20.3,
            "edges": {
                "pts": 0.0,
                "reb": 0.5,
                "ast": 0.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 10.5,
            "note": "Usage boost +4% (Flagg OUT) | O/U 228.5"
        },
        {
            "name": "Klay Thompson",
            "team": "DAL",
            "opp": "ORL",
            "pos": "SG",
            "role": "bench",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 7,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 15,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 18,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 21,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 12,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 2
                }
            ],
            "min_avg": 27.4,
            "min_l10": 24.5,
            "edges": {
                "pts": 0.2,
                "reb": 0.0,
                "ast": 2.2
            },
            "fd_line_cat": "P",
            "fd_line": 10.5,
            "note": "Usage boost +4% (Flagg OUT) | Bounce-back (10 PRA last game vs 15 avg) | O/U 228.5"
        },
        {
            "name": "AJ Johnson",
            "team": "DAL",
            "opp": "ORL",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 15,
                    "reb": 1,
                    "ast": 8
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 7,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 8,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 12,
                    "reb": 0,
                    "ast": 4
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 20,
                    "reb": 2,
                    "ast": 6
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 21,
                    "reb": 1,
                    "ast": 4
                },
                {
                    "pts": 2,
                    "reb": 3,
                    "ast": 0
                }
            ],
            "min_avg": 28.2,
            "min_l10": 34.9,
            "edges": {
                "pts": 3.8,
                "reb": 1.5,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 11.0,
            "note": "Usage boost +4% (Flagg OUT) | Minutes trending up (28.2->34.9) | ORL #29 vs PG pts | O/U 228.5"
        },
        {
            "name": "Anthony Black",
            "team": "ORL",
            "opp": "DAL",
            "pos": "PG",
            "role": "starter",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 20,
                    "reb": 10,
                    "ast": 2
                },
                {
                    "pts": 21,
                    "reb": 6,
                    "ast": 7
                },
                {
                    "pts": 6,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 4,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 8,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 20,
                    "reb": 5,
                    "ast": 0
                }
            ],
            "min_avg": 24.1,
            "min_l10": 26.5,
            "edges": {
                "pts": 2.2,
                "reb": 3.8,
                "ast": 3.0
            },
            "fd_line_cat": "P",
            "fd_line": 11.0,
            "note": "DAL #30 vs PG reb | O/U 228.5"
        },
        {
            "name": "Desmond Bane",
            "team": "ORL",
            "opp": "DAL",
            "pos": "SG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 24,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 28,
                    "reb": 6,
                    "ast": 9
                },
                {
                    "pts": 19,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 38,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 17,
                    "reb": 9,
                    "ast": 6
                },
                {
                    "pts": 19,
                    "reb": 4,
                    "ast": 5
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 29,
                    "reb": 4,
                    "ast": 6
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 6
                },
                {
                    "pts": 21,
                    "reb": 4,
                    "ast": 6
                }
            ],
            "min_avg": 31.9,
            "min_l10": 33.3,
            "edges": {
                "pts": 0.0,
                "reb": 3.8,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 20.0,
            "note": "DAL #29 vs SG reb | O/U 228.5"
        },
        {
            "name": "Tristan da Silva",
            "team": "ORL",
            "opp": "DAL",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 14,
                    "reb": 7,
                    "ast": 6
                },
                {
                    "pts": 14,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 5,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 9,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 2,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 0
                }
            ],
            "min_avg": 22.9,
            "min_l10": 17.4,
            "edges": {
                "pts": 0.0,
                "reb": 2.2,
                "ast": 3.8
            },
            "fd_line_cat": "PRA",
            "fd_line": 9.5,
            "note": "DAL #28 vs SF ast | O/U 228.5"
        },
        {
            "name": "Paolo Banchero",
            "team": "ORL",
            "opp": "DAL",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 15,
                    "reb": 4,
                    "ast": 6
                },
                {
                    "pts": 33,
                    "reb": 10,
                    "ast": 4
                },
                {
                    "pts": 33,
                    "reb": 18,
                    "ast": 8
                },
                {
                    "pts": 24,
                    "reb": 10,
                    "ast": 4
                },
                {
                    "pts": 26,
                    "reb": 6,
                    "ast": 4
                },
                {
                    "pts": 24,
                    "reb": 6,
                    "ast": 6
                },
                {
                    "pts": 35,
                    "reb": 10,
                    "ast": 4
                },
                {
                    "pts": 32,
                    "reb": 7,
                    "ast": 6
                },
                {
                    "pts": 30,
                    "reb": 7,
                    "ast": 1
                },
                {
                    "pts": 30,
                    "reb": 8,
                    "ast": 5
                }
            ],
            "min_avg": 34.4,
            "min_l10": 34.8,
            "edges": {
                "pts": 1.5,
                "reb": 0.5,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 27.0,
            "note": "Bounce-back (25 PRA last game vs 42 avg) | O/U 228.5"
        },
        {
            "name": "Wendell Carter Jr.",
            "team": "ORL",
            "opp": "DAL",
            "pos": "C",
            "role": "starter",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 4,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 17,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 9,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 12,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 12,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 11,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 8,
                    "ast": 0
                }
            ],
            "min_avg": 25.9,
            "min_l10": 25.8,
            "edges": {
                "pts": 3.8,
                "reb": 2.2,
                "ast": 3.8
            },
            "fd_line_cat": "PRA",
            "fd_line": 16.0,
            "note": "Bounce-back (9 PRA last game vs 17 avg) | DAL #28 vs C pts | O/U 228.5"
        },
        {
            "name": "Jalen Suggs",
            "team": "ORL",
            "opp": "DAL",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 8,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 24,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 8,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 27,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 29,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 16,
                    "reb": 6,
                    "ast": 5
                },
                {
                    "pts": 9,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 9,
                    "reb": 5,
                    "ast": 8
                },
                {
                    "pts": 32,
                    "reb": 9,
                    "ast": 1
                }
            ],
            "min_avg": 28.7,
            "min_l10": 25.0,
            "edges": {
                "pts": 2.2,
                "reb": 3.8,
                "ast": 3.0
            },
            "fd_line_cat": "P",
            "fd_line": 16.0,
            "note": "Bounce-back (13 PRA last game vs 24 avg) | DAL #30 vs PG reb | O/U 228.5"
        },
        {
            "name": "Jevon Carter",
            "team": "ORL",
            "opp": "DAL",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 5,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 17,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 4
                },
                {
                    "pts": 10,
                    "reb": 2,
                    "ast": 6
                },
                {
                    "pts": 2,
                    "reb": 0,
                    "ast": 0
                }
            ],
            "min_avg": 13.9,
            "min_l10": 16.4,
            "edges": {
                "pts": 2.2,
                "reb": 3.8,
                "ast": 3.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 10.5,
            "note": "Minutes trending up (13.9->16.4) | DAL #30 vs PG reb | O/U 228.5"
        },
        {
            "name": "Jett Howard",
            "team": "ORL",
            "opp": "DAL",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 16,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 17,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 4,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 1,
                    "ast": 1
                }
            ],
            "min_avg": 13.0,
            "min_l10": 15.0,
            "edges": {
                "pts": 0.0,
                "reb": 3.8,
                "ast": 0.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 6.5,
            "note": "Minutes trending up (13.0->15.0) | DAL #29 vs SG reb | O/U 228.5"
        },
        {
            "name": "Goga Bitadze",
            "team": "ORL",
            "opp": "DAL",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 10,
                    "reb": 6,
                    "ast": 4
                },
                {
                    "pts": 11,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 6,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 12,
                    "reb": 10,
                    "ast": 5
                },
                {
                    "pts": 3,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 0,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 2
                }
            ],
            "min_avg": 20.8,
            "min_l10": 16.9,
            "edges": {
                "pts": 3.8,
                "reb": 2.2,
                "ast": 3.8
            },
            "fd_line_cat": "PRA",
            "fd_line": 12.0,
            "note": "DAL #28 vs C pts | O/U 228.5"
        },
        {
            "name": "Jamal Cain",
            "team": "ORL",
            "opp": "DAL",
            "pos": "SF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 18,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 25,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 20,
                    "reb": 7,
                    "ast": 0
                },
                {
                    "pts": 15,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 6,
                    "ast": 0
                },
                {
                    "pts": 11,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 4,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 5,
                    "reb": 3,
                    "ast": 2
                }
            ],
            "min_avg": 16.6,
            "min_l10": 20.8,
            "edges": {
                "pts": 0.0,
                "reb": 2.2,
                "ast": 3.8
            },
            "fd_line_cat": "P",
            "fd_line": 11.0,
            "note": "Minutes trending up (16.6->20.8) | DAL #28 vs SF ast | O/U 228.5"
        }
    ],
    "UTA_WAS": [
        {
            "name": "Isaiah Collier",
            "team": "UTA",
            "opp": "WAS",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 17,
                    "reb": 3,
                    "ast": 12
                },
                {
                    "pts": 15,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 22,
                    "reb": 5,
                    "ast": 10
                },
                {
                    "pts": 17,
                    "reb": 2,
                    "ast": 7
                },
                {
                    "pts": 3,
                    "reb": 3,
                    "ast": 7
                },
                {
                    "pts": 16,
                    "reb": 1,
                    "ast": 5
                },
                {
                    "pts": 21,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 7,
                    "reb": 7,
                    "ast": 6
                },
                {
                    "pts": 5,
                    "reb": 4,
                    "ast": 5
                },
                {
                    "pts": 16,
                    "reb": 3,
                    "ast": 6
                }
            ],
            "min_avg": 26.2,
            "min_l10": 30.7,
            "edges": {
                "pts": 0.5,
                "reb": 1.5,
                "ast": 1.5
            },
            "fd_line_cat": "A",
            "fd_line": 6.5,
            "note": "Minutes trending up (26.2->30.7) | High O/U 243.5 \u2014 shootout potential"
        },
        {
            "name": "Cody Williams",
            "team": "UTA",
            "opp": "WAS",
            "pos": "SG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 4,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 5,
                    "reb": 6,
                    "ast": 0
                }
            ],
            "min_avg": 21.1,
            "min_l10": 24.2,
            "edges": {
                "pts": 3.8,
                "reb": 1.0,
                "ast": 3.8
            },
            "fd_line_cat": "PRA",
            "fd_line": 6.5,
            "note": "Bounce-back (5 PRA last game vs 7 avg) | WAS #29 vs SG pts | High O/U 243.5 \u2014 shootout potential"
        },
        {
            "name": "Kyle Filipowski",
            "team": "UTA",
            "opp": "WAS",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 15,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 15,
                    "reb": 13,
                    "ast": 1
                },
                {
                    "pts": 30,
                    "reb": 18,
                    "ast": 5
                },
                {
                    "pts": 9,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 9,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 11,
                    "ast": 1
                },
                {
                    "pts": 14,
                    "reb": 13,
                    "ast": 2
                },
                {
                    "pts": 18,
                    "reb": 13,
                    "ast": 1
                },
                {
                    "pts": 16,
                    "reb": 7,
                    "ast": 4
                },
                {
                    "pts": 13,
                    "reb": 2,
                    "ast": 0
                }
            ],
            "min_avg": 21.6,
            "min_l10": 29.7,
            "edges": {
                "pts": 3.8,
                "reb": 3.8,
                "ast": 3.0
            },
            "fd_line_cat": "R",
            "fd_line": 9.5,
            "note": "Minutes trending up (21.6->29.7) | WAS #29 vs PF pts | High O/U 243.5 \u2014 shootout potential"
        },
        {
            "name": "Brice Sensabaugh",
            "team": "UTA",
            "opp": "WAS",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 22,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 25,
                    "reb": 5,
                    "ast": 6
                },
                {
                    "pts": 22,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 15,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 9,
                    "reb": 10,
                    "ast": 0
                },
                {
                    "pts": 10,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 19,
                    "reb": 1,
                    "ast": 5
                },
                {
                    "pts": 12,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 17,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 9,
                    "reb": 1,
                    "ast": 5
                }
            ],
            "min_avg": 20.5,
            "min_l10": 28.7,
            "edges": {
                "pts": 3.8,
                "reb": 1.0,
                "ast": 3.8
            },
            "fd_line_cat": "P",
            "fd_line": 15.5,
            "note": "Minutes trending up (20.5->28.7) | WAS #29 vs SG pts | High O/U 243.5 \u2014 shootout potential"
        },
        {
            "name": "Oscar Tshiebwe",
            "team": "UTA",
            "opp": "WAS",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 18,
                    "reb": 12,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 14,
                    "ast": 0
                },
                {
                    "pts": 17,
                    "reb": 10,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 11,
                    "ast": 1
                },
                {
                    "pts": 7,
                    "reb": 10,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 10,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 13,
                    "ast": 0
                },
                {
                    "pts": 1,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 16,
                    "reb": 13,
                    "ast": 1
                }
            ],
            "min_avg": 18.1,
            "min_l10": 20.0,
            "edges": {
                "pts": 3.8,
                "reb": 3.8,
                "ast": 1.5
            },
            "fd_line_cat": "R",
            "fd_line": 9.5,
            "note": "WAS #29 vs C pts | High O/U 243.5 \u2014 shootout potential"
        },
        {
            "name": "Svi Mykhailiuk",
            "team": "UTA",
            "opp": "WAS",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 14,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 27,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 7,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 6,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 3,
                    "reb": 0,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 3,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 4,
                    "reb": 1,
                    "ast": 1
                }
            ],
            "min_avg": 20.5,
            "min_l10": 19.6,
            "edges": {
                "pts": 3.8,
                "reb": 1.0,
                "ast": 3.8
            },
            "fd_line_cat": "PRA",
            "fd_line": 11.0,
            "note": "WAS #29 vs SG pts | High O/U 243.5 \u2014 shootout potential"
        },
        {
            "name": "Trae Young",
            "team": "WAS",
            "opp": "UTA",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 36,
                    "reb": 3,
                    "ast": 11
                },
                {
                    "pts": 24,
                    "reb": 1,
                    "ast": 12
                },
                {
                    "pts": 28,
                    "reb": 1,
                    "ast": 10
                },
                {
                    "pts": 23,
                    "reb": 5,
                    "ast": 15
                },
                {
                    "pts": 16,
                    "reb": 1,
                    "ast": 9
                },
                {
                    "pts": 25,
                    "reb": 4,
                    "ast": 12
                },
                {
                    "pts": 29,
                    "reb": 4,
                    "ast": 15
                },
                {
                    "pts": 19,
                    "reb": 3,
                    "ast": 19
                },
                {
                    "pts": 29,
                    "reb": 2,
                    "ast": 12
                },
                {
                    "pts": 19,
                    "reb": 2,
                    "ast": 12
                }
            ],
            "min_avg": 36.0,
            "min_l10": 36.1,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "PA",
            "fd_line": 36.0,
            "note": "High O/U 243.5 \u2014 shootout potential"
        },
        {
            "name": "Bilal Coulibaly",
            "team": "WAS",
            "opp": "UTA",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 4,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 18,
                    "reb": 10,
                    "ast": 4
                },
                {
                    "pts": 11,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 17,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 16,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 20,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 2,
                    "ast": 6
                },
                {
                    "pts": 7,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 3,
                    "reb": 5,
                    "ast": 8
                }
            ],
            "min_avg": 33.0,
            "min_l10": 31.2,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 10.5,
            "note": "Bounce-back (7 PRA last game vs 19 avg) | High O/U 243.5 \u2014 shootout potential"
        },
        {
            "name": "Justin Champagnie",
            "team": "WAS",
            "opp": "UTA",
            "pos": "PF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 27,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 22,
                    "reb": 14,
                    "ast": 1
                },
                {
                    "pts": 14,
                    "reb": 12,
                    "ast": 1
                },
                {
                    "pts": 20,
                    "reb": 13,
                    "ast": 0
                },
                {
                    "pts": 15,
                    "reb": 13,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 8,
                    "reb": 11,
                    "ast": 3
                },
                {
                    "pts": 5,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 9,
                    "reb": 9,
                    "ast": 1
                },
                {
                    "pts": 15,
                    "reb": 7,
                    "ast": 1
                }
            ],
            "min_avg": 24.0,
            "min_l10": 31.9,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "R",
            "fd_line": 8.5,
            "note": "Minutes trending up (24.0->31.9) | High O/U 243.5 \u2014 shootout potential"
        },
        {
            "name": "Jaden Hardy",
            "team": "WAS",
            "opp": "UTA",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 17,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 3,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 16,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 13,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 22,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 15,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 0,
                    "ast": 2
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 0
                }
            ],
            "min_avg": 17.5,
            "min_l10": 18.7,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 10.0,
            "note": "High O/U 243.5 \u2014 shootout potential"
        },
        {
            "name": "Anthony Gill",
            "team": "WAS",
            "opp": "UTA",
            "pos": "C",
            "role": "bench",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 0,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 4,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 10,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 4,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 10,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 0
                }
            ],
            "min_avg": 12.5,
            "min_l10": 18.2,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 9.5,
            "note": "Bounce-back (4 PRA last game vs 10 avg) | Minutes trending up (12.5->18.2) | High O/U 243.5 \u2014 shootout potential"
        }
    ],
    "BKN_MIA": [
        {
            "name": "Terance Mann",
            "team": "BKN",
            "opp": "MIA",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 19,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 5,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 14,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 4,
                    "ast": 5
                },
                {
                    "pts": 10,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 14,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 9,
                    "reb": 1,
                    "ast": 4
                },
                {
                    "pts": 14,
                    "reb": 1,
                    "ast": 1
                }
            ],
            "min_avg": 21.1,
            "min_l10": 22.9,
            "edges": {
                "pts": 1.5,
                "reb": 3.8,
                "ast": 1.5
            },
            "fd_line_cat": "PRA",
            "fd_line": 14.0,
            "note": "MIA #28 vs PG reb | O/U 226.5"
        },
        {
            "name": "Michael Porter Jr.",
            "team": "BKN",
            "opp": "MIA",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 19,
                    "reb": 7,
                    "ast": 0
                },
                {
                    "pts": 7,
                    "reb": 12,
                    "ast": 0
                },
                {
                    "pts": 21,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 15,
                    "reb": 6,
                    "ast": 4
                },
                {
                    "pts": 23,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 20,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 23,
                    "reb": 10,
                    "ast": 4
                },
                {
                    "pts": 16,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 17,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 17,
                    "reb": 5,
                    "ast": 3
                }
            ],
            "min_avg": 33.7,
            "min_l10": 33.5,
            "edges": {
                "pts": 1.5,
                "reb": 0.2,
                "ast": 0.2
            },
            "fd_line_cat": "PR",
            "fd_line": 24.0,
            "note": "O/U 226.5"
        },
        {
            "name": "Noah Clowney",
            "team": "BKN",
            "opp": "MIA",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 13,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 5,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 1,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 12,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 19,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 1,
                    "ast": 0
                }
            ],
            "min_avg": 22.7,
            "min_l10": 20.2,
            "edges": {
                "pts": 3.8,
                "reb": 3.8,
                "ast": 2.2
            },
            "fd_line_cat": "PRA",
            "fd_line": 12.0,
            "note": "MIA #27 vs PF pts | O/U 226.5"
        },
        {
            "name": "Nic Claxton",
            "team": "BKN",
            "opp": "MIA",
            "pos": "C",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 7,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 18,
                    "reb": 6,
                    "ast": 5
                },
                {
                    "pts": 6,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 6,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 22,
                    "reb": 11,
                    "ast": 1
                },
                {
                    "pts": 19,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 10,
                    "ast": 4
                },
                {
                    "pts": 6,
                    "reb": 14,
                    "ast": 0
                }
            ],
            "min_avg": 26.9,
            "min_l10": 24.8,
            "edges": {
                "pts": 0.5,
                "reb": 3.0,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 11.5,
            "note": "Bounce-back (14 PRA last game vs 21 avg) | MIA #25 vs C reb | O/U 226.5"
        },
        {
            "name": "Day'Ron Sharpe",
            "team": "BKN",
            "opp": "MIA",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 10,
                    "reb": 7,
                    "ast": 4
                },
                {
                    "pts": 2,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 9,
                    "reb": 7,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 9,
                    "reb": 16,
                    "ast": 5
                },
                {
                    "pts": 7,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 8,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 7,
                    "ast": 1
                },
                {
                    "pts": 4,
                    "reb": 3,
                    "ast": 1
                }
            ],
            "min_avg": 18.1,
            "min_l10": 20.1,
            "edges": {
                "pts": 0.5,
                "reb": 3.0,
                "ast": 1.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 16.0,
            "note": "MIA #25 vs C reb | O/U 226.5"
        },
        {
            "name": "Ziaire Williams",
            "team": "BKN",
            "opp": "MIA",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 9,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 9,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 11,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 22,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 15,
                    "reb": 4,
                    "ast": 0
                }
            ],
            "min_avg": 24.5,
            "min_l10": 23.6,
            "edges": {
                "pts": 1.0,
                "reb": 3.8,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 10.0,
            "note": "Bounce-back (10 PRA last game vs 14 avg) | MIA #30 vs SG reb | O/U 226.5"
        },
        {
            "name": "Jalen Wilson",
            "team": "BKN",
            "opp": "MIA",
            "pos": "PF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 18,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 14,
                    "reb": 9,
                    "ast": 3
                },
                {
                    "pts": 20,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 12,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 20,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 8,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 8,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 13,
                    "reb": 6,
                    "ast": 0
                }
            ],
            "min_avg": 25.7,
            "min_l10": 26.6,
            "edges": {
                "pts": 3.8,
                "reb": 3.8,
                "ast": 2.2
            },
            "fd_line_cat": "P",
            "fd_line": 12.5,
            "note": "MIA #27 vs PF pts | O/U 226.5"
        },
        {
            "name": "Ochai Agbaji",
            "team": "BKN",
            "opp": "MIA",
            "pos": "SF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 14,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 24,
                    "reb": 6,
                    "ast": 0
                },
                {
                    "pts": 15,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 15,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 9,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 8,
                    "ast": 2
                },
                {
                    "pts": 9,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 2,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 19,
                    "reb": 3,
                    "ast": 2
                }
            ],
            "min_avg": 27.7,
            "min_l10": 28.3,
            "edges": {
                "pts": 1.5,
                "reb": 0.2,
                "ast": 0.2
            },
            "fd_line_cat": "P",
            "fd_line": 12.5,
            "note": "O/U 226.5"
        },
        {
            "name": "Davion Mitchell",
            "team": "MIA",
            "opp": "BKN",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 4,
                    "reb": 4,
                    "ast": 8
                },
                {
                    "pts": 11,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 17,
                    "reb": 3,
                    "ast": 8
                },
                {
                    "pts": 12,
                    "reb": 4,
                    "ast": 9
                },
                {
                    "pts": 20,
                    "reb": 2,
                    "ast": 5
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 7
                },
                {
                    "pts": 13,
                    "reb": 4,
                    "ast": 7
                },
                {
                    "pts": 6,
                    "reb": 1,
                    "ast": 8
                },
                {
                    "pts": 16,
                    "reb": 2,
                    "ast": 6
                },
                {
                    "pts": 12,
                    "reb": 5,
                    "ast": 7
                }
            ],
            "min_avg": 27.8,
            "min_l10": 32.3,
            "edges": {
                "pts": 0.0,
                "reb": 1.0,
                "ast": 2.2
            },
            "fd_line_cat": "A",
            "fd_line": 6.5,
            "note": "Bounce-back (16 PRA last game vs 22 avg) | Minutes trending up (27.8->32.3) | O/U 226.5"
        },
        {
            "name": "Tyler Herro",
            "team": "MIA",
            "opp": "BKN",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 22,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 30,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 20,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 35,
                    "reb": 9,
                    "ast": 4
                },
                {
                    "pts": 25,
                    "reb": 6,
                    "ast": 9
                },
                {
                    "pts": 27,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 30,
                    "reb": 3,
                    "ast": 7
                },
                {
                    "pts": 36,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 20,
                    "reb": 3,
                    "ast": 7
                },
                {
                    "pts": 29,
                    "reb": 6,
                    "ast": 3
                }
            ],
            "min_avg": 35.4,
            "min_l10": 34.7,
            "edges": {
                "pts": 0.0,
                "reb": 1.0,
                "ast": 2.2
            },
            "fd_line_cat": "P",
            "fd_line": 26.5,
            "note": "O/U 226.5"
        },
        {
            "name": "Pelle Larsson",
            "team": "MIA",
            "opp": "BKN",
            "pos": "SG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 12,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 3,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 16,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 15,
                    "reb": 7,
                    "ast": 5
                },
                {
                    "pts": 14,
                    "reb": 6,
                    "ast": 4
                },
                {
                    "pts": 3,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 4,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 0,
                    "ast": 0
                }
            ],
            "min_avg": 17.5,
            "min_l10": 22.9,
            "edges": {
                "pts": 0.5,
                "reb": 0.2,
                "ast": 1.5
            },
            "fd_line_cat": "PRA",
            "fd_line": 12.5,
            "note": "Minutes trending up (17.5->22.9) | O/U 226.5"
        },
        {
            "name": "Andrew Wiggins",
            "team": "MIA",
            "opp": "BKN",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 10,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 14,
                    "reb": 6,
                    "ast": 5
                },
                {
                    "pts": 16,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 10,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 42,
                    "reb": 3,
                    "ast": 5
                },
                {
                    "pts": 30,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 8,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 23,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 22,
                    "reb": 3,
                    "ast": 5
                },
                {
                    "pts": 19,
                    "reb": 7,
                    "ast": 2
                }
            ],
            "min_avg": 30.7,
            "min_l10": 30.6,
            "edges": {
                "pts": 2.2,
                "reb": 2.2,
                "ast": 0.5
            },
            "fd_line_cat": "P",
            "fd_line": 18.5,
            "note": "Bounce-back (18 PRA last game vs 27 avg) | O/U 226.5"
        },
        {
            "name": "Bam Adebayo",
            "team": "MIA",
            "opp": "BKN",
            "pos": "C",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 23,
                    "reb": 12,
                    "ast": 4
                },
                {
                    "pts": 18,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 31,
                    "reb": 12,
                    "ast": 5
                },
                {
                    "pts": 26,
                    "reb": 7,
                    "ast": 5
                },
                {
                    "pts": 21,
                    "reb": 5,
                    "ast": 6
                },
                {
                    "pts": 28,
                    "reb": 12,
                    "ast": 5
                },
                {
                    "pts": 16,
                    "reb": 7,
                    "ast": 5
                },
                {
                    "pts": 12,
                    "reb": 10,
                    "ast": 4
                },
                {
                    "pts": 27,
                    "reb": 8,
                    "ast": 1
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 2
                }
            ],
            "min_avg": 34.3,
            "min_l10": 32.8,
            "edges": {
                "pts": 2.2,
                "reb": 0.0,
                "ast": 0.2
            },
            "fd_line_cat": "P",
            "fd_line": 20.5,
            "note": "O/U 226.5"
        },
        {
            "name": "Jaime Jaquez",
            "team": "MIA",
            "opp": "BKN",
            "pos": "SF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 41,
                    "reb": 10,
                    "ast": 7
                },
                {
                    "pts": 11,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 5,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 0,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 4,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 11,
                    "ast": 7
                },
                {
                    "pts": 13,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 13,
                    "reb": 5,
                    "ast": 3
                }
            ],
            "min_avg": 21.7,
            "min_l10": 23.1,
            "edges": {
                "pts": 2.2,
                "reb": 0.5,
                "ast": 3.8
            },
            "fd_line_cat": "P",
            "fd_line": 11.0,
            "note": "BKN #27 vs SF ast | O/U 226.5"
        },
        {
            "name": "Kel'el Ware",
            "team": "MIA",
            "opp": "BKN",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 13,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 11,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 7,
                    "ast": 1
                },
                {
                    "pts": 19,
                    "reb": 17,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 15,
                    "ast": 0
                },
                {
                    "pts": 7,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 11,
                    "ast": 0
                },
                {
                    "pts": 13,
                    "reb": 14,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 12,
                    "ast": 0
                }
            ],
            "min_avg": 23.5,
            "min_l10": 26.6,
            "edges": {
                "pts": 2.2,
                "reb": 0.0,
                "ast": 0.2
            },
            "fd_line_cat": "R",
            "fd_line": 10.0,
            "note": "O/U 226.5"
        },
        {
            "name": "Dru Smith",
            "team": "MIA",
            "opp": "BKN",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 13,
                    "reb": 0,
                    "ast": 4
                },
                {
                    "pts": 7,
                    "reb": 0,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 8,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 6,
                    "ast": 3
                }
            ],
            "min_avg": 21.9,
            "min_l10": 24.1,
            "edges": {
                "pts": 0.0,
                "reb": 1.0,
                "ast": 2.2
            },
            "fd_line_cat": "PRA",
            "fd_line": 13.0,
            "note": "Bounce-back (2 PRA last game vs 13 avg) | O/U 226.5"
        }
    ],
    "GSW_HOU": [
        {
            "name": "Brandin Podziemski",
            "team": "GSW",
            "opp": "HOU",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 21,
                    "reb": 8,
                    "ast": 4
                },
                {
                    "pts": 11,
                    "reb": 8,
                    "ast": 3
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 5
                },
                {
                    "pts": 24,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 21,
                    "reb": 6,
                    "ast": 4
                },
                {
                    "pts": 28,
                    "reb": 9,
                    "ast": 6
                },
                {
                    "pts": 30,
                    "reb": 9,
                    "ast": 6
                },
                {
                    "pts": 9,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 29,
                    "reb": 6,
                    "ast": 5
                },
                {
                    "pts": 11,
                    "reb": 6,
                    "ast": 2
                }
            ],
            "min_avg": 27.3,
            "min_l10": 31.7,
            "edges": {
                "pts": 0.0,
                "reb": 0.0,
                "ast": 0.2
            },
            "fd_line_cat": "P",
            "fd_line": 18.0,
            "note": "Usage boost +8% (Cryer OUT) | Minutes trending up (27.3->31.7)"
        },
        {
            "name": "De'Anthony Melton",
            "team": "GSW",
            "opp": "HOU",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 15,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 21,
                    "reb": 11,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 4
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 4
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 4
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 4
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 4
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 4
                }
            ],
            "min_avg": 20.2,
            "min_l10": 20.2,
            "edges": {
                "pts": 0.0,
                "reb": 0.0,
                "ast": 0.2
            },
            "fd_line_cat": "P",
            "fd_line": 11.0,
            "note": "Usage boost +8% (Cryer OUT)"
        },
        {
            "name": "Draymond Green",
            "team": "GSW",
            "opp": "HOU",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 15,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 3,
                    "reb": 8,
                    "ast": 5
                },
                {
                    "pts": 14,
                    "reb": 10,
                    "ast": 9
                },
                {
                    "pts": 5,
                    "reb": 2,
                    "ast": 4
                },
                {
                    "pts": 2,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 9,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 12,
                    "ast": 5
                },
                {
                    "pts": 14,
                    "reb": 11,
                    "ast": 13
                },
                {
                    "pts": 15,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 5,
                    "ast": 6
                }
            ],
            "min_avg": 29.5,
            "min_l10": 29.1,
            "edges": {
                "pts": 0.0,
                "reb": 0.0,
                "ast": 0.0
            },
            "fd_line_cat": "RA",
            "fd_line": 11.5,
            "note": "Usage boost +8% (Cryer OUT)"
        },
        {
            "name": "Al Horford",
            "team": "GSW",
            "opp": "HOU",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 14,
                    "reb": 12,
                    "ast": 0
                },
                {
                    "pts": 12,
                    "reb": 11,
                    "ast": 4
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 28,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 17,
                    "reb": 11,
                    "ast": 5
                },
                {
                    "pts": 15,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 10,
                    "ast": 2
                },
                {
                    "pts": 4,
                    "reb": 5,
                    "ast": 6
                },
                {
                    "pts": 10,
                    "reb": 10,
                    "ast": 5
                },
                {
                    "pts": 19,
                    "reb": 11,
                    "ast": 6
                }
            ],
            "min_avg": 27.7,
            "min_l10": 29.9,
            "edges": {
                "pts": 0.0,
                "reb": 0.0,
                "ast": 0.0
            },
            "fd_line_cat": "R",
            "fd_line": 8.5,
            "note": "Usage boost +8% (Cryer OUT)"
        },
        {
            "name": "Quinten Post",
            "team": "GSW",
            "opp": "HOU",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 0,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 10,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 2,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 9,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 7,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 16,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 3,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 1
                }
            ],
            "min_avg": 16.7,
            "min_l10": 15.9,
            "edges": {
                "pts": 0.2,
                "reb": 0.0,
                "ast": 2.2
            },
            "fd_line_cat": "PRA",
            "fd_line": 10.0,
            "note": "Usage boost +4% (Cryer OUT) | Bounce-back (3 PRA last game vs 10 avg)"
        },
        {
            "name": "Amen Thompson",
            "team": "HOU",
            "opp": "GSW",
            "pos": "PG",
            "role": "starter",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 16,
                    "reb": 6,
                    "ast": 6
                },
                {
                    "pts": 15,
                    "reb": 6,
                    "ast": 6
                },
                {
                    "pts": 17,
                    "reb": 9,
                    "ast": 6
                },
                {
                    "pts": 10,
                    "reb": 4,
                    "ast": 5
                },
                {
                    "pts": 22,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 13,
                    "reb": 11,
                    "ast": 10
                },
                {
                    "pts": 16,
                    "reb": 11,
                    "ast": 5
                },
                {
                    "pts": 12,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 19,
                    "reb": 10,
                    "ast": 5
                },
                {
                    "pts": 16,
                    "reb": 10,
                    "ast": 12
                }
            ],
            "min_avg": 32.2,
            "min_l10": 30.7,
            "edges": {
                "pts": 3.8,
                "reb": 0.2,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 15.0,
            "note": "Usage boost +8% (Smith OUT) | GSW #27 vs PG pts"
        },
        {
            "name": "Tari Eason",
            "team": "HOU",
            "opp": "GSW",
            "pos": "SG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 8,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 18,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 4,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 5,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 16,
                    "reb": 10,
                    "ast": 3
                },
                {
                    "pts": 14,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 16,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 15,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 7,
                    "reb": 8,
                    "ast": 2
                }
            ],
            "min_avg": 24.9,
            "min_l10": 22.6,
            "edges": {
                "pts": 1.5,
                "reb": 1.0,
                "ast": 1.5
            },
            "fd_line_cat": "P",
            "fd_line": 10.0,
            "note": "Usage boost +6% (Smith OUT)"
        },
        {
            "name": "Kevin Durant",
            "team": "HOU",
            "opp": "GSW",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 12,
                    "reb": 7,
                    "ast": 1
                },
                {
                    "pts": 24,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 32,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 40,
                    "reb": 8,
                    "ast": 5
                },
                {
                    "pts": 45,
                    "reb": 6,
                    "ast": 8
                },
                {
                    "pts": 28,
                    "reb": 4,
                    "ast": 8
                },
                {
                    "pts": 15,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 22,
                    "reb": 10,
                    "ast": 2
                },
                {
                    "pts": 23,
                    "reb": 4,
                    "ast": 6
                },
                {
                    "pts": 20,
                    "reb": 7,
                    "ast": 0
                }
            ],
            "min_avg": 36.6,
            "min_l10": 33.5,
            "edges": {
                "pts": 0.0,
                "reb": 1.0,
                "ast": 3.0
            },
            "fd_line_cat": "P",
            "fd_line": 25.0,
            "note": "Usage boost +6% (Smith OUT) | Bounce-back (20 PRA last game vs 36 avg) | GSW #24 vs SF ast"
        },
        {
            "name": "Alperen Sengun",
            "team": "HOU",
            "opp": "GSW",
            "pos": "C",
            "role": "starter",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 15,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 20,
                    "reb": 15,
                    "ast": 4
                },
                {
                    "pts": 33,
                    "reb": 2,
                    "ast": 4
                },
                {
                    "pts": 16,
                    "reb": 15,
                    "ast": 10
                },
                {
                    "pts": 15,
                    "reb": 7,
                    "ast": 6
                },
                {
                    "pts": 17,
                    "reb": 10,
                    "ast": 3
                },
                {
                    "pts": 35,
                    "reb": 11,
                    "ast": 2
                },
                {
                    "pts": 19,
                    "reb": 10,
                    "ast": 5
                },
                {
                    "pts": 18,
                    "reb": 15,
                    "ast": 11
                },
                {
                    "pts": 8,
                    "reb": 11,
                    "ast": 2
                }
            ],
            "min_avg": 31.9,
            "min_l10": 32.5,
            "edges": {
                "pts": 1.0,
                "reb": 3.8,
                "ast": 3.8
            },
            "fd_line_cat": "R",
            "fd_line": 9.5,
            "note": "Usage boost +6% (Smith OUT) | Bounce-back (24 PRA last game vs 35 avg) | GSW #29 vs C reb"
        },
        {
            "name": "Reed Sheppard",
            "team": "HOU",
            "opp": "GSW",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 7
                },
                {
                    "pts": 14,
                    "reb": 3,
                    "ast": 5
                },
                {
                    "pts": 20,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 15,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 2,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 4,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 25,
                    "reb": 2,
                    "ast": 5
                },
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 0,
                    "ast": 0
                }
            ],
            "min_avg": 13.4,
            "min_l10": 18.8,
            "edges": {
                "pts": 3.8,
                "reb": 0.2,
                "ast": 0.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 14.0,
            "note": "Usage boost +0% (Smith OUT) | Bounce-back (8 PRA last game vs 14 avg) | Minutes trending up (13.4->18.8) | GSW #27 vs PG pts"
        },
        {
            "name": "Dorian Finney-Smith",
            "team": "HOU",
            "opp": "GSW",
            "pos": "SF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 18,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 5,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 5,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 20,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 11,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 3,
                    "ast": 1
                }
            ],
            "min_avg": 28.9,
            "min_l10": 31.4,
            "edges": {
                "pts": 0.0,
                "reb": 1.0,
                "ast": 3.0
            },
            "fd_line_cat": "P",
            "fd_line": 9.5,
            "note": "Usage boost +0% (Smith OUT) | GSW #24 vs SF ast"
        },
        {
            "name": "Clint Capela",
            "team": "HOU",
            "opp": "GSW",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 4,
                    "reb": 9,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 9,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 8,
                    "reb": 8,
                    "ast": 1
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 11,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 7,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 4,
                    "ast": 1
                }
            ],
            "min_avg": 21.5,
            "min_l10": 16.7,
            "edges": {
                "pts": 1.0,
                "reb": 3.8,
                "ast": 3.8
            },
            "fd_line_cat": "PRA",
            "fd_line": 13.0,
            "note": "Usage boost +0% (Smith OUT) | GSW #29 vs C reb"
        },
        {
            "name": "Josh Okogie",
            "team": "HOU",
            "opp": "GSW",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 14,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 7,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 5,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 9,
                    "reb": 2,
                    "ast": 2
                }
            ],
            "min_avg": 17.5,
            "min_l10": 16.7,
            "edges": {
                "pts": 1.5,
                "reb": 1.0,
                "ast": 1.5
            },
            "fd_line_cat": "PRA",
            "fd_line": 11.0,
            "note": "Usage boost +0% (Smith OUT)"
        }
    ],
    "TOR_MIN": [
        {
            "name": "Immanuel Quickley",
            "team": "TOR",
            "opp": "MIN",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 8,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 14,
                    "reb": 8,
                    "ast": 8
                },
                {
                    "pts": 17,
                    "reb": 1,
                    "ast": 9
                },
                {
                    "pts": 19,
                    "reb": 1,
                    "ast": 9
                },
                {
                    "pts": 21,
                    "reb": 4,
                    "ast": 7
                },
                {
                    "pts": 21,
                    "reb": 4,
                    "ast": 8
                },
                {
                    "pts": 15,
                    "reb": 7,
                    "ast": 7
                },
                {
                    "pts": 20,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 15,
                    "reb": 6,
                    "ast": 6
                },
                {
                    "pts": 34,
                    "reb": 5,
                    "ast": 5
                }
            ],
            "min_avg": 27.7,
            "min_l10": 26.3,
            "edges": {
                "pts": 3.0,
                "reb": 3.0,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 17.5,
            "note": "Bounce-back (11 PRA last game vs 29 avg) | MIN #25 vs PG pts | O/U 226.5"
        },
        {
            "name": "RJ Barrett",
            "team": "TOR",
            "opp": "MIN",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 11,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 18,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 31,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 15,
                    "reb": 6,
                    "ast": 5
                },
                {
                    "pts": 18,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 17,
                    "reb": 2,
                    "ast": 5
                },
                {
                    "pts": 14,
                    "reb": 10,
                    "ast": 8
                },
                {
                    "pts": 23,
                    "reb": 9,
                    "ast": 3
                },
                {
                    "pts": 21,
                    "reb": 8,
                    "ast": 9
                }
            ],
            "min_avg": 32.2,
            "min_l10": 26.8,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 0.5
            },
            "fd_line_cat": "P",
            "fd_line": 17.5,
            "note": "Bounce-back (13 PRA last game vs 28 avg) | O/U 226.5"
        },
        {
            "name": "Brandon Ingram",
            "team": "TOR",
            "opp": "MIN",
            "pos": "SG",
            "role": "starter",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 5,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 29,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 18,
                    "reb": 3,
                    "ast": 7
                },
                {
                    "pts": 17,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 32,
                    "reb": 4,
                    "ast": 8
                },
                {
                    "pts": 29,
                    "reb": 9,
                    "ast": 7
                },
                {
                    "pts": 18,
                    "reb": 6,
                    "ast": 6
                },
                {
                    "pts": 24,
                    "reb": 5,
                    "ast": 9
                },
                {
                    "pts": 11,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 20,
                    "reb": 5,
                    "ast": 5
                }
            ],
            "min_avg": 33.0,
            "min_l10": 33.5,
            "edges": {
                "pts": 0.0,
                "reb": 0.0,
                "ast": 0.2
            },
            "fd_line_cat": "P",
            "fd_line": 19.5,
            "note": "Bounce-back (9 PRA last game vs 31 avg) | O/U 226.5"
        },
        {
            "name": "Scottie Barnes",
            "team": "TOR",
            "opp": "MIN",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 35,
                    "reb": 11,
                    "ast": 8
                },
                {
                    "pts": 26,
                    "reb": 9,
                    "ast": 3
                },
                {
                    "pts": 17,
                    "reb": 11,
                    "ast": 5
                },
                {
                    "pts": 5,
                    "reb": 2,
                    "ast": 5
                },
                {
                    "pts": 9,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 9,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 18,
                    "reb": 6,
                    "ast": 6
                },
                {
                    "pts": 15,
                    "reb": 7,
                    "ast": 5
                },
                {
                    "pts": 13,
                    "reb": 10,
                    "ast": 8
                },
                {
                    "pts": 22,
                    "reb": 6,
                    "ast": 6
                }
            ],
            "min_avg": 32.9,
            "min_l10": 28.0,
            "edges": {
                "pts": 0.0,
                "reb": 1.0,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 16.0,
            "note": "O/U 226.5"
        },
        {
            "name": "Jakob Poeltl",
            "team": "TOR",
            "opp": "MIN",
            "pos": "C",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 10,
                    "reb": 11,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 24,
                    "reb": 12,
                    "ast": 3
                },
                {
                    "pts": 21,
                    "reb": 11,
                    "ast": 1
                },
                {
                    "pts": 18,
                    "reb": 8,
                    "ast": 2
                },
                {
                    "pts": 19,
                    "reb": 8,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 21,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 17,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 16,
                    "reb": 11,
                    "ast": 3
                }
            ],
            "min_avg": 29.6,
            "min_l10": 25.1,
            "edges": {
                "pts": 2.2,
                "reb": 0.0,
                "ast": 3.0
            },
            "fd_line_cat": "R",
            "fd_line": 8.0,
            "note": "MIN #25 vs C ast | O/U 226.5"
        },
        {
            "name": "Jamal Shead",
            "team": "TOR",
            "opp": "MIN",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 9
                },
                {
                    "pts": 9,
                    "reb": 0,
                    "ast": 5
                },
                {
                    "pts": 9,
                    "reb": 4,
                    "ast": 12
                },
                {
                    "pts": 14,
                    "reb": 1,
                    "ast": 9
                },
                {
                    "pts": 10,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 0,
                    "ast": 5
                },
                {
                    "pts": 11,
                    "reb": 2,
                    "ast": 9
                },
                {
                    "pts": 17,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 7,
                    "reb": 5,
                    "ast": 8
                },
                {
                    "pts": 14,
                    "reb": 2,
                    "ast": 3
                }
            ],
            "min_avg": 19.7,
            "min_l10": 26.3,
            "edges": {
                "pts": 3.0,
                "reb": 3.0,
                "ast": 1.0
            },
            "fd_line_cat": "A",
            "fd_line": 6.5,
            "note": "Minutes trending up (19.7->26.3) | MIN #25 vs PG pts | O/U 226.5"
        },
        {
            "name": "Ja'Kobe Walter",
            "team": "TOR",
            "opp": "MIN",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 8,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 22,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 9,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 17,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 17,
                    "reb": 8,
                    "ast": 4
                },
                {
                    "pts": 11,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 11,
                    "reb": 2,
                    "ast": 6
                },
                {
                    "pts": 10,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 14,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 17,
                    "reb": 3,
                    "ast": 0
                }
            ],
            "min_avg": 21.6,
            "min_l10": 27.2,
            "edges": {
                "pts": 3.0,
                "reb": 3.0,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 13.0,
            "note": "Bounce-back (15 PRA last game vs 20 avg) | Minutes trending up (21.6->27.2) | MIN #25 vs PG pts | O/U 226.5"
        },
        {
            "name": "Sandro Mamukelashvili",
            "team": "TOR",
            "opp": "MIN",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 12,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 19,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 8,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 0,
                    "ast": 2
                },
                {
                    "pts": 5,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 16,
                    "reb": 10,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 14,
                    "reb": 11,
                    "ast": 4
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 0
                }
            ],
            "min_avg": 13.0,
            "min_l10": 19.9,
            "edges": {
                "pts": 2.2,
                "reb": 0.0,
                "ast": 3.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 15.0,
            "note": "Minutes trending up (13.0->19.9) | MIN #25 vs C ast | O/U 226.5"
        },
        {
            "name": "Jamison Battle",
            "team": "TOR",
            "opp": "MIN",
            "pos": "SF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 25,
                    "reb": 9,
                    "ast": 3
                },
                {
                    "pts": 11,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 9,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 9,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 16,
                    "reb": 7,
                    "ast": 1
                },
                {
                    "pts": 2,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 10,
                    "ast": 0
                }
            ],
            "min_avg": 19.3,
            "min_l10": 28.4,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 0.5
            },
            "fd_line_cat": "P",
            "fd_line": 10.5,
            "note": "Minutes trending up (19.3->28.4) | O/U 226.5"
        },
        {
            "name": "Gradey Dick",
            "team": "TOR",
            "opp": "MIN",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 13,
                    "reb": 9,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 12,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 9,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 10,
                    "ast": 1
                },
                {
                    "pts": 2,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 17,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 17,
                    "reb": 7,
                    "ast": 1
                }
            ],
            "min_avg": 29.5,
            "min_l10": 27.1,
            "edges": {
                "pts": 0.0,
                "reb": 0.0,
                "ast": 0.2
            },
            "fd_line_cat": "PRA",
            "fd_line": 14.5,
            "note": "Bounce-back (3 PRA last game vs 15 avg) | O/U 226.5"
        },
        {
            "name": "Garrett Temple",
            "team": "TOR",
            "opp": "MIN",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 12,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 8,
                    "reb": 2,
                    "ast": 8
                },
                {
                    "pts": 0,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 0,
                    "ast": 0
                }
            ],
            "min_avg": 13.7,
            "min_l10": 16.1,
            "edges": {
                "pts": 0.0,
                "reb": 0.0,
                "ast": 0.2
            },
            "fd_line_cat": "PRA",
            "fd_line": 7.5,
            "note": "Minutes trending up (13.7->16.1) | O/U 226.5"
        },
        {
            "name": "Jonathan Mogbo",
            "team": "TOR",
            "opp": "MIN",
            "pos": "PF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 9,
                    "reb": 14,
                    "ast": 10
                },
                {
                    "pts": 8,
                    "reb": 8,
                    "ast": 8
                },
                {
                    "pts": 17,
                    "reb": 10,
                    "ast": 11
                },
                {
                    "pts": 17,
                    "reb": 11,
                    "ast": 7
                },
                {
                    "pts": 6,
                    "reb": 8,
                    "ast": 0
                },
                {
                    "pts": 10,
                    "reb": 3,
                    "ast": 5
                },
                {
                    "pts": 6,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 13,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 5,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 16,
                    "reb": 7,
                    "ast": 5
                }
            ],
            "min_avg": 20.7,
            "min_l10": 30.3,
            "edges": {
                "pts": 0.0,
                "reb": 1.0,
                "ast": 0.0
            },
            "fd_line_cat": "RA",
            "fd_line": 12.5,
            "note": "Minutes trending up (20.7->30.3) | O/U 226.5"
        },
        {
            "name": "Donte DiVincenzo",
            "team": "MIN",
            "opp": "TOR",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 16,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 6,
                    "ast": 4
                },
                {
                    "pts": 9,
                    "reb": 0,
                    "ast": 4
                },
                {
                    "pts": 24,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 13,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 13,
                    "reb": 2,
                    "ast": 5
                },
                {
                    "pts": 9,
                    "reb": 9,
                    "ast": 4
                },
                {
                    "pts": 13,
                    "reb": 1,
                    "ast": 3
                }
            ],
            "min_avg": 25.9,
            "min_l10": 22.4,
            "edges": {
                "pts": 3.0,
                "reb": 0.2,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 11.0,
            "note": "TOR #26 vs PG pts | O/U 226.5"
        },
        {
            "name": "Anthony Edwards",
            "team": "MIN",
            "opp": "TOR",
            "pos": "SG",
            "role": "starter",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 43,
                    "reb": 6,
                    "ast": 5
                },
                {
                    "pts": 9,
                    "reb": 4,
                    "ast": 5
                },
                {
                    "pts": 44,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 25,
                    "reb": 7,
                    "ast": 4
                },
                {
                    "pts": 37,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 28,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 34,
                    "reb": 10,
                    "ast": 8
                },
                {
                    "pts": 25,
                    "reb": 6,
                    "ast": 4
                },
                {
                    "pts": 20,
                    "reb": 4,
                    "ast": 5
                },
                {
                    "pts": 17,
                    "reb": 2,
                    "ast": 4
                }
            ],
            "min_avg": 36.3,
            "min_l10": 36.6,
            "edges": {
                "pts": 0.5,
                "reb": 0.0,
                "ast": 2.2
            },
            "fd_line_cat": "P",
            "fd_line": 27.0,
            "note": "O/U 226.5"
        },
        {
            "name": "Jaden McDaniels",
            "team": "MIN",
            "opp": "TOR",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 8,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 11,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 2,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 6,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 9,
                    "ast": 3
                },
                {
                    "pts": 16,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 1,
                    "ast": 1
                }
            ],
            "min_avg": 31.9,
            "min_l10": 29.9,
            "edges": {
                "pts": 0.0,
                "reb": 0.2,
                "ast": 0.2
            },
            "fd_line_cat": "PRA",
            "fd_line": 13.5,
            "note": "Bounce-back (10 PRA last game vs 14 avg) | O/U 226.5"
        },
        {
            "name": "Julius Randle",
            "team": "MIN",
            "opp": "TOR",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 10,
                    "reb": 10,
                    "ast": 5
                },
                {
                    "pts": 21,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 31,
                    "reb": 10,
                    "ast": 5
                },
                {
                    "pts": 9,
                    "reb": 7,
                    "ast": 6
                },
                {
                    "pts": 15,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 11,
                    "reb": 8,
                    "ast": 4
                },
                {
                    "pts": 26,
                    "reb": 9,
                    "ast": 7
                },
                {
                    "pts": 26,
                    "reb": 8,
                    "ast": 5
                },
                {
                    "pts": 25,
                    "reb": 6,
                    "ast": 8
                },
                {
                    "pts": 9,
                    "reb": 6,
                    "ast": 2
                }
            ],
            "min_avg": 32.3,
            "min_l10": 33.1,
            "edges": {
                "pts": 0.2,
                "reb": 0.5,
                "ast": 0.2
            },
            "fd_line_cat": "P",
            "fd_line": 17.5,
            "note": "O/U 226.5"
        },
        {
            "name": "Rudy Gobert",
            "team": "MIN",
            "opp": "TOR",
            "pos": "C",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 19,
                    "reb": 18,
                    "ast": 0
                },
                {
                    "pts": 35,
                    "reb": 11,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 8,
                    "ast": 4
                },
                {
                    "pts": 6,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 23,
                    "reb": 19,
                    "ast": 2
                },
                {
                    "pts": 21,
                    "reb": 18,
                    "ast": 1
                },
                {
                    "pts": 19,
                    "reb": 12,
                    "ast": 1
                },
                {
                    "pts": 19,
                    "reb": 25,
                    "ast": 0
                },
                {
                    "pts": 17,
                    "reb": 13,
                    "ast": 1
                },
                {
                    "pts": 16,
                    "reb": 16,
                    "ast": 3
                }
            ],
            "min_avg": 33.2,
            "min_l10": 36.4,
            "edges": {
                "pts": 0.0,
                "reb": 1.0,
                "ast": 0.0
            },
            "fd_line_cat": "R",
            "fd_line": 14.5,
            "note": "O/U 226.5"
        },
        {
            "name": "Naz Reid",
            "team": "MIN",
            "opp": "TOR",
            "pos": "PF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 11,
                    "reb": 8,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 17,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 13,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 2,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 9,
                    "reb": 7,
                    "ast": 4
                },
                {
                    "pts": 20,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 15,
                    "reb": 5,
                    "ast": 6
                }
            ],
            "min_avg": 27.6,
            "min_l10": 24.0,
            "edges": {
                "pts": 0.2,
                "reb": 0.5,
                "ast": 0.2
            },
            "fd_line_cat": "P",
            "fd_line": 11.0,
            "note": "O/U 226.5"
        },
        {
            "name": "Ayo Dosunmu",
            "team": "MIN",
            "opp": "TOR",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 11,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 5,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 23,
                    "reb": 3,
                    "ast": 6
                },
                {
                    "pts": 8,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 1,
                    "ast": 4
                },
                {
                    "pts": 11,
                    "reb": 0,
                    "ast": 4
                },
                {
                    "pts": 21,
                    "reb": 2,
                    "ast": 9
                },
                {
                    "pts": 14,
                    "reb": 3,
                    "ast": 5
                },
                {
                    "pts": 6,
                    "reb": 4,
                    "ast": 8
                },
                {
                    "pts": 12,
                    "reb": 4,
                    "ast": 4
                }
            ],
            "min_avg": 30.3,
            "min_l10": 30.0,
            "edges": {
                "pts": 0.5,
                "reb": 0.0,
                "ast": 2.2
            },
            "fd_line_cat": "P",
            "fd_line": 11.5,
            "note": "O/U 226.5"
        },
        {
            "name": "Kyle Anderson",
            "team": "MIN",
            "opp": "TOR",
            "pos": "PF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 6,
                    "reb": 6,
                    "ast": 4
                },
                {
                    "pts": 9,
                    "reb": 4,
                    "ast": 6
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 8,
                    "ast": 6
                },
                {
                    "pts": 12,
                    "reb": 14,
                    "ast": 3
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 19,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 6,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 2,
                    "ast": 4
                }
            ],
            "min_avg": 17.5,
            "min_l10": 23.6,
            "edges": {
                "pts": 0.2,
                "reb": 0.5,
                "ast": 0.2
            },
            "fd_line_cat": "PRA",
            "fd_line": 16.5,
            "note": "Minutes trending up (17.5->23.6) | O/U 226.5"
        },
        {
            "name": "Mike Conley",
            "team": "MIN",
            "opp": "TOR",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 0,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 8,
                    "reb": 2,
                    "ast": 9
                },
                {
                    "pts": 5,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 8,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 6,
                    "reb": 1,
                    "ast": 6
                },
                {
                    "pts": 9,
                    "reb": 1,
                    "ast": 8
                },
                {
                    "pts": 17,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 13,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 7,
                    "reb": 4,
                    "ast": 5
                }
            ],
            "min_avg": 24.7,
            "min_l10": 25.1,
            "edges": {
                "pts": 3.0,
                "reb": 0.2,
                "ast": 0.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 14.5,
            "note": "Bounce-back (4 PRA last game vs 15 avg) | TOR #26 vs PG pts | O/U 226.5"
        }
    ],
    "DET_SAS": [
        {
            "name": "Cade Cunningham",
            "team": "DET",
            "opp": "SAS",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 36,
                    "reb": 6,
                    "ast": 12
                },
                {
                    "pts": 36,
                    "reb": 2,
                    "ast": 8
                },
                {
                    "pts": 35,
                    "reb": 3,
                    "ast": 5
                },
                {
                    "pts": 25,
                    "reb": 9,
                    "ast": 4
                },
                {
                    "pts": 35,
                    "reb": 7,
                    "ast": 6
                },
                {
                    "pts": 25,
                    "reb": 12,
                    "ast": 11
                },
                {
                    "pts": 24,
                    "reb": 4,
                    "ast": 8
                },
                {
                    "pts": 11,
                    "reb": 7,
                    "ast": 9
                },
                {
                    "pts": 38,
                    "reb": 3,
                    "ast": 10
                },
                {
                    "pts": 27,
                    "reb": 8,
                    "ast": 10
                }
            ],
            "min_avg": 35.0,
            "min_l10": 33.5,
            "edges": {
                "pts": 1.0,
                "reb": 2.2,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 28.0,
            "note": "O/U 228.5"
        },
        {
            "name": "Duncan Robinson",
            "team": "DET",
            "opp": "SAS",
            "pos": "SG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 21,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 21,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 16,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 4,
                    "reb": 0,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 22,
                    "reb": 2,
                    "ast": 2
                }
            ],
            "min_avg": 24.1,
            "min_l10": 22.0,
            "edges": {
                "pts": 0.0,
                "reb": 1.5,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 11.0,
            "note": "Bounce-back (10 PRA last game vs 15 avg) | O/U 228.5"
        },
        {
            "name": "Ausar Thompson",
            "team": "DET",
            "opp": "SAS",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 11,
                    "reb": 7,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 15,
                    "reb": 4,
                    "ast": 5
                },
                {
                    "pts": 18,
                    "reb": 11,
                    "ast": 5
                },
                {
                    "pts": 15,
                    "reb": 7,
                    "ast": 4
                },
                {
                    "pts": 13,
                    "reb": 8,
                    "ast": 3
                },
                {
                    "pts": 14,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 18,
                    "reb": 10,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 5,
                    "reb": 1,
                    "ast": 1
                }
            ],
            "min_avg": 22.5,
            "min_l10": 27.2,
            "edges": {
                "pts": 0.0,
                "reb": 0.2,
                "ast": 1.0
            },
            "fd_line_cat": "PR",
            "fd_line": 18.0,
            "note": "Minutes trending up (22.5->27.2) | O/U 228.5"
        },
        {
            "name": "Tobias Harris",
            "team": "DET",
            "opp": "SAS",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 4,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 17,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 17,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 15,
                    "reb": 8,
                    "ast": 4
                },
                {
                    "pts": 14,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 9,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 13,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 9,
                    "reb": 6,
                    "ast": 0
                },
                {
                    "pts": 18,
                    "reb": 7,
                    "ast": 0
                }
            ],
            "min_avg": 31.6,
            "min_l10": 27.8,
            "edges": {
                "pts": 0.2,
                "reb": 0.0,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 12.0,
            "note": "Bounce-back (8 PRA last game vs 20 avg) | O/U 228.5"
        },
        {
            "name": "Jalen Duren",
            "team": "DET",
            "opp": "SAS",
            "pos": "C",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 4,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 16,
                    "ast": 5
                },
                {
                    "pts": 18,
                    "reb": 13,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 9,
                    "ast": 6
                },
                {
                    "pts": 21,
                    "reb": 18,
                    "ast": 6
                },
                {
                    "pts": 13,
                    "reb": 13,
                    "ast": 3
                },
                {
                    "pts": 13,
                    "reb": 11,
                    "ast": 3
                },
                {
                    "pts": 16,
                    "reb": 13,
                    "ast": 0
                },
                {
                    "pts": 14,
                    "reb": 4,
                    "ast": 7
                },
                {
                    "pts": 22,
                    "reb": 12,
                    "ast": 2
                }
            ],
            "min_avg": 26.1,
            "min_l10": 26.9,
            "edges": {
                "pts": 0.5,
                "reb": 1.5,
                "ast": 3.8
            },
            "fd_line_cat": "R",
            "fd_line": 10.5,
            "note": "Bounce-back (7 PRA last game vs 28 avg) | SAS #30 vs C ast | O/U 228.5"
        },
        {
            "name": "Isaiah Stewart",
            "team": "DET",
            "opp": "SAS",
            "pos": "PF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 10,
                    "ast": 4
                },
                {
                    "pts": 16,
                    "reb": 8,
                    "ast": 4
                },
                {
                    "pts": 0,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 14,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 4,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 9,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 5,
                    "ast": 1
                }
            ],
            "min_avg": 19.9,
            "min_l10": 20.7,
            "edges": {
                "pts": 0.2,
                "reb": 0.0,
                "ast": 1.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 14.0,
            "note": "Bounce-back (2 PRA last game vs 14 avg) | O/U 228.5"
        },
        {
            "name": "Ronald Holland II",
            "team": "DET",
            "opp": "SAS",
            "pos": "PF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 5,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 5,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 4,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 26,
                    "reb": 5,
                    "ast": 6
                }
            ],
            "min_avg": 15.7,
            "min_l10": 17.6,
            "edges": {
                "pts": 0.2,
                "reb": 0.0,
                "ast": 1.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 12.0,
            "note": "Bounce-back (6 PRA last game vs 12 avg) | O/U 228.5"
        },
        {
            "name": "Caris LeVert",
            "team": "DET",
            "opp": "SAS",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 31,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 4,
                    "reb": 3,
                    "ast": 5
                },
                {
                    "pts": 13,
                    "reb": 6,
                    "ast": 0
                },
                {
                    "pts": 21,
                    "reb": 5,
                    "ast": 6
                },
                {
                    "pts": 14,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 14,
                    "reb": 4,
                    "ast": 5
                },
                {
                    "pts": 10,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 9,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 17,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 5,
                    "reb": 1,
                    "ast": 0
                }
            ],
            "min_avg": 24.9,
            "min_l10": 24.9,
            "edges": {
                "pts": 1.0,
                "reb": 2.2,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 13.0,
            "note": "O/U 228.5"
        },
        {
            "name": "Kevin Huerter",
            "team": "DET",
            "opp": "SAS",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 18,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 4,
                    "ast": 6
                },
                {
                    "pts": 22,
                    "reb": 4,
                    "ast": 7
                },
                {
                    "pts": 13,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 9,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 16,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 6
                },
                {
                    "pts": 21,
                    "reb": 6,
                    "ast": 5
                },
                {
                    "pts": 9,
                    "reb": 1,
                    "ast": 6
                },
                {
                    "pts": 14,
                    "reb": 3,
                    "ast": 2
                }
            ],
            "min_avg": 24.3,
            "min_l10": 32.2,
            "edges": {
                "pts": 0.0,
                "reb": 1.5,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 13.0,
            "note": "Minutes trending up (24.3->32.2) | O/U 228.5"
        },
        {
            "name": "Marcus Sasser",
            "team": "DET",
            "opp": "SAS",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 18,
                    "reb": 1,
                    "ast": 10
                },
                {
                    "pts": 8,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 7,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 4,
                    "reb": 1,
                    "ast": 4
                },
                {
                    "pts": 27,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 20,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 0,
                    "ast": 3
                }
            ],
            "min_avg": 16.1,
            "min_l10": 18.0,
            "edges": {
                "pts": 1.0,
                "reb": 2.2,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 10.0,
            "note": "O/U 228.5"
        },
        {
            "name": "De'Aaron Fox",
            "team": "SAS",
            "opp": "DET",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 32,
                    "reb": 9,
                    "ast": 11
                },
                {
                    "pts": 14,
                    "reb": 4,
                    "ast": 8
                },
                {
                    "pts": 22,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 16,
                    "reb": 4,
                    "ast": 8
                },
                {
                    "pts": 15,
                    "reb": 3,
                    "ast": 7
                },
                {
                    "pts": 20,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 20,
                    "reb": 3,
                    "ast": 7
                },
                {
                    "pts": 7,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 15,
                    "reb": 3,
                    "ast": 9
                },
                {
                    "pts": 13,
                    "reb": 7,
                    "ast": 5
                }
            ],
            "min_avg": 36.2,
            "min_l10": 33.1,
            "edges": {
                "pts": 0.0,
                "reb": 0.5,
                "ast": 0.0
            },
            "fd_line_cat": "A",
            "fd_line": 6.0,
            "note": "O/U 228.5"
        },
        {
            "name": "Stephon Castle",
            "team": "SAS",
            "opp": "DET",
            "pos": "SG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 20,
                    "reb": 8,
                    "ast": 6
                },
                {
                    "pts": 16,
                    "reb": 4,
                    "ast": 10
                },
                {
                    "pts": 21,
                    "reb": 3,
                    "ast": 5
                },
                {
                    "pts": 19,
                    "reb": 1,
                    "ast": 8
                },
                {
                    "pts": 22,
                    "reb": 7,
                    "ast": 5
                },
                {
                    "pts": 22,
                    "reb": 9,
                    "ast": 11
                },
                {
                    "pts": 15,
                    "reb": 15,
                    "ast": 9
                },
                {
                    "pts": 16,
                    "reb": 8,
                    "ast": 6
                },
                {
                    "pts": 9,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 22,
                    "reb": 2,
                    "ast": 8
                }
            ],
            "min_avg": 26.7,
            "min_l10": 31.9,
            "edges": {
                "pts": 0.2,
                "reb": 0.0,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 17.5,
            "note": "Minutes trending up (26.7->31.9) | O/U 228.5"
        },
        {
            "name": "Devin Vassell",
            "team": "SAS",
            "opp": "DET",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 11,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 7,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 21,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 24,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 12,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 14,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 22,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 26,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 25,
                    "reb": 6,
                    "ast": 3
                }
            ],
            "min_avg": 31.0,
            "min_l10": 31.1,
            "edges": {
                "pts": 0.2,
                "reb": 0.0,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 16.5,
            "note": "O/U 228.5"
        },
        {
            "name": "Julian Champagnie",
            "team": "SAS",
            "opp": "DET",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 14,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 23,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 7,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 15,
                    "reb": 6,
                    "ast": 0
                },
                {
                    "pts": 14,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 19,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 1
                }
            ],
            "min_avg": 23.6,
            "min_l10": 27.0,
            "edges": {
                "pts": 0.2,
                "reb": 0.0,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 12.0,
            "note": "O/U 228.5"
        },
        {
            "name": "Victor Wembanyama",
            "team": "SAS",
            "opp": "DET",
            "pos": "C",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 17,
                    "reb": 13,
                    "ast": 4
                },
                {
                    "pts": 31,
                    "reb": 15,
                    "ast": 4
                },
                {
                    "pts": 18,
                    "reb": 9,
                    "ast": 4
                },
                {
                    "pts": 16,
                    "reb": 11,
                    "ast": 3
                },
                {
                    "pts": 24,
                    "reb": 12,
                    "ast": 2
                },
                {
                    "pts": 27,
                    "reb": 10,
                    "ast": 5
                },
                {
                    "pts": 30,
                    "reb": 14,
                    "ast": 1
                },
                {
                    "pts": 23,
                    "reb": 12,
                    "ast": 4
                },
                {
                    "pts": 20,
                    "reb": 12,
                    "ast": 2
                },
                {
                    "pts": 30,
                    "reb": 11,
                    "ast": 6
                }
            ],
            "min_avg": 33.2,
            "min_l10": 33.5,
            "edges": {
                "pts": 0.0,
                "reb": 0.2,
                "ast": 0.0
            },
            "fd_line_cat": "R",
            "fd_line": 11.5,
            "note": "O/U 228.5"
        },
        {
            "name": "Keldon Johnson",
            "team": "SAS",
            "opp": "DET",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 23,
                    "reb": 9,
                    "ast": 0
                },
                {
                    "pts": 21,
                    "reb": 8,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 7,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 7,
                    "reb": 7,
                    "ast": 4
                },
                {
                    "pts": 19,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 23,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 17,
                    "reb": 10,
                    "ast": 0
                },
                {
                    "pts": 10,
                    "reb": 5,
                    "ast": 3
                }
            ],
            "min_avg": 23.8,
            "min_l10": 24.7,
            "edges": {
                "pts": 0.2,
                "reb": 0.0,
                "ast": 0.0
            },
            "fd_line_cat": "PR",
            "fd_line": 19.5,
            "note": "O/U 228.5"
        },
        {
            "name": "Luke Kornet",
            "team": "SAS",
            "opp": "DET",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 11,
                    "reb": 8,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 2,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 14,
                    "ast": 3
                },
                {
                    "pts": 12,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 14,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 15,
                    "reb": 16,
                    "ast": 4
                },
                {
                    "pts": 2,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 13,
                    "reb": 8,
                    "ast": 3
                }
            ],
            "min_avg": 19.2,
            "min_l10": 22.9,
            "edges": {
                "pts": 0.0,
                "reb": 0.2,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 10.0,
            "note": "Minutes trending up (19.2->22.9) | O/U 228.5"
        },
        {
            "name": "Kelly Olynyk",
            "team": "SAS",
            "opp": "DET",
            "pos": "PF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 8,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 12,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 13,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 11,
                    "ast": 7
                },
                {
                    "pts": 10,
                    "reb": 5,
                    "ast": 8
                },
                {
                    "pts": 10,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 13,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 9,
                    "reb": 3,
                    "ast": 3
                }
            ],
            "min_avg": 20.3,
            "min_l10": 25.0,
            "edges": {
                "pts": 0.2,
                "reb": 0.2,
                "ast": 0.0
            },
            "fd_line_cat": "P",
            "fd_line": 10.5,
            "note": "Bounce-back (12 PRA last game vs 19 avg) | Minutes trending up (20.3->25.0) | O/U 228.5"
        },
        {
            "name": "Bismack Biyombo",
            "team": "SAS",
            "opp": "DET",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 2,
                    "reb": 7,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 8,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 8,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 10,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 7,
                    "ast": 0
                },
                {
                    "pts": 11,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 7,
                    "ast": 3
                }
            ],
            "min_avg": 19.5,
            "min_l10": 21.2,
            "edges": {
                "pts": 0.0,
                "reb": 0.2,
                "ast": 0.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 12.0,
            "note": "Bounce-back (9 PRA last game vs 13 avg) | O/U 228.5"
        }
    ],
    "CHI_PHX": [
        {
            "name": "Josh Giddey",
            "team": "CHI",
            "opp": "PHX",
            "pos": "PG",
            "role": "starter",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 28,
                    "reb": 16,
                    "ast": 11
                },
                {
                    "pts": 23,
                    "reb": 10,
                    "ast": 8
                },
                {
                    "pts": 15,
                    "reb": 19,
                    "ast": 12
                },
                {
                    "pts": 17,
                    "reb": 7,
                    "ast": 12
                },
                {
                    "pts": 15,
                    "reb": 8,
                    "ast": 10
                },
                {
                    "pts": 8,
                    "reb": 8,
                    "ast": 4
                },
                {
                    "pts": 25,
                    "reb": 14,
                    "ast": 11
                },
                {
                    "pts": 26,
                    "reb": 7,
                    "ast": 9
                },
                {
                    "pts": 15,
                    "reb": 10,
                    "ast": 17
                },
                {
                    "pts": 22,
                    "reb": 7,
                    "ast": 7
                }
            ],
            "min_avg": 30.2,
            "min_l10": 33.6,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 18.5,
            "note": "O/U 224.5"
        },
        {
            "name": "Tre Jones",
            "team": "CHI",
            "opp": "PHX",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 15,
                    "reb": 4,
                    "ast": 7
                },
                {
                    "pts": 12,
                    "reb": 6,
                    "ast": 9
                },
                {
                    "pts": 18,
                    "reb": 4,
                    "ast": 12
                },
                {
                    "pts": 19,
                    "reb": 2,
                    "ast": 6
                },
                {
                    "pts": 18,
                    "reb": 6,
                    "ast": 6
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 8
                },
                {
                    "pts": 15,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 20,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 9,
                    "reb": 8,
                    "ast": 7
                },
                {
                    "pts": 11,
                    "reb": 0,
                    "ast": 6
                }
            ],
            "min_avg": 19.7,
            "min_l10": 32.6,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "A",
            "fd_line": 6.5,
            "note": "Minutes trending up (19.7->32.6) | O/U 224.5"
        },
        {
            "name": "Isaac Okoro",
            "team": "CHI",
            "opp": "PHX",
            "pos": "SG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 15,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 7,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 11,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 7,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 9,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 2,
                    "reb": 4,
                    "ast": 3
                }
            ],
            "min_avg": 19.2,
            "min_l10": 21.1,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 12.5,
            "note": "O/U 224.5"
        },
        {
            "name": "Matas Buzelis",
            "team": "CHI",
            "opp": "PHX",
            "pos": "PF",
            "role": "starter",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 7,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 20,
                    "reb": 6,
                    "ast": 4
                },
                {
                    "pts": 17,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 19,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 10,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 12,
                    "reb": 12,
                    "ast": 1
                },
                {
                    "pts": 9,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 14,
                    "reb": 7,
                    "ast": 1
                },
                {
                    "pts": 28,
                    "reb": 9,
                    "ast": 6
                },
                {
                    "pts": 12,
                    "reb": 7,
                    "ast": 1
                }
            ],
            "min_avg": 20.4,
            "min_l10": 28.8,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "PR",
            "fd_line": 20.0,
            "note": "Bounce-back (11 PRA last game vs 23 avg) | Minutes trending up (20.4->28.8) | O/U 224.5"
        },
        {
            "name": "Guerschon Yabusele",
            "team": "CHI",
            "opp": "PHX",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 19,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 22,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 1,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 21,
                    "reb": 8,
                    "ast": 1
                },
                {
                    "pts": 12,
                    "reb": 7,
                    "ast": 4
                },
                {
                    "pts": 11,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 23,
                    "reb": 9,
                    "ast": 5
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 15,
                    "ast": 2
                }
            ],
            "min_avg": 27.0,
            "min_l10": 30.9,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "PR",
            "fd_line": 20.0,
            "note": "O/U 224.5"
        },
        {
            "name": "Collin Sexton",
            "team": "CHI",
            "opp": "PHX",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 15,
                    "reb": 0,
                    "ast": 5
                },
                {
                    "pts": 27,
                    "reb": 5,
                    "ast": 6
                },
                {
                    "pts": 27,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 18,
                    "reb": 0,
                    "ast": 4
                },
                {
                    "pts": 20,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 21,
                    "reb": 1,
                    "ast": 5
                },
                {
                    "pts": 15,
                    "reb": 3,
                    "ast": 5
                },
                {
                    "pts": 10,
                    "reb": 0,
                    "ast": 2
                },
                {
                    "pts": 30,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 18,
                    "reb": 3,
                    "ast": 5
                }
            ],
            "min_avg": 28.4,
            "min_l10": 26.8,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 19.5,
            "note": "Bounce-back (20 PRA last game vs 26 avg) | O/U 224.5"
        },
        {
            "name": "Nick Richards",
            "team": "CHI",
            "opp": "PHX",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 4,
                    "reb": 9,
                    "ast": 0
                },
                {
                    "pts": 5,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 7,
                    "ast": 0
                },
                {
                    "pts": 13,
                    "reb": 11,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 10,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 10,
                    "reb": 10,
                    "ast": 1
                },
                {
                    "pts": 18,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 4,
                    "ast": 1
                }
            ],
            "min_avg": 22.0,
            "min_l10": 21.9,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 14.5,
            "note": "O/U 224.5"
        }
    ],
    "LAL_DEN": [
        {
            "name": "Austin Reaves",
            "team": "LAL",
            "opp": "DEN",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 23,
                    "reb": 7,
                    "ast": 6
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 24,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 20,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 30,
                    "reb": 3,
                    "ast": 7
                },
                {
                    "pts": 31,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 12,
                    "reb": 8,
                    "ast": 3
                },
                {
                    "pts": 31,
                    "reb": 7,
                    "ast": 8
                },
                {
                    "pts": 30,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 24,
                    "reb": 4,
                    "ast": 5
                }
            ],
            "min_avg": 34.9,
            "min_l10": 36.8,
            "edges": {
                "pts": 0.2,
                "reb": 0.2,
                "ast": 0.5
            },
            "fd_line_cat": "P",
            "fd_line": 22.5,
            "note": "High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Marcus Smart",
            "team": "LAL",
            "opp": "DEN",
            "pos": "SG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 12,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 3,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 17,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 0,
                    "reb": 0,
                    "ast": 4
                },
                {
                    "pts": 15,
                    "reb": 4,
                    "ast": 7
                },
                {
                    "pts": 16,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 9,
                    "reb": 1,
                    "ast": 4
                },
                {
                    "pts": 13,
                    "reb": 4,
                    "ast": 5
                }
            ],
            "min_avg": 20.0,
            "min_l10": 18.3,
            "edges": {
                "pts": 1.0,
                "reb": 0.0,
                "ast": 0.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 14.0,
            "note": "High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "LeBron James",
            "team": "LAL",
            "opp": "DEN",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 14,
                    "reb": 4,
                    "ast": 8
                },
                {
                    "pts": 27,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 28,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 19,
                    "reb": 3,
                    "ast": 7
                },
                {
                    "pts": 27,
                    "reb": 0,
                    "ast": 8
                },
                {
                    "pts": 33,
                    "reb": 5,
                    "ast": 9
                },
                {
                    "pts": 16,
                    "reb": 8,
                    "ast": 4
                },
                {
                    "pts": 25,
                    "reb": 6,
                    "ast": 8
                },
                {
                    "pts": 17,
                    "reb": 5,
                    "ast": 12
                },
                {
                    "pts": 13,
                    "reb": 13,
                    "ast": 7
                }
            ],
            "min_avg": 35.0,
            "min_l10": 35.2,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 3.8
            },
            "fd_line_cat": "P",
            "fd_line": 21.0,
            "note": "Bounce-back (26 PRA last game vs 35 avg) | DEN #29 vs PF ast | High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Deandre Ayton",
            "team": "LAL",
            "opp": "DEN",
            "pos": "C",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 10,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 14,
                    "ast": 2
                },
                {
                    "pts": 18,
                    "reb": 8,
                    "ast": 4
                },
                {
                    "pts": 8,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 25,
                    "reb": 20,
                    "ast": 2
                },
                {
                    "pts": 24,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 22,
                    "reb": 8,
                    "ast": 3
                },
                {
                    "pts": 21,
                    "reb": 14,
                    "ast": 2
                },
                {
                    "pts": 22,
                    "reb": 15,
                    "ast": 2
                },
                {
                    "pts": 15,
                    "reb": 13,
                    "ast": 2
                }
            ],
            "min_avg": 30.2,
            "min_l10": 31.9,
            "edges": {
                "pts": 1.5,
                "reb": 0.0,
                "ast": 0.2
            },
            "fd_line_cat": "R",
            "fd_line": 10.5,
            "note": "Bounce-back (10 PRA last game vs 30 avg) | High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Rui Hachimura",
            "team": "LAL",
            "opp": "DEN",
            "pos": "SF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 16,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 15,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 7,
                    "ast": 1
                },
                {
                    "pts": 24,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 7,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 13,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 14,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 5,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 5,
                    "reb": 3,
                    "ast": 2
                }
            ],
            "min_avg": 31.6,
            "min_l10": 28.3,
            "edges": {
                "pts": 3.0,
                "reb": 0.5,
                "ast": 1.5
            },
            "fd_line_cat": "P",
            "fd_line": 11.0,
            "note": "DEN #25 vs SF pts | High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Luke Kennard",
            "team": "LAL",
            "opp": "DEN",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 12,
                    "reb": 6,
                    "ast": 4
                },
                {
                    "pts": 0,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 4,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 1,
                    "ast": 5
                },
                {
                    "pts": 1,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 0,
                    "ast": 2
                },
                {
                    "pts": 9,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 3,
                    "ast": 6
                },
                {
                    "pts": 15,
                    "reb": 2,
                    "ast": 4
                }
            ],
            "min_avg": 22.6,
            "min_l10": 22.4,
            "edges": {
                "pts": 0.2,
                "reb": 0.2,
                "ast": 0.5
            },
            "fd_line_cat": "PRA",
            "fd_line": 10.5,
            "note": "High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Jake LaRavia",
            "team": "LAL",
            "opp": "DEN",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 11,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 11,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 10,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 13,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 7,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 8,
                    "ast": 3
                },
                {
                    "pts": 15,
                    "reb": 5,
                    "ast": 1
                }
            ],
            "min_avg": 20.7,
            "min_l10": 23.0,
            "edges": {
                "pts": 1.0,
                "reb": 0.0,
                "ast": 0.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 13.0,
            "note": "High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Maxi Kleber",
            "team": "LAL",
            "opp": "DEN",
            "pos": "PF",
            "role": "bench",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 1,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 10,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 2,
                    "ast": 4
                },
                {
                    "pts": 0,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 5,
                    "reb": 3,
                    "ast": 5
                }
            ],
            "min_avg": 18.7,
            "min_l10": 17.3,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 3.8
            },
            "fd_line_cat": "PRA",
            "fd_line": 8.0,
            "note": "Bounce-back (3 PRA last game vs 8 avg) | DEN #29 vs PF ast | High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Jarred Vanderbilt",
            "team": "LAL",
            "opp": "DEN",
            "pos": "PF",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 8,
                    "reb": 4,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 12,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 2,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 7,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 6,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 7,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 6,
                    "ast": 3
                }
            ],
            "min_avg": 16.1,
            "min_l10": 15.1,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 3.8
            },
            "fd_line_cat": "PRA",
            "fd_line": 10.0,
            "note": "DEN #29 vs PF ast | High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Jamal Murray",
            "team": "DEN",
            "opp": "LAL",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 16,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 15,
                    "reb": 5,
                    "ast": 7
                },
                {
                    "pts": 17,
                    "reb": 4,
                    "ast": 6
                },
                {
                    "pts": 28,
                    "reb": 5,
                    "ast": 7
                },
                {
                    "pts": 39,
                    "reb": 4,
                    "ast": 7
                },
                {
                    "pts": 10,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 24,
                    "reb": 6,
                    "ast": 7
                },
                {
                    "pts": 26,
                    "reb": 4,
                    "ast": 5
                },
                {
                    "pts": 12,
                    "reb": 5,
                    "ast": 8
                },
                {
                    "pts": 34,
                    "reb": 4,
                    "ast": 6
                }
            ],
            "min_avg": 36.1,
            "min_l10": 35.0,
            "edges": {
                "pts": 0.5,
                "reb": 0.0,
                "ast": 3.8
            },
            "fd_line_cat": "P",
            "fd_line": 21.0,
            "note": "LAL #30 vs PG ast | High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Christian Braun",
            "team": "DEN",
            "opp": "LAL",
            "pos": "SG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 11,
                    "reb": 7,
                    "ast": 6
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 5
                },
                {
                    "pts": 25,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 30,
                    "reb": 8,
                    "ast": 4
                },
                {
                    "pts": 16,
                    "reb": 7,
                    "ast": 4
                },
                {
                    "pts": 18,
                    "reb": 12,
                    "ast": 4
                },
                {
                    "pts": 16,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 19,
                    "reb": 10,
                    "ast": 6
                },
                {
                    "pts": 18,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 2
                }
            ],
            "min_avg": 33.9,
            "min_l10": 37.1,
            "edges": {
                "pts": 0.2,
                "reb": 0.2,
                "ast": 1.0
            },
            "fd_line_cat": "PR",
            "fd_line": 23.0,
            "note": "High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Julian Strawther",
            "team": "DEN",
            "opp": "LAL",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 9,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 1,
                    "reb": 7,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 12,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 2,
                    "reb": 0,
                    "ast": 2
                },
                {
                    "pts": 16,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 5,
                    "ast": 1
                }
            ],
            "min_avg": 21.6,
            "min_l10": 16.6,
            "edges": {
                "pts": 3.8,
                "reb": 0.0,
                "ast": 2.2
            },
            "fd_line_cat": "PRA",
            "fd_line": 10.0,
            "note": "LAL #30 vs SF pts | High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Cameron Johnson",
            "team": "DEN",
            "opp": "LAL",
            "pos": "SF",
            "role": "starter",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 18,
                    "reb": 9,
                    "ast": 7
                },
                {
                    "pts": 11,
                    "reb": 0,
                    "ast": 6
                },
                {
                    "pts": 17,
                    "reb": 2,
                    "ast": 8
                },
                {
                    "pts": 20,
                    "reb": 9,
                    "ast": 5
                },
                {
                    "pts": 11,
                    "reb": 2,
                    "ast": 4
                },
                {
                    "pts": 28,
                    "reb": 4,
                    "ast": 7
                },
                {
                    "pts": 23,
                    "reb": 10,
                    "ast": 6
                },
                {
                    "pts": 16,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 17,
                    "reb": 5,
                    "ast": 5
                },
                {
                    "pts": 18,
                    "reb": 7,
                    "ast": 5
                }
            ],
            "min_avg": 31.6,
            "min_l10": 30.7,
            "edges": {
                "pts": 3.8,
                "reb": 0.0,
                "ast": 2.2
            },
            "fd_line_cat": "PA",
            "fd_line": 22.5,
            "note": "LAL #30 vs SF pts | High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Bruce Brown",
            "team": "DEN",
            "opp": "LAL",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 9,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 16,
                    "reb": 4,
                    "ast": 9
                },
                {
                    "pts": 1,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 16,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 3,
                    "reb": 12,
                    "ast": 2
                },
                {
                    "pts": 18,
                    "reb": 7,
                    "ast": 1
                },
                {
                    "pts": 12,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 14,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 15,
                    "reb": 7,
                    "ast": 6
                },
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 0
                }
            ],
            "min_avg": 22.4,
            "min_l10": 26.8,
            "edges": {
                "pts": 0.5,
                "reb": 0.0,
                "ast": 3.8
            },
            "fd_line_cat": "P",
            "fd_line": 10.0,
            "note": "Bounce-back (13 PRA last game vs 18 avg) | Minutes trending up (22.4->26.8) | LAL #30 vs PG ast | High O/U 240.5 \u2014 shootout potential"
        },
        {
            "name": "Jalen Pickett",
            "team": "DEN",
            "opp": "LAL",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 18,
                    "reb": 1,
                    "ast": 4
                },
                {
                    "pts": 4,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 8,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 17,
                    "reb": 11,
                    "ast": 10
                },
                {
                    "pts": 9,
                    "reb": 4,
                    "ast": 5
                },
                {
                    "pts": 0,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 4,
                    "reb": 0,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 2,
                    "ast": 3
                }
            ],
            "min_avg": 17.8,
            "min_l10": 22.2,
            "edges": {
                "pts": 0.5,
                "reb": 0.0,
                "ast": 3.8
            },
            "fd_line_cat": "PRA",
            "fd_line": 12.0,
            "note": "Bounce-back (2 PRA last game vs 12 avg) | Minutes trending up (17.8->22.2) | LAL #30 vs PG ast | High O/U 240.5 \u2014 shootout potential"
        }
    ],
    "NOP_SAC": [
        {
            "name": "Jaxson Hayes",
            "team": "SAC",
            "opp": "NOP",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 7,
                    "reb": 1,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 7,
                    "reb": 6,
                    "ast": 2
                },
                {
                    "pts": 7,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 12,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 3,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 2,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 19,
                    "reb": 8,
                    "ast": 1
                },
                {
                    "pts": 13,
                    "reb": 2,
                    "ast": 1
                }
            ],
            "min_avg": 19.5,
            "min_l10": 18.6,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 12.0,
            "note": "Bounce-back (8 PRA last game vs 12 avg) | High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "Herbert Jones",
            "team": "NOP",
            "opp": "SAC",
            "pos": "SF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 0,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 6,
                    "ast": 5
                },
                {
                    "pts": 11,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 1,
                    "ast": 6
                },
                {
                    "pts": 8,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 18,
                    "reb": 4,
                    "ast": 5
                },
                {
                    "pts": 4,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 10,
                    "reb": 6,
                    "ast": 7
                },
                {
                    "pts": 8,
                    "reb": 6,
                    "ast": 6
                },
                {
                    "pts": 5,
                    "reb": 4,
                    "ast": 4
                }
            ],
            "min_avg": 32.5,
            "min_l10": 32.4,
            "edges": {
                "pts": 1.5,
                "reb": 0.0,
                "ast": 0.5
            },
            "fd_line_cat": "PRA",
            "fd_line": 16.0,
            "note": "Bounce-back (1 PRA last game vs 17 avg) | High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "Trey Murphy",
            "team": "NOP",
            "opp": "SAC",
            "pos": "PG",
            "role": "starter",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 20,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 17,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 21,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 27,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 13,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 26,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 19,
                    "reb": 6,
                    "ast": 5
                },
                {
                    "pts": 20,
                    "reb": 6,
                    "ast": 6
                },
                {
                    "pts": 10,
                    "reb": 3,
                    "ast": 8
                },
                {
                    "pts": 18,
                    "reb": 4,
                    "ast": 1
                }
            ],
            "min_avg": 35.7,
            "min_l10": 35.4,
            "edges": {
                "pts": 3.8,
                "reb": 2.2,
                "ast": 3.8
            },
            "fd_line_cat": "P",
            "fd_line": 18.5,
            "note": "SAC #28 vs PG pts | High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "Zion Williamson",
            "team": "NOP",
            "opp": "SAC",
            "pos": "PF",
            "role": "starter",
            "inj": "GTD",
            "last10_games": [
                {
                    "pts": 29,
                    "reb": 5,
                    "ast": 8
                },
                {
                    "pts": 30,
                    "reb": 6,
                    "ast": 3
                },
                {
                    "pts": 20,
                    "reb": 8,
                    "ast": 5
                },
                {
                    "pts": 22,
                    "reb": 10,
                    "ast": 12
                },
                {
                    "pts": 20,
                    "reb": 2,
                    "ast": 3
                },
                {
                    "pts": 20,
                    "reb": 10,
                    "ast": 3
                },
                {
                    "pts": 37,
                    "reb": 4,
                    "ast": 6
                },
                {
                    "pts": 24,
                    "reb": 6,
                    "ast": 9
                },
                {
                    "pts": 27,
                    "reb": 10,
                    "ast": 11
                },
                {
                    "pts": 18,
                    "reb": 6,
                    "ast": 3
                }
            ],
            "min_avg": 28.5,
            "min_l10": 29.4,
            "edges": {
                "pts": 2.2,
                "reb": 1.5,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 23.5,
            "note": "High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "DeAndre Jordan",
            "team": "NOP",
            "opp": "SAC",
            "pos": "C",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 4,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 2,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 5,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 17,
                    "ast": 1
                },
                {
                    "pts": 2,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 11,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 17,
                    "ast": 7
                },
                {
                    "pts": 11,
                    "reb": 15,
                    "ast": 4
                },
                {
                    "pts": 1,
                    "reb": 3,
                    "ast": 0
                }
            ],
            "min_avg": 12.8,
            "min_l10": 16.8,
            "edges": {
                "pts": 3.8,
                "reb": 3.8,
                "ast": 2.2
            },
            "fd_line_cat": "PRA",
            "fd_line": 14.0,
            "note": "Bounce-back (9 PRA last game vs 14 avg) | Minutes trending up (12.8->16.8) | SAC #30 vs C pts | High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "Yves Missi",
            "team": "NOP",
            "opp": "SAC",
            "pos": "C",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 9,
                    "reb": 5,
                    "ast": 0
                },
                {
                    "pts": 18,
                    "reb": 12,
                    "ast": 3
                },
                {
                    "pts": 13,
                    "reb": 11,
                    "ast": 2
                },
                {
                    "pts": 6,
                    "reb": 12,
                    "ast": 4
                },
                {
                    "pts": 8,
                    "reb": 11,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 10,
                    "ast": 0
                },
                {
                    "pts": 16,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 5,
                    "reb": 10,
                    "ast": 2
                },
                {
                    "pts": 13,
                    "reb": 7,
                    "ast": 2
                },
                {
                    "pts": 12,
                    "reb": 10,
                    "ast": 0
                }
            ],
            "min_avg": 26.8,
            "min_l10": 25.8,
            "edges": {
                "pts": 3.8,
                "reb": 3.8,
                "ast": 2.2
            },
            "fd_line_cat": "R",
            "fd_line": 9.5,
            "note": "Bounce-back (14 PRA last game vs 23 avg) | SAC #30 vs C pts | High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "Jordan Poole",
            "team": "NOP",
            "opp": "SAC",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 19,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 15,
                    "reb": 2,
                    "ast": 5
                },
                {
                    "pts": 23,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 35,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 12,
                    "reb": 2,
                    "ast": 4
                },
                {
                    "pts": 18,
                    "reb": 0,
                    "ast": 3
                },
                {
                    "pts": 18,
                    "reb": 2,
                    "ast": 7
                },
                {
                    "pts": 23,
                    "reb": 1,
                    "ast": 1
                },
                {
                    "pts": 25,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 18,
                    "reb": 2,
                    "ast": 2
                }
            ],
            "min_avg": 29.5,
            "min_l10": 24.3,
            "edges": {
                "pts": 3.8,
                "reb": 2.2,
                "ast": 3.8
            },
            "fd_line_cat": "P",
            "fd_line": 20.0,
            "note": "SAC #28 vs PG pts | High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "Jordan Hawkins",
            "team": "NOP",
            "opp": "SAC",
            "pos": "SG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 8,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 9,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 25,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 10,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 13,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 11,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 11,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 12,
                    "reb": 5,
                    "ast": 0
                }
            ],
            "min_avg": 23.6,
            "min_l10": 24.8,
            "edges": {
                "pts": 2.2,
                "reb": 1.5,
                "ast": 3.0
            },
            "fd_line_cat": "P",
            "fd_line": 10.0,
            "note": "SAC #26 vs SG ast | High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "Russell Westbrook",
            "team": "SAC",
            "opp": "NOP",
            "pos": "PG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 17,
                    "reb": 0,
                    "ast": 6
                },
                {
                    "pts": 14,
                    "reb": 3,
                    "ast": 4
                },
                {
                    "pts": 5,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 16,
                    "reb": 5,
                    "ast": 4
                },
                {
                    "pts": 5,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 30,
                    "reb": 11,
                    "ast": 6
                },
                {
                    "pts": 12,
                    "reb": 6,
                    "ast": 7
                },
                {
                    "pts": 17,
                    "reb": 2,
                    "ast": 7
                },
                {
                    "pts": 6,
                    "reb": 2,
                    "ast": 6
                },
                {
                    "pts": 14,
                    "reb": 5,
                    "ast": 10
                }
            ],
            "min_avg": 27.9,
            "min_l10": 26.3,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "PA",
            "fd_line": 18.5,
            "note": "High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "DeMar DeRozan",
            "team": "SAC",
            "opp": "NOP",
            "pos": "SG",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 8,
                    "reb": 0,
                    "ast": 5
                },
                {
                    "pts": 16,
                    "reb": 3,
                    "ast": 8
                },
                {
                    "pts": 22,
                    "reb": 4,
                    "ast": 4
                },
                {
                    "pts": 37,
                    "reb": 4,
                    "ast": 2
                },
                {
                    "pts": 28,
                    "reb": 4,
                    "ast": 7
                },
                {
                    "pts": 22,
                    "reb": 4,
                    "ast": 3
                },
                {
                    "pts": 29,
                    "reb": 7,
                    "ast": 8
                },
                {
                    "pts": 31,
                    "reb": 3,
                    "ast": 8
                },
                {
                    "pts": 21,
                    "reb": 4,
                    "ast": 1
                },
                {
                    "pts": 21,
                    "reb": 2,
                    "ast": 10
                }
            ],
            "min_avg": 35.9,
            "min_l10": 36.0,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 22.5,
            "note": "Bounce-back (13 PRA last game vs 33 avg) | High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "Precious Achiuwa",
            "team": "SAC",
            "opp": "NOP",
            "pos": "PF",
            "role": "starter",
            "inj": None,
            "last10_games": [
                {
                    "pts": 18,
                    "reb": 9,
                    "ast": 2
                },
                {
                    "pts": 0,
                    "reb": 6,
                    "ast": 0
                },
                {
                    "pts": 18,
                    "reb": 10,
                    "ast": 3
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 13,
                    "reb": 6,
                    "ast": 1
                },
                {
                    "pts": 2,
                    "reb": 9,
                    "ast": 1
                },
                {
                    "pts": 10,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 0,
                    "reb": 2,
                    "ast": 0
                },
                {
                    "pts": 6,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 11,
                    "reb": 2,
                    "ast": 2
                }
            ],
            "min_avg": 20.8,
            "min_l10": 20.6,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 14.0,
            "note": "High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "Malik Monk",
            "team": "SAC",
            "opp": "NOP",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 2,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 8,
                    "reb": 7,
                    "ast": 3
                },
                {
                    "pts": 17,
                    "reb": 1,
                    "ast": 3
                },
                {
                    "pts": 13,
                    "reb": 3,
                    "ast": 3
                },
                {
                    "pts": 5,
                    "reb": 7,
                    "ast": 7
                },
                {
                    "pts": 9,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 16,
                    "reb": 3,
                    "ast": 2
                },
                {
                    "pts": 34,
                    "reb": 1,
                    "ast": 5
                },
                {
                    "pts": 22,
                    "reb": 6,
                    "ast": 8
                },
                {
                    "pts": 28,
                    "reb": 3,
                    "ast": 7
                }
            ],
            "min_avg": 31.6,
            "min_l10": 26.2,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "P",
            "fd_line": 15.0,
            "note": "Bounce-back (3 PRA last game vs 23 avg) | High O/U 234.5 \u2014 shootout potential"
        },
        {
            "name": "Devin Carter",
            "team": "SAC",
            "opp": "NOP",
            "pos": "PG",
            "role": "bench",
            "inj": None,
            "last10_games": [
                {
                    "pts": 5,
                    "reb": 5,
                    "ast": 1
                },
                {
                    "pts": 7,
                    "reb": 1,
                    "ast": 2
                },
                {
                    "pts": 4,
                    "reb": 3,
                    "ast": 1
                },
                {
                    "pts": 7,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 2,
                    "ast": 1
                },
                {
                    "pts": 0,
                    "reb": 0,
                    "ast": 1
                },
                {
                    "pts": 1,
                    "reb": 3,
                    "ast": 0
                },
                {
                    "pts": 4,
                    "reb": 2,
                    "ast": 2
                },
                {
                    "pts": 16,
                    "reb": 5,
                    "ast": 3
                },
                {
                    "pts": 2,
                    "reb": 1,
                    "ast": 2
                }
            ],
            "min_avg": 13.0,
            "min_l10": 17.2,
            "edges": {
                "pts": 1.0,
                "reb": 1.0,
                "ast": 1.0
            },
            "fd_line_cat": "PRA",
            "fd_line": 8.0,
            "note": "Minutes trending up (13.0->17.2) | High O/U 234.5 \u2014 shootout potential"
        }
    ]
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
    # Score each combo by: matchup edge + def rank bonus + floor safety
    # Uses L10 avg as baseline — L10 low is the TRUE floor (actual minimum)
    cat_scores = {}
    for cat in CATS:
        s = 0.0
        if "P" in cat:
            s += edges.get("pts", 0)
            if dc["pts"] >= 22: s += 1.4
        if "R" in cat:
            s += edges.get("reb", 0)
            if dc["reb"] >= 22: s += 1.4
        if "A" in cat:
            s += edges.get("ast", 0)
            if dc["ast"] >= 20: s += 1.2
        # Floor safety: how close is the true minimum to the L10 average?
        # Higher = more consistent = safer bet
        if l10_combos[cat] > 0:
            floor_pct = l10_lows[cat] / l10_combos[cat]
            s += floor_pct * 1.0
        cat_scores[cat] = round(s, 2)

    best_cat = max(cat_scores, key=cat_scores.get)

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
    results = [analyze(game_id, p, players) for p in players]
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
