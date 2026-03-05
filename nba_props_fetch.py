#!/usr/bin/env python3
"""
NBA Props — Automated Data Pipeline (100% Free APIs)
=====================================================
No API key needed. Run it and it works.

SETUP:
  pip install requests beautifulsoup4 lxml

USAGE:
  python nba_props_fetch.py
  python nba_props_fetch.py --cache   (re-render HTML without re-fetching)

DATA SOURCES (all free):
  1. Games today + player game logs  -> balldontlie.io (free, no key)
  2. Probable lineups                -> NBA.com CDN    (free, official)
  3. DVP rankings                    -> FantasyPros    (scraped)
  4. Pace per team                   -> Basketball Ref (scraped, fallback)
  5. Injury report                   -> ESPN           (scraped)
"""

import requests
import json
import time
import re
import sys
import subprocess
from datetime import datetime, date
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

# Minimum average minutes to include a player
MIN_MINUTES_THRESHOLD = 15

# Only include players with at least this many games in last 10
MIN_GAMES_PLAYED = 5

TODAY      = date.today()
TODAY_STR  = TODAY.strftime("%Y-%m-%d")
TODAY_FMT  = TODAY.strftime("%B %d, %Y")

# ─────────────────────────────────────────────────────────────────────────────
# TEAM MAPS
# ─────────────────────────────────────────────────────────────────────────────

TEAM_ABV = {
    "Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BKN",
    "Charlotte Hornets": "CHA", "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN", "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW", "Houston Rockets": "HOU", "Indiana Pacers": "IND",
    "LA Clippers": "LAC", "Los Angeles Clippers": "LAC", "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM", "Miami Heat": "MIA", "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK", "Oklahoma City Thunder": "OKC", "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHX", "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS", "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA", "Washington Wizards": "WAS",
    # short names
    "76ers":"PHI","Bucks":"MIL","Bulls":"CHI","Cavaliers":"CLE","Celtics":"BOS",
    "Clippers":"LAC","Grizzlies":"MEM","Hawks":"ATL","Heat":"MIA","Hornets":"CHA",
    "Jazz":"UTA","Kings":"SAC","Knicks":"NYK","Lakers":"LAL","Magic":"ORL",
    "Mavericks":"DAL","Nets":"BKN","Nuggets":"DEN","Pacers":"IND","Pelicans":"NOP",
    "Pistons":"DET","Raptors":"TOR","Rockets":"HOU","Spurs":"SAS","Suns":"PHX",
    "Thunder":"OKC","Timberwolves":"MIN","Trail Blazers":"POR","Warriors":"GSW",
    "Wizards":"WAS",
}

# balldontlie team ID -> our abbreviation
BDL_TEAM_ID_TO_ABV = {}   # populated at runtime from BDL teams endpoint

POS_MAP = {
    "PG":"PG","SG":"SG","SF":"SF","PF":"PF","C":"C",
    "G":"PG","F":"SF","G-F":"SG","F-C":"PF","F-G":"SG","C-F":"PF",
}

