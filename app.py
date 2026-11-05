
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# ==========================================
# SMARTDEPLOY WEB DASHBOARD
# ==========================================

st.set_page_config(
    page_title="SmartDeploy",
    page_icon="🚀",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

Q_TABLE_FILE = BASE_DIR / "q_table.json"
HISTORY_FILE = BASE_DIR / "training_history.json"


# ==========================================
# SERVER CONFIGURATION
# ==========================================

SERVERS = [
    {"name": "Small", "capacity": 300, "cost": 10},
    {"name": "Medium", "capacity": 700, "cost": 20},
    {"name": "Large", "capacity": 1200, "cost": 35}
]


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def load_json(path):

    if not path.exists():
        return None

    with open(path, "r") as file:
        return json.load(file)


def get_state(workload):

    if workload <= 300:
        return "Low"

    elif workload <= 700:
        return "Medium"

    return "High"


def get_valid_actions(workload):

    return [
        index
        for index, server in enumerate(SERVERS)
        if workload <= server["capacity"]
    ]


def get_recommendation(workload, q_table):

    state = get_state(workload)

    valid_actions = get_valid_actions(workload)

    if not valid_actions:
        return None

    best_index = max(
        valid_actions,
        key=lambda index: q_table[state][index]
    )

    server = SERVERS[best_index]

    utilization = (
        workload / server["capacity"]
    ) * 100

    latency = 50 + (
        workload / server["capacity"]
    ) * 100

    return {
        "state": state,
        "server": server,
        "utilization": utilization,
        "latency": latency,
        "q_value": q_table[state][best_index]
    }


def load_agent_data():

    q_table = load_json(Q_TABLE_FILE)
    history = load_json(HISTORY_FILE)

    return q_table, history


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🚀 SmartDeploy")

st.sidebar.caption(
    "Intelligent Deployment Optimization"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Deploy Application",
        "Q-Table",
        "Training Center"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Powered by Python and Reinforcement Learning"
)


# ==========================================
# HEADER
# ==========================================

st.title("🚀 SmartDeploy")

st.subheader(
    "Intelligent Deployment Optimization"
)

st.caption(
    "Reinforcement Learning Based Deployment Management"
)

st.divider()


# Load saved agent data

q_table, history = load_agent_data()


# ==========================================
# OVERVIEW PAGE
# ==========================================

if page == "Overview":

    st.header("Dashboard Overview")

    episodes_completed = (
        len(history) if history else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Training Episodes",
        f"{episodes_completed:,}"
    )

    col2.metric(
        "Available Servers",
        "3"
    )

    col3.metric(
        "RL Algorithm",
        "Q-Learning"
    )

    st.divider()

    st.subheader("Server Configurations")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "**Small Server**\n\n"
            "Capacity: 300\n\n"
            "Cost: 10"
        )

    with col2:
        st.info(
            "**Medium Server**\n\n"
            "Capacity: 700\n\n"
            "Cost: 20"
        )

    with col3:
        st.info(
            "**Large Server**\n\n"
            "Capacity: 1200\n\n"
            "Cost: 35"
        )

    st.divider()

    st.subheader("System Status")

    if q_table and history:
        st.success("RL agent trained and ready for deployment.")
    else:
        st.warning("Agent not trained yet. Visit Training Center.")


# ==========================================
# DEPLOY APPLICATION PAGE
# ==========================================

