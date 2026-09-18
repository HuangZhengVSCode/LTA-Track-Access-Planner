# ============================================================
# LTA TRACK ACCESS CONTROL CENTRE
# Streamlit Web Application
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# Import scheduling engine
from scheduler import run_ps1_scheduler


# ============================================================
# 1. PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="LTA Track Access Control Centre",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. WEBSITE CSS
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   MAIN BACKGROUND
   ========================================================== */

.stApp {

    background:

        radial-gradient(
            ellipse at 50% 115%,
            rgba(0, 145, 255, 0.50) 0%,
            rgba(0, 90, 210, 0.28) 23%,
            rgba(0, 40, 120, 0.12) 45%,
            transparent 68%
        ),

        linear-gradient(
            180deg,
            #010307 0%,
            #020812 28%,
            #031427 62%,
            #052c50 100%
        );

    background-attachment: fixed;

    color: #eaf4ff;
}


/* ==========================================================
   STREAMLIT HEADER
   ========================================================== */

[data-testid="stHeader"] {
    background: transparent;
}


/* ==========================================================
   MAIN CONTENT
   ========================================================== */

.block-container {

    padding-top: 2rem;

    padding-bottom: 4rem;

    max-width: 1550px;
}


/* ==========================================================
   NORMAL TEXT
   ========================================================== */

.stApp h1,
.stApp h2,
.stApp h3 {

    color: #ffffff !important;
}


.stApp p,
.stApp label {

    color: #c8dceb;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {

    background:

        linear-gradient(
            180deg,
            rgba(1, 6, 12, 0.99),
            rgba(3, 20, 38, 0.99) 58%,
            rgba(4, 39, 70, 0.99)
        );

    border-right:
        1px solid rgba(75, 165, 255, 0.20);
}


section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {

    color: #ffffff !important;
}


section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {

    color: #b8cfe0 !important;
}


/* ==========================================================
   MAIN HEADER PANEL
   ========================================================== */

.main-header-panel {

    padding: 24px 28px;

    border-radius: 16px;

    border:
        1px solid rgba(80, 170, 255, 0.18);

    background:
        rgba(1, 9, 18, 0.42);

    margin-bottom: 28px;
}


.header-eyebrow {

    color: #8396a8 !important;

    font-size: 0.82rem;

    font-weight: 650;

    letter-spacing: 0.4px;

    margin-bottom: 18px;
}


/* ==========================================================
   WHITE TITLE CLOUD
   ========================================================== */

.title-cloud {

    display: inline-block;

    position: relative;

    background:

        linear-gradient(
            135deg,
            #ffffff 0%,
            #f4f9ff 100%
        );

    color: #082f56 !important;

    padding: 13px 27px;

    border-radius: 28px;

    font-size: clamp(
        1.55rem,
        2.5vw,
        2.45rem
    );

    font-weight: 800;

    letter-spacing: 0.5px;

    border:
        1px solid rgba(180, 215, 240, 0.90);

    box-shadow:
        0 7px 24px rgba(0, 0, 0, 0.25),
        0 0 20px rgba(255, 255, 255, 0.14);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}


/* Cloud bumps */

.title-cloud::before {

    content: "";

    position: absolute;

    width: 32px;

    height: 32px;

    border-radius: 50%;

    background: #ffffff;

    left: 35px;

    top: -10px;

    z-index: -1;
}


.title-cloud::after {

    content: "";

    position: absolute;

    width: 24px;

    height: 24px;

    border-radius: 50%;

    background: #ffffff;

    right: 48px;

    top: -7px;

    z-index: -1;
}


/* Title glow */

.title-cloud:hover {

    transform:
        translateY(-2px);

    box-shadow:

        0 10px 30px rgba(0, 0, 0, 0.30),

        0 0 12px rgba(255, 255, 255, 0.50),

        0 0 28px rgba(80, 185, 255, 0.30);
}


.header-subtitle {

    color: #c9deee !important;

    margin-top: 22px;

    font-size: 1rem;
}


/* ==========================================================
   ONLINE STATUS
   ========================================================== */

.online-status {

    display: flex;

    align-items: center;

    gap: 11px;

    margin-top: 20px;

    color: #dfffee !important;

    font-weight: 700;
}


.online-dot {

    width: 11px;

    height: 11px;

    border-radius: 50%;

    background: #38f58a;

    animation:
        onlinePulse 1.35s infinite;

    box-shadow:
        0 0 7px #38f58a;
}


@keyframes onlinePulse {

    0% {

        opacity: 1;

        transform:
            scale(1);

        box-shadow:
            0 0 5px #38f58a,
            0 0 10px rgba(56, 245, 138, 0.55);
    }


    50% {

        opacity: 0.45;

        transform:
            scale(0.72);

        box-shadow:
            0 0 2px #38f58a;
    }


    100% {

        opacity: 1;

        transform:
            scale(1);

        box-shadow:
            0 0 7px #38f58a,
            0 0 18px rgba(56, 245, 138, 0.85);
    }
}


/* ==========================================================
   WHITE INFORMATION CARDS
   ========================================================== */

.white-info-card {

    background:

        linear-gradient(
            145deg,
            #ffffff 0%,
            #f5f9fd 100%
        );

    border-radius: 15px;

    padding: 22px 24px;

    height: 165px;

    box-sizing: border-box;

    border:
        1px solid #d7e5ef;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.22);

    transition:
        transform 0.20s ease,
        box-shadow 0.20s ease;
}