INJ_MAP = {
    "Out":"OUT","Doubtful":"DOUBTFUL","Questionable":"QUESTIONABLE",
    "Game Time Decision":"GTD","GTD":"GTD","Day-To-Day":"GTD",
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def safe_float(val, default=0.0):
    try:
        return float(str(val).replace(",", "").strip())
    except:
        return default

def normalize_team(raw):
    raw = raw.strip()
    if raw in TEAM_ABV:
        return TEAM_ABV[raw]
    for k, v in TEAM_ABV.items():
        if raw.upper() == v:
            return v
    return raw.upper()[:3]

def scrape(url, delay=1.0):
    time.sleep(delay)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return BeautifulSoup(r.text, "lxml")
        print(f"  ⚠️  Scrape failed {r.status_code}: {url}")
    except Exception as e:
        print(f"  ⚠️  Scrape error: {e}")
    return None

# ─────────────────────────────────────────────────────────────────────────────
# BALLDONTLIE API  (free, no key required)
# ─────────────────────────────────────────────────────────────────────────────

BDL_BASE = "https://api.balldontlie.io/v1"
BDL_API_KEY = "d2a0fcf0-7641-4048-90fe-681b64be61df"

def bdl_get(path, params=None, delay=0.5):
    """Fetch from balldontlie. Retries on 429."""
    time.sleep(delay)
    try:
        r = requests.get(
            f"{BDL_BASE}/{path}",
            params=params,
            headers={"Authorization": BDL_API_KEY},
            timeout=15,
        )
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 429:
            print("  ⚠️  Rate limited — waiting 8s...")
            time.sleep(8)
            return bdl_get(path, params, delay=0)
        else:
            print(f"  ⚠️  BDL error {r.status_code}: {path}")
            return None
    except Exception as e:
        print(f"  ⚠️  BDL exception: {e}")
        return None

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: FETCH TODAY'S GAMES from balldontlie
# ─────────────────────────────────────────────────────────────────────────────

def fetch_games():
    """
    Returns (games_meta, team_id_map)
    games_meta = list of game dicts
    team_id_map = {bdl_team_id: abbv}
    """
    print("📅 Fetching today's schedule from balldontlie...")

    data = bdl_get("games", params={"dates[]": TODAY_STR, "per_page": 30})
    if not data:
        return [], {}

    games_meta = []
    team_id_map = {}

    for g in data.get("data", []):
        status = g.get("status", "")
        home   = g["home_team"]
        away   = g["visitor_team"]

        home_abv = normalize_team(home.get("full_name", home.get("name", "")))
        away_abv = normalize_team(away.get("full_name", away.get("name", "")))

        # Map BDL team IDs to our abbreviations
        team_id_map[home["id"]] = home_abv
        team_id_map[away["id"]] = away_abv

        # Win probability — BDL doesn't provide this, default 50/50
        # Parse game time from BDL datetime field into readable ET time
        raw_dt = g.get("datetime") or g.get("date") or ""
        game_time = "TBD"
        if raw_dt and "T" in raw_dt:
            try:
                from datetime import timezone, timedelta
                dt_utc = datetime.strptime(raw_dt[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
                dt_et  = dt_utc.astimezone(timezone(timedelta(hours=-5)))  # EST
                game_time = dt_et.strftime("%-I:%M %p ET").replace("AM","am").replace("PM","pm")
            except:
                game_time = g.get("status", "TBD")
        else:
            game_time = g.get("status", "TBD")

        # Normalize status
        if status in ("Final", "final"):
            status_label = "FINAL"
        elif "/" in status or ":" in status:
            status_label = "UPCOMING"
        else:
            status_label = status.upper() if status else "UPCOMING"

        home_rec = f"{g.get('home_team_score',0) or 0}-{g.get('visitor_team_score',0) or 0}"

        games_meta.append({
            "id":        f"{away_abv}_{home_abv}",
            "away":      away_abv,
            "home":      home_abv,
            "away_rec":  "",
            "home_rec":  "",
            "time":      game_time,
            "prob_away": 50,
            "prob_home": 50,
            "status":    status_label,
            "_bdl_game_id":  g["id"],
            "_home_bdl_id":  home["id"],
            "_away_bdl_id":  away["id"],
        })

    # Update global team ID map
    BDL_TEAM_ID_TO_ABV.update(team_id_map)

    print(f"  ✅ Found {len(games_meta)} games today")
    return games_meta, team_id_map


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: FETCH DVP RANKINGS from FantasyPros
# ─────────────────────────────────────────────────────────────────────────────

def fetch_dvp():
    """
    Scrape DVP from bettingpros.com.
    Data is embedded as JSON in a <script> tag:
    const bpDefenseVsPositionStats = { teamStats: {"ATL": {"PG": {...}, "SG": {...}...}}}
    """
    print("Fetching DVP from BettingPros...")
    positions = ["PG", "SG", "SF", "PF", "C"]
    pos_data = {pos: {} for pos in positions}

    url = "https://www.bettingpros.com/nba/defense-vs-position/"
    try:
        r = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.bettingpros.com/",
        }, timeout=20)

        if r.status_code != 200:
            print(f"  BettingPros failed: {r.status_code}")
            return {}

        import re
        # Extract teamStats block — fix JS object to valid JSON
        match = re.search(r'teamStats\s*:\s*(\{.+?\})\s*,\s*\w+\s*:', r.text, re.DOTALL)
        if not match:
            # Try broader match up to end of script
            match = re.search(r'teamStats["\']?\s*:\s*(\{.+)$', r.text, re.DOTALL)
        if not match:
            print("  BettingPros: could not find teamStats in page")
            return {}

        raw = match.group(1)
        # Fix JS object syntax to valid JSON:
        # - unquoted keys -> quoted keys
        raw = re.sub(r'(\{|,)\s*([A-Za-z_][A-Za-z0-9_]*)\s*:', r'\1"\2":', raw)
        # Remove trailing comma before } or ]
        raw = re.sub(r',\s*([}\]])', r'\1', raw)
        # Trim to valid JSON object
        depth = 0
        end = 0
        for i, ch in enumerate(raw):
            if ch == '{': depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        raw = raw[:end]

        try:
            team_stats = json.loads(raw)
        except Exception as je:
            print(f"  JSON parse error: {je}")
            print(f"  Raw sample: {raw[:200]}")
            return {}

        print(f"  BettingPros: found {len(team_stats)} teams")

        for team_raw, pos_dict in team_stats.items():
            team = normalize_team(team_raw) or team_raw.upper()
            for pos in positions:
                if pos not in pos_dict:
                    continue
                stats = pos_dict[pos]
                pts = safe_float(str(stats.get("points", 0)))
                reb = safe_float(str(stats.get("rebounds", 0)))
                ast_v = safe_float(str(stats.get("assists", 0)))
                if pts > 0:
                    pos_data[pos][team] = {"pts": pts, "reb": reb, "ast": ast_v}

        for pos in positions:
            print(f"  DVP {pos}: {len(pos_data[pos])} teams")

    except Exception as e:
        print(f"  BettingPros DVP error: {e}")

    return _build_dvp_ranks(pos_data, positions)
def _build_dvp_ranks(pos_data, positions):
    """Convert raw stat values to 1-30 ranks."""
    dvp = {}
    for pos, teams in pos_data.items():
        for stat in ["pts", "reb", "ast"]:
            valid = {t: v for t, v in teams.items() if v.get(stat, 0) > 0}
            sorted_teams = sorted(valid.keys(), key=lambda t: valid[t][stat])
            for rank, team in enumerate(sorted_teams, start=1):
                if team not in dvp:
                    dvp[team] = {"pace": 112.0}
                dvp[team][f"{pos}_{stat}"] = rank
    for team in dvp:
        for stat in ["pts", "reb", "ast"]:
            vals = [dvp[team][f"{p}_{stat}"] for p in positions if f"{p}_{stat}" in dvp[team]]
            dvp[team][stat] = round(sum(vals) / len(vals)) if vals else 15
    print(f"  DVP complete: {len(dvp)} teams")
    return dvp
def fetch_pace(dvp):
    print("⚡ Fetching pace from Basketball Reference...")
    BREF_TO_ABV = {
        "ATL":"ATL","BOS":"BOS","BRK":"BKN","CHO":"CHA","CHI":"CHI",
        "CLE":"CLE","DAL":"DAL","DEN":"DEN","DET":"DET","GSW":"GSW",
        "HOU":"HOU","IND":"IND","LAC":"LAC","LAL":"LAL","MEM":"MEM",
        "MIA":"MIA","MIL":"MIL","MIN":"MIN","NOP":"NOP","NYK":"NYK",
        "OKC":"OKC","ORL":"ORL","PHI":"PHI","PHO":"PHX","POR":"POR",
        "SAC":"SAC","SAS":"SAS","TOR":"TOR","UTA":"UTA","WAS":"WAS",
    }
    soup = scrape("https://www.basketball-reference.com/leagues/NBA_2026.html", delay=2.0)
    if not soup:
        print("  ⚠️  Could not fetch pace — using defaults")
        return dvp

    table = None
    for tbl in soup.find_all("table"):
        hdrs = [th.get_text() for th in tbl.find_all("th")]
        if "Pace" in hdrs:
            table = tbl
            break

    if not table:
        print("  ⚠️  Pace table not found — using defaults")
        return dvp

    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    try:
        pace_idx = headers.index("Pace")
    except ValueError:
        return dvp

    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if not cols or len(cols) < pace_idx:
            continue
        team_raw = cols[0].get_text(strip=True).replace("*", "")
        pace_val = safe_float(cols[pace_idx - 1].get_text(strip=True), 112.0)
        our_abv  = BREF_TO_ABV.get(team_raw, normalize_team(team_raw))
        if our_abv in dvp:
            dvp[our_abv]["pace"] = pace_val

    print("  ✅ Pace data merged")
    return dvp


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: FETCH INJURIES from NBA.com CDN
# ─────────────────────────────────────────────────────────────────────────────

def fetch_injuries():
    """
    Fetch injury report from ESPN — covers OUT/DOUBTFUL/GTD/QUESTIONABLE.
    Falls back to NBA.com CDN if ESPN fails.
    Returns {player_name: status}
    """
    print("🏥 Fetching injury report from ESPN...")
    injuries = {}

    # ── ESPN injuries page ────────────────────────────────────────────────────
    try:
        r = requests.get(
            "https://www.espn.com/nba/injuries",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "text/html,*/*",
                "Accept-Language": "en-US,en;q=0.9",
            },
            timeout=20
        )
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
            # ESPN injury table: each team section has a <table>
            # Rows: player name | position | date | status | comment
            tables = soup.find_all("table")
            for table in tables:
                for row in table.find_all("tr")[1:]:  # skip header
                    cols = row.find_all("td")
                    if len(cols) < 4:
                        continue
                    name   = cols[0].get_text(strip=True)
                    status_raw = cols[3].get_text(strip=True) if len(cols) > 3 else ""
                    # Normalize status
                    status = INJ_MAP.get(status_raw, None)
                    if not status:
                        sr = status_raw.upper()
                        if "OUT" in sr:          status = "OUT"
                        elif "DOUBTFUL" in sr:   status = "DOUBTFUL"
                        elif "GTD" in sr or "GAME TIME" in sr or "DAY" in sr: status = "GTD"
                        elif "QUESTION" in sr:   status = "QUESTIONABLE"
                    if name and status:
                        injuries[name] = status
            print(f"  ESPN: {len(injuries)} injured players")
    except Exception as e:
        print(f"  ESPN injury error: {e}")

    # ── NBA.com CDN fallback ──────────────────────────────────────────────────
    if not injuries:
        print("  Trying NBA.com CDN fallback...")
        try:
            r = requests.get(
                "https://cdn.nba.com/static/json/liveData/injuries/injuries_00.json",
                headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.nba.com/"},
                timeout=15
            )
            if r.status_code == 200:
                data = r.json()
                # Try multiple known structures
                players = (data.get("liveData", {}).get("injuries", {}).get("InactivePlayers", [])
                           or data.get("injuries", {}).get("InactivePlayers", [])
                           or data.get("InactivePlayers", []))
                for p in players:
                    name   = f"{p.get('FirstName','')} {p.get('LastName','')}".strip()
                    status = INJ_MAP.get(p.get("InjuryStatus",""), None) or "OUT"
                    if name:
                        injuries[name] = status
                print(f"  NBA.com CDN: {len(injuries)} players")
        except Exception as e:
            print(f"  NBA.com CDN error: {e}")

    print(f"  ✅ {len(injuries)} total injured players found")
    if injuries:
        # Show sample
        sample = list(injuries.items())[:5]
        for nm, st in sample:
            print(f"    {nm}: {st}")
    return injuries


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5: FETCH LINEUPS from NBA.com
# ─────────────────────────────────────────────────────────────────────────────

