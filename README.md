# 🏋️ IronLog · Workout Planner

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Track · Plan · Dominate**

A brutalist dark-themed workout planner built with Streamlit. Plan your weekly training schedule, log every set, and visualize your personal records — all locally, no API keys required.

[![🚀 Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Open%20App-FF4500?style=for-the-badge)](https://nlp-workout-planner-iybcdrecktfl6wwdyk2mut.streamlit.app/)

</div>

---

## ✨ Features

- 📅 **Weekly Schedule Builder** — Assign exercises to each day, visualize your weekly load at a glance
- 📝 **Workout Logger** — Log sets, reps, and weight with optional notes; auto-detects today's plan
- 🏆 **Automatic PR Detection** — Instantly flags when you hit a new Personal Record
- 📈 **Progress Charts** — Weight progression over time with ⭐ PR markers and volume area fill
- 📊 **Weekly Volume Tracker** — Bar chart of total training volume across the last 12 weeks
- 📋 **Full History** — Filter by exercise and time period, grouped by date
- ⬇️ **CSV Export** — Download your full workout log anytime
- 💾 **Local Persistence** — All data saved to `ironlog_data.json`, no database needed
- 🔥 **Zero API Keys** — Completely free and offline-capable

---

## 🖥️ Screenshots

> *Dark brutalist UI with Bebas Neue typography and signature orange `#ff4500` accent*

| Schedule | Log Workout | Progress & PRs |
|----------|-------------|----------------|
| Weekly plan with today highlighted | Quick-log sets with PR alerts | Line chart + PR star markers |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ironlog-workout-planner.git
cd ironlog-workout-planner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run workout_planner.py
```

Open your browser at `http://localhost:8501` and start training.

---

## 📦 Dependencies

```txt
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
```

No external APIs. No accounts. No cost.

---

## 📁 Project Structure

```
ironlog-workout-planner/
│
├── workout_planner.py      # Main Streamlit app (single file)
├── requirements.txt        # Python dependencies
├── ironlog_data.json       # Auto-generated data file (gitignored)
└── README.md
```

> **Note:** `ironlog_data.json` is created automatically on first run and stores all your schedule, logs, and exercise library locally.

---

## 🗂️ App Tabs

### 📅 Schedule
Build your 7-day training plan. Select exercises per day from the library or add your own. Today's day is highlighted in orange. A bar chart shows how many exercises are planned per day.

### 📝 Log Workout
Log any set with exercise, sets, reps, weight (kg), and optional notes. The app surfaces today's scheduled exercises and shows your last 5 logged sets in real time. If you beat your previous max weight, a **PR banner** fires automatically.

### 📈 Progress & PRs
- **PR Cards** — max weight achieved for every exercise you've logged
- **Weight Progression Chart** — interactive line chart per exercise with PR star markers and volume area
- **Weekly Volume Bar Chart** — total volume (sets × reps × weight) across the last 12 weeks

### 📋 History
Full log of every set, filterable by exercise and time window (7 / 14 / 30 / 60 / 90 / 365 days). Entries are grouped by date. Export to CSV with one click.

---

## 💾 Data Model

All data lives in `ironlog_data.json`:

```json
{
  "schedule": {
    "Monday": ["Squat", "Deadlift"],
    "Tuesday": [],
    ...
  },
  "logs": [
    {
      "date": "2025-03-05",
      "exercise": "Bench Press",
      "sets": 4,
      "reps": 8,
      "weight": 80.0,
      "notes": "Felt strong",
      "volume": 2560.0,
      "is_pr": true
    }
  ],
  "exercises": ["Bench Press", "Squat", "Deadlift", ...]
}
```

---

## 🎨 Design

IronLog uses a **brutalist dark aesthetic** — raw, high-contrast, and gym-appropriate:

- **Fonts:** [Bebas Neue](https://fonts.google.com/specimen/Bebas+Neue) (display) + [Barlow](https://fonts.google.com/specimen/Barlow) (body)
- **Accent Color:** `#ff4500` (OrangeRed)
- **Background:** `#0a0a0a` near-black
- **Charts:** Plotly with transparent backgrounds and custom dark styling

All UI components (cards, pills, badges, log entries) are custom HTML/CSS injected via `st.markdown()`.

---

## 🌐 Deploy on Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `workout_planner.py`
5. Click **Deploy**

> ⚠️ On Streamlit Cloud, `ironlog_data.json` resets on each redeploy since the filesystem is ephemeral. For persistent cloud storage, consider connecting a database like Supabase or using `st.session_state` only.

---

## 🔧 Customization

**Add exercises to the library** — Use the sidebar input to add any custom exercise permanently to your library.

**Change weight unit** — Search for `kg` in `workout_planner.py` and replace with `lbs` throughout (labels and display only; the math is unit-agnostic).

**Adjust chart colors** — The accent color `#ff4500` appears in Plotly chart configs. Replace with any hex color for a different theme.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙌 Acknowledgements

Built with [Streamlit](https://streamlit.io), [Plotly](https://plotly.com/python/), and [Pandas](https://pandas.pydata.org/).

---

<div align="center">
  Made with 🔥 by a lifter, for lifters.<br/>
  <a href="https://nlp-workout-planner-iybcdrecktfl6wwdyk2mut.streamlit.app/">Try it live →</a>
</div>
