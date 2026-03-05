import streamlit as st
import json
import os
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path 


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IronLog · Workout Planner",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Data persistence ──────────────────────────────────────────────────────────
DATA_FILE = "ironlog_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "schedule": {
            "Monday": [], "Tuesday": [], "Wednesday": [],
            "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []
        },
        "logs": [],      # [{date, exercise, sets, reps, weight, notes}]
        "exercises": [   # predefined exercise library
            "Bench Press", "Squat", "Deadlift", "Overhead Press",
            "Barbell Row", "Pull-ups", "Push-ups", "Dips",
            "Bicep Curl", "Tricep Extension", "Lat Pulldown",
            "Leg Press", "Lunges", "Plank", "Romanian Deadlift",
            "Incline Bench Press", "Cable Fly", "Face Pull",
            "Hip Thrust", "Calf Raise"
        ]
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── Session state ─────────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Schedule"

data = st.session_state.data

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }

.stApp {
    background: #0a0a0a;
    color: #e0ddd8;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: 1px solid #1e1e1e;
}

/* Brand header */
.brand {
    text-align: center;
    padding: 10px 0 24px;
    border-bottom: 1px solid #1e1e1e;
    margin-bottom: 20px;
}
.brand-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 0.12em;
    background: linear-gradient(180deg, #ff4500 0%, #ff7043 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.brand-tagline {
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #444;
    margin-top: 4px;
}

/* Stat cards */
.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 20px;
}
.stat-card {
    background: #141414;
    border: 1px solid #1e1e1e;
    border-radius: 8px;
    padding: 14px;
    text-align: center;
}
.stat-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: #ff4500;
    line-height: 1;
}
.stat-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #555;
    margin-top: 3px;
}

/* Section headers */
.section-head {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 0.1em;
    color: #e0ddd8;
    border-left: 3px solid #ff4500;
    padding-left: 12px;
    margin: 24px 0 16px;
}

