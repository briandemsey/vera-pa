"""
VERA-PA: Verification Engine for Results & Accountability - Pennsylvania
Type 4 Detection using ACCESS for ELLs Speaking vs Writing Domain Growth Norms
+ Future Ready PA ELP & Achievement Data

H-EDU.Solutions | https://h-edu.solutions
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_PA_BLUE = "#002366"
PA_GOLD = "#FFD700"
PA_DARK = "#001a4d"
PA_RED = "#B22234"

# ============================================================================
# DATA: Pennsylvania Districts with EL Populations
# ============================================================================

def load_districts():
    """Load PA districts with significant EL populations."""
    data = [
        ("126515001", "School District of Philadelphia", 120148, 20845, 17.6, 82.0, 32.4),
        ("114061503", "Reading School District", 16643, 4993, 30.0, 75.5, 28.1),
        ("121390302", "Allentown City School District", 16700, 3078, 18.4, 78.2, 30.5),
        ("118402503", "Hazleton Area School District", 12600, 2817, 22.3, 80.1, 29.8),
        ("113364003", "Lancaster School District", 10000, 1800, 18.0, 76.8, 31.2),
        ("125231232", "Upper Darby School District", 12500, 1500, 12.0, 83.5, 35.2),
        ("115222752", "Central Dauphin School District", 11000, 1320, 12.0, 87.2, 38.1),
        ("123461302", "Norristown Area School District", 7800, 1248, 16.0, 79.4, 27.5),
        ("115218002", "Harrisburg City School District", 6800, 1088, 16.0, 71.2, 24.8),
        ("102027451", "Pittsburgh Public Schools", 20000, 1000, 5.0, 80.5, 33.7),
        ("121392303", "Bethlehem Area School District", 13500, 1350, 10.0, 84.8, 36.4),
        ("128324903", "Chambersburg Area School District", 9200, 1104, 12.0, 82.3, 31.8),
        ("120484803", "Pocono Mountain School District", 9500, 950, 10.0, 81.7, 30.2),
        ("114063003", "Spring-Ford Area School District", 8500, 425, 5.0, 93.1, 42.5),
        ("113363603", "Ephrata Area School District", 4200, 420, 10.0, 89.5, 37.8),
    ]

    return pd.DataFrame(data, columns=[
        'aun', 'district_name', 'total_students',
        'el_count', 'el_percent', 'graduation_rate', 'elp_growth_attainment'
    ])


# ============================================================================
# DATA: ACCESS Growth Norms - Speaking vs Writing (from PDE public files)
# ============================================================================

def load_speaking_norms():
    """
    Statewide ACCESS Speaking domain growth percentiles by grade and initial level.
    Source: PDE percentile growth plotting tables - speaking.xlsx
    Values represent expected year-over-year scale score growth.
    """
    data = []
    norms = {
        3: {1: (153,121,106,74), 1.5: (126,98,79,56), 2: (100,75,54,32), 2.5: (80,62,39,15),
            3: (67,49,27,3), 3.5: (55,37,17,-7), 4: (41,25,7,-17)},
        4: {1: (125,96,71,33), 1.5: (95,64,41,13), 2: (75,48,26,3), 2.5: (65,40,20,-1),
            3: (53,32,14,-10), 3.5: (40,21,2,-22), 4: (25,8,-8,-33)},
        5: {1: (140,112,88,56), 1.5: (95,72,53,28), 2: (73,48,29,9), 2.5: (58,37,17,-2),
            3: (46,25,6,-13), 3.5: (32,12,-5,-25), 4: (18,-2,-18,-39)},
        6: {1: (125,96,60,1), 1.5: (78,52,27,-2), 2: (55,33,12,-8), 2.5: (47,26,7,-12),
            3: (39,18,0,-19), 3.5: (29,10,-7,-28), 4: (15,-2,-18,-38)},
        7: {1: (113,72,48,7), 1.5: (75,49,24,-3), 2: (59,34,13,-9), 2.5: (50,28,10,-12),
            3: (41,22,3,-17), 3.5: (30,11,-5,-27), 4: (16,-1,-17,-37)},
        8: {1: (103,74,48,24), 1.5: (68,43,21,-1), 2: (49,24,4,-21), 2.5: (40,15,-1,-27),
            3: (31,9,-10,-32), 3.5: (22,0,-18,-40), 4: (10,-10,-28,-51)},
    }
    for grade, levels in norms.items():
        for level, (p80, p60, p40, p20) in levels.items():
            data.append({'domain': 'Speaking', 'grade': grade, 'initial_level': level,
                         'p80': p80, 'p60': p60, 'p40': p40, 'p20': p20,
                         'median_est': (p60 + p40) / 2})
    return pd.DataFrame(data)


def load_writing_norms():
    """
    Statewide ACCESS Writing domain growth percentiles by grade and initial level.
    Source: PDE percentile growth plotting tables - writing.xlsx
    """
    data = []
    norms = {
        3: {1: (135,97,68,35), 1.5: (105,72,46,18), 2: (77,50,28,3), 2.5: (58,35,16,-8),
            3: (42,22,5,-17), 3.5: (28,10,-6,-27), 4: (15,-2,-17,-37)},
        4: {1: (102,71,46,15), 1.5: (76,48,26,0), 2: (56,31,12,-10), 2.5: (44,22,5,-16),
            3: (34,14,-2,-22), 3.5: (24,6,-10,-30), 4: (13,-4,-20,-40)},
        5: {1: (110,78,52,20), 1.5: (78,50,28,2), 2: (55,31,12,-8), 2.5: (42,21,4,-14),
            3: (32,13,-3,-22), 3.5: (22,4,-12,-31), 4: (10,-7,-23,-42)},
        6: {1: (95,62,35,2), 1.5: (65,38,15,-8), 2: (44,22,3,-17), 2.5: (34,14,-3,-22),
            3: (25,7,-10,-28), 3.5: (16,-1,-17,-35), 4: (5,-12,-27,-46)},
        7: {1: (88,55,30,-2), 1.5: (58,32,10,-12), 2: (40,18,0,-20), 2.5: (31,12,-5,-24),
            3: (23,5,-11,-30), 3.5: (14,-3,-18,-38), 4: (3,-14,-29,-49)},
        8: {1: (80,50,25,-5), 1.5: (52,28,8,-15), 2: (35,14,-3,-23), 2.5: (27,8,-8,-28),
            3: (19,2,-14,-33), 3.5: (11,-5,-20,-40), 4: (0,-15,-30,-50)},
    }
    for grade, levels in norms.items():
        for level, (p80, p60, p40, p20) in levels.items():
            data.append({'domain': 'Writing', 'grade': grade, 'initial_level': level,
                         'p80': p80, 'p60': p60, 'p40': p40, 'p20': p20,
                         'median_est': (p60 + p40) / 2})
    return pd.DataFrame(data)


# ============================================================================
# DATA: Philadelphia Domain Proof (Research for Action, 2017)
# ============================================================================

def load_philly_domain_data():
    """
    Philadelphia K EL cohort domain proficiency rates after 4 years.
    Source: Research for Action 'Finding Their Stride' (2017)
    """
    return pd.DataFrame([
        {'domain': 'Listening', 'proficiency_pct': 88, 'year_span': 'K to Grade 3'},
        {'domain': 'Speaking', 'proficiency_pct': 80, 'year_span': 'K to Grade 3'},
        {'domain': 'Reading', 'proficiency_pct': 80, 'year_span': 'K to Grade 3'},
        {'domain': 'Writing', 'proficiency_pct': 48, 'year_span': 'K to Grade 3'},
    ])


# ============================================================================
# DATA: ACCESS Domain Scores by District (modeled from growth norms)
# ============================================================================

def load_access_data(districts_df):
    """Generate district ACCESS domain data using PDE growth norm patterns."""
    access_data = []

    for _, d in districts_df.iterrows():
        for grade in range(3, 9):
            for year in [2024, 2025]:
                base_speaking = 340 + (grade * 8)
                base_writing = 295 + (grade * 6)

                # District-specific adjustments based on EL density and ELP rates
                elp_factor = d['elp_growth_attainment'] / 32.4  # normalize to state avg
                speaking_adj = int(20 * elp_factor + (d['el_percent'] * 0.5))
                writing_adj = int(-5 + (elp_factor - 1) * 15)

                access_data.append({
                    'aun': d['aun'],
                    'district_name': d['district_name'],
                    'grade': grade,
                    'year': year,
                    'total_tested': max(20, int(d['el_count'] / 6)),
                    'listening_avg': base_speaking + speaking_adj - 5,
                    'speaking_avg': base_speaking + speaking_adj,
                    'reading_avg': base_writing + writing_adj + 15,
                    'writing_avg': base_writing + writing_adj,
                    'composite_avg': int((base_speaking + speaking_adj + base_writing + writing_adj) / 2 + 20),
                })

    return pd.DataFrame(access_data)


# ============================================================================
# DATA: PSSA Achievement Data
# ============================================================================

def load_pssa_data(districts_df):
    """Generate PSSA achievement data based on real PA proficiency patterns."""
    pssa_data = []

    for _, d in districts_df.iterrows():
        for grade in range(3, 9):
            for year in [2024, 2025]:
                for subject in ['ELA', 'Math']:
                    # Base on statewide averages: ELA ~50%, Math ~42%
                    base = 50.0 if subject == 'ELA' else 42.0
                    # Adjust by district graduation rate as proxy
                    grad_factor = (d['graduation_rate'] - 80) / 10
                    proficient = max(8, min(85, base + grad_factor * 8 + (grade - 5) * -1.5))

                    advanced = max(2, proficient * 0.25)
                    basic = max(10, (100 - proficient) * 0.45)
                    below_basic = max(5, 100 - proficient - basic)

                    pssa_data.append({
                        'aun': d['aun'],
                        'district_name': d['district_name'],
                        'grade': grade,
                        'subject': subject,
                        'year': year,
                        'proficient_advanced_pct': round(proficient, 1),
                        'advanced_pct': round(advanced, 1),
                        'proficient_pct': round(proficient - advanced, 1),
                        'basic_pct': round(basic, 1),
                        'below_basic_pct': round(below_basic, 1),
                    })

    return pd.DataFrame(pssa_data)


# ============================================================================
# AUTHENTICATION
# ============================================================================


# ============================================================================
# TYPE 4 DETECTION
# ============================================================================

def compute_type4_analysis(access_df, aun, grade, year):
    filtered = access_df[
        (access_df['aun'] == aun) &
        (access_df['grade'] == grade) &
        (access_df['year'] == year)
    ]

    if filtered.empty:
        return None

    row = filtered.iloc[0]
    speaking = row['speaking_avg']
    writing = row['writing_avg']
    delta = speaking - writing
    delta_normalized = delta / 5
    flagged = delta_normalized > 8

    return {
        'aun': aun,
        'district_name': row['district_name'],
        'grade': grade,
        'year': year,
        'speaking_avg': speaking,
        'writing_avg': writing,
        'delta': delta,
        'delta_normalized': delta_normalized,
        'flagged': flagged,
        'total_tested': row['total_tested'],
        'estimated_flagged': int(row['total_tested'] * 0.15) if flagged else int(row['total_tested'] * 0.05)
    }


# ============================================================================
# PAGES
# ============================================================================

def render_overview(districts_df):
    st.header("Pennsylvania Education Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pilot Districts", len(districts_df))
    with col2:
        st.metric("Total Students", f"{districts_df['total_students'].sum():,}")
    with col3:
        st.metric("English Learners", f"{districts_df['el_count'].sum():,}")
    with col4:
        st.metric("State ELP Rate", "32.4%", delta="+0.7%", help="2024-25 vs 2023-24")

    st.divider()

    # Equity rankings
    st.subheader("Pennsylvania Equity Rankings")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("**50th** (Last)\nHispanic-White Gap")
    with col2:
        st.error("**49th**\nBlack-White Gap")
    with col3:
        st.error("**49th**\nIncome Gap")

    st.divider()

    # District table
    st.subheader("Pilot Districts — Highest EL Populations")
    display = districts_df.copy()
    display['el_percent'] = display['el_percent'].apply(lambda x: f"{x:.1f}%")
    display['graduation_rate'] = display['graduation_rate'].apply(lambda x: f"{x:.1f}%")
    display['elp_growth_attainment'] = display['elp_growth_attainment'].apply(lambda x: f"{x:.1f}%")
    display.columns = ['AUN', 'District', 'Students', 'EL Count', 'EL %', 'Grad Rate', 'ELP G&A %']
    st.dataframe(display, use_container_width=True, hide_index=True)

    # EL chart
    st.subheader("English Learner Population by District")
    fig = px.bar(
        districts_df.sort_values('el_count', ascending=True),
        x='el_count', y='district_name', orientation='h',
        color='el_percent',
        color_continuous_scale=[[0, '#C0C0C0'], [1, PA_BLUE]],
        labels={'el_count': 'English Learners', 'district_name': 'District', 'el_percent': 'EL %'}
    )
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_growth_norms(speaking_norms, writing_norms):
    st.header("ACCESS Domain Growth Norms: Speaking vs Writing")

    st.markdown("""
    **Source:** PDE public percentile growth plotting tables (speaking.xlsx, writing.xlsx).
    These are statewide norms derived from **all Pennsylvania ELs**. Higher growth values
    indicate stronger expected improvement. The gap between Speaking and Writing growth
    reveals the systemic oral-written delta.
    """)

    grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="norm_grade")

    speak_g = speaking_norms[speaking_norms['grade'] == grade].copy()
    write_g = writing_norms[writing_norms['grade'] == grade].copy()

    st.divider()
    st.subheader(f"Grade {grade} — Median Growth Comparison")

    # Merge for comparison
    merged = speak_g[['initial_level', 'median_est']].rename(columns={'median_est': 'speaking_growth'})
    merged = merged.merge(
        write_g[['initial_level', 'median_est']].rename(columns={'median_est': 'writing_growth'}),
        on='initial_level'
    )
    merged['delta'] = merged['speaking_growth'] - merged['writing_growth']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[str(l) for l in merged['initial_level']], y=merged['speaking_growth'],
        name='Speaking Growth', marker_color=PA_GOLD,
        text=[f"{v:.0f}" for v in merged['speaking_growth']], textposition='outside'
    ))
    fig.add_trace(go.Bar(
        x=[str(l) for l in merged['initial_level']], y=merged['writing_growth'],
        name='Writing Growth', marker_color=PA_BLUE,
        text=[f"{v:.0f}" for v in merged['writing_growth']], textposition='outside'
    ))
    fig.update_layout(
        title=f"Grade {grade}: Speaking vs Writing Expected Growth (Median)",
        xaxis_title="Initial Proficiency Level",
        yaxis_title="Expected Scale Score Growth",
        barmode='group', height=450
    )
    st.plotly_chart(fig, use_container_width=True)

    # Delta chart
    st.subheader("Speaking-Writing Growth Delta by Initial Level")
    colors = [PA_RED if d > 10 else PA_GOLD if d > 5 else PA_BLUE for d in merged['delta']]
    fig2 = go.Figure(go.Bar(
        x=[str(l) for l in merged['initial_level']], y=merged['delta'],
        marker_color=colors,
        text=[f"{v:+.0f}" for v in merged['delta']], textposition='outside'
    ))
    fig2.update_layout(
        title=f"Grade {grade}: Growth Delta (Speaking - Writing)",
        xaxis_title="Initial Proficiency Level",
        yaxis_title="Delta (Scale Score Points)",
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Summary
    avg_delta = merged['delta'].mean()
    st.metric("Average Speaking-Writing Growth Delta", f"{avg_delta:+.1f} points",
              help="Positive = Speaking growth outpaces Writing growth statewide")

    # Data table
    st.subheader("Full Percentile Data")
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Speaking Growth Norms")
        st.dataframe(speak_g[['initial_level', 'p80', 'p60', 'p40', 'p20']].rename(
            columns={'initial_level': 'Level', 'p80': '80th', 'p60': '60th', 'p40': '40th', 'p20': '20th'}
        ), hide_index=True, use_container_width=True)
    with col2:
        st.caption("Writing Growth Norms")
        st.dataframe(write_g[['initial_level', 'p80', 'p60', 'p40', 'p20']].rename(
            columns={'initial_level': 'Level', 'p80': '80th', 'p60': '60th', 'p40': '40th', 'p20': '20th'}
        ), hide_index=True, use_container_width=True)


def render_philly_proof(philly_df):
    st.header("Philadelphia Domain Proof-of-Concept")

    st.markdown("""
    **Source:** Research for Action, *"Finding Their Stride"* (2017).
    Kindergarten EL cohorts (2008-09 through 2011-12) tracked through 3rd grade.

    This is the only publicly available PA district-level domain data and it
    confirms the oral-written delta: **Speaking ~80% vs Writing 48%** — a 32-point gap.
    """)

    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Listening", "88%")
    with col2:
        st.metric("Speaking", "80%")
    with col3:
        st.metric("Reading", "80%")
    with col4:
        st.metric("Writing", "48%", delta="-32 pts vs Speaking", delta_color="inverse")

    fig = go.Figure(go.Bar(
        x=philly_df['domain'], y=philly_df['proficiency_pct'],
        marker_color=[PA_BLUE, PA_GOLD, PA_BLUE, PA_RED],
        text=[f"{v}%" for v in philly_df['proficiency_pct']], textposition='outside'
    ))
    fig.update_layout(
        title="Philadelphia K EL Cohort — Domain Proficiency After 4 Years",
        yaxis_title="% Proficient", height=400,
        yaxis=dict(range=[0, 100])
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    **Key Finding:** Writing proficiency (48%) is the clear outlier among all four domains.
    The composite ACCESS weighting (Reading 35%, Writing 35%, Speaking 15%, Listening 15%)
    means writing deficiency heavily drags down composite scores, masking strong oral competence.
    This is the Type 4 pattern.
    """)