.white-info-card:hover {

    transform:
        translateY(-3px);

    box-shadow:
        0 12px 30px rgba(0, 0, 0, 0.28),
        0 0 16px rgba(70, 175, 255, 0.16);
}


.white-card-title {

    color: #0b365d !important;

    font-size: 1.35rem;

    font-weight: 750;

    margin-bottom: 18px;
}


.white-card-value {

    color: #164d77 !important;

    font-size: 1rem;

    font-weight: 650;
}


.white-card-caption {

    color: #657d91 !important;

    font-size: 0.88rem;

    margin-top: 13px;
}


/* Ready indicator */

.ready-value {

    display: inline-block;

    color: #15704a !important;

    background: #e5f8ef;

    border:
        1px solid #b8ead3;

    border-radius: 8px;

    padding: 7px 12px;

    font-weight: 750;
}


/* Standby indicator */

.standby-value {

    display: inline-block;

    color: #6a7884 !important;

    background: #edf2f5;

    border:
        1px solid #d5dfe6;

    border-radius: 8px;

    padding: 7px 12px;

    font-weight: 700;
}


/* ==========================================================
   WHITE KPI CARDS
   ========================================================== */

.white-kpi-card {

    background: #ffffff;

    border-radius: 14px;

    padding: 21px 23px;

    height: 150px;

    box-sizing: border-box;

    border:
        1px solid #d7e5ef;

    box-shadow:
        0 8px 24px rgba(0, 0, 0, 0.20);

    transition:
        transform 0.20s ease,
        box-shadow 0.20s ease;
}


.white-kpi-card:hover {

    transform:
        translateY(-3px);

    box-shadow:
        0 12px 30px rgba(0, 0, 0, 0.28);
}


.white-kpi-label {

    color: #24496a !important;

    font-size: 0.92rem;

    font-weight: 650;

    margin-bottom: 10px;
}


.white-kpi-value {

    color: #073763 !important;

    font-size: 2.25rem;

    font-weight: 750;

    line-height: 1;
}


/* Urgent KPI */

.white-kpi-danger-label {

    color: #d94f59 !important;

    font-size: 0.92rem;

    font-weight: 700;

    margin-bottom: 10px;
}


.white-kpi-danger-value {

    color: #ef646c !important;

    font-size: 2.25rem;

    font-weight: 750;

    line-height: 1;
}


/* ==========================================================
   CONSTRAINT STATUS
   ========================================================== */

.status-good {

    color: #25A65A !important;

    font-size: 2.05rem;

    font-weight: 800;

    line-height: 1.05;
}


