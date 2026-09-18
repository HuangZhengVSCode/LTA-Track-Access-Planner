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

/* ----------------------------------------------------------
   MAIN BACKGROUND
   ---------------------------------------------------------- */

.stApp {
    background:
        radial-gradient(
            ellipse at 50% 115%,
            rgba(0, 145, 255, 0.46) 0%,
            rgba(0, 90, 210, 0.25) 24%,
            rgba(0, 40, 120, 0.10) 48%,
            transparent 70%
        ),
        linear-gradient(
            180deg,
            #010307 0%,
            #020812 30%,
            #031427 64%,
            #052c50 100%
        );

    background-attachment: fixed;
    color: #eaf4ff;
}


/* ----------------------------------------------------------
   STREAMLIT HEADER
   ---------------------------------------------------------- */

[data-testid="stHeader"] {
    background: transparent;
}


/* ----------------------------------------------------------
   MAIN PAGE WIDTH
   ---------------------------------------------------------- */

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 3rem;
    max-width: 1550px;
}


/* ----------------------------------------------------------
   NORMAL TEXT
   ---------------------------------------------------------- */

.stApp h1,
.stApp h2,
.stApp h3 {
    color: #ffffff !important;
}

.stApp p,
.stApp label {
    color: #c8dceb;
}


/* ----------------------------------------------------------
   SIDEBAR
   ---------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            rgba(1, 6, 12, 0.995),
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


/* ----------------------------------------------------------
   SIDEBAR BRAND
   ---------------------------------------------------------- */

.sidebar-brand {
    margin-bottom: 12px;
}


.sidebar-brand-title {
    color: #ffffff !important;
    font-size: 1.45rem;
    font-weight: 800;
}


.sidebar-brand-subtitle {
    color: #7990a3 !important;
    font-size: 0.86rem;
    margin-top: 6px;
}


/* ----------------------------------------------------------
   SCENARIO STATUS PANEL
   ---------------------------------------------------------- */

.strategy-panel {
    margin-top: 12px;
    padding: 13px 14px;

    border-radius: 10px;

    background:
        rgba(4, 31, 55, 0.82);

    border:
        1px solid rgba(70, 160, 220, 0.17);
}


.strategy-row {
    display: flex;
    align-items: center;
    gap: 8px;

    margin: 8px 0;

    color: #bcd2e2 !important;

    font-size: 0.78rem;
    font-weight: 650;
}


.strategy-dot-blue,
.strategy-dot-green,
.strategy-dot-yellow {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    flex: 0 0 auto;
}


.strategy-dot-blue {
    background: #39a9ff;

    box-shadow:
        0 0 6px rgba(57, 169, 255, 0.60);
}


.strategy-dot-green {
    background: #39d98a;

    box-shadow:
        0 0 6px rgba(57, 217, 138, 0.60);
}


.strategy-dot-yellow {
    background: #ffd84d;

    box-shadow:
        0 0 6px rgba(255, 216, 77, 0.60);
}


/* ----------------------------------------------------------
   MAIN HEADER PANEL
   ---------------------------------------------------------- */

.main-header-panel {
    padding: 22px 28px;

    border-radius: 16px;

    border:
        1px solid rgba(80, 170, 255, 0.18);

    background:
        rgba(1, 9, 18, 0.45);

    margin-bottom: 24px;
}


/* Smaller header after schedule generation */

.main-header-panel.compact {
    padding: 15px 24px;
    margin-bottom: 18px;
}


.header-eyebrow {
    color: #8396a8 !important;

    font-size: 0.78rem;
    font-weight: 700;

    letter-spacing: 0.5px;

    margin-bottom: 15px;
}


/* ----------------------------------------------------------
   WHITE TITLE CLOUD
   ---------------------------------------------------------- */