elif page == "Deploy Application":

    st.header("Deploy Your Application")

    st.write(
        "Enter your workload to receive an intelligent "
        "server recommendation from the trained agent."
    )

    workload = st.number_input(
        "Application Workload (requests)",
        min_value=1,
        max_value=1200,
        value=500,
        step=50
    )

    if st.button(
        "Get Deployment Recommendation",
        type="primary"
    ):

        if not q_table:

            st.error(
                "The RL agent has not been trained. "
                "Please visit Training Center first."
            )

        else:

            result = get_recommendation(
                workload,
                q_table
            )

            if result:

                server = result["server"]

                st.success(
                    "RL deployment recommendation generated!"
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Recommended Server",
                    server["name"]
                )

                col2.metric(
                    "Server Cost",
                    server["cost"]
                )

                col3.metric(
                    "Utilization",
                    f"{result['utilization']:.2f}%"
                )

                st.divider()

                st.subheader("Deployment Details")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Workload:**", workload)
                    st.write("**Workload State:**", result["state"])
                    st.write("**Server Capacity:**", server["capacity"])

                with col2:
                    st.write(
                        "**Estimated Latency:**",
                        f"{result['latency']:.2f} ms"
                    )

                    st.write(
                        "**Learned Q-Value:**",
                        round(result["q_value"], 2)
                    )

                st.subheader("Server Utilization")

                st.progress(
                    min(
                        int(result["utilization"]),
                        100
                    )
                )

                if result["utilization"] > 100:
                    st.error("Server overloaded.")

                elif result["utilization"] >= 80:
                    st.warning("High server utilization.")

                else:
                    st.success("Server operating within capacity.")


# ==========================================
# Q-TABLE PAGE
# ==========================================

elif page == "Q-Table":

    st.header("Agent Learning")

    st.write(
        "Explore the Q-values learned by the SmartDeploy agent."
    )

    if not q_table:

        st.warning(
            "No Q-table available. Train the agent first."
        )

    else:

        q_table_data = pd.DataFrame(
            q_table,
            index=["Small", "Medium", "Large"]
        ).T

        st.subheader("Learned Q-Table")

        st.dataframe(
            q_table_data.style.format("{:.2f}"),
            use_container_width=True
        )

        st.divider()

        st.subheader("Q-Value Comparison")

        st.bar_chart(q_table_data)

        st.caption(
            "Higher Q-values represent higher estimated returns "
            "for a particular workload state and server action."
        )


# ==========================================
# TRAINING CENTER PAGE
# ==========================================

elif page == "Training Center":

    st.header("Training Center")

    st.write(
        "Train and evaluate the SmartDeploy reinforcement "
        "learning agent."
    )

    st.subheader("Training Configuration")

    col1, col2 = st.columns(2)

    col1.metric("Training Episodes", "1,000")
    col2.metric("Steps per Episode", "20")

    st.info(
        "Training updates the Q-table and saves training "
        "rewards for dashboard analytics."
    )

    if st.button(
        "Start Agent Training",
        type="primary"
    ):

        with st.spinner(
            "Training SmartDeploy agent..."
        ):

            try:

                result = subprocess.run(
                    [
                        sys.executable,
                        str(BASE_DIR / "main.py")
                    ],
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                if result.returncode == 0:

                    st.success(
                        "Agent training completed successfully!"
                    )

                    st.session_state["training_output"] = (
                        result.stdout
                    )

                    # Reload updated files
                    q_table, history = load_agent_data()

                else:

                    st.error("Training failed.")

                    st.code(
                        result.stderr,
                        language="text"
                    )

            except subprocess.TimeoutExpired:

                st.error(
                    "Training timed out. Please try again."
                )

            except Exception as error:

                st.error(
                    f"An error occurred: {error}"
                )

    if "training_output" in st.session_state:

        with st.expander("View Training Output"):

            st.code(
                st.session_state["training_output"],
                language="text"
            )

    if history:

        st.divider()

        st.subheader("Training Analytics")

        average_reward = sum(history) / len(history)

        col1, col2 = st.columns(2)

        col1.metric(
            "Completed Episodes",
            len(history)
        )

        col2.metric(
            "Average Episode Reward",
            f"{average_reward:.2f}"
        )

        history_df = pd.DataFrame({
            "Episode": range(1, len(history) + 1),
            "Average Reward": history
        })

        st.subheader("Reward Progression")

        st.line_chart(
            history_df.set_index("Episode")
        )

        st.caption(
            "The chart displays the average reward "
            "collected during each training episode."
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "SmartDeploy | Reinforcement Learning Based "
    "Intelligent Deployment Optimization"
)