NBA_CDN_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer":    "https://www.nba.com/",
    "Origin":     "https://www.nba.com",
    "Accept":     "application/json",
}

def _nba_cdn_get(url, delay=0.8):
    time.sleep(delay)
    try:
        r = requests.get(url, headers=NBA_CDN_HEADERS, timeout=15)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"  ⚠️  NBA CDN error: {e}")
    return None


def fetch_spreads():
    """
    Scrape spreads from RotoWire NBA lineups page.
    Returns {game_id: spread} e.g. {"OKC_NYK": 4.5}
    Spread = absolute value of the away team spread line.
    """
    print("  Fetching spreads from RotoWire...")
    spreads = {}
    try:
        r = requests.get(
            "https://www.rotowire.com/basketball/nba-lineups.php",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "text/html,*/*",
                "Accept-Language": "en-US,en;q=0.9",
            },
            timeout=20
        )
        if r.status_code != 200:
            print(f"  RotoWire spread: HTTP {r.status_code}")
            return spreads

        soup = BeautifulSoup(r.text, "lxml")
        import re as _re

        # Each game is a .lineup container
        for game in soup.find_all("div", {"class": lambda c: c and "lineup" in (c if isinstance(c, list) else c.split()) and "is-nba" in (c if isinstance(c, list) else c.split())}):
            # Get team abbrs
            team_els = game.find_all("a", {"class": lambda c: c and "lineup__team" in " ".join(c if isinstance(c, list) else [c])})
            abbrs = []
            for t in team_els:
                abbr = t.find("div", {"class": lambda c: c and "lineup__abbr" in " ".join(c if isinstance(c, list) else [c])})
                if abbr:
                    abbrs.append(abbr.get_text(strip=True).upper())
            if len(abbrs) < 2:
                continue
            away_abv, home_abv = abbrs[0], abbrs[1]
            game_key = f"{away_abv}_{home_abv}"

            # Find SPREAD odds item
            for item in game.find_all("div", {"class": lambda c: c and "lineup__odds-item" in " ".join(c if isinstance(c, list) else [c])}):
                label_el = item.find("b")
                if not label_el or "SPREAD" not in label_el.get_text(strip=True).upper():
                    continue
                # Prefer draftkings is-selected, then fanduel, then composite
                val_el = None
                for cls in ("draftkings", "fanduel", "composite"):
                    val_el = item.find("span", {"class": lambda c, b=cls: c and b in (c if isinstance(c, list) else c.split())})
                    if val_el:
                        break
                if not val_el:
                    continue
                raw = val_el.get_text(strip=True)
                nums = _re.findall(r"[-+]?\d+\.?\d*", raw)
                if nums:
                    spreads[game_key] = abs(float(nums[-1]))
                    break

        print(f"  RotoWire spreads: {len(spreads)} games")
        for k, v in spreads.items():
            print(f"    {k}: spread {v}")
    except Exception as e:
        print(f"  RotoWire spread error: {e}")
    return spreads