.status-bad {

    color: #EF5B63 !important;

    font-size: 1.85rem;

    font-weight: 800;

    line-height: 1.05;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton > button {

    width: 100%;

    min-height: 46px;

    border-radius: 9px;

    border:
        1px solid #42b9ff !important;

    background:

        linear-gradient(
            100deg,
            #0758ad,
            #0788d9,
            #08a9ed
        ) !important;

    color: #ffffff !important;

    font-weight: 700 !important;

    box-shadow:
        0 5px 20px rgba(0, 125, 255, 0.25);

    transition:
        transform 0.22s ease,
        box-shadow 0.22s ease;
}


.stButton > button p {

    color: #ffffff !important;

    font-weight: 700 !important;
}


.stButton > button:hover {

    transform:
        translateY(-2px);

    border-color:
        #8ae3ff !important;

    box-shadow:
        0 8px 28px rgba(0, 155, 255, 0.45),
        0 0 22px rgba(0, 155, 255, 0.25);
}


.stButton > button:disabled {

    background:

        linear-gradient(
            100deg,
            #153b5b,
            #185176
        ) !important;

    opacity: 0.72;

    box-shadow: none;
}


/* ==========================================================
   SELECT BOX
   ========================================================== */

div[data-baseweb="select"] > div {

    background:
        #f7f9fc !important;

    color:
        #173a58 !important;

    border-color:
        #d5e1ea !important;
}


/* ==========================================================
   FILE UPLOADER
   ========================================================== */

[data-testid="stFileUploaderDropzone"] {

    background:
        rgba(7, 29, 52, 0.72) !important;

    border:
        1px dashed rgba(70, 175, 255, 0.42) !important;

    border-radius: 10px;
}


/* ==========================================================
   TABS
   ========================================================== */

button[data-baseweb="tab"] {

    color:
        #a7c2d7 !important;

    font-weight: 500;
}


button[data-baseweb="tab"][aria-selected="true"] {

    color:
        #ffffff !important;

    font-weight: 700;
}


/* ==========================================================
   DATA TABLE
   ========================================================== */

[data-testid="stDataFrame"] {

    border:
        1px solid rgba(80, 170, 255, 0.15);

    border-radius: 10px;

    overflow: hidden;
}


/* ==========================================================
   ANIMATED SIDE-VIEW TRAIN
   ========================================================== */

.train-status-row {

    display: flex;

    align-items: center;

    gap: 18px;

    margin:
        14px 0 20px 0;

    color:
        #d7e8f5 !important;
}


.train-track {

    position: relative;

    width: 200px;

    height: 45px;

    overflow: hidden;

    border-bottom:
        2px solid rgba(200, 220, 235, 0.55);
}


.side-train {

    position: absolute;

    bottom: 4px;

    left: -120px;

    display: flex;

    align-items: flex-end;

    animation:
        trainMove 2.5s linear infinite;
}


.train-carriage {

    width: 31px;

    height: 20px;

    background: #dce8f0;

    border:
        2px solid #4f7895;

    border-radius:
        4px 4px 2px 2px;

    margin-right: 3px;

    position: relative;
}


.train-carriage::before {

    content: "";

    position: absolute;

    width: 8px;

    height: 7px;

    left: 5px;

    top: 4px;

    background: #49b8ff;

    border-radius: 2px;

    box-shadow:
        12px 0 0 #49b8ff;
}


.train-carriage::after {

    content: "●  ●";

    position: absolute;

    bottom: -9px;

    left: 3px;

    color: #9aaab5;

    font-size: 8px;
}


/* Train head faces RIGHT */

.train-head {

    width: 38px;

    height: 25px;

    position: relative;

    background:

        linear-gradient(
            90deg,
            #e6eef4,
            #6bc5ff
        );

    border:
        2px solid #4f7895;

    border-radius:
        4px 13px 4px 3px;
}


.train-head::before {

    content: "";

    position: absolute;

    width: 11px;

    height: 9px;

    right: 5px;

    top: 4px;

    background: #123a58;

    border-radius:
        2px 7px 2px 2px;
}


.train-head::after {

    content: "";

    position: absolute;

    width: 5px;

    height: 5px;

    right: -4px;

    top: 14px;

    border-radius: 50%;

    background: #fff3a6;

    box-shadow:
        0 0 8px #fff3a6,
        0 0 13px rgba(255, 243, 166, 0.7);
}


@keyframes trainMove {

    0% {
        left: -120px;
    }

    100% {
        left: 210px;
    }
}


/* ==========================================================
   DIVIDERS / FOOTER
   ========================================================== */

hr {

    border-color:
        rgba(110, 180, 230, 0.12) !important;
}


footer {

    visibility: hidden;
}

</style>
    """,

    unsafe_allow_html=True
)


# ============================================================
# 3. SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # Sidebar title
    # --------------------------------------------------------

    st.title(
        "Track Access Planner"
    )


    st.caption(
        "Network Planning & Possession Control"
    )


    st.divider()


    # --------------------------------------------------------
    # Operating strategy
    # --------------------------------------------------------

    st.subheader(
        "Operating Strategy"
    )


    scenario = st.selectbox(

        "Operating Strategy",

        options=[
            "A",
            "B",
            "C"
        ],

        format_func=lambda value: {

            "A":
                "Fixed Capacity",

            "B":
                "Fixed Completion Dates",

            "C":
                "Balanced Operations"

        }[value],

        label_visibility=
            "collapsed"
    )


    # --------------------------------------------------------
    # Scenario descriptions
    # --------------------------------------------------------

    if scenario == "A":

        st.caption(
            "Nominal supply enforced · "
            "Early Closure / Late Opening disabled · "
            "schedule extension permitted"
        )


    elif scenario == "B":

        st.caption(
            "Planned completion dates enforced · "
            "additional capacity and Early Closure / "
            "Late Opening permitted"
        )


    else:

        st.caption(
            "Controlled capacity flexibility · "
            "schedule and operational impacts balanced"
        )


    st.divider()


    # --------------------------------------------------------
    # Network input
    # --------------------------------------------------------

    st.subheader(
        "Network Instance"
    )


    uploaded_files = st.file_uploader(

        "Network dataset",

        accept_multiple_files=True,

        type=[
            "csv"
        ],

        label_visibility=
            "collapsed"
    )


    file_count = (

        len(uploaded_files)

        if uploaded_files

        else 0
    )


    files_ready = (
        file_count == 8
    )


    # --------------------------------------------------------
    # Network status
    # --------------------------------------------------------

    if files_ready:

        st.success(
            "● Network instance ready"
        )

        st.caption(
            "8 / 8 source tables loaded"
        )


    elif file_count > 0:

        st.warning(
            f"● Incomplete instance · {file_count}/8"
        )


    else:

        st.caption(
            "○ No network instance loaded"
        )


    # --------------------------------------------------------
    # Uploaded filenames
    # --------------------------------------------------------

    if uploaded_files:

        with st.expander(
            "Source Tables"
        ):

            for uploaded_file in uploaded_files:

                st.caption(
                    f"✓ {uploaded_file.name}"
                )


    st.divider()


    # --------------------------------------------------------
    # Solver button
    # --------------------------------------------------------

    st.subheader(
        "Solver"
    )


    run_button = st.button(

        "Generate Possession Plan",

        type="primary",

        width="stretch",

        disabled=
            not files_ready
    )


    if files_ready:

        st.caption(
            "Scheduling engine ready."
        )


    else:

        st.caption(
            "Load all 8 source tables to enable the solver."
        )


# ============================================================
# 4. MAIN TITLE PANEL
# ============================================================

st.markdown(

    '<div class="main-header-panel">'

    '<div class="header-eyebrow">'
    'LTA · NETWORK OPERATIONS'
    '</div>'

    '<div class="title-cloud">'
    'LTA TRACK ACCESS CONTROL CENTRE'
    '</div>'

    '<div class="header-subtitle">'
    'Railway Possession Planning · '
    'Capacity Management · '
    'Line Alpha / Line Beta'
    '</div>'

    '<div class="online-status">'
    '<span class="online-dot"></span>'
    '<span>PLANNING SYSTEM ONLINE</span>'
    '</div>'

    '</div>',

    unsafe_allow_html=True
)


# ============================================================
# 5. RUN SCHEDULER
# ============================================================

if run_button:

    # --------------------------------------------------------
    # Animated train while scheduler is running
    # --------------------------------------------------------

    animation_placeholder = (
        st.empty()
    )


    animation_placeholder.markdown(

        '<div class="train-status-row">'

        '<span>'
        'Generating possession plan...'
        '</span>'

        '<div class="train-track">'

        '<div class="side-train">'

        '<div class="train-carriage"></div>'

        '<div class="train-carriage"></div>'

        '<div class="train-head"></div>'

        '</div>'

        '</div>'

        '</div>',

        unsafe_allow_html=True
    )


    try:

        # ----------------------------------------------------
        # Package uploaded CSV files
        # ----------------------------------------------------

        file_dict = {

            uploaded_file.name:
                uploaded_file

            for uploaded_file
            in uploaded_files
        }


        # ----------------------------------------------------
        # Run scheduling engine
        # ----------------------------------------------------

        df_acc, df_occ, df_res = (

            run_ps1_scheduler(

                file_dict,

                scenario=
                    scenario
            )
        )


        # ----------------------------------------------------
        # Save generated results
        # ----------------------------------------------------

        st.session_state[
            "df_acc"
        ] = df_acc


        st.session_state[
            "df_occ"
        ] = df_occ


        st.session_state[
            "df_res"
        ] = df_res


        st.session_state[
            "scenario"
        ] = scenario


        animation_placeholder.empty()


    except Exception as error:

        animation_placeholder.empty()


        st.error(
            f"Scheduling engine error: {error}"
        )


        st.stop()


# ============================================================
# 6. SCREEN BEFORE SCHEDULE EXISTS
# ============================================================

if "df_acc" not in st.session_state:

    st.write("")


    status1, status2, status3 = (
        st.columns(3)
    )


    # --------------------------------------------------------
    # Network card
    # --------------------------------------------------------

    with status1:

        if files_ready:

            network_value = (
                '<span class="ready-value">'
                'READY'
                '</span>'
            )

            network_caption = (
                "8 source tables loaded"
            )


        else:

            network_value = (
                '<span class="standby-value">'
                'AWAITING DATA'
                '</span>'
            )

            network_caption = (
                f"{file_count} / 8 source tables"
            )


        st.markdown(

            '<div class="white-info-card">'

            '<div class="white-card-title">'
            'Network'
            '</div>'

            f'<div class="white-card-value">'
            f'{network_value}'
            f'</div>'

            f'<div class="white-card-caption">'
            f'{network_caption}'
            f'</div>'

            '</div>',

            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # Planning mode card
    # --------------------------------------------------------

    with status2:

        mode_name = {

            "A":
                "Fixed Capacity",

            "B":
                "Fixed Completion Dates",

            "C":
                "Balanced Operations"

        }[scenario]


        st.markdown(

            '<div class="white-info-card">'

            '<div class="white-card-title">'
            'Planning Mode'
            '</div>'

            f'<div class="white-card-value">'
            f'{mode_name}'
            f'</div>'

            '<div class="white-card-caption">'
            'Current operating strategy'
            '</div>'

            '</div>',

            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # Solver card
    # --------------------------------------------------------

    with status3:

        if files_ready:

            solver_value = (
                '<span class="ready-value">'
                'READY TO RUN'
                '</span>'
            )


        else:

            solver_value = (
                '<span class="standby-value">'
                'STANDBY'
                '</span>'
            )


        st.markdown(

            '<div class="white-info-card">'

            '<div class="white-card-title">'
            'Solver'
            '</div>'

            f'<div class="white-card-value">'
            f'{solver_value}'
            f'</div>'

            '<div class="white-card-caption">'
            'Possession allocation engine'
            '</div>'

            '</div>',

            unsafe_allow_html=True
        )


    st.stop()


# ============================================================
# 7. LOAD GENERATED RESULTS
# ============================================================

df_acc = (
    st.session_state[
        "df_acc"
    ]
)


df_occ = (
    st.session_state[
        "df_occ"
    ]
)


df_res = (
    st.session_state[
        "df_res"
    ]
)


active_scenario = (
    st.session_state[
        "scenario"
    ]
)


# ============================================================
# 8. CALCULATE MAIN KPIs
# ============================================================

# ------------------------------------------------------------
# Activities
# ------------------------------------------------------------

if not df_acc.empty:

    total_activities = int(

        df_acc[
            "activity_id"
        ].nunique()
    )


else:

    total_activities = 0


# ------------------------------------------------------------
# Access allocations
# ------------------------------------------------------------

total_accesses = (
    len(df_acc)
)


# ------------------------------------------------------------
# Late contracts
# ------------------------------------------------------------

if not df_res.empty:

    late_contracts = int(

        (
            df_res[
                "overrun_days"
            ] > 0
        ).sum()
    )


else:

    late_contracts = 0


# ------------------------------------------------------------
# Total overrun
# ------------------------------------------------------------

if not df_res.empty:

    total_overrun = int(

        df_res[
            "overrun_days"
        ].sum()
    )


else:

    total_overrun = 0


# ------------------------------------------------------------
# Final planning week
# ------------------------------------------------------------

if not df_acc.empty:

    max_week = int(

        df_acc[
            "week"
        ].max()
    )


else:

    max_week = 0


# ------------------------------------------------------------
# ECLO accesses
# ------------------------------------------------------------

if (
    not df_acc.empty
    and "eclo" in df_acc.columns
):

    eclo_nights = int(

        df_acc[
            "eclo"
        ].sum()
    )


else:

    eclo_nights = 0


# ============================================================
# 9. WHITE KPI HELPER
# ============================================================

def white_kpi(
    column,
    label,
    value,
    danger=False
):

    with column:

        if danger:

            label_class = (
                "white-kpi-danger-label"
            )

            value_class = (
                "white-kpi-danger-value"
            )


        else:

            label_class = (
                "white-kpi-label"
            )

            value_class = (
                "white-kpi-value"
            )


        st.markdown(

            f'<div class="white-kpi-card">'

            f'<div class="{label_class}">'
            f'{label}'
            f'</div>'

            f'<div class="{value_class}">'
            f'{value}'
            f'</div>'

            f'</div>',

            unsafe_allow_html=True
        )


# ============================================================
# 10. CURRENT PLAN TITLE
# ============================================================

st.write("")


mode_display = {

    "A":
        "Fixed Capacity",

    "B":
        "Fixed Completion Dates",

    "C":
        "Balanced Operations"

}[active_scenario]


st.subheader(
    f"{mode_display} · Current Possession Plan"
)


# ============================================================
# 11. MAIN KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4, kpi5 = (
    st.columns(5)
)


white_kpi(
    kpi1,
    "Activities",
    total_activities
)


white_kpi(
    kpi2,
    "Access Allocations",
    total_accesses
)


white_kpi(
    kpi3,
    "Contracts Late",
    late_contracts,
    danger=
        late_contracts > 0
)


white_kpi(
    kpi4,
    "Early Closure / Late Opening",
    eclo_nights
)


white_kpi(
    kpi5,
    "Final Week",
    max_week
)


st.divider()


# ============================================================
# 12. MAIN TABS
# ============================================================

(
    tab_plan,
    tab_capacity,
    tab_delivery,
    tab_constraints,
    tab_export

) = st.tabs(

    [
        "Possession Plan",
        "Network Capacity",
        "Contract Delivery",
        "Constraints",
        "Schedule Export"
    ]
)


# ============================================================
# 13. POSSESSION PLAN TAB
# ============================================================

with tab_plan:

    st.subheader(
        "Possession Schedule"
    )


    st.caption(
        "Review scheduled access allocations "
        "across the planning horizon."
    )


    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    filter1, filter2, filter3 = (
        st.columns(
            [
                2,
                2,
                3
            ]
        )
    )


    # --------------------------------------------------------
    # Activity filter
    # --------------------------------------------------------

    with filter1:

        activity_options = sorted(

            df_acc[
                "activity_id"
            ]
            .astype(str)
            .unique()
        )


        selected_activities = (
            st.multiselect(
                "Activities",
                activity_options
            )
        )


    # --------------------------------------------------------
    # Access type filter
    # --------------------------------------------------------

    with filter2:

        access_filter = (
            st.selectbox(

                "Access Type",

                [
                    "All Access Types",
                    "Standard Access",
                    "Early Closure / Late Opening (ECLO)"
                ]
            )
        )


    # --------------------------------------------------------
    # Planning week filter
    # --------------------------------------------------------

    with filter3:

        if max_week > 0:

            week_range = (
                st.slider(

                    "Planning Week",

                    1,

                    max_week,

                    (
                        1,
                        max_week
                    )
                )
            )


        else:

            week_range = (
                1,
                1
            )


    # --------------------------------------------------------
    # Apply filters
    # --------------------------------------------------------

    filtered_acc = (
        df_acc.copy()
    )


    if max_week > 0:

        filtered_acc = (

            filtered_acc[

                filtered_acc[
                    "week"
                ].between(

                    week_range[0],

                    week_range[1]
                )
            ]
        )


    if selected_activities:

        filtered_acc = (

            filtered_acc[

                filtered_acc[
                    "activity_id"
                ]
                .astype(str)
                .isin(
                    selected_activities
                )
            ]
        )


    if access_filter == "Standard Access":

        filtered_acc = (

            filtered_acc[

                filtered_acc[
                    "eclo"
                ] == 0
            ]
        )


    elif (
        access_filter
        ==
        "Early Closure / Late Opening (ECLO)"
    ):

        filtered_acc = (

            filtered_acc[

                filtered_acc[
                    "eclo"
                ] == 1
            ]
        )


    # ========================================================
    # POSSESSION SCHEDULE CHART
    # ========================================================

    if filtered_acc.empty:

        st.warning(
            "No allocations match the current filters."
        )


    else:

        timeline = (
            filtered_acc.copy()
        )


        # Activity labels

        timeline[
            "Activity"
        ] = (

            timeline[
                "activity_id"
            ].astype(str)
        )


        # ----------------------------------------------------
        # Convert ECLO flag into readable names
        # ----------------------------------------------------

        timeline[
            "Access Type"
        ] = (

            timeline[
                "eclo"
            ].map(

                {
                    0:
                        "Standard Access",

                    1:
                        "Early Closure / Late Opening"
                }
            )
        )


        # ====================================================
        # IMPORTANT LEGEND / MARKER DESIGN
        #
        # STANDARD ACCESS
        #   Green Diamond
        #
        # ECLO
        #   Yellow Circle
        # ====================================================

        fig_plan = px.scatter(

            timeline,

            x=
                "week",

            y=
                "Activity",

            # Colour depends on access type
            color=
                "Access Type",

            # Shape depends on access type
            symbol=
                "Access Type",

            # ------------------------------------------------
            # EXACT COLOURS
            # ------------------------------------------------

            color_discrete_map={

                # Standard = classic/lime green
                "Standard Access":
                    "#32CD32",

                # ECLO = yellow
                "Early Closure / Late Opening":
                    "#FFD84D"
            },

            # ------------------------------------------------
            # EXACT SHAPES
            # ------------------------------------------------

            symbol_map={

                # STANDARD ACCESS = GREEN DIAMOND
                "Standard Access":
                    "diamond",

                # ECLO = YELLOW CIRCLE
                "Early Closure / Late Opening":
                    "circle"
            },

            # ------------------------------------------------
            # Hover information
            # ------------------------------------------------

            hover_data=[
                "access_seq",
                "access_night"
            ],

            labels={
                "week":
                    "Planning Week"
            },

            height=max(

                520,

                timeline[
                    "activity_id"
                ].nunique() * 20
            )
        )


        # ----------------------------------------------------
        # Marker appearance
        # ----------------------------------------------------

        fig_plan.update_traces(

            marker=dict(

                size=12,

                # Light border around marker
                line=dict(

                    width=1,

                    color=
                        "#FFF4D6"
                )
            )
        )


        # ----------------------------------------------------
        # Chart appearance
        # ----------------------------------------------------

        fig_plan.update_layout(

            paper_bgcolor=
                "rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(0,0,0,0)",

            font=dict(
                color=
                    "#dceaf6"
            ),

            xaxis=dict(

                dtick=1,

                gridcolor=
                    "rgba(255,255,255,0.07)",

                rangeslider=dict(
                    visible=True
                )
            ),

            yaxis=dict(

                gridcolor=
                    "rgba(255,255,255,0.04)"
            ),

            # Remove redundant legend title
            legend_title_text=""
        )


        # ----------------------------------------------------
        # Display chart
        # ----------------------------------------------------

        st.plotly_chart(

            fig_plan,

            width="stretch"
        )


    # --------------------------------------------------------
    # Access ledger
    # --------------------------------------------------------

    with st.expander(
        "Access Allocation Ledger"
    ):

        st.dataframe(

            filtered_acc,

            width="stretch",

            hide_index=True
        )


# ============================================================
# 14. NETWORK CAPACITY TAB
# ============================================================

with tab_capacity:

    st.subheader(
        "Network Capacity"
    )


    st.caption(
        "Identify high-demand locations and inspect "
        "possession loading across the planning horizon."
    )


    if df_occ.empty:

        st.warning(
            "No occupancy records available."
        )


    else:

        # ----------------------------------------------------
        # Location/week summary
        # ----------------------------------------------------

        occupancy_summary = (

            df_occ

            .groupby(
                [
                    "location_id",
                    "week"
                ]
            )

            .agg(

                activities=(
                    "activity_id",
                    "nunique"
                ),

                possessions=(
                    "co_share_group",
                    "nunique"
                )
            )

            .reset_index()
        )


        # ----------------------------------------------------
        # Total location demand
        # ----------------------------------------------------

        location_totals = (

            occupancy_summary

            .groupby(
                "location_id"
            )

            .agg(

                total_possessions=(
                    "possessions",
                    "sum"
                ),

                total_activities=(
                    "activities",
                    "sum"
                ),

                active_weeks=(
                    "week",
                    "nunique"
                ),

                peak_weekly_possessions=(
                    "possessions",
                    "max"
                )
            )

            .reset_index()
        )


        # ----------------------------------------------------
        # Capacity KPI cards
        # ----------------------------------------------------

        cap1, cap2, cap3 = (
            st.columns(3)
        )


        white_kpi(

            cap1,

            "Locations Used",

            location_totals[
                "location_id"
            ].nunique()
        )


        white_kpi(

            cap2,

            "Active Location-Weeks",

            len(
                occupancy_summary
            )
        )


        white_kpi(

            cap3,

            "Peak Weekly Possessions",

            int(

                occupancy_summary[
                    "possessions"
                ].max()
            )
        )


        st.divider()


        # ====================================================
        # HIGHEST-DEMAND LOCATIONS
        # ====================================================

        st.subheader(
            "Highest-Demand Locations"
        )


        st.caption(
            "Locations are ranked by total scheduled "
            "possession demand."
        )


        top_n = st.selectbox(

            "Locations to Display",

            [
                10,
                15,
                20
            ],

            index=0
        )


        busiest = (

            location_totals

            .sort_values(
                "total_possessions",
                ascending=False
            )

            .head(
                top_n
            )

            .sort_values(
                "total_possessions",
                ascending=True
            )
        )


        # ----------------------------------------------------
        # Green capacity bars
        # ----------------------------------------------------

        fig_pressure = px.bar(

            busiest,

            x=
                "total_possessions",

            y=
                "location_id",

            orientation=
                "h",

            hover_data={
                "total_activities":
                    True,

                "active_weeks":
                    True,

                "peak_weekly_possessions":
                    True,

                "location_id":
                    False,

                "total_possessions":
                    True
            },

            labels={
                "total_possessions":
                    "Total Possessions",

                "location_id":
                    "Network Location"
            }
        )


        fig_pressure.update_traces(

            marker_color=
                "#2E8B57",

            marker_line_color=
                "#66C28A",

            marker_line_width=
                1
        )


        fig_pressure.update_layout(

            height=max(

                450,

                top_n * 38
            ),

            paper_bgcolor=
                "rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(0,0,0,0)",

            font=dict(
                color=
                    "#dceaf6"
            ),

            xaxis=dict(

                title=
                    "Total Scheduled Possessions",

                gridcolor=
                    "rgba(255,255,255,0.08)"
            ),

            yaxis=dict(
                title=""
            )
        )


        st.plotly_chart(

            fig_pressure,

            width="stretch"
        )


        st.divider()


        # ====================================================
        # LOCATION INSPECTOR
        # ====================================================

        st.subheader(
            "Location Inspector"
        )


        st.caption(
            "Inspect weekly possession demand "
            "for an individual network location."
        )


        all_locations = sorted(

            df_occ[
                "location_id"
            ].unique()
        )


        selected_location = (
            st.selectbox(

                "Network Location",

                all_locations
            )
        )


        selected_summary = (

            occupancy_summary[

                occupancy_summary[
                    "location_id"
                ] == selected_location
            ]

            .sort_values(
                "week"
            )
        )


        selected_raw = (

            df_occ[

                df_occ[
                    "location_id"
                ] == selected_location
            ]

            .sort_values(
                "week"
            )
        )


        # ----------------------------------------------------
        # Location KPIs
        # ----------------------------------------------------

        loc1, loc2, loc3 = (
            st.columns(3)
        )


        white_kpi(

            loc1,

            "Activities",

            selected_raw[
                "activity_id"
            ].nunique()
        )


        white_kpi(

            loc2,

            "Possession Groups",

            selected_raw[
                "co_share_group"
            ].nunique()
        )


        white_kpi(

            loc3,

            "Active Weeks",

            selected_raw[
                "week"
            ].nunique()
        )


        # ----------------------------------------------------
        # Weekly location demand
        # ----------------------------------------------------

        fig_location = px.bar(

            selected_summary,

            x=
                "week",

            y=
                "possessions",

            hover_data=[
                "activities"
            ],

            labels={
                "week":
                    "Planning Week",

                "possessions":
                    "Possessions"
            },

            title=
                "Weekly Possession Demand"
        )


        fig_location.update_traces(

            marker_color=
                "#2E8B57",

            marker_line_color=
                "#66C28A",

            marker_line_width=
                1
        )


        fig_location.update_layout(

            height=390,

            paper_bgcolor=
                "rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(0,0,0,0)",

            font=dict(
                color=
                    "#dceaf6"
            ),

            xaxis=dict(

                dtick=1,

                gridcolor=
                    "rgba(255,255,255,0.04)"
            ),

            yaxis=dict(

                dtick=1,

                gridcolor=
                    "rgba(255,255,255,0.09)"
            )
        )


        st.plotly_chart(

            fig_location,

            width="stretch"
        )


        # ----------------------------------------------------
        # Location ledger
        # ----------------------------------------------------

        with st.expander(
            "Location Possession Ledger"
        ):

            st.dataframe(

                selected_raw,

                width="stretch",

                hide_index=True
            )


# ============================================================
# 15. CONTRACT DELIVERY TAB
# ============================================================

with tab_delivery:

    st.subheader(
        "Contract Completion"
    )


    st.caption(
        "Monitor contract delivery performance and "
        "identify schedules requiring attention."
    )


    if df_res.empty:

        st.warning(
            "No contract results available."
        )


    else:

        performance = (

            df_res

            .sort_values(
                "overrun_days",
                ascending=False
            )
        )


        contract_count = (
            len(
                performance
            )
        )


        late_count = int(

            (
                performance[
                    "overrun_days"
                ] > 0
            ).sum()
        )


        overrun_total = int(

            performance[
                "overrun_days"
            ].sum()
        )


        # ----------------------------------------------------
        # Contract KPI cards
        # ----------------------------------------------------

        delivery1, delivery2, delivery3 = (
            st.columns(3)
        )


        white_kpi(

            delivery1,

            "Contracts",

            contract_count
        )


        white_kpi(

            delivery2,

            "Contracts Late",

            late_count,

            danger=
                late_count > 0
        )


        white_kpi(

            delivery3,

            "Total Overrun Days",

            overrun_total
        )


        st.write("")


        # ----------------------------------------------------
        # Contract overrun graph
        # ----------------------------------------------------

        fig_delivery = px.bar(

            performance,

            x=
                "contract_number",

            y=
                "overrun_days",

            hover_data=[
                "simulated_completion_date"
            ],

            labels={
                "contract_number":
                    "Contract",

                "overrun_days":
                    "Overrun Days"
            },

            title=
                "Contract Schedule Overrun"
        )


        # Red bars indicate delay

        fig_delivery.update_traces(

            marker_color=
                "#EF5B63",

            marker_line_color=
                "#FF9AA0",

            marker_line_width=
                1
        )


        fig_delivery.update_layout(

            height=500,

            paper_bgcolor=
                "rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(0,0,0,0)",

            font=dict(
                color=
                    "#dceaf6"
            ),

            xaxis=dict(

                gridcolor=
                    "rgba(255,255,255,0.03)"
            ),

            yaxis=dict(

                gridcolor=
                    "rgba(255,255,255,0.13)"
            )
        )


        st.plotly_chart(

            fig_delivery,

            width="stretch"
        )


        # ----------------------------------------------------
        # Contract warning
        # ----------------------------------------------------

        if late_count == 0:

            st.success(
                "All contracts are within their "
                "planned completion dates."
            )


        else:

            st.warning(

                f"{late_count} contract(s) currently "
                "exceed their planned completion date."
            )


        # ----------------------------------------------------
        # Contract ledger
        # ----------------------------------------------------

        st.subheader(
            "Contract Delivery Ledger"
        )


        st.dataframe(

            performance,

            width="stretch",

            hide_index=True
        )


# ============================================================
# 16. CONSTRAINTS TAB
# ============================================================

with tab_constraints:

    st.subheader(
        "Plan Assurance"
    )


    st.caption(
        "Automated operational checks for the "
        "generated possession schedule."
    )


    # --------------------------------------------------------
    # Duplicate access check
    # --------------------------------------------------------

    duplicates = int(

        df_acc.duplicated(

            subset=[
                "activity_id",
                "access_seq"
            ]

        ).sum()
    )


    check1, check2, check3 = (
        st.columns(3)
    )


    # --------------------------------------------------------
    # Schedule status
    # --------------------------------------------------------

    white_kpi(

        check1,

        "Schedule",

        "Generated"
        if total_activities > 0
        else "Empty"
    )


    # --------------------------------------------------------
    # ECLO policy status
    # --------------------------------------------------------

    if (
        active_scenario == "A"
        and eclo_nights > 0
    ):

        eclo_status = (
            "REVIEW REQUIRED"
        )

        eclo_status_class = (
            "status-bad"
        )


    else:

        eclo_status = (
            "NORMAL"
        )

        eclo_status_class = (
            "status-good"
        )


    with check2:

        st.markdown(

            '<div class="white-kpi-card">'

            '<div class="white-kpi-label">'
            'Early Closure / Late Opening Status'
            '</div>'

            f'<div class="{eclo_status_class}">'
            f'{eclo_status}'
            '</div>'

            '</div>',

            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # Duplicate IDs
    # --------------------------------------------------------

    white_kpi(

        check3,

        "Duplicate Access IDs",

        duplicates,

        danger=
            duplicates > 0
    )


    st.divider()


    # --------------------------------------------------------
    # Constraint monitoring
    # --------------------------------------------------------

    st.subheader(
        "Constraint Monitoring"
    )


    if duplicates == 0:

        st.success(
            "No duplicate access identifiers detected."
        )


    else:

        st.warning(

            f"{duplicates} duplicate access "
            "identifier(s) detected."
        )


    if (
        active_scenario == "A"
        and eclo_nights > 0
    ):

        st.error(
            "Early Closure / Late Opening access "
            "detected under Fixed Capacity mode."
        )


    else:

        st.success(
            "Early Closure / Late Opening status is normal."
        )


# ============================================================
# 17. SCHEDULE EXPORT TAB
# ============================================================

with tab_export:

    st.subheader(
        "Schedule Export"
    )


    st.caption(
        "Operational schedule output package"
    )


    download1, download2, download3 = (
        st.columns(3)
    )


    # --------------------------------------------------------
    # SCHEDULE_ACCESS.csv
    # --------------------------------------------------------

    download1.download_button(

        "SCHEDULE_ACCESS.csv",

        df_acc.to_csv(
            index=False
        ).encode(
            "utf-8"
        ),

        "SCHEDULE_ACCESS.csv",

        mime=
            "text/csv",

        width="stretch"
    )


    # --------------------------------------------------------
    # SCHEDULE_OCCUPANCY.csv
    # --------------------------------------------------------

    download2.download_button(

        "SCHEDULE_OCCUPANCY.csv",

        df_occ.to_csv(
            index=False
        ).encode(
            "utf-8"
        ),

        "SCHEDULE_OCCUPANCY.csv",

        mime=
            "text/csv",

        width="stretch"
    )


    # --------------------------------------------------------
    # RESULTS.csv
    # --------------------------------------------------------

    download3.download_button(

        "RESULTS.csv",

        df_res.to_csv(
            index=False
        ).encode(
            "utf-8"
        ),

        "RESULTS.csv",

        mime=
            "text/csv",

        width="stretch"
    )


    st.divider()


    # ========================================================
    # OUTPUT PREVIEW
    # ========================================================

    st.subheader(
        "Output Preview"
    )


    preview = st.radio(

        "Dataset",

        [
            "Schedule Access",
            "Schedule Occupancy",
            "Results"
        ],

        horizontal=True
    )


    # --------------------------------------------------------
    # Select dataset
    # --------------------------------------------------------

    if preview == "Schedule Access":

        preview_df = (
            df_acc
        )


    elif preview == "Schedule Occupancy":

        preview_df = (
            df_occ
        )


    else:

        preview_df = (
            df_res
        )


    # --------------------------------------------------------
    # Display dataset
    # --------------------------------------------------------

    st.dataframe(

        preview_df,

        width="stretch",

        hide_index=True
    )


# ============================================================
# END OF APP
# ============================================================