.title-cloud {
    display: inline-block;

    background:
        linear-gradient(
            135deg,
            #ffffff 0%,
            #f4f9ff 100%
        );

    color: #082f56 !important;

    padding: 12px 25px;

    border-radius: 28px;

    font-size: clamp(
        1.5rem,
        2.35vw,
        2.3rem
    );

    font-weight: 850;

    letter-spacing: 0.45px;

    border:
        1px solid rgba(180, 215, 240, 0.90);

    box-shadow:
        0 7px 24px rgba(0, 0, 0, 0.25),
        0 0 20px rgba(255, 255, 255, 0.12);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}


.compact .title-cloud {
    padding: 9px 21px;

    font-size: clamp(
        1.3rem,
        2vw,
        1.9rem
    );
}


.title-cloud:hover {
    transform: translateY(-2px);

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.30),
        0 0 13px rgba(255, 255, 255, 0.50),
        0 0 28px rgba(80, 185, 255, 0.30);
}


.header-subtitle {
    color: #c9deee !important;

    margin-top: 18px;

    font-size: 0.94rem;
}


.compact .header-subtitle {
    margin-top: 12px;
    font-size: 0.86rem;
}


/* ----------------------------------------------------------
   ONLINE STATUS
   ---------------------------------------------------------- */

.online-status {
    display: flex;
    align-items: center;

    gap: 10px;

    margin-top: 16px;

    color: #dfffee !important;

    font-size: 0.88rem;

    font-weight: 750;
}


.compact .online-status {
    margin-top: 11px;
    font-size: 0.80rem;
}


.online-dot {
    width: 10px;
    height: 10px;

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
        transform: scale(1);

        box-shadow:
            0 0 5px #38f58a,
            0 0 10px rgba(56, 245, 138, 0.55);
    }

    50% {
        opacity: 0.45;
        transform: scale(0.72);

        box-shadow:
            0 0 2px #38f58a;
    }

    100% {
        opacity: 1;
        transform: scale(1);

        box-shadow:
            0 0 7px #38f58a,
            0 0 18px rgba(56, 245, 138, 0.85);
    }
}


/* ----------------------------------------------------------
   PRE-SCHEDULE INFORMATION CARDS
   ---------------------------------------------------------- */

.white-info-card {
    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #f5f9fd 100%
        );

    border-radius: 14px;

    padding: 20px 22px;

    height: 150px;

    box-sizing: border-box;

    border:
        1px solid #d7e5ef;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.20);

    transition:
        transform 0.20s ease,
        box-shadow 0.20s ease;
}


.white-info-card:hover {
    transform: translateY(-3px);

    box-shadow:
        0 12px 30px rgba(0, 0, 0, 0.28),
        0 0 16px rgba(70, 175, 255, 0.16);
}


.white-card-title {
    color: #0b365d !important;

    font-size: 1.25rem;

    font-weight: 800;

    margin-bottom: 16px;
}


.white-card-value {
    color: #164d77 !important;

    font-size: 0.98rem;

    font-weight: 700;
}


.white-card-caption {
    color: #657d91 !important;

    font-size: 0.82rem;

    margin-top: 11px;
}


.ready-value {
    display: inline-block;

    color: #15704a !important;

    background: #e5f8ef;

    border:
        1px solid #b8ead3;

    border-radius: 7px;

    padding: 6px 11px;

    font-weight: 800;
}


.standby-value {
    display: inline-block;

    color: #6a7884 !important;

    background: #edf2f5;

    border:
        1px solid #d5dfe6;

    border-radius: 7px;

    padding: 6px 11px;

    font-weight: 750;
}


/* ----------------------------------------------------------
   COMPACT KPI CARDS
   ---------------------------------------------------------- */

.white-kpi-card {
    background: #ffffff;

    border-radius: 12px;

    padding: 16px 18px;

    height: 112px;

    box-sizing: border-box;

    border:
        1px solid #d7e5ef;

    box-shadow:
        0 6px 20px rgba(0, 0, 0, 0.18);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}