def fetch_lineups():
    """
    Scrape lineups + O/U totals from RotoGrinders.
    Structure confirmed from page source.
    Returns {player_name: {team, role, status, pos, ou_total}}
    """
    print("  Fetching lineups from RotoGrinders...")
    lineups = {}
    game_totals = {}  # "AWAY_HOME" -> ou_total
    try:
        r = requests.get(
            "https://rotogrinders.com/lineups/nba",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "text/html,*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://rotogrinders.com/",
            },
            timeout=20,
        )
        if r.status_code != 200:
            print(f"  RotoGrinders failed: {r.status_code}")
            return {}

        soup = BeautifulSoup(r.text, "lxml")

        # Each game is a div.game-card
        game_cards = soup.find_all("div", {"class": lambda c: c and "game-card" in " ".join(c if isinstance(c, list) else [c]) and "module" in " ".join(c if isinstance(c, list) else [c])})

        for card in game_cards:
            # Get team abbreviations from data-abbr attributes
            team_nameplates = card.find_all("span", {"class": "team-nameplate-title"})
            team_abvs = [t.get("data-abbr", "").upper() for t in team_nameplates]
            if len(team_abvs) < 2:
                continue
            away_abv, home_abv = team_abvs[0], team_abvs[1]

            # Get O/U total
            ou_el = card.find("span", {"class": lambda c: c and "vegas-bar-total-points" in " ".join(c if isinstance(c, list) else [c])})
            ou_total = safe_float(ou_el.get_text(strip=True)) if ou_el else 0.0
            game_key = f"{away_abv}_{home_abv}"
            if ou_total:
                game_totals[game_key] = ou_total

            # Each game-card-lineups div has two lineup-card divs (away, home)
            lineups_container = card.find("div", {"class": lambda c: c and "game-card-lineups" in " ".join(c if isinstance(c, list) else [c])})
            if not lineups_container:
                continue
            lineup_cards = lineups_container.find_all("div", {"class": lambda c: c and "lineup-card" in " ".join(c if isinstance(c, list) else [c]) and "lineup-card-" not in " ".join(c if isinstance(c, list) else [c])})

            for card_idx, lc in enumerate(lineup_cards[:2]):
                team = away_abv if card_idx == 0 else home_abv

                # Starters — in first <ul> after "Starters" span
                starters_label = lc.find("span", string=lambda t: t and "Starters" in t)
                if starters_label:
                    starters_ul = starters_label.find_next("ul")
                    if starters_ul:
                        for li in starters_ul.find_all("li", {"class": "lineup-card-player"}):
                            a = li.find("a", {"class": "player-nameplate-name"})
                            if not a:
                                continue
                            name = a.get_text(strip=True)
                            span = li.find("span", {"class": "player-nameplate"})
                            pos_raw = span.get("data-position", "") if span else ""
                            pos = pos_raw.split("/")[0].strip() if pos_raw else "SF"
                            lineups[name] = {"team": team, "role": "starter", "status": None, "pos": pos, "ou": ou_total}

                # Bench — in <ul> after "Bench" span
                bench_label = lc.find("span", {"class": lambda c: c and "lineup-card-bench" in " ".join(c if isinstance(c, list) else [c])})
                if bench_label:
                    bench_ul = bench_label.find_next("ul")
                    if bench_ul:
                        for li in bench_ul.find_all("li", {"class": "lineup-card-player"}):
                            a = li.find("a", {"class": "player-nameplate-name"})
                            if not a:
                                continue
                            name = a.get_text(strip=True)
                            span = li.find("span", {"class": "player-nameplate"})
                            pos_raw = span.get("data-position", "") if span else ""
                            pos = pos_raw.split("/")[0].strip() if pos_raw else "SF"
                            lineups[name] = {"team": team, "role": "bench", "status": None, "pos": pos, "ou": ou_total}

        if lineups:
            starters = sum(1 for v in lineups.values() if v["role"] == "starter")
            print(f"  RotoGrinders: {len(lineups)} players ({starters} starters), {len(game_totals)} game totals")
            for gk, tot in game_totals.items():
                print(f"    {gk}: O/U {tot}")
        else:
            print("  RotoGrinders: 0 players found")

    except Exception as e:
        print(f"  RotoGrinders error: {e}")

    return lineups, game_totals


# ─────────────────────────────────────────────────────────────────────────────
# STEP 6: FETCH PLAYER GAME LOGS from balldontlie
# ─────────────────────────────────────────────────────────────────────────────

_bdl_player_id_cache = {}   # name -> bdl player id
_nba_player_list_cache = None  # cached NBA.com player list
_nba_player_pos_cache  = {}    # name (lower) -> position string

# Hardcoded 2024-25 NBA player positions (saves API calls)
_PLAYER_POS_MAP = {
    # Guards
    "shai gilgeous-alexander":"PG","tyrese haliburton":"PG","luka doncic":"PG",
    "jalen brunson":"PG","trae young":"PG","damian lillard":"PG","stephen curry":"PG",
    "james harden":"PG","fred vanvleet":"PG","tyrese maxey":"PG","lamelo ball":"PG",
    "dejounte murray":"PG","kyrie irving":"PG","ja morant":"PG","josh giddey":"PG",
    "cade cunningham":"PG","jordan poole":"PG","darius garland":"PG","immanuel quickley":"PG",
    "markelle fultz":"PG","tre mann":"PG","landry shamet":"PG","jose alvarado":"PG",
    "alex caruso":"PG","cason wallace":"PG","isaiah joe":"PG","jared mccain":"PG",
    "cameron payne":"PG","kyle lowry":"PG","quentin grimes":"SG","scotty pippen jr.":"PG",
    "ty jerome":"PG","walter clayton jr.":"PG","brooks barnhizer":"PG",
    # Shooting Guards  
    "devin booker":"SG","donovan mitchell":"SG","bradley beal":"SG","zach lavine":"SG",
    "jaylen brown":"SG","mikal bridges":"SG","og anunoby":"SF","josh hart":"SF",
    "luguentz dort":"SG","aaron wiggins":"SG","rayan rupert":"SG","jaylen wells":"SG",
    "dominick barlow":"SF","justin edwards":"SG","trendon watford":"SF","dalen terry":"SF",
    "tyrese martin":"SG","pat connaughton":"SG","josh green":"SG",
    # Forwards
    "lebron james":"SF","kevin durant":"SF","giannis antetokounmpo":"PF",
    "kawhi leonard":"SF","paul george":"SF","jimmy butler":"SF","jayson tatum":"SF",
    "julius randle":"PF","pascal siakam":"PF","brandon ingram":"SF","demar derozan":"SF",
    "miles bridges":"SF","brandon miller":"SF","grant williams":"PF","jeremy sochan":"PF",
    "olivier-maxence prosper":"SF","gg jackson":"PF","santi aldama":"PF",
    "jabari walker":"PF","kenrich williams":"SF","jaylin williams":"PF",
    "payton sandfort":"SF","tidjane salaun":"SF","kon knueppel":"SF",
    # Power Forwards / Centers
    "joel embiid":"C","nikola jokic":"C","karl-anthony towns":"C","bam adebayo":"C",
    "anthony davis":"C","rudy gobert":"C","brook lopez":"C","myles turner":"C",
    "jarrett allen":"C","chet holmgren":"C","isaiah hartenstein":"C","mitchell robinson":"C",
    "moussa diabate":"C","andre drummond":"C","adem bona":"C","ryan kalkbrenner":"C",
    "ariel hukporti":"C","brandon clarke":"C","taylor hendricks":"PF",
    # Additional
    "malcolm brogdon":"SG","jordan clarkson":"SG","kevin mccullar jr.":"SG",
    "tyler kolek":"PG","vjEdgecombe":"SG","vj edgecombe":"SG",
}