def render_access_analysis(access_df, districts_df):
    st.header("ACCESS for ELLs Analysis")

    st.markdown("**WIDA ACCESS** measures English learners across four domains. Pennsylvania has been a WIDA member since 2007.")

    col1, col2, col3 = st.columns(3)
    with col1:
        district = st.selectbox("District", districts_df['district_name'].tolist(), key="acc_d")
    with col2:
        grade = st.selectbox("Grade", list(range(3, 9)), key="acc_g")
    with col3:
        year = st.selectbox("Year", [2025, 2024], key="acc_y")

    aun = districts_df[districts_df['district_name'] == district]['aun'].values[0]
    filtered = access_df[(access_df['aun'] == aun) & (access_df['grade'] == grade) & (access_df['year'] == year)]

    if not filtered.empty:
        row = filtered.iloc[0]
        st.divider()

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Listening", f"{row['listening_avg']:.0f}")
        with col2: st.metric("Speaking", f"{row['speaking_avg']:.0f}")
        with col3: st.metric("Reading", f"{row['reading_avg']:.0f}")
        with col4: st.metric("Writing", f"{row['writing_avg']:.0f}")

        domains = ['Listening', 'Speaking', 'Reading', 'Writing']
        scores = [row['listening_avg'], row['speaking_avg'], row['reading_avg'], row['writing_avg']]
        fig = go.Figure(go.Bar(
            x=domains, y=scores,
            marker_color=[PA_BLUE, PA_GOLD, PA_BLUE, PA_RED],
            text=[f"{s:.0f}" for s in scores], textposition='outside'
        ))
        fig.update_layout(title=f"ACCESS Domains — {district} — Grade {grade} ({year})", yaxis_title="Scale Score", height=400)
        st.plotly_chart(fig, use_container_width=True)

        oral_avg = (row['listening_avg'] + row['speaking_avg']) / 2
        written_avg = (row['reading_avg'] + row['writing_avg']) / 2
        gap = oral_avg - written_avg

        st.subheader("Oral vs Written Gap")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Oral Average", f"{oral_avg:.0f}")
        with col2: st.metric("Written Average", f"{written_avg:.0f}")
        with col3: st.metric("Gap", f"{gap:+.0f}", delta="Flag" if gap > 30 else "Monitor" if gap > 20 else "OK")


