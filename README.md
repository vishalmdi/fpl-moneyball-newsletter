# FPL Moneyball Newsletter 🏆⚽

A snarky, data-driven Fantasy Premier League (FPL) newsletter generator that crunches mini-league stats using the FPL API. Written in Python, it delivers witty insights on fixtures, player picks, captains, chips (including Assistant Manager), transfers, and more—perfect for FPL fanatics looking to roast their rivals or chase green arrows. Whether you're dodging red arrows or flexing differentials, this tool brings the banter to your mini-league.

## 🚀 Features

- **Live FPL Data**: Pulls fixtures, picks, transfers, and chips from the FPL API.
- **Mini-League Insights**:
  - 🥵 **Hot Picks**: Most-owned players (e.g., "Salah? Groundbreaking.").
  - ❄️ **Differentials**: Low-ownership punts (e.g., "Martínez: Lonely island vibes.").
  - 🎖️ **Captains**: Tracks armband trends and Chaos Captains (e.g., "Who hurt you, mate?").
  - 🎰 **Chips**: Spotlights Wildcard, Free Hit, and Assistant Manager, with stats (e.g., "Glasner: 49 points in 3 GWs, Palace fanboys?").
  - 🔄 **Transfers**: Highlights bandwagons and point-hit kings.
  - 😎 **Vibe Check**: Random FPL humor to set the mood.
- **Snarky Flair**: Packed with cheeky commentary for maximum fun.
- **Easy to Tweak**: Swap league IDs or Gameweeks in one line.

## 🛠️ Tech Stack

- **Python 3.8+**: Clean, modular code with error handling.
- **Requests**: Fetches live FPL API data.
- **Counter & Random**: Drives stats and randomized snark.
- **Minimal Dependencies**: Just `requests` for a lean setup.

## 📋 Requirements

- Python 3.8 or higher
- `requests` (see `requirements.txt`)

## 🏃‍♂️ Getting Started

Follow these steps to generate your own snarky FPL newsletter:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vishalmdi/fpl-moneyball-newsletter.git
   cd fpl-moneyball-newsletter

    Set Up a Virtual Environment (recommended):
    bash

python3 -m venv venv
source venv/bin/activate

2. **Install Dependencies**:

  bash
  pip install -r requirements.txt

3. **Run the Script**:

Open fpl_newsletter.py and set your mini-league ID (default: league_id = 378266).
Generate a newsletter for Gameweek 32:
bash

    python3 fpl_newsletter.py
    The snarky output will print to your console. Check for a preview.
    
4. **Customize**:
    Change league_id or gw in fpl_newsletter.py to target your mini-league or Gameweek.
    Tweak snark in am_snarks (e.g., add "Howe: St James’ fortress or bust?"), diff_snarks, or vibe_checks.
    Add new sections (e.g., "Biggest Flops") by extending analyze_gameweek_preview.

📈 Example Output

Here’s a taste of the newsletter’s vibe:
markdown
🌍 FPL Moneyball Newsletter - Gameweek 32 Preview 🌍
==================================================

Welcome to the chaos, managers! GW32 is here, and it’s time to flex those questionable decisions. Let’s dive into the mini-league madness.

❄️ Differentials: The Mavericks and Madlads
Low ownership, high hopes, probable benchings.
🟡 Emiliano Martínez Romero: 17.1% - Lonely island vibes—hope it pays off!
🟡 Gabriel dos Santos Magalhães: 17.1% - Dreaming of a clean sheet miracle?
🟡 William Saliba: 17.1% - Bold bet, but will they even start?

🎰 Chips in Play: Wild Moves or Snooze Fest? 🎰
Let’s see who’s burning their chips and who’s hoarding them like a dragon.
🟣 Assistant Manager: Rahul Bhandari (The RB XV), Siddharth Muthukali (The StretfordEnders), Vikrant Kamal (MountainGlory), Bharat Barki (winwincibles), Himanshu Poddar (GIGLAMESH) - Letting the robot pick your team? Lazy or genius?
    Top Assistant Manager: Oliver Glasner - 49 points in 3 GWs, chasing table bonuses or just Palace fanboys?

==================================================


🔮 Future Improvements

    Dynamic Manager Tracking: Capture actual Assistant Manager picks (e.g., Glasner vs. Howe) if FPL API exposes them.
    Fancier Outputs: Export newsletters to HTML, PDF, or email for easy sharing.
    Web App: Build a Flask or FastAPI frontend to generate newsletters online.
    Post-GW Analysis: Add a section for flops (e.g., "Who blanked?") or haul heroes.
    Tests: Add pytest for API response validation and snark randomization.

📜 License

This project is licensed under the . Feel free to use, modify, or share it (just don’t claim you wrote the snark!).

🙌 Acknowledgements

    Fantasy Premier League API for the data.
    FPL communities on Reddit, Discord, and Twitter/X for endless banter and inspiration.
    Every mini-league rival who’s ever benched a 20-point haul.

📬 Contact

Built by Vishal M. I’m a Python enthusiast and FPL addict. Reach out to collaborate, share FPL tips, or roast my captain picks:

    Email: vishal.jaiswal23@gmail.com

    LinkedIn: https://www.linkedin.com/in/vishal-jaiswal-68725113/

⭐️ Star this repo if you love FPL, Python, or snarky code! Happy Gameweek, you beautiful disasters!