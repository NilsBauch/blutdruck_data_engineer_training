## @file app.py
#  @brief Interaktives Streamlit-Dashboard zur Visualisierung der Gesundheitsdaten.
#
#  Dieses Modul stellt die Benutzeroberfläche bereit, mit der Nutzer die 
#  historisierten Daten aus dem DWH explorieren können. Es beantwortet die 
#  Kernfragen zu Medikation, Bewegung und Stress.
#
#  @date 2026-04-08

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# --- KONFIGURATION ---
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'blutdruck_dwh.db')
ST_PALETTE = ["#008080", "#2E8B57", "#4682B4", "#20B2AA", "#7FFFD4"] # Healthcare Teal/Green

st.set_page_config(
    page_title="Health Monitoring Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS für den Health-Look
st.markdown(f"""
    <style>
    .main {{
        background-color: #f0f4f4;
    }}
    .stMetric {{
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    h1, h2, h3 {{
        color: #004d4d;
    }}
    </style>
""", unsafe_allow_html=True)

# --- DATENLADEN ---
@st.cache_data
def load_data(user_id=None):
    conn = sqlite3.connect(DB_PATH)
    
    # Nutzerliste holen
    users_df = pd.read_sql("SELECT user_id FROM dim_user", conn)
    
    # Haupt-Datenabfrage
    query = """
    SELECT 
        f.*, 
        d.full_date, 
        d.is_weekend, 
        m.name as med_name, 
        m.dosage_mg as med_dose,
        l.movement_type,
        l.is_smoker
    FROM fact_health_metrics f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_medication m ON f.med_key = m.med_key
    JOIN dim_lifestyle l ON f.lifestyle_key = l.lifestyle_key
    """
    if user_id and user_id != "Alle":
        query += f" WHERE f.user_id = {user_id}"
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Formatierung
    df['full_date'] = pd.to_datetime(df['full_date'])
    df['datetime'] = pd.to_datetime(df['full_date'].dt.strftime('%Y-%m-%d') + ' ' + df['time_key'])
    return df, users_df['user_id'].tolist()

# --- SIDEBAR ---
st.sidebar.title("🩺 Health Control")
st.sidebar.markdown("---")

# Mehrmandantenfähigkeit: Patientenauswahl
raw_df_test, user_ids = load_data()
selected_user = st.sidebar.selectbox("PatientenID auswählen", ["Alle"] + user_ids)

df, _ = load_data(selected_user)

st.sidebar.markdown("---")
st.sidebar.info("Dieses Dashboard nutzt DWH-Daten mit SCD Type 2 Historisierung.")

# --- HAUPTBEREICH ---
st.title(f"Patienten-Analyse: {selected_user if selected_user != 'Alle' else 'Gesamtübersicht'}")

if df.empty:
    st.warning("Keine Daten für diesen Patienten gefunden. Bitte führen Sie die Pipeline aus.")
    st.stop()

# KPIs in der Übersicht
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("⌀ Systolisch", f"{df['systolic'].mean():.1f} mmHg")
with col2:
    st.metric("⌀ Diastolisch", f"{df['diastolic'].mean():.1f} mmHg")
with col3:
    st.metric("⌀ Puls", f"{df['pulse'].mean():.1f} bpm")
with col4:
    st.metric("⌀ Schritte", f"{df['steps_hourly'].mean():.0f}")

st.markdown("---")

# --- FRAGE 1: Medikations-Effekt ---
st.header("1. Effekt der Medikation")
col_l, col_r = st.columns(2)

with col_l:
    st.subheader("Blutdruck im Vergleich")
    # Vergleich Post-Medication vs Normal
    med_compare = df.groupby('is_post_medication')[['systolic', 'diastolic']].mean().reset_index()
    med_compare['is_post_medication'] = med_compare['is_post_medication'].map({1: 'Nach Einnahme (4h)', 0: 'Referenz'})
    
    fig_med = px.bar(med_compare, x='is_post_medication', y=['systolic', 'diastolic'], 
                     barmode='group', color_discrete_sequence=[ST_PALETTE[0], ST_PALETTE[2]],
                     title="Durchschnittliche Senkung")
    st.plotly_chart(fig_med, use_container_width=True)

with col_r:
    st.markdown("""
        **Analyse:**
        - Vergleicht Messungen innerhalb von 4 Stunden nach der geplanten Medikation mit dem Rest des Tages.
        - Ein signifikanter Abfall der Systole deutet auf ein wirksames Medikamenten-Zeitfenster hin.
    """)
    if selected_user != "Alle":
        med_plan = df['med_name'].unique()
        st.write(f"Aktuelle Medikation: **{', '.join(med_plan)}**")

st.markdown("---")

# --- FRAGE 2: Bewegung vs. Puls ---
st.header("2. Korrelation: Schritte & Ruhepuls")
fig_corr = px.scatter(df, x="steps_hourly", y="pulse", color="movement_type",
                     trendline="ols", color_discrete_sequence=ST_PALETTE,
                     labels={"steps_hourly": "Schritte", "pulse": "Puls (bpm)"},
                     title="Einfluss der Aktivität auf den Puls")
st.plotly_chart(fig_corr, use_container_width=True)

st.info("💡 Die Trendlinie zeigt den statistischen Zusammenhang. Ein Gefälle nach rechts deutet darauf hin, dass mehr Bewegung den Puls senkt.")

st.markdown("---")

# --- FRAGE 3: Werktag vs. Wochenende ---
st.header("3. Stress-Faktor: Werktag vs. Wochenende")
df['DayType'] = df['is_weekend'].map({0: 'Werktag', 1: 'Wochenende'})
fig_stress = px.box(df, x="DayType", y="systolic", color="DayType",
                   color_discrete_sequence=[ST_PALETTE[3], ST_PALETTE[1]],
                   title="Blutdruck-Varianz (Stress-Check)")
st.plotly_chart(fig_stress, use_container_width=True)

st.markdown("---")

# --- FRAGE 4: SCD 2 Historie ---
st.header("4. Historischer Verlauf & Lifestyle-Wechsel (SCD 2)")
st.markdown("Diese Ansicht zeigt, wie sich die Werte über die Zeit verändert haben, markiert nach den verschiedenen SCD-Lebensphasen.")

# Zeitstrahl mit Hintergrundfarben für Lifestyle
fig_history = px.line(df.sort_values('datetime'), x='datetime', y='systolic', 
                      color='movement_type', symbol='movement_type',
                      line_shape='spline', render_mode='svg',
                      title="SCD Type 2 Analyse: Blutdruckentwicklung über Lifestyle-Perioden")

# Zusätzlich Puls-Druck als Bereich (falls gewünscht)
fig_history.add_trace(go.Scatter(
    x=df.sort_values('datetime')['datetime'], 
    y=df.sort_values('datetime')['diastolic'],
    name='Diastolisch',
    line=dict(color='rgba(0,128,128,0.3)', dash='dot')
))

st.plotly_chart(fig_history, use_container_width=True)

st.success("Analysedaten basieren auf der 'blutdruck_dwh.db' mit technischer Provenienz/Load-Timestamps.")