.white-kpi-card:hover {
    transform: translateY(-2px);

    box-shadow:
        0 10px 25px rgba(0, 0, 0, 0.25);
}


.white-kpi-label {
    color: #355570 !important;

    font-size: 0.76rem;

    font-weight: 750;

    text-transform: uppercase;

    letter-spacing: 0.35px;

    margin-bottom: 10px;
}


.white-kpi-value {
    color: #073763 !important;

    font-size: 1.85rem;

    font-weight: 850;

    line-height: 1;
}


.white-kpi-danger-label {
    color: #cf4b55 !important;

    font-size: 0.76rem;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: 0.35px;

    margin-bottom: 10px;
}


.white-kpi-danger-value {
    color: #ef5b63 !important;

    font-size: 1.85rem;

    font-weight: 850;

    line-height: 1;
}


.white-kpi-success-label {
    color: #26734d !important;

    font-size: 0.76rem;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: 0.35px;

    margin-bottom: 10px;
}


.white-kpi-success-value {
    color: #1c9b5f !important;

    font-size: 1.85rem;

    font-weight: 850;

    line-height: 1;
}


/* ----------------------------------------------------------
   SCHEDULE HEALTH STRIP
   ---------------------------------------------------------- */

.health-strip {
    display: flex;

    align-items: center;

    flex-wrap: wrap;

    gap: 10px;

    padding: 11px 14px;

    margin: 17px 0 20px 0;

    border-radius: 10px;

    background:
        rgba(3, 27, 47, 0.88);

    border:
        1px solid rgba(70, 170, 225, 0.18);

    box-shadow:
        0 4px 16px rgba(0, 0, 0, 0.14);
}


.health-item {
    display: flex;

    align-items: center;

    gap: 7px;

    padding: 6px 10px;

    border-radius: 7px;

    background:
        rgba(255, 255, 255, 0.035);

    color: #c7dbe9 !important;

    font-size: 0.76rem;

    font-weight: 700;
}


.health-dot-green,
.health-dot-red,
.health-dot-blue,
.health-dot-yellow {
    width: 7px;
    height: 7px;

    border-radius: 50%;
}


.health-dot-green {
    background: #39d98a;
}


.health-dot-red {
    background: #ef5b63;
}


.health-dot-blue {
    background: #39a9ff;
}


.health-dot-yellow {
    background: #ffd84d;
}


/* ----------------------------------------------------------
   CONSTRAINT STATUS
   ---------------------------------------------------------- */

.status-good {
    color: #25A65A !important;

    font-size: 1.75rem;

    font-weight: 850;

    line-height: 1.05;
}


.status-bad {
    color: #EF5B63 !important;

    font-size: 1.55rem;

    font-weight: 850;

    line-height: 1.05;
}


/* ----------------------------------------------------------
   BUTTONS
   ---------------------------------------------------------- */

.stButton > button {
    width: 100%;

    min-height: 44px;

    border-radius: 8px;

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

    font-weight: 750 !important;

    box-shadow:
        0 5px 20px rgba(0, 125, 255, 0.24);

    transition:
        transform 0.22s ease,
        box-shadow 0.22s ease;
}


.stButton > button p {
    color: #ffffff !important;
    font-weight: 750 !important;
}


.stButton > button:hover {
    transform: translateY(-2px);

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

    opacity: 0.70;

    box-shadow: none;
}


/* ----------------------------------------------------------
   SELECT BOX
   ---------------------------------------------------------- */

div[data-baseweb="select"] > div {
    background:
        #f7f9fc !important;

    color:
        #173a58 !important;

    border-color:
        #d5e1ea !important;
}


/* ----------------------------------------------------------
   FILE UPLOADER
   ---------------------------------------------------------- */

[data-testid="stFileUploaderDropzone"] {
    background:
        rgba(7, 29, 52, 0.72) !important;

    border:
        1px dashed rgba(70, 175, 255, 0.42) !important;

    border-radius: 10px;
}