def _find_bdl_player(name):
    """Find player ID in balldontlie by name."""
    if name in _bdl_player_id_cache:
        return _bdl_player_id_cache[name]

    # Search by last name
    last = name.split()[-1]
    data = bdl_get("players", params={"search": last, "per_page": 25})
    if not data:
        return None

    name_lower = name.lower()
    best = None
    for p in data.get("data", []):
        full = f"{p.get('first_name','')} {p.get('last_name','')}".strip().lower()
        if full == name_lower:
            best = p["id"]
            break
        # partial match fallback
        if name_lower in full or full in name_lower:
            best = p["id"]

    _bdl_player_id_cache[name] = best
    return best


NBA_STATS_HEADERS = {
    "User-Agent":         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer":            "https://www.nba.com/",
    "Accept":             "application/json",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token":  "true",
}

def _get_nba_player_list():
    """Fetch and cache the full NBA.com active player list once."""
    global _nba_player_list_cache
    if _nba_player_list_cache is not None:
        return _nba_player_list_cache

    print("  📋 Loading NBA.com player list (one-time)...")
    try:
        time.sleep(1.0)
        r = requests.get(
            "https://stats.nba.com/stats/commonallplayers",
            headers=NBA_STATS_HEADERS,
            params={"LeagueID": "00", "Season": "2024-25", "IsOnlyCurrentSeason": "0"},
            timeout=20,
        )
        if r.status_code != 200:
            print(f"  ⚠️  NBA.com player list failed: {r.status_code}")
            _nba_player_list_cache = []
            return []

        result_sets = r.json().get("resultSets", [])
        if not result_sets:
            _nba_player_list_cache = []
            return []

        ps       = result_sets[0]
        hdrs     = ps.get("headers", [])
        rows     = ps.get("rowSet", [])
        name_idx = hdrs.index("DISPLAY_FIRST_LAST") if "DISPLAY_FIRST_LAST" in hdrs else None
        id_idx   = hdrs.index("PERSON_ID") if "PERSON_ID" in hdrs else None

        if name_idx is None or id_idx is None:
            _nba_player_list_cache = []
            return []

        pos_idx = hdrs.index("POSITION") if "POSITION" in hdrs else None
        _nba_player_list_cache = [(str(row[id_idx]), str(row[name_idx]).lower()) for row in rows]
        print(f"  ✅ {len(_nba_player_list_cache)} players loaded from NBA.com")
        return _nba_player_list_cache

    except Exception as e:
        print(f"  ⚠️  NBA.com player list error: {e}")
        _nba_player_list_cache = []
        return []