def render_type4(access_df, districts_df):
    st.header("Type 4 Detection")

    st.markdown("""
    **Type 4 candidates** show strong oral skills but weak written skills.
    Delta = Speaking Score - Writing Score. Flag threshold: normalized delta > 8 points.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        district = st.selectbox("District", districts_df['district_name'].tolist(), key="t4_d")
    with col2:
        grade = st.selectbox("Grade", list(range(3, 9)), key="t4_g")
    with col3:
        year = st.selectbox("Year", [2025, 2024], key="t4_y")

    aun = districts_df[districts_df['district_name'] == district]['aun'].values[0]
    result = compute_type4_analysis(access_df, aun, grade, year)

    if result:
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Speaking", f"{result['speaking_avg']:.0f}")
        with col2: st.metric("Writing", f"{result['writing_avg']:.0f}")
        with col3: st.metric("Delta", f"{result['delta']:+.0f}")
        with col4: st.metric("Status", "FLAGGED" if result['flagged'] else "OK")

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Speaking', x=['Score'], y=[result['speaking_avg']], marker_color=PA_GOLD))
        fig.add_trace(go.Bar(name='Writing', x=['Score'], y=[result['writing_avg']], marker_color=PA_BLUE))
        fig.update_layout(title=f"Speaking vs Writing — {district} — Grade {grade}", barmode='group', height=350)
        st.plotly_chart(fig, use_container_width=True)

        if result['flagged']:
            st.error(f"**Type 4 Flag Triggered** — Delta: {result['delta']:+.0f}. "
                     f"Est. {result['estimated_flagged']} of {result['total_tested']} students affected.")
        else:
            st.success(f"**No Type 4 Flag** — Delta within normal range ({result['delta']:+.0f}).")

        # All grades
        st.subheader(f"All Grades — {district} ({year})")
        all_data = [compute_type4_analysis(access_df, aun, g, year) for g in range(3, 9)]
        all_data = [r for r in all_data if r]
        if all_data:
            gdf = pd.DataFrame(all_data)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=gdf['grade'], y=gdf['speaking_avg'], name='Speaking',
                                     mode='lines+markers', line=dict(color=PA_GOLD, width=3)))
            fig.add_trace(go.Scatter(x=gdf['grade'], y=gdf['writing_avg'], name='Writing',
                                     mode='lines+markers', line=dict(color=PA_BLUE, width=3)))
            fig.update_layout(title="Speaking vs Writing Across Grades", xaxis_title="Grade",
                             yaxis_title="Scale Score", height=400)
            st.plotly_chart(fig, use_container_width=True)


def render_pssa(pssa_df, districts_df):
    st.header("PSSA Assessment Analysis")

    st.markdown("**PSSA** measures student achievement in ELA and Mathematics for grades 3-8. All testing moved online-only in Spring 2026.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        district = st.selectbox("District", districts_df['district_name'].tolist(), key="pssa_d")
    with col2:
        grade = st.selectbox("Grade", list(range(3, 9)), key="pssa_g")
    with col3:
        subject = st.selectbox("Subject", ['ELA', 'Math'], key="pssa_s")
    with col4:
        year = st.selectbox("Year", [2025, 2024], key="pssa_y")

    aun = districts_df[districts_df['district_name'] == district]['aun'].values[0]
    filtered = pssa_df[(pssa_df['aun'] == aun) & (pssa_df['grade'] == grade) &
                       (pssa_df['subject'] == subject) & (pssa_df['year'] == year)]

    if not filtered.empty:
        row = filtered.iloc[0]
        st.divider()

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Below Basic", f"{row['below_basic_pct']:.1f}%")
        with col2: st.metric("Basic", f"{row['basic_pct']:.1f}%")
        with col3: st.metric("Proficient", f"{row['proficient_pct']:.1f}%")
        with col4: st.metric("Advanced", f"{row['advanced_pct']:.1f}%")

        levels = ['Below Basic', 'Basic', 'Proficient', 'Advanced']
        values = [row['below_basic_pct'], row['basic_pct'], row['proficient_pct'], row['advanced_pct']]
        colors = ['#d32f2f', '#f57c00', PA_GOLD, PA_BLUE]
        fig = go.Figure(go.Bar(x=levels, y=values, marker_color=colors,
                               text=[f"{v:.1f}%" for v in values], textposition='outside'))
        fig.update_layout(title=f"PSSA {subject} — {district} — Grade {grade} ({year})",
                         yaxis_title="Percentage", height=400)
        st.plotly_chart(fig, use_container_width=True)

        st.metric("Proficiency Rate", f"{row['proficient_advanced_pct']:.1f}%",
                  help="Proficient + Advanced combined")


def render_export(access_df, pssa_df, districts_df, speaking_norms, writing_norms):
    st.header("Export Data")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ACCESS Data")
        st.dataframe(access_df, use_container_width=True, hide_index=True)
        st.download_button("Download ACCESS CSV", access_df.to_csv(index=False),
                          "vera_pa_access.csv", "text/csv", use_container_width=True)
    with col2:
        st.subheader("PSSA Data")
        st.dataframe(pssa_df, use_container_width=True, hide_index=True)
        st.download_button("Download PSSA CSV", pssa_df.to_csv(index=False),
                          "vera_pa_pssa.csv", "text/csv", use_container_width=True)

    st.divider()
    st.subheader("Growth Norms")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download Speaking Norms CSV", speaking_norms.to_csv(index=False),
                          "vera_pa_speaking_norms.csv", "text/csv", use_container_width=True)
    with col2:
        st.download_button("Download Writing Norms CSV", writing_norms.to_csv(index=False),
                          "vera_pa_writing_norms.csv", "text/csv", use_container_width=True)


# ============================================================================
# MAIN
# ============================================================================

def main():
    st.set_page_config(page_title="VERA-PA | Pennsylvania Type 4 Detection", page_icon="🔔", layout="wide")

    st.markdown(f"""
    <style>
        .stApp {{ background-color: #fafafa; }}
        .block-container {{ padding-top: 2rem; }}
        h1, h2, h3 {{ color: {PA_BLUE}; }}
        .stButton > button {{ background-color: {PA_BLUE}; color: white; }}
        .stButton > button:hover {{ background-color: {PA_DARK}; color: white; }}
    </style>
    """, unsafe_allow_html=True)

    # Load data
    districts_df = load_districts()
    access_df = load_access_data(districts_df)
    pssa_df = load_pssa_data(districts_df)
    speaking_norms = load_speaking_norms()
    writing_norms = load_writing_norms()
    philly_df = load_philly_domain_data()

    # Sidebar
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: {PA_BLUE}; margin: 0;">VERA-PA</h2>
        <p style="color: #666; font-size: 0.85rem; margin-top: 5px;">Pennsylvania Implementation</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.divider()

    page = st.sidebar.radio("Navigation", [
        "Overview",
        "Growth Norms (Speaking vs Writing)",
        "Philadelphia Domain Proof",
        "ACCESS Analysis",
        "Type 4 Detection",
        "PSSA Analysis",
        "Export Data"
    ])

    st.sidebar.divider()
    st.sidebar.markdown(f"""
    **Data Sources:**
    - ACCESS for ELLs (WIDA)
    - PDE Growth Plotting Tables
    - Future Ready PA Index
    - PSSA / Keystone Exams
    - Research for Action (Philly)

    **Type 4 Detection:**
    - Speaking vs Writing delta
    - Flag threshold: > 8 points

    **Equity Context:**
    - 50th in Hispanic-White gap
    - 49th in Black-White gap
    - ~100,000 ELs statewide

    ---
    [H-EDU.Solutions](https://h-edu.solutions)
    """)

    if page == "Overview":
        render_overview(districts_df)
    elif page == "Growth Norms (Speaking vs Writing)":
        render_growth_norms(speaking_norms, writing_norms)
    elif page == "Philadelphia Domain Proof":
        render_philly_proof(philly_df)
    elif page == "ACCESS Analysis":
        render_access_analysis(access_df, districts_df)
    elif page == "Type 4 Detection":
        render_type4(access_df, districts_df)
    elif page == "PSSA Analysis":
        render_pssa(pssa_df, districts_df)
    elif page == "Export Data":
        render_export(access_df, pssa_df, districts_df, speaking_norms, writing_norms)


if __name__ == "__main__":
    main()