/* Day card */
.day-card {
    background: #141414;
    border: 1px solid #1e1e1e;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.day-card:hover { border-color: #333; }
.day-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 0.08em;
    color: #888;
    margin-bottom: 8px;
}
.day-name.today { color: #ff4500; }
.exercise-pill {
    display: inline-block;
    background: #1e1e1e;
    border-radius: 4px;
    padding: 3px 9px;
    font-size: 0.75rem;
    color: #aaa;
    margin: 2px;
}
.rest-day { color: #333; font-size: 0.8rem; font-style: italic; }

/* Log entry */
.log-entry {
    background: #141414;
    border: 1px solid #1e1e1e;
    border-left: 3px solid #ff4500;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.log-exercise { font-weight: 600; font-size: 0.95rem; color: #e0ddd8; }
.log-detail { font-size: 0.78rem; color: #666; margin-top: 2px; }
.log-weight {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: #ff4500;
    text-align: right;
    line-height: 1;
}
.log-weight-unit { font-size: 0.7rem; color: #555; letter-spacing: 0.1em; }

/* PR badge */
.pr-badge {
    display: inline-block;
    background: linear-gradient(135deg, #ff4500, #ff7043);
    color: white;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.8rem;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    border-radius: 3px;
    margin-left: 8px;
}

/* Buttons */
.stButton > button {
    background: #ff4500 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.45rem 1.4rem !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #e03d00 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(255,69,0,0.3) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div {
    background: #141414 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 6px !important;
    color: #e0ddd8 !important;
    font-family: 'Barlow', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #ff4500 !important;
    box-shadow: 0 0 0 2px rgba(255,69,0,0.15) !important;
}
.stSelectbox > div > div > div { color: #e0ddd8 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #111 !important;
    border-bottom: 1px solid #1e1e1e !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1rem !important;
    letter-spacing: 0.1em !important;
    color: #555 !important;
    background: transparent !important;
    border: none !important;
    padding: 10px 24px !important;
}
.stTabs [aria-selected="true"] {
    color: #ff4500 !important;
    border-bottom: 2px solid #ff4500 !important;
}

/* Multiselect */
[data-baseweb="tag"] {
    background: #ff4500 !important;
    border-radius: 4px !important;
}

/* Hide streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
hr { border-color: #1e1e1e !important; }

/* Plotly chart background */
.js-plotly-plot { background: transparent !important; }

/* Labels */
.stTextInput label, .stSelectbox label, .stNumberInput label,
.stMultiSelect label, .stTextArea label, .stDateInput label {
    color: #666 !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-name">IronLog</div>
        <div class="brand-tagline">Track · Plan · Dominate</div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    total_logs = len(data["logs"])
    unique_days = len(set(l["date"] for l in data["logs"])) if data["logs"] else 0
    
    # This week sessions
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_logs = [l for l in data["logs"] 
                 if datetime.strptime(l["date"], "%Y-%m-%d").date() >= week_start]
    week_sessions = len(set(l["date"] for l in week_logs))
    
    # Total volume this week
    week_vol = sum(l["sets"] * l["reps"] * l.get("weight", 0) for l in week_logs)

    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">{total_logs}</div>
            <div class="stat-label">Total Sets</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{unique_days}</div>
            <div class="stat-label">Days Trained</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{week_sessions}</div>
            <div class="stat-label">This Week</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{int(week_vol):,}</div>
            <div class="stat-label">Week Volume</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Add custom exercise
    st.markdown('<div style="font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;color:#555;margin-bottom:8px;">Add Exercise to Library</div>', unsafe_allow_html=True)
    new_ex = st.text_input("Exercise name", placeholder="e.g. Cable Row", label_visibility="collapsed")
    if st.button("+ Add to Library", use_container_width=True):
        if new_ex.strip() and new_ex.strip() not in data["exercises"]:
            data["exercises"].append(new_ex.strip())
            save_data(data)
            st.success(f"Added: {new_ex.strip()}")
            st.rerun()


# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:16px 0 8px;">
    <span style="font-family:'Bebas Neue',sans-serif;font-size:2.4rem;
                 letter-spacing:0.08em;color:#e0ddd8;">
        WORKOUT
    </span>
    <span style="font-family:'Bebas Neue',sans-serif;font-size:2.4rem;
                 letter-spacing:0.08em;color:#ff4500;margin-left:12px;">
        PLANNER
    </span>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📅  SCHEDULE", "📝  LOG WORKOUT", "📈  PROGRESS & PRS", "📋  HISTORY"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — WEEKLY SCHEDULE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-head">Weekly Training Schedule</div>', unsafe_allow_html=True)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today_name = date.today().strftime("%A")

    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        for day in days:
            exercises = data["schedule"].get(day, [])
            is_today = day == today_name
            day_class = "today" if is_today else ""
            today_indicator = " 🔥 TODAY" if is_today else ""

            pills = "".join([f'<span class="exercise-pill">{e}</span>' for e in exercises]) if exercises else '<span class="rest-day">Rest Day</span>'

            st.markdown(f"""
            <div class="day-card">
                <div class="day-name {day_class}">{day.upper()}{today_indicator}</div>
                <div>{pills}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-head" style="font-size:1.1rem;">Edit Day</div>', unsafe_allow_html=True)
        
        edit_day = st.selectbox("Select Day", days, key="edit_day")
        current = data["schedule"].get(edit_day, [])
        
        selected_exercises = st.multiselect(
            "Exercises",
            options=sorted(data["exercises"]),
            default=current,
            key="day_exercises"
        )

        # Custom exercise for this day
        custom_ex = st.text_input("Or type custom exercise", key="custom_day_ex", placeholder="e.g. Box Jumps")

        if st.button("💾 Save Day", use_container_width=True):
            final_list = list(selected_exercises)
            if custom_ex.strip():
                final_list.append(custom_ex.strip())
                if custom_ex.strip() not in data["exercises"]:
                    data["exercises"].append(custom_ex.strip())
            data["schedule"][edit_day] = final_list
            save_data(data)
            st.success(f"✅ {edit_day} saved!")
            st.rerun()

        if st.button("🗑 Clear Day", use_container_width=True):
            data["schedule"][edit_day] = []
            save_data(data)
            st.rerun()

        # Weekly overview chart
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        counts = [len(data["schedule"].get(d, [])) for d in days]
        short_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        colors = ["#ff4500" if d == today_name else "#2a2a2a" for d in days]

        fig = go.Figure(go.Bar(
            x=short_days, y=counts,
            marker_color=colors,
            marker_line_width=0,
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=20, b=0),
            height=160,
            font=dict(family="Barlow", color="#555"),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(showgrid=False, showticklabels=False),
            title=dict(text="Exercises per Day", font=dict(size=11, color="#555"), x=0),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LOG WORKOUT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-head">Log a Set</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        log_date = st.date_input("Date", value=date.today(), key="log_date")
        
        # Suggest today's exercises from schedule
        today_schedule = data["schedule"].get(date.today().strftime("%A"), [])
        
        exercise_options = sorted(data["exercises"])
        default_ex = exercise_options[0] if exercise_options else None
        
        exercise = st.selectbox("Exercise", exercise_options, key="log_exercise")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            sets = st.number_input("Sets", min_value=1, max_value=20, value=3, key="log_sets")
        with c2:
            reps = st.number_input("Reps", min_value=1, max_value=100, value=10, key="log_reps")
        with c3:
            weight = st.number_input("Weight (kg)", min_value=0.0, max_value=1000.0, value=0.0, step=2.5, key="log_weight")

        notes = st.text_input("Notes (optional)", placeholder="e.g. Felt strong today", key="log_notes")

        if st.button("🔥 Log Set", use_container_width=True):
            # Check if PR
            prev_logs = [l for l in data["logs"] if l["exercise"] == exercise]
            prev_max = max([l.get("weight", 0) for l in prev_logs], default=0)
            is_pr = weight > prev_max and weight > 0

            entry = {
                "date": str(log_date),
                "exercise": exercise,
                "sets": sets,
                "reps": reps,
                "weight": weight,
                "notes": notes,
                "volume": sets * reps * weight,
                "is_pr": is_pr,
            }
            data["logs"].append(entry)
            save_data(data)

            if is_pr:
                st.success(f"🏆 NEW PR! {exercise} — {weight} kg!")
            else:
                st.success(f"✅ Logged: {sets}×{reps} @ {weight}kg")
            st.rerun()

    with col2:
        if today_schedule:
            st.markdown(f"""
            <div style="background:#141414;border:1px solid #1e1e1e;border-top:3px solid #ff4500;
                        border-radius:8px;padding:16px;margin-top:32px;">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;
                            letter-spacing:0.1em;color:#ff4500;margin-bottom:10px;">
                    TODAY'S PLAN — {date.today().strftime("%A").upper()}
                </div>
                {"".join(f'<div style="padding:5px 0;border-bottom:1px solid #1e1e1e;font-size:0.88rem;color:#aaa;">▸ {ex}</div>' for ex in today_schedule)}
            </div>
            """, unsafe_allow_html=True)
        
        # Recent logs today
        today_str = str(date.today())
        today_logs = [l for l in data["logs"] if l["date"] == today_str]
        
        if today_logs:
            st.markdown(f"""
            <div style="margin-top:16px;">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:0.9rem;
                            letter-spacing:0.1em;color:#555;margin-bottom:8px;">
                    LOGGED TODAY
                </div>
            """, unsafe_allow_html=True)
            for l in today_logs[-5:]:
                pr_html = '<span class="pr-badge">PR</span>' if l.get("is_pr") else ""
                st.markdown(f"""
                <div class="log-entry">
                    <div>
                        <div class="log-exercise">{l['exercise']}{pr_html}</div>
                        <div class="log-detail">{l['sets']} sets × {l['reps']} reps</div>
                    </div>
                    <div class="log-weight">{l['weight']}<div class="log-weight-unit">KG</div></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PROGRESS & PRs
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    if not data["logs"]:
        st.markdown("""
        <div style="text-align:center;padding:60px;color:#333;">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:3rem;letter-spacing:0.1em;">
                NO DATA YET
            </div>
            <p style="color:#444;">Log your first workout to see progress charts.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        df = pd.DataFrame(data["logs"])
        df["date"] = pd.to_datetime(df["date"])
        df["volume"] = df["sets"] * df["reps"] * df["weight"]

        st.markdown('<div class="section-head">Personal Records</div>', unsafe_allow_html=True)

        # PRs table
        pr_data = df.groupby("exercise")["weight"].max().sort_values(ascending=False).reset_index()
        pr_data.columns = ["Exercise", "Max Weight (kg)"]
        
        cols = st.columns(min(4, len(pr_data)))
        for i, (_, row) in enumerate(pr_data.head(8).iterrows()):
            with cols[i % len(cols)]:
                st.markdown(f"""
                <div class="stat-card" style="margin-bottom:10px;">
                    <div class="stat-number">{row['Max Weight (kg)']:.1f}</div>
                    <div style="font-size:0.7rem;letter-spacing:0.05em;color:#555;margin-top:2px;">KG</div>
                    <div class="stat-label" style="color:#888;font-size:0.68rem;">{row['Exercise'][:16]}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="section-head">Exercise Progress</div>', unsafe_allow_html=True)

        col_sel, _ = st.columns([1, 2])
        with col_sel:
            selected_ex = st.selectbox(
                "Select Exercise",
                options=sorted(df["exercise"].unique()),
                key="progress_ex"
            )

        ex_df = df[df["exercise"] == selected_ex].sort_values("date")

        if len(ex_df) > 0:
            fig = go.Figure()

            # Volume area
            daily_vol = ex_df.groupby("date")["volume"].sum().reset_index()
            fig.add_trace(go.Scatter(
                x=daily_vol["date"], y=daily_vol["volume"],
                fill="tozeroy",
                fillcolor="rgba(255,69,0,0.08)",
                line=dict(color="rgba(255,69,0,0.3)", width=1),
                name="Volume",
                yaxis="y2",
            ))

            # Max weight line
            daily_max = ex_df.groupby("date")["weight"].max().reset_index()
            fig.add_trace(go.Scatter(
                x=daily_max["date"], y=daily_max["weight"],
                mode="lines+markers",
                line=dict(color="#ff4500", width=2.5),
                marker=dict(size=7, color="#ff4500", line=dict(color="#0a0a0a", width=2)),
                name="Max Weight (kg)",
            ))

            # PR points
            pr_points = ex_df[ex_df["is_pr"] == True]
            if len(pr_points) > 0:
                pr_max = pr_points.groupby("date")["weight"].max().reset_index()
                fig.add_trace(go.Scatter(
                    x=pr_max["date"], y=pr_max["weight"],
                    mode="markers",
                    marker=dict(size=14, color="#ff4500", symbol="star",
                                line=dict(color="#ffcc00", width=2)),
                    name="⭐ PR",
                ))

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(14,14,14,0.8)",
                height=340,
                font=dict(family="Barlow", color="#666"),
                legend=dict(
                    bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#888", size=11),
                    orientation="h", y=1.08
                ),
                margin=dict(l=0, r=0, t=40, b=0),
                xaxis=dict(
                    showgrid=False, color="#444",
                    showline=True, linecolor="#2a2a2a"
                ),
                yaxis=dict(
                    showgrid=True, gridcolor="#1a1a1a",
                    color="#666", title="Weight (kg)",
                    title_font=dict(size=10)
                ),
                yaxis2=dict(
                    overlaying="y", side="right",
                    showgrid=False, showticklabels=False
                ),
                hovermode="x unified",
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Weekly volume chart
        st.markdown('<div class="section-head">Weekly Volume</div>', unsafe_allow_html=True)

        df["week"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)
        weekly = df.groupby("week")["volume"].sum().reset_index()
        weekly = weekly.tail(12)

        fig2 = go.Figure(go.Bar(
            x=weekly["week"].dt.strftime("%b %d"),
            y=weekly["volume"],
            marker_color="#ff4500",
            marker_line_width=0,
            opacity=0.85,
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14,14,14,0.8)",
            height=240,
            font=dict(family="Barlow", color="#666"),
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False, color="#444"),
            yaxis=dict(showgrid=True, gridcolor="#1a1a1a", color="#666"),
            hovermode="x",
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — HISTORY
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-head">Workout History</div>', unsafe_allow_html=True)

    if not data["logs"]:
        st.markdown("""
        <div style="text-align:center;padding:60px;color:#333;">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:3rem;">NO LOGS YET</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Filter controls
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filter_ex = st.selectbox("Filter by Exercise", ["All"] + sorted(set(l["exercise"] for l in data["logs"])), key="hist_filter")
        with col_f2:
            n_days = st.selectbox("Time Period", [7, 14, 30, 60, 90, 365], index=2, key="hist_days")
            n_days = int(n_days)
        with col_f3:
            sort_order = st.selectbox("Sort", ["Newest First", "Oldest First"], key="hist_sort")

        cutoff = date.today() - timedelta(days=n_days)
        filtered = [
            l for l in data["logs"]
            if datetime.strptime(l["date"], "%Y-%m-%d").date() >= cutoff
            and (filter_ex == "All" or l["exercise"] == filter_ex)
        ]

        if sort_order == "Newest First":
            filtered = sorted(filtered, key=lambda x: x["date"], reverse=True)
        else:
            filtered = sorted(filtered, key=lambda x: x["date"])

        st.markdown(f'<div style="font-size:0.78rem;color:#444;margin-bottom:12px;">{len(filtered)} entries found</div>', unsafe_allow_html=True)

        # Group by date
        from itertools import groupby
        grouped = {}
        for l in filtered:
            grouped.setdefault(l["date"], []).append(l)

        for d_str, entries in sorted(grouped.items(), reverse=(sort_order == "Newest First")):
            d_obj = datetime.strptime(d_str, "%Y-%m-%d")
            st.markdown(f"""
            <div style="font-family:'Bebas Neue',sans-serif;font-size:0.85rem;
                        letter-spacing:0.15em;color:#ff4500;margin:20px 0 8px;">
                {d_obj.strftime("%A, %B %d %Y").upper()}
            </div>
            """, unsafe_allow_html=True)

            for entry in entries:
                pr_html = ' <span class="pr-badge">PR</span>' if entry.get("is_pr") else ""
                notes_html = f'<span style="color:#444;font-size:0.75rem;margin-left:8px;">· {entry["notes"]}</span>' if entry.get("notes") else ""
                vol = entry.get("volume", entry["sets"] * entry["reps"] * entry.get("weight", 0))
                st.markdown(f"""
                <div class="log-entry">
                    <div>
                        <div class="log-exercise">{entry['exercise']}{pr_html}{notes_html}</div>
                        <div class="log-detail">{entry['sets']} sets × {entry['reps']} reps · Vol: {int(vol):,} kg</div>
                    </div>
                    <div class="log-weight">{entry.get('weight',0):.1f}<div class="log-weight-unit">KG</div></div>
                </div>
                """, unsafe_allow_html=True)

        # Export
        st.markdown("---")
        if filtered:
            df_export = pd.DataFrame(filtered)
            csv = df_export.to_csv(index=False)
            st.download_button(
                "⬇ Export CSV",
                data=csv,
                file_name=f"ironlog_export_{date.today()}.csv",
                mime="text/csv",
            )