def fetch_player_logs(player_name):
    """
    Get last 10 game logs from NBA.com stats API (free, no key).
    Returns (last10_games, min_avg, min_l10) or None if insufficient data.
    """
    player_list = _get_nba_player_list()
    if not player_list:
        return None

    # Find NBA.com player ID by name match
    name_lower = player_name.lower()
    nba_player_id = None
    for pid, pname in player_list:
        if pname == name_lower or name_lower in pname or pname in name_lower:
            nba_player_id = pid
            break

    if not nba_player_id:
        return None

    name_lower = player_name.lower()

    try:
        time.sleep(0.8)
        r = requests.get(
            "https://stats.nba.com/stats/playergamelog",
            headers=NBA_STATS_HEADERS,
            params={
                "PlayerID":   nba_player_id,
                "Season":     "2024-25",
                "SeasonType": "Regular Season",
            },
            timeout=15,
        )
        if r.status_code != 200:
            return None

        log_sets = r.json().get("resultSets", [])
        if not log_sets:
            return None

        log_set     = log_sets[0]
        log_headers = log_set.get("headers", [])
        log_rows    = log_set.get("rowSet", [])

        pts_idx = log_headers.index("PTS") if "PTS" in log_headers else None
        reb_idx = log_headers.index("REB") if "REB" in log_headers else None
        ast_idx = log_headers.index("AST") if "AST" in log_headers else None
        min_idx = log_headers.index("MIN") if "MIN" in log_headers else None

        if None in (pts_idx, reb_idx, ast_idx, min_idx):
            return None

        played = []
        for row in log_rows:  # NBA.com returns most recent first
            mins_str = str(row[min_idx] or "0")
            try:
                mins = float(mins_str.split(":")[0]) if ":" in mins_str else float(mins_str)
            except:
                mins = 0
            if mins >= 5:
                played.append({
                    "pts": int(row[pts_idx] or 0),
                    "reb": int(row[reb_idx] or 0),
                    "ast": int(row[ast_idx] or 0),
                    "min": mins,
                })

        if len(played) < MIN_GAMES_PLAYED:
            return None

        last10  = played[:10]
        min_l10 = round(sum(g["min"] for g in last10) / len(last10), 1)
        min_avg = round(sum(g["min"] for g in played) / len(played), 1)

        last10_clean = [{"pts": g["pts"], "reb": g["reb"], "ast": g["ast"]} for g in last10]
        while len(last10_clean) < 10:
            last10_clean.append(last10_clean[-1])

        return last10_clean, min_avg, min_l10

    except Exception as e:
        print(f"        ⚠️  NBA.com game log error for {player_name}: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# STEP 7: FETCH TEAM ROSTER from balldontlie
# ─────────────────────────────────────────────────────────────────────────────

def fetch_team_roster(bdl_team_id, team_abv):
    """
    Returns list of active players via balldontlie /players endpoint.
    Filters to current season (2024) and the given team.
    """
    # balldontlie team ID map
    BDL_TEAM_IDS = {
        "ATL":1,"BOS":2,"BKN":3,"CHA":4,"CHI":5,"CLE":6,"DAL":7,"DEN":8,
        "DET":9,"GSW":10,"HOU":11,"IND":12,"LAC":13,"LAL":14,"MEM":15,
        "MIA":16,"MIL":17,"MIN":18,"NOP":19,"NYK":20,"OKC":21,"ORL":22,
        "PHI":23,"PHX":24,"POR":25,"SAC":26,"SAS":27,"TOR":28,"UTA":29,"WAS":30,
    }
    team_id = BDL_TEAM_IDS.get(team_abv)
    if not team_id:
        return []
    try:
        data = bdl_get("/players", params={"team_ids[]": team_id, "per_page": 50, "seasons[]": 2025})
        if not data:
            return []
        players = []
        for p in data.get("data", []):
            first = p.get("first_name","").strip()
            last  = p.get("last_name","").strip()
            name  = f"{first} {last}".strip()
            pos_raw = p.get("position","") or ""
            pos = POS_MAP.get(pos_raw.split("-")[0], "SF") if pos_raw else "SF"
            if name and len(name) > 3:
                players.append({"name": name, "pos": pos})
        return players
    except Exception as e:
        print(f"  Roster fetch error for {team_abv}: {e}")
        return []


# ─────────────────────────────────────────────────────────────────────────────
# STEP 8: COMPUTE MATCHUP EDGES
# ─────────────────────────────────────────────────────────────────────────────

def compute_edges(player_l10_avg, opp_team, dvp, pos="SF"):
    def rank_to_edge(rank):
        if rank >= 27: return 3.8
        if rank >= 24: return 3.0
        if rank >= 21: return 2.2
        if rank >= 18: return 1.5
        if rank >= 15: return 1.0
        if rank >= 12: return 0.5
        if rank >= 8:  return 0.2
        return 0.0

    team_dvp = dvp.get(opp_team, {})
    return {
        "pts": round(rank_to_edge(team_dvp.get(f"{pos}_pts", team_dvp.get("pts", 15))), 1),
        "reb": round(rank_to_edge(team_dvp.get(f"{pos}_reb", team_dvp.get("reb", 15))), 1),
        "ast": round(rank_to_edge(team_dvp.get(f"{pos}_ast", team_dvp.get("ast", 15))), 1),
    }


# ─────────────────────────────────────────────────────────────────────────────
# STEP 9: ESTIMATE FD LINES
# ─────────────────────────────────────────────────────────────────────────────

def estimate_fd_lines(l10_avg, opp_dvp=None):
    """
    Pick best prop category based purely on player's L10 stat profile.
    DVP is used as a tiebreaker/boost, not the primary driver.
    """
    pts  = l10_avg.get("pts", 0)
    reb  = l10_avg.get("reb", 0)
    ast  = l10_avg.get("ast", 0)
    pra  = pts + reb + ast
    BOOK_SHADE = 0.96
    pr = pts + reb
    pa = pts + ast
    ra = reb + ast

    # Pure stat-based category selection
    # Single stat: player clearly dominates in one area
    if pts >= 18 and pts > reb * 2.5 and pts > ast * 2.5:
        return "P",   round(pts * BOOK_SHADE * 2) / 2
    elif reb >= 8 and reb > pts * 0.4 and reb >= ast * 1.5:
        return "R",   round(reb * BOOK_SHADE * 2) / 2
    elif ast >= 6 and ast > reb and pts < 18:
        return "A",   round(ast * BOOK_SHADE * 2) / 2
    elif pts >= 12 and reb >= 6 and ast < 5:
        return "PR",  round(pr  * BOOK_SHADE * 2) / 2
    elif pts >= 12 and ast >= 5 and reb < 6:
        return "PA",  round(pa  * BOOK_SHADE * 2) / 2
    elif reb >= 6 and ast >= 4 and pts < 12:
        return "RA",  round(ra  * BOOK_SHADE * 2) / 2
    elif pts >= 10:
        return "P",   round(pts * BOOK_SHADE * 2) / 2
    else:
        return "PRA", round(pra * BOOK_SHADE * 2) / 2


# ─────────────────────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────────────────────────

def run_pipeline():
    print("\n" + "="*60)
    print("  NBA PROPS PIPELINE  (100% Free APIs)")
    print(f"  {TODAY_FMT}")
    print("="*60 + "\n")

    # ── Fetch schedule ────────────────────────────────────────────────────────
    games_meta, team_id_map = fetch_games()
    if not games_meta:
        print("❌ No games found today.")
        sys.exit(1)

    # ── Fetch supporting data ─────────────────────────────────────────────────
    dvp      = fetch_dvp()
    dvp      = fetch_pace(dvp)
    injuries = fetch_injuries()
    lineups, game_totals = fetch_lineups()
    spreads = fetch_spreads()
    for g in games_meta:
        gid = g["id"]
        if gid in game_totals:
            g["ou"] = game_totals[gid]
        if gid in spreads:
            g["spread"] = spreads[gid]
        if g.get("ou") or g.get("spread"):
            print(f"  Game meta: {gid} O/U={g.get('ou',0)} spread={g.get('spread',0)}")

    # ── Build RAW_PLAYERS per game ────────────────────────────────────────────
    RAW_PLAYERS = {}
    GAMES_META  = []

    for g in games_meta:
        game_id      = g["id"]
        away_abv     = g["away"]
        home_abv     = g["home"]
        away_bdl_id  = g.get("_away_bdl_id")
        home_bdl_id  = g.get("_home_bdl_id")

        clean_g = {k: v for k, v in g.items() if not k.startswith("_")}
        GAMES_META.append(clean_g)

        print(f"\n🏀 Processing {away_abv} @ {home_abv}...")
        game_players = []

        # Use lineups if available, otherwise fall back to NBA.com rosters
        game_lineup = {nm: li for nm, li in lineups.items()
                       if li.get("team") in (away_abv, home_abv)} if lineups else {}

        if not game_lineup:
            print(f"  Lineups not posted — fetching rosters from balldontlie...")
            for team_abv_r in (away_abv, home_abv):
                roster = fetch_team_roster(None, team_abv_r)
                # Take first 15 — scrubs filtered later by MIN_MINUTES_THRESHOLD
                for i, p in enumerate(roster[:15]):
                    game_lineup[p["name"]] = {
                        "team":   team_abv_r,
                        "role":   "starter" if i < 5 else "bench",
                        "status": None,
                    }
            print(f"  Got {len(game_lineup)} players from rosters")

        # ── Identify OUT players per team for usage boost logic ──────────────
        out_players = {}
        for nm, li in game_lineup.items():
            t = li.get("team", "")
            if t not in (away_abv, home_abv):
                continue
            inj_status = li.get("status")
            if not inj_status:
                for inj_name, inj_s in injuries.items():
                    if nm.lower() in inj_name.lower() or inj_name.lower() in nm.lower():
                        inj_status = inj_s
                        break
            if inj_status == "OUT":
                out_players.setdefault(t, []).append(nm)

        # Filter to players on either team in this game
        for name, lineup_info in game_lineup.items():
            team_abv = lineup_info.get("team", "")
            if team_abv not in (away_abv, home_abv):
                continue

            # Position: from lineup (most accurate), then hardcoded map, then default
            pos = (lineup_info.get("pos") or 
                   _PLAYER_POS_MAP.get(name.lower()) or 
                   _nba_player_pos_cache.get(name.lower(), "SF"))
            opp = home_abv if team_abv == away_abv else away_abv
            role = lineup_info.get("role", "bench")
            inj  = lineup_info.get("status")

            # Cross-reference injury report
            if not inj:
                for inj_name, inj_status in injuries.items():
                    if name.lower() in inj_name.lower() or \
                       inj_name.lower() in name.lower():
                        inj = inj_status
                        break

            if inj == "OUT":
                print(f"     ⛔ {name} — OUT, skipping")
                continue

            # Fetch game logs
            print(f"     📊 {name} ({team_abv}, {role}{' ' + inj if inj else ''})...")
            result = fetch_player_logs(name)
            if not result:
                print(f"        ⚠️  Insufficient data — skipping")
                continue

            last10_games, min_avg, min_l10 = result

            if min_l10 < MIN_MINUTES_THRESHOLD:
                print(f"        ⚠️  {min_l10} min/g L10 — below threshold, skipping")
                continue

            l10_avg = {
                "pts": round(sum(g2["pts"] for g2 in last10_games) / len(last10_games), 1),
                "reb": round(sum(g2["reb"] for g2 in last10_games) / len(last10_games), 1),
                "ast": round(sum(g2["ast"] for g2 in last10_games) / len(last10_games), 1),
            }

            # ── Usage boost: redistribute minutes/stats from OUT players ──
            team_out = out_players.get(team_abv, [])
            usage_boost = 0.0
            usage_note  = []

            if team_out and role in ("starter", "bench"):
                # Get active starters on this team (excluding current player)
                team_starters = [
                    nm for nm, li in game_lineup.items()
                    if li.get("team") == team_abv
                    and li.get("role") == "starter"
                    and nm != name
                    and li.get("status") != "OUT"
                ]
                team_active = [
                    nm for nm, li in game_lineup.items()
                    if li.get("team") == team_abv
                    and nm != name
                    and li.get("status") != "OUT"
                ]

                for out_name in team_out:
                    # Primary beneficiary = same-pos starter + highest-min active player
                    # We split the boost between them (both = this player qualifies both ways)
                    is_starter        = role == "starter"
                    is_highest_active = (len(team_active) > 0 and
                                         team_active[0] == name)  # first = most prominent

                    if is_starter and is_highest_active:
                        boost = 0.12   # both criteria — full primary
                    elif is_starter or is_highest_active:
                        boost = 0.08   # one criteria — shared primary
                    else:
                        boost = 0.04   # secondary beneficiary

                    usage_boost += boost
                    usage_note.append(f"{out_name.split()[-1]} OUT")

            # Check for returning starters (GTD) — reduces boost for players who benefited
            gtd_penalty = 0.0
            for tm2 in game_players:
                if tm2["name"] == name:
                    continue
                if tm2.get("role") == "starter" and tm2.get("inj") == "GTD":
                    # A starter returning reduces usage for bench beneficiaries
                    if role == "bench":
                        gtd_penalty += 0.06  # give back ~half the gained usage
                    else:
                        gtd_penalty += 0.02
            usage_boost = max(0, usage_boost - gtd_penalty)

            # Cap total usage boost at 18% — realistic redistribution ceiling
            usage_boost = min(usage_boost, 0.18)

            if usage_boost > 0:
                # Apply boost to l10_avg
                l10_avg = {
                    "pts": round(l10_avg["pts"] * (1 + usage_boost), 1),
                    "reb": round(l10_avg["reb"] * (1 + usage_boost), 1),
                    "ast": round(l10_avg["ast"] * (1 + usage_boost), 1),
                }
                # Also boost last10_games for sparkline accuracy
                last10_games = [
                    {
                        "pts": round(g2["pts"] * (1 + usage_boost)),
                        "reb": round(g2["reb"] * (1 + usage_boost)),
                        "ast": round(g2["ast"] * (1 + usage_boost)),
                    }
                    for g2 in last10_games
                ]
                print(f"        ++ Usage boost +{usage_boost*100:.0f}% ({', '.join(usage_note)})")

            edges      = compute_edges(l10_avg, opp, dvp, pos=pos)
            opp_dvp_full = dvp.get(opp, {})
            # Use position-specific DVP if available
            pos_dvp = {
                "pts":  opp_dvp_full.get(f"{pos}_pts", opp_dvp_full.get("pts", 15)),
                "reb":  opp_dvp_full.get(f"{pos}_reb", opp_dvp_full.get("reb", 15)),
                "ast":  opp_dvp_full.get(f"{pos}_ast", opp_dvp_full.get("ast", 15)),
                "pace": opp_dvp_full.get("pace", 112.0),
            }
            fd_cat, fd_line = estimate_fd_lines(l10_avg, opp_dvp=pos_dvp)
            print(f"        -> {name}: pts={l10_avg['pts']} reb={l10_avg['reb']} ast={l10_avg['ast']} => {fd_cat}")

            # Build note
            note_parts = []
            if usage_note:
                pct = f"+{usage_boost*100:.0f}%"
                note_parts.append(f"Usage boost {pct} ({', '.join(usage_note)})")
            last_pra = last10_games[0]["pts"] + last10_games[0]["reb"] + last10_games[0]["ast"]
            l10_pra  = l10_avg["pts"] + l10_avg["reb"] + l10_avg["ast"]
            if last_pra < l10_pra * 0.78:
                note_parts.append(f"Bounce-back ({last_pra} PRA last game vs {l10_pra:.0f} avg)")
            if min_l10 > min_avg * 1.15:
                note_parts.append(f"Minutes trending up ({min_avg}->{min_l10})")
            ou_total = lineup_info.get("ou", 0.0)
            opp_dvp = dvp.get(opp, {})
            pos_dvp_pts = opp_dvp.get(f"{pos}_pts", opp_dvp.get("pts", 0))
            pos_dvp_reb = opp_dvp.get(f"{pos}_reb", opp_dvp.get("reb", 0))
            pos_dvp_ast = opp_dvp.get(f"{pos}_ast", opp_dvp.get("ast", 0))
            if pos_dvp_pts >= 24:
                note_parts.append(f"{opp} #{pos_dvp_pts} vs {pos} pts")
            elif pos_dvp_reb >= 24:
                note_parts.append(f"{opp} #{pos_dvp_reb} vs {pos} reb")
            elif pos_dvp_ast >= 24:
                note_parts.append(f"{opp} #{pos_dvp_ast} vs {pos} ast")
            # Add O/U total note
            if ou_total >= 230:
                note_parts.append(f"High O/U {ou_total} — shootout potential")
            elif ou_total >= 220:
                note_parts.append(f"O/U {ou_total}")

            # Add pace note if game pace is high
            opp_pace = opp_dvp.get("pace", 112.0)
            team_pace = dvp.get(team_abv, {}).get("pace", 112.0)
            avg_pace  = (opp_pace + team_pace) / 2
            if avg_pace >= 115:
                note_parts.append(f"Fast pace ({avg_pace:.0f} possessions)")
            elif avg_pace >= 113:
                note_parts.append(f"Above avg pace ({avg_pace:.0f})")

            note = " | ".join(note_parts) if note_parts else f"{pos} vs {opp}"

            game_players.append({
                "name":         name,
                "team":         team_abv,
                "opp":          opp,
                "pos":          pos,
                "role":         role,
                "inj":          inj,
                "last10_games": last10_games,
                "min_avg":      min_avg,
                "min_l10":      min_l10,
                "edges":        edges,
                "fd_line_cat":  fd_cat,
                "fd_line":      fd_line,
                "note":         note,
            })

        if game_players:
            RAW_PLAYERS[game_id] = game_players
            print(f"  ✅ {len(game_players)} players added for {away_abv} @ {home_abv}")
        else:
            print(f"  ⚠️  No players found for {away_abv} @ {home_abv}")

    # ── Cache ─────────────────────────────────────────────────────────────────
    cache = {
        "fetched_at":  datetime.now().isoformat(),
        "games_meta":  GAMES_META,
        "dvp":         dvp,
        "raw_players": RAW_PLAYERS,
    }
    with open("nba_props_cache.json", "w") as f:
        json.dump(cache, f, indent=2)
    print(f"\n💾 Data cached to nba_props_cache.json")

    return GAMES_META, dvp, RAW_PLAYERS


# ─────────────────────────────────────────────────────────────────────────────
# INJECT INTO ENGINE AND RUN
# ─────────────────────────────────────────────────────────────────────────────

def inject_and_run(games_meta, dvp, raw_players):
    print("\n⚙️  Running analysis engine...")

    with open("nba_props_engine.py", encoding="utf-8") as f:
        engine = f.read()

    def to_py(obj):
        """Convert JSON string to Python-safe literal (null->None, true->True, false->False)."""
        s = json.dumps(obj, indent=4, ensure_ascii=True)
        s = s.replace(': null', ': None').replace(': true', ': True').replace(': false', ': False')
        s = s.replace('[null]', '[None]').replace(', null', ', None').replace('[null,', '[None,')
        return s

    games_json   = to_py(games_meta)
    dvp_json     = to_py(dvp)
    players_json = to_py(raw_players)

    # Inject data by line number (avoids regex/encoding issues)
    # Engine structure: GAMES_META lines 27-40, DEF lines 48-69, RAW_PLAYERS lines 103-146
    eng_lines = engine.splitlines(keepends=True)
    
    # Find sections by scanning for exact start lines
    games_s = next((i for i,l in enumerate(eng_lines) if l.startswith('GAMES_META = [')), None)
    games_e = next((i for i,l in enumerate(eng_lines) if i > (games_s or 0) and l.startswith(']')), None)
    def_s   = next((i for i,l in enumerate(eng_lines) if l.startswith('DEF = {')), None)
    def_e   = next((i for i,l in enumerate(eng_lines) if i > (def_s or 0) and l.startswith('}')), None)
    raw_s   = next((i for i,l in enumerate(eng_lines) if l.startswith('RAW_PLAYERS = {')), None)
    # Find end of RAW_PLAYERS by locating the ENGINE section comment
    raw_e   = next((i-1 for i,l in enumerate(eng_lines) if i > (raw_s or 0) and '# ENGINE' in l and '====' in l), None)
    # Fall back: find closing } on its own line
    if raw_e is None:
        raw_e = next((i for i,l in enumerate(eng_lines) if i > (raw_s or 0) + 10 and l.strip() == '}'), None)

    if None in (games_s, games_e, def_s, def_e, raw_s, raw_e):
        print(f"  ⚠️  Could not locate engine sections: {games_s},{games_e},{def_s},{def_e},{raw_s},{raw_e}")
    else:
        new_lines = (
            eng_lines[:games_s] +
            [f'GAMES_META = {games_json}\n'] +
            eng_lines[games_e+1:def_s] +
            [f'DEF = {dvp_json}\n'] +
            eng_lines[def_e+1:raw_s] +
            [f'RAW_PLAYERS = {players_json}\n'] +
            eng_lines[raw_e+1:]
        )
        engine = ''.join(new_lines)
        # Fix JSON nulls/booleans to Python equivalents

    # # SCRUB_BAD_ONCLICK_LINES
    _lines = engine_code.split("\n")
    _lines = [l for l in _lines if not (
        'ctrl-btn' in l and 'onclick' in l and 'data-gid' not in l
        and 'function filt' not in l and 'function srt' not in l
    )]
    engine_code = "\n".join(_lines)

    with open("nba_props_engine_today.py", "w", encoding="utf-8") as f:
        f.write(engine)

    result = subprocess.run(
        [sys.executable, "nba_props_engine_today.py"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr[:500])

    return result.returncode == 0


# ─────────────────────────────────────────────────────────────────────────────
# CACHE REPLAY
# ─────────────────────────────────────────────────────────────────────────────

def run_from_cache():
    print("📂 Loading from cache...")
    with open("nba_props_cache.json") as f:
        cache = json.load(f)
    print(f"   Fetched at: {cache['fetched_at']}")
    return cache["games_meta"], cache["dvp"], cache["raw_players"]


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    use_cache = "--cache" in sys.argv

    if use_cache:
        games_meta, dvp, raw_players = run_from_cache()
    else:
        games_meta, dvp, raw_players = run_pipeline()

    success = inject_and_run(games_meta, dvp, raw_players)

    if success:
        DATE = datetime.now().strftime("%m%d")
        out  = f"nba_props_{DATE}.html"
        print(f"\n✅ Done! Report saved -> {out}")
        import platform
        opener = {"Darwin": "open", "Linux": "xdg-open", "Windows": "start"}.get(platform.system(), "open")
        subprocess.run([opener, out], check=False)
    else:
        print("\n❌ Engine run failed. Check nba_props_engine_today.py for errors.")
