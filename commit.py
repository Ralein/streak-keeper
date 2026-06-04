#!/usr/bin/env python3
"""
streak-keeper 🔥
Keeps your GitHub streak alive with daily auto-commits.
Generates random quotes, task logs, and journal entries.
"""

import random
import datetime
import json
import os
from pathlib import Path

# ─── Quotes Pool ───────────────────────────────────────────────────────────────
QUOTES = [
    ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
    ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Experience is the name everyone gives to their mistakes.", "Oscar Wilde"),
    ("In order to be irreplaceable, one must always be different.", "Coco Chanel"),
    ("Java is to JavaScript what car is to carpet.", "Chris Heilmann"),
    ("Knowledge is power.", "Francis Bacon"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Stay hungry, stay foolish.", "Steve Jobs"),
    ("Simplicity is the soul of efficiency.", "Austin Freeman"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("Any fool can write code that a computer can understand.", "Martin Fowler"),
    ("Debugging is twice as hard as writing the code.", "Brian Kernighan"),
    ("The most disastrous thing that you can ever learn is your first programming language.", "Alan Kay"),
    ("Programs must be written for people to read.", "Harold Abelson"),
    ("Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away.", "Antoine de Saint-Exupéry"),
    ("Every great developer you know got there by solving problems they were unqualified to solve.", "Patrick McKenzie"),
    ("One of my most productive days was throwing away 1000 lines of code.", "Ken Thompson"),
    ("Weeks of coding can save you hours of planning.", "Unknown"),
    ("A ship in harbor is safe, but that's not what ships are for.", "John A. Shedd"),
    ("You miss 100% of the shots you don't take.", "Wayne Gretzky"),
    ("Consistency is the true foundation of trust.", "Roy T. Bennett"),
    ("Small daily improvements over time lead to stunning results.", "Robin Sharma"),
    ("Done is better than perfect.", "Sheryl Sandberg"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
    ("Build something 100 people love, not something 1 million people kind of like.", "Paul Graham"),
    ("Move fast and learn things.", "Unknown"),
]

# ─── Random Task Logs ──────────────────────────────────────────────────────────
TASK_TEMPLATES = [
    "Reviewed and refactored legacy code",
    "Updated documentation",
    "Fixed a sneaky edge case bug",
    "Optimized database queries",
    "Wrote unit tests for core module",
    "Resolved merge conflicts",
    "Dependency updates and security patches",
    "Code review session completed",
    "Explored new library: {}".format(random.choice(["FastAPI", "Pydantic", "Rich", "Typer", "httpx", "Polars", "DuckDB", "Ruff"])),
    "Brainstormed architecture improvements",
    "Set up local dev environment tweaks",
    "Read through open issues and triaged",
    "Prototyped a new feature idea",
    "Cleaned up dead code and TODO comments",
    "Improved error handling and logging",
    "Performance profiling session",
    "Planned next sprint tasks",
    "Researched best practices",
    "Reviewed pull requests",
    "CI/CD pipeline maintenance",
]

# ─── Mood Emojis ───────────────────────────────────────────────────────────────
MOODS = ["🔥", "💪", "🚀", "✨", "🎯", "⚡", "🧠", "💡", "🌱", "🎉", "😤", "🛠️", "📚", "🤔", "😎"]


def get_part_of_day_info(hour):
    """Determine part of the day title and key based on current hour."""
    if 5 <= hour < 12:
        return "🌅 Morning Update", "Morning"
    elif 12 <= hour < 17:
        return "☀️ Afternoon Update", "Afternoon"
    elif 17 <= hour < 21:
        return "🌇 Evening Update", "Evening"
    elif 21 <= hour <= 23:
        return "🌙 Night Update", "Night"
    else:
        return "🌌 Midnight Update", "Midnight"


def generate_entry():
    ist_tz = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now = datetime.datetime.now(ist_tz)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    weekday = now.strftime("%A")
    week_num = now.strftime("%U")

    quote_text, quote_author = random.choice(QUOTES)
    mood = random.choice(MOODS)
    tasks = random.sample(TASK_TEMPLATES, k=random.randint(2, 4))
    energy = random.randint(60, 100)
    focus_score = random.randint(55, 100)

    part_of_day_title, part_of_day_key = get_part_of_day_info(now.hour)

    entry = {
        "date": date_str,
        "time": time_str,
        "weekday": weekday,
        "week": int(week_num),
        "mood": mood,
        "energy_level": energy,
        "focus_score": focus_score,
        "quote": {"text": quote_text, "author": quote_author},
        "tasks_completed": tasks,
        "streak_alive": True,
        "part_of_day": part_of_day_key,
        "part_of_day_title": part_of_day_title,
    }
    return entry


def write_daily_log(entry):
    """Write or append a human-readable daily log entry."""
    date_str = entry["date"]
    log_path = Path(f"logs/{date_str}.md")

    # Ensure directory exists
    log_path.parent.mkdir(parents=True, exist_ok=True)

    new_section = [
        f"## {entry['part_of_day_title']}",
        f"_Generated at {entry['time']} · Week {entry['week']} · Mood: {entry['mood']}_",
        "",
        "### 💬 Quote of the Day",
        f"> \"{entry['quote']['text']}\"",
        f"> — *{entry['quote']['author']}*",
        "",
        "### ✅ Tasks & Activity",
    ]
    for task in entry["tasks_completed"]:
        new_section.append(f"- {task}")

    new_section += [
        "",
        "### 📊 Stats",
        f"| Metric        | Score |",
        f"|---------------|-------|",
        f"| Energy Level  | {entry['energy_level']}% |",
        f"| Focus Score   | {entry['focus_score']}% |",
        "",
        "---",
    ]

    if log_path.exists():
        current_content = log_path.read_text(encoding="utf-8")
        if not current_content.endswith("\n"):
            current_content += "\n"
        log_path.write_text(current_content + "\n" + "\n".join(new_section), encoding="utf-8")
        print(f"📝 Appended daily log section to → {log_path}")
    else:
        lines = [
            f"# {entry['weekday']}, {date_str} 🔥",
            "",
            "_Auto-generated by streak-keeper 🔥_",
            "",
            "---",
            "",
        ] + new_section
        log_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"📝 Created new daily log → {log_path}")

    return log_path


def update_streak_json(entry):
    """Update the master streak tracking JSON."""
    streak_file = Path("streak.json")

    if streak_file.exists():
        data = json.loads(streak_file.read_text())
    else:
        data = {"total_days": 0, "started": entry["date"], "entries": []}

    # Avoid duplicate entries for same date
    existing_dates = {e["date"] for e in data["entries"]}
    if entry["date"] not in existing_dates:
        data["entries"].append(entry)
        data["total_days"] = len(data["entries"])
        data["last_commit"] = entry["date"]
        data["last_mood"] = entry["mood"]

    streak_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"📊 Updated streak.json → Day #{data['total_days']}")
    return data["total_days"]


def update_readme(entry, day_count):
    """Update the README with current streak info."""
    readme = Path("README.md")
    streak_bar = "🟩" * min(day_count, 30) + ("+" if day_count > 30 else "")

    content = f"""# 🔥 streak-keeper

> Keeping the GitHub streak alive, one commit at a time.

## Current Streak

| | |
|---|---|
| **Total Days** | {day_count} |
| **Last Active** | {entry['date']} ({entry['weekday']}) |
| **Today's Mood** | {entry['mood']} |
| **Last Quote** | *"{entry['quote']['text']}"* — {entry['quote']['author']} |

## Streak Grid (last 30 days)
{streak_bar}

## How it works
- A GitHub Action runs **5 times a day** (Morning, Afternoon, Evening, Night, and Midnight IST)
- It generates a daily log update with a quote, tasks, and stats for each run
- Commits and pushes automatically → streak never breaks 🚀
- You can also trigger it manually from your phone via GitHub Actions UI

## Manual trigger
Go to **Actions → Daily Streak Commit → Run workflow** on GitHub.

---
_Last updated: {entry['date']} at {entry['time']}_
"""
    readme.write_text(content, encoding="utf-8")
    print(f"📄 Updated README.md")


def main():
    print("🔥 streak-keeper starting...")
    entry = generate_entry()
    print(f"📅 Date: {entry['date']} | Mood: {entry['mood']} | Part of Day: {entry['part_of_day']}")

    write_daily_log(entry)
    day_count = update_streak_json(entry)
    update_readme(entry, day_count)

    # Set output for GitHub Actions workflow to use in commit message
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"part_of_day={entry['part_of_day']}\n")

    print(f"✅ Done! Day #{day_count} logged.")


if __name__ == "__main__":
    main()
