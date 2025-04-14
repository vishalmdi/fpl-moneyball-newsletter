import requests
from collections import Counter
import random

def get_bootstrap_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch bootstrap data: {response.status_code}")
    return response.json()

def get_fixtures_data():
    url = "https://fantasy.premierleague.com/api/fixtures/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch fixtures data: {response.status_code}")
    return response.json()

def get_player_name_map(bootstrap_data):
    return {player['id']: f"{player['first_name']} {player['second_name']}" for player in bootstrap_data['elements']}

def get_team_name_map(bootstrap_data):
    return {team['id']: team['name'] for team in bootstrap_data['teams']}

def get_team_id_map(bootstrap_data):
    return {player['id']: player['team'] for player in bootstrap_data['elements']}

def get_minileague_members(league_id):
    url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch mini-league data: {response.status_code}")
    return response.json()['standings']['results']

def get_entry_picks(entry_id, gw):
    picks_url = f"https://fantasy.premierleague.com/api/entry/{entry_id}/event/{gw}/picks/"
    response = requests.get(picks_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch picks data for entry {entry_id}: {response.status_code}")
    return response.json()

def get_transfers(entry_id, gw):
    transfers_url = f"https://fantasy.premierleague.com/api/entry/{entry_id}/transfers/"
    response = requests.get(transfers_url)
    if response.status_code != 200:
        return []
    transfers = response.json()
    return [t for t in transfers if t['event'] == gw]

def get_entry_event(entry_id, gw):
    event_url = f"https://fantasy.premierleague.com/api/entry/{entry_id}/event/{gw}/picks/"
    response = requests.get(event_url)
    if response.status_code != 200:
        return {'entry_history': {'event_transfers_cost': 0}}
    return response.json()

def analyze_gameweek_preview(league_id, gw, newsletter_name="Moneyball"):
    bootstrap = get_bootstrap_data()
    fixtures = get_fixtures_data()
    player_names = get_player_name_map(bootstrap)
    team_names = get_team_name_map(bootstrap)
    team_id_map = get_team_id_map(bootstrap)
    members = get_minileague_members(league_id)

    captain_counter = Counter()
    chip_counter = Counter()
    player_counter = Counter()
    transfer_in_counter = Counter()
    transfer_out_counter = Counter()
    manager_data = []
    dgw_team_counts = Counter()
    hits_data = {}

    valid_chips = {'wildcard', 'freehit', 'bboost', '3xc', 'manager'}

    gw_fixtures = [f for f in fixtures if f['event'] == gw and not f['finished']]
    team_fixtures = Counter()
    for f in gw_fixtures:
        team_fixtures[f['team_h']] += 1
        team_fixtures[f['team_a']] += 1
    dgw_teams = [team_id for team_id, count in team_fixtures.items() if count >= 2]

    for m in members:
        entry_id = m.get('entry')
        if not entry_id:
            continue
        entry_name = m.get('entry_name', 'Unknown Team')
        player_name = m.get('player_name', 'Unknown Manager')

        if not entry_name.strip() or not player_name.strip():
            continue

        try:
            picks_data = get_entry_picks(entry_id, gw)
            picks = picks_data.get('picks', [])
            active_chip = picks_data.get('active_chip', None)
            if active_chip and active_chip in valid_chips:
                chip_counter[active_chip] += 1

            dgw_player_count = sum(1 for p in picks if team_id_map.get(p.get('element')) in dgw_teams)
            dgw_team_counts[dgw_player_count] += 1

            captain_id = None
            for p in picks:
                pid = p.get('element')
                if pid:
                    player_counter[pid] += 1
                    if p.get('is_captain'):
                        captain_id = pid
                        captain_counter[pid] += 1

            transfers = get_transfers(entry_id, gw)
            for t in transfers:
                transfer_in_counter[t['element_in']] += 1
                transfer_out_counter[t['element_out']] += 1

            event_data = get_entry_event(entry_id, gw)
            hits = event_data.get('entry_history', {}).get('event_transfers_cost', 0) // 4
            if hits > 0:
                hits_data[entry_id] = (player_name, entry_name, hits)

            manager_entry = {
                'entry_id': entry_id,
                'team': entry_name,
                'manager': player_name,
                'chip': active_chip,
                'captain_id': captain_id
            }
            required_keys = ['entry_id', 'team', 'manager']
            if all(k in manager_entry and manager_entry[k] for k in required_keys) and \
               isinstance(manager_entry['team'], str) and isinstance(manager_entry['manager'], str):
                manager_data.append(manager_entry)

        except Exception:
            continue

    if not manager_data:
        return "Error: No valid manager data collected. Check API responses or league settings."

    newsletter = [f"🌍 FPL {newsletter_name} Newsletter - Gameweek {gw} Preview 🌍"]
    newsletter.append(f"{'='*50}\n")
    newsletter.append(f"Welcome to the chaos, managers! GW{gw} is here, and it’s time to flex those questionable decisions. Let’s dive into the mini-league madness.")

    newsletter.append(f"\n⚽ GW{gw} Fixtures to Overthink ⚽")
    newsletter.append("Because nothing screams FPL like stressing over Southampton’s defense.")
    for f in gw_fixtures[:4]:
        home_team = team_names.get(f['team_h'], "Unknown")
        away_team = team_names.get(f['team_a'], "Unknown")
        newsletter.append(f"🔵 {home_team} v {away_team}")
    newsletter.append("")

    if dgw_teams:
        dgw_team_names = [team_names.get(tid, "Unknown") for tid in dgw_teams]
        newsletter.append(f"🔥 Double Gameweek Alert: Buckle Up! 🔥")
        newsletter.append(f"Teams: {', '.join(dgw_team_names)}")
        newsletter.append(f"Load up on Palace and Newcastle or regret it when your rival’s bench hauls.")
        dgw_stats = [f"{count} teams have {players} DGW players" for players, count in sorted(dgw_team_counts.items(), reverse=True) if count > 0]
        if dgw_stats:
            newsletter.append("Squad Breakdown (How Deep Are You?)")
            newsletter.extend([f"🟡 {stat}" for stat in dgw_stats])
        else:
            newsletter.append("🟡 Nobody’s brave enough for DGW players yet. Sad.")
        newsletter.append("")

    newsletter.append(f"📊 Mini-League Buzz: Who’s Basic, Who’s Brave? 📊")
    total_managers = len(manager_data)
    newsletter.append(f"🔥 Hot Picks (The Sheep Are Baa-ffled)")
    newsletter.append("These are the players you picked because Twitter told you to.")
    for pid, count in player_counter.most_common(3):
        player_name = player_names.get(pid, "Unknown")
        ownership = (count / total_managers) * 100
        snark = "Groundbreaking choice, folks." if "Salah" in player_name else "Bold, but we respect it." if ownership < 70 else "Yawn, next."
        newsletter.append(f"🟢 {player_name}: {ownership:.1f}% - {snark}")
    newsletter.append("")

    newsletter.append(f"❄️ Differentials: The Mavericks and Madlads")
    newsletter.append("Low ownership, high hopes, probable benchings.")
    differentials = [(pid, count) for pid, count in player_counter.items() if (count / total_managers) * 100 <= 20.0]
    if differentials:
        diff_snarks = [
            "Lonely island vibes—hope it pays off!",
            "Dreaming of a clean sheet miracle?",
            "Bold bet, but will they even start?",
            "Chasing unicorns, are we?",
            "One haul and you’re a legend. Or not."
        ]
        random.shuffle(diff_snarks)
        for i, (pid, count) in enumerate(sorted(differentials, key=lambda x: x[1], reverse=True)[:3]):
            player_name = player_names.get(pid, "Unknown")
            ownership = (count / total_managers) * 100
            snark = diff_snarks[i % len(diff_snarks)]
            newsletter.append(f"🟡 {player_name}: {ownership:.1f}% - {snark}")
    else:
        newsletter.append("🟡 No differentials? Y’all are allergic to fun.")
    newsletter.append("")

    newsletter.append(f"🎖️ Armband Buzz: Captain Chaos Unleashed 🎖️")
    newsletter.append("Who’s getting the armband? And who’s trolling?")
    if captain_counter:
        most_captained = captain_counter.most_common(1)[0]
        captain_name = player_names.get(most_captained[0], "Unknown")
        captain_count = most_captained[1]
        captain_pct = (captain_count / total_managers) * 100
        snark = "Safe as a 0-0 draw." if captain_pct > 50 else "Spicy, but we’re intrigued."
        newsletter.append(f"Top Captain: {captain_name} ({captain_pct:.1f}%, {captain_count}/{total_managers}) - {snark}")
        all_captains = [f"{player_names.get(pid, 'Unknown')}: {(count/total_managers)*100:.1f}% ({count})" for pid, count in captain_counter.most_common()]
        newsletter.append(f"All Captains: {', '.join(all_captains)}")
        chaos_captain = captain_counter.most_common()[-1] if len(captain_counter) > 1 else None
        if chaos_captain and chaos_captain[1] == 1:
            chaos_name = player_names.get(chaos_captain[0], "Unknown")
            chaos_manager = next((m['manager'] for m in manager_data if m['captain_id'] == chaos_captain[0]), "Unknown")
            newsletter.append(f"🏆 Chaos Captain Award: {chaos_manager} picks {chaos_name}! Who hurt you, mate?")
    else:
        newsletter.append("No captain data. Did everyone forget to set their team?")
    newsletter.append("")

    newsletter.append(f"🎰 Chips in Play: Wild Moves or Snooze Fest? 🎰")
    newsletter.append("Let’s see who’s burning their chips and who’s hoarding them like a dragon.")
    chip_users_by_type = {'wildcard': [], 'freehit': [], 'bboost': [], '3xc': [], 'manager': []}
    chip_captains = {'wildcard': Counter(), 'freehit': Counter(), 'bboost': Counter(), '3xc': Counter(), 'manager': Counter()}
    for m in manager_data:
        if not all(m.get(k) and isinstance(m[k], str) for k in ['manager', 'team']) or 'chip' not in m:
            continue
        if m['chip'] and m['chip'] in valid_chips:
            chip_users_by_type[m['chip']].append(f"{m['manager']} ({m['team']})")
            if m['captain_id']:
                chip_captains[m['chip']][m['captain_id']] += 1
    chip_displayed = False
    for chip in chip_users_by_type:
        if chip_users_by_type[chip]:
            chip_name = chip.replace('wildcard', 'Wildcard').replace('freehit', 'Free Hit').replace('bboost', 'Bench Boost').replace('3xc', 'Triple Captain').replace('manager', 'Assistant Manager')
            managers = ", ".join(chip_users_by_type[chip])
            snark = {
                'Wildcard': "Ripping up the squad? Brave or desperate?",
                'Free Hit': "One-week wonders or one-week blunders?",
                'Bench Boost': "Praying your bench doesn’t score 2 points total.",
                'Triple Captain': "Big swing! Hope it’s not a blank.",
                'Assistant Manager': "Letting the robot pick your team? Lazy or genius?"
            }.get(chip_name, "What even is this chip?")
            newsletter.append(f"🟣 {chip_name}: {managers} - {snark}")
            if chip_name == 'Assistant Manager':
                # Assume Glasner as top AM pick for DGW32 (based on external context)
                am_snarks = [
                    "49 points in 3 GWs, chasing table bonuses or just Palace fanboys?",
                    "Two games in DGW32, but City and Newcastle? Bold or bonkers?",
                    "Table bonus dreams, but will Palace upset the big boys?",
                    "Five fixtures in three GWs, banking on an Eagles miracle?"
                ]
                newsletter.append(f"    Top Assistant Manager: Oliver Glasner - {random.choice(am_snarks)}")
            elif chip_captains[chip]:
                top_captain = chip_captains[chip].most_common(1)[0]
                captain_name = player_names.get(top_captain[0], "Unknown")
                captain_count = top_captain[1]
                captain_snark = "Predictable." if "Salah" in captain_name or captain_count > 3 else "Bold move, let’s see it pay off."
                newsletter.append(f"    Top Captain: {captain_name} ({captain_count} picks) - {captain_snark}")
            chip_displayed = True
    if not chip_displayed:
        newsletter.append("🟣 No chips played. Y’all saving them for GW38 or what?")
    newsletter.append("")

    newsletter.append(f"🔄 Transfer Talk: In, Out, Shake It All About 🔄")
    newsletter.append("Who’s hopping on the bandwagon, and who’s jumping off?")
    if transfer_in_counter:
        top_in = transfer_in_counter.most_common(1)[0]
        snark = "Bandwagon’s full, mate." if top_in[1] > 5 else "Sneaky pick, we see you."
        newsletter.append(f"🟢 Most Transferred In: {player_names.get(top_in[0], 'Unknown')} ({top_in[1]} transfers) - {snark}")
    else:
        newsletter.append("🟢 No transfers in. Everyone’s too scared to press the button.")
    if transfer_out_counter:
        top_out = transfer_out_counter.most_common(1)[0]
        snark = "Harsh crowd!" if top_out[1] > 5 else "Guess they missed the memo."
        newsletter.append(f"🔴 Most Transferred Out: {player_names.get(top_out[0], 'Unknown')} ({top_out[1]} transfers) - {snark}")
    else:
        newsletter.append("🔴 No transfers out. Loyalty or laziness?")
    if hits_data:
        max_hits = max(hits_data.values(), key=lambda x: x[2])
        snark = "Your wallet’s crying, mate." if max_hits[2] > 2 else "Living dangerously, we love it."
        newsletter.append(f"👑 Hit King: {max_hits[0]} took {max_hits[2]} hits ({max_hits[1]}) - {snark}")
    else:
        newsletter.append("👑 No hits taken. Cowards or masterminds?")
    newsletter.append("")

    newsletter.append(f"😎 GW{gw} Vibe Check: What’s the Mood? 😎")
    vibe_checks = [
        f"Newcastle and Palace DGW? Load up or flop hard, no in-between. Assistant Managers are out here acting unwise.",
        "Captain roulette’s spinning, and half of you are still on Salah. Wake up, sheep!",
        f"{', '.join([team_names.get(tid, 'Unknown') for tid in dgw_teams])} are about to make or break your season. No pressure!",
        "Chips are popping, hits are dropping, and someone’s bench is about to outscore their XI. Classic FPL."
    ]
    newsletter.append(random.choice(vibe_checks))
    newsletter.append("")

    newsletter.append(f"🎉 Battle Stations: Time to Shine (or Hide) 🎉")
    newsletter.append(f"Good luck in GW{gw}, you beautiful disasters! May your differentials haul, your captains bang, and your rivals’ autosubs score zero!")
    newsletter.append(f"{'='*50}")

    return "\n".join(newsletter)

# Example usage
league_id = 378266
for gw in range(32, 33):
    print(analyze_gameweek_preview(league_id, gw))
    print("="*60)