/* ----------------------------------------------------------
   TABS
   ---------------------------------------------------------- */

button[data-baseweb="tab"] {
    color:
        #a7c2d7 !important;

    font-weight: 550;
}


button[data-baseweb="tab"][aria-selected="true"] {
    color:
        #ffffff !important;

    font-weight: 750;
}


/* ----------------------------------------------------------
   TABLES
   ---------------------------------------------------------- */

[data-testid="stDataFrame"] {
    border:
        1px solid rgba(80, 170, 255, 0.15);

    border-radius: 10px;

    overflow: hidden;
}


/* ----------------------------------------------------------
   ANIMATED TRAIN
   ---------------------------------------------------------- */

.train-status-row {
    display: flex;

    align-items: center;

    gap: 18px;

    margin: 12px 0 18px 0;

    color: #d7e8f5 !important;
}


.train-track {
    position: relative;

    width: 200px;
    height: 43px;

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


/* ----------------------------------------------------------
   DIVIDERS / FOOTER
   ---------------------------------------------------------- */

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
    # Sidebar branding
    #
    # IMPORTANT:
    # HTML is kept as a single string so Streamlit does not
    # interpret indented HTML as a Markdown code block.
    # --------------------------------------------------------

    sidebar_brand_html = (
        '<div class="sidebar-brand">'
        '<div class="sidebar-brand-title">'
        'Track Access Planner'
        '</div>'
        '<div class="sidebar-brand-subtitle">'
        'Network Planning &amp; Possession Control'
        '</div>'
        '</div>'
    )

    st.markdown(
        sidebar_brand_html,
        unsafe_allow_html=True
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

        label_visibility="collapsed"
    )


    # --------------------------------------------------------
    # Scenario A information
    # --------------------------------------------------------

    if scenario == "A":

        strategy_html = (
            '<div class="strategy-panel">'

            '<div class="strategy-row">'
            '<span class="strategy-dot-blue"></span>'
            '<span>NOMINAL CAPACITY ENFORCED</span>'
            '</div>'

            '<div class="strategy-row">'
            '<span class="strategy-dot-blue"></span>'
            '<span>ECLO DISABLED</span>'
            '</div>'

            '<div class="strategy-row">'
            '<span class="strategy-dot-yellow"></span>'
            '<span>SCHEDULE EXTENSION PERMITTED</span>'
            '</div>'

            '</div>'
        )


    # --------------------------------------------------------
    # Scenario B information
    # --------------------------------------------------------

    elif scenario == "B":

        strategy_html = (
            '<div class="strategy-panel">'

            '<div class="strategy-row">'
            '<span class="strategy-dot-green"></span>'
            '<span>DEADLINES ENFORCED</span>'
            '</div>'

            '<div class="strategy-row">'
            '<span class="strategy-dot-blue"></span>'
            '<span>EXCESS CAPACITY PERMITTED</span>'
            '</div>'

            '<div class="strategy-row">'
            '<span class="strategy-dot-yellow"></span>'
            '<span>ECLO PERMITTED</span>'
            '</div>'

            '</div>'
        )


    # --------------------------------------------------------
    # Scenario C information
    # --------------------------------------------------------

    else:

        strategy_html = (
            '<div class="strategy-panel">'

            '<div class="strategy-row">'
            '<span class="strategy-dot-blue"></span>'
            '<span>CAPACITY FLEXIBILITY CONTROLLED</span>'
            '</div>'

            '<div class="strategy-row">'
            '<span class="strategy-dot-yellow"></span>'
            '<span>DELIVERY / CAPACITY BALANCED</span>'
            '</div>'

            '<div class="strategy-row">'
            '<span class="strategy-dot-green"></span>'
            '<span>ECLO CONTROLLED</span>'
            '</div>'

            '</div>'
        )


    # Display scenario information

    st.markdown(
        strategy_html,
        unsafe_allow_html=True
    )


    st.divider()


    # --------------------------------------------------------
    # Network files
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

        label_visibility="collapsed"
    )


    # Number of uploaded files

    file_count = (
        len(uploaded_files)
        if uploaded_files
        else 0
    )


    # All 8 files required

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
            f"● Incomplete network · {file_count}/8"
        )


    else:

        st.caption(
            "○ No network instance loaded"
        )


    # --------------------------------------------------------
    # Uploaded file list
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
    # Solver
    # --------------------------------------------------------

    st.subheader(
        "Solver"
    )


    run_button = st.button(

        "Generate Possession Plan",

        type="primary",

        width="stretch",

        disabled=not files_ready
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
# 4. CHECK WHETHER A PLAN EXISTS
# ============================================================

plan_exists = (
    "df_acc"
    in st.session_state
)


# ============================================================
# 5. MAIN HEADER
# ============================================================

header_class = (
    "main-header-panel compact"
    if plan_exists
    else "main-header-panel"
)


# Use one HTML string to avoid Markdown formatting problems

main_header_html = (
    f'<div class="{header_class}">'

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

    '</div>'
)


st.markdown(
    main_header_html,
    unsafe_allow_html=True
)


# ============================================================
# 6. RUN SCHEDULER
# ============================================================

if run_button:

    animation_placeholder = (
        st.empty()
    )


    # --------------------------------------------------------
    # Train animation
    # --------------------------------------------------------

    train_html = (
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

        '</div>'
    )


    animation_placeholder.markdown(
        train_html,
        unsafe_allow_html=True
    )


    try:

        # ----------------------------------------------------
        # Package uploaded files
        # ----------------------------------------------------

        file_dict = {

            uploaded_file.name:
                uploaded_file

            for uploaded_file
            in uploaded_files
        }


        # ----------------------------------------------------
        # Run scheduler
        # ----------------------------------------------------

        df_acc, df_occ, df_res = (

            run_ps1_scheduler(

                file_dict,

                scenario=scenario
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


        # Refresh page after schedule is generated

        st.rerun()


    except Exception as error:

        animation_placeholder.empty()


        st.error(
            f"Scheduling engine error: {error}"
        )


        st.stop()


# ============================================================
# 7. PRE-SCHEDULE HOME SCREEN
# ============================================================

if "df_acc" not in st.session_state:

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


        network_card_html = (
            '<div class="white-info-card">'

            '<div class="white-card-title">'
            'Network'
            '</div>'

            '<div class="white-card-value">'
            f'{network_value}'
            '</div>'

            '<div class="white-card-caption">'
            f'{network_caption}'
            '</div>'

            '</div>'
        )


        st.markdown(
            network_card_html,
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


        planning_card_html = (
            '<div class="white-info-card">'

            '<div class="white-card-title">'
            'Planning Mode'
            '</div>'

            '<div class="white-card-value">'
            f'{mode_name}'
            '</div>'

            '<div class="white-card-caption">'
            'Current operating strategy'
            '</div>'

            '</div>'
        )


        st.markdown(
            planning_card_html,
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


        solver_card_html = (
            '<div class="white-info-card">'

            '<div class="white-card-title">'
            'Solver'
            '</div>'

            '<div class="white-card-value">'
            f'{solver_value}'
            '</div>'

            '<div class="white-card-caption">'
            'Possession allocation engine'
            '</div>'

            '</div>'
        )


        st.markdown(
            solver_card_html,
            unsafe_allow_html=True
        )


    st.stop()


# ============================================================
# 8. LOAD GENERATED RESULTS
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
# 9. CALCULATE KPIs
# ============================================================

# Activities

if not df_acc.empty:

    total_activities = int(

        df_acc[
            "activity_id"
        ].nunique()
    )


else:

    total_activities = 0


# Access allocations

total_accesses = (
    len(df_acc)
)


# Contracts late

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


# Total overrun

if not df_res.empty:

    total_overrun = int(

        df_res[
            "overrun_days"
        ].sum()
    )


else:

    total_overrun = 0


# Final planning week

if not df_acc.empty:

    max_week = int(

        df_acc[
            "week"
        ].max()
    )


else:

    max_week = 0


# ECLO accesses

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


# Duplicate access IDs

duplicates = int(

    df_acc.duplicated(

        subset=[
            "activity_id",
            "access_seq"
        ]

    ).sum()
)


# ============================================================
# 10. KPI CARD HELPER
# ============================================================

def white_kpi(
    column,
    label,
    value,
    state="normal"
):

    with column:

        if state == "danger":

            label_class = (
                "white-kpi-danger-label"
            )

            value_class = (
                "white-kpi-danger-value"
            )


        elif state == "success":

            label_class = (
                "white-kpi-success-label"
            )

            value_class = (
                "white-kpi-success-value"
            )


        else:

            label_class = (
                "white-kpi-label"
            )

            value_class = (
                "white-kpi-value"
            )


        card_html = (
            '<div class="white-kpi-card">'

            f'<div class="{label_class}">'
            f'{label}'
            '</div>'

            f'<div class="{value_class}">'
            f'{value}'
            '</div>'

            '</div>'
        )


        st.markdown(
            card_html,
            unsafe_allow_html=True
        )


# ============================================================
# 11. CURRENT PLAN SUMMARY
# ============================================================

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
# 12. KPI ROW
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


# Late contract colour

if late_contracts == 0:

    white_kpi(
        kpi3,
        "Contracts Late",
        late_contracts,
        state="success"
    )


else:

    white_kpi(
        kpi3,
        "Contracts Late",
        late_contracts,
        state="danger"
    )


white_kpi(
    kpi4,
    "ECLO Accesses",
    eclo_nights
)


white_kpi(
    kpi5,
    "Final Week",
    max_week
)


# ============================================================
# 13. SCHEDULE HEALTH STRIP
# ============================================================

schedule_dot = (
    "health-dot-green"
    if total_activities > 0
    else "health-dot-red"
)


late_dot = (
    "health-dot-green"
    if late_contracts == 0
    else "health-dot-red"
)


duplicate_dot = (
    "health-dot-green"
    if duplicates == 0
    else "health-dot-red"
)


health_html = (
    '<div class="health-strip">'

    '<div class="health-item">'
    f'<span class="{schedule_dot}"></span>'
    '<span>SCHEDULE GENERATED</span>'
    '</div>'

    '<div class="health-item">'
    '<span class="health-dot-blue"></span>'
    f'<span>{total_activities} ACTIVITIES</span>'
    '</div>'

    '<div class="health-item">'
    f'<span class="{late_dot}"></span>'
    f'<span>{late_contracts} CONTRACTS LATE</span>'
    '</div>'

    '<div class="health-item">'
    f'<span class="{duplicate_dot}"></span>'
    f'<span>{duplicates} DUPLICATE ACCESS IDs</span>'
    '</div>'

    '<div class="health-item">'
    '<span class="health-dot-yellow"></span>'
    f'<span>{eclo_nights} ECLO ACCESSES</span>'
    '</div>'

    '<div class="health-item">'
    '<span class="health-dot-blue"></span>'
    '<span>READY TO EXPORT</span>'
    '</div>'

    '</div>'
)


st.markdown(
    health_html,
    unsafe_allow_html=True
)


# ============================================================
# 14. MAIN TABS
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
# 15. POSSESSION PLAN TAB
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


    # Activity filter

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


    # Access type filter

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


    # Planning week filter

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
    # Filter schedule
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


    # --------------------------------------------------------
    # Possession schedule chart
    # --------------------------------------------------------

    if filtered_acc.empty:

        st.warning(
            "No allocations match the current filters."
        )


    else:

        timeline = (
            filtered_acc.copy()
        )


        timeline[
            "Activity"
        ] = (

            timeline[
                "activity_id"
            ].astype(str)
        )


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


        # ----------------------------------------------------
        # Marker design
        #
        # Standard = green diamond
        # ECLO     = yellow circle
        # ----------------------------------------------------

        fig_plan = px.scatter(

            timeline,

            x="week",

            y="Activity",

            color="Access Type",

            symbol="Access Type",

            color_discrete_map={

                "Standard Access":
                    "#32CD32",

                "Early Closure / Late Opening":
                    "#FFD84D"
            },

            symbol_map={

                "Standard Access":
                    "diamond",

                "Early Closure / Late Opening":
                    "circle"
            },

            hover_data=[
                "access_seq",
                "access_night"
            ],

            labels={
                "week":
                    "Planning Week"
            },

            height=max(

                500,

                timeline[
                    "activity_id"
                ].nunique() * 19
            )
        )


        fig_plan.update_traces(

            marker=dict(

                size=11,

                line=dict(

                    width=1,

                    color="#F5F8FA"
                )
            )
        )


        fig_plan.update_layout(

            paper_bgcolor=
                "rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(0,0,0,0)",

            font=dict(
                color="#dceaf6"
            ),

            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            ),

            xaxis=dict(

                dtick=1,

                gridcolor=
                    "rgba(255,255,255,0.065)",

                rangeslider=dict(
                    visible=True
                )
            ),

            yaxis=dict(

                gridcolor=
                    "rgba(255,255,255,0.04)"
            ),

            legend_title_text=""
        )


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
# 16. NETWORK CAPACITY TAB
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
        # Summarise occupancy
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
        # Location totals
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
        # Capacity KPIs
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


        # ----------------------------------------------------
        # Highest-demand locations
        # ----------------------------------------------------

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
        # Green demand bars
        # ----------------------------------------------------

        fig_pressure = px.bar(

            busiest,

            x="total_possessions",

            y="location_id",

            orientation="h",

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

            marker_color="#2E8B57",

            marker_line_color="#66C28A",

            marker_line_width=1
        )


        fig_pressure.update_layout(

            height=max(
                420,
                top_n * 36
            ),

            paper_bgcolor=
                "rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(0,0,0,0)",

            font=dict(
                color="#dceaf6"
            ),

            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
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


        # ----------------------------------------------------
        # Location inspector
        # ----------------------------------------------------

        st.subheader(
            "Location Inspector"
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
                ]
                == selected_location
            ]

            .sort_values(
                "week"
            )
        )


        selected_raw = (

            df_occ[

                df_occ[
                    "location_id"
                ]
                == selected_location
            ]

            .sort_values(
                "week"
            )
        )


        # Location KPI cards

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


        # Weekly location demand

        fig_location = px.bar(

            selected_summary,

            x="week",

            y="possessions",

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

            marker_color="#2E8B57",

            marker_line_color="#66C28A",

            marker_line_width=1
        )


        fig_location.update_layout(

            height=370,

            paper_bgcolor=
                "rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(0,0,0,0)",

            font=dict(
                color="#dceaf6"
            ),

            margin=dict(
                l=10,
                r=10,
                t=45,
                b=10
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


        with st.expander(
            "Location Possession Ledger"
        ):

            st.dataframe(

                selected_raw,

                width="stretch",

                hide_index=True
            )


# ============================================================
# 17. CONTRACT DELIVERY TAB
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
        # Contract KPIs
        # ----------------------------------------------------

        delivery1, delivery2, delivery3 = (
            st.columns(3)
        )


        white_kpi(

            delivery1,

            "Contracts",

            contract_count
        )


        if late_count == 0:

            white_kpi(

                delivery2,

                "Contracts Late",

                late_count,

                state="success"
            )


        else:

            white_kpi(

                delivery2,

                "Contracts Late",

                late_count,

                state="danger"
            )


        if overrun_total == 0:

            white_kpi(

                delivery3,

                "Total Overrun Days",

                overrun_total,

                state="success"
            )


        else:

            white_kpi(

                delivery3,

                "Total Overrun Days",

                overrun_total,

                state="danger"
            )


        st.write("")


        # ----------------------------------------------------
        # Contract overrun chart
        # ----------------------------------------------------

        fig_delivery = px.bar(

            performance,

            x="contract_number",

            y="overrun_days",

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


        fig_delivery.update_traces(

            marker_color="#EF5B63",

            marker_line_color="#FF9AA0",

            marker_line_width=1
        )


        fig_delivery.update_layout(

            height=450,

            paper_bgcolor=
                "rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(0,0,0,0)",

            font=dict(
                color="#dceaf6"
            ),

            margin=dict(
                l=10,
                r=10,
                t=45,
                b=10
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


        # Contract message

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


        # Contract ledger

        st.subheader(
            "Contract Delivery Ledger"
        )


        st.dataframe(

            performance,

            width="stretch",

            hide_index=True
        )


# ============================================================
# 18. CONSTRAINTS TAB
# ============================================================

with tab_constraints:

    st.subheader(
        "Plan Assurance"
    )


    st.caption(
        "Automated operational checks for the "
        "generated possession schedule."
    )


    check1, check2, check3 = (
        st.columns(3)
    )


    # --------------------------------------------------------
    # Schedule card
    # --------------------------------------------------------

    white_kpi(

        check1,

        "Schedule",

        "Generated"
        if total_activities > 0
        else "Empty"
    )


    # --------------------------------------------------------
    # ECLO status
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

        eclo_card_html = (
            '<div class="white-kpi-card">'

            '<div class="white-kpi-label">'
            'ECLO Status'
            '</div>'

            f'<div class="{eclo_status_class}">'
            f'{eclo_status}'
            '</div>'

            '</div>'
        )


        st.markdown(
            eclo_card_html,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # Duplicate access IDs
    # --------------------------------------------------------

    if duplicates == 0:

        white_kpi(

            check3,

            "Duplicate Access IDs",

            duplicates,

            state="success"
        )


    else:

        white_kpi(

            check3,

            "Duplicate Access IDs",

            duplicates,

            state="danger"
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

        st.error(

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
# 19. SCHEDULE EXPORT TAB
# ============================================================

with tab_export:

    st.subheader(
        "Schedule Export"
    )


    st.caption(
        "Download the generated operational schedule package."
    )


    st.success(
        "Schedule outputs generated and ready for export."
    )


    download1, download2, download3 = (
        st.columns(3)
    )


    # --------------------------------------------------------
    # Schedule Access
    # --------------------------------------------------------

    download1.download_button(

        "SCHEDULE_ACCESS.csv",

        df_acc.to_csv(
            index=False
        ).encode(
            "utf-8"
        ),

        "SCHEDULE_ACCESS.csv",

        mime="text/csv",

        width="stretch"
    )


    # --------------------------------------------------------
    # Schedule Occupancy
    # --------------------------------------------------------

    download2.download_button(

        "SCHEDULE_OCCUPANCY.csv",

        df_occ.to_csv(
            index=False
        ).encode(
            "utf-8"
        ),

        "SCHEDULE_OCCUPANCY.csv",

        mime="text/csv",

        width="stretch"
    )


    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    download3.download_button(

        "RESULTS.csv",

        df_res.to_csv(
            index=False
        ).encode(
            "utf-8"
        ),

        "RESULTS.csv",

        mime="text/csv",

        width="stretch"
    )


    st.divider()


    # --------------------------------------------------------
    # Output preview
    # --------------------------------------------------------

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


    st.dataframe(

        preview_df,

        width="stretch",

        hide_index=True
    )


# ============================================================
# END OF APP
# ============================================================