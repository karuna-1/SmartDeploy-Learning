
import json
import random

# ==========================================
# SMARTDEPLOY: RL DEPLOYMENT OPTIMIZER
# ==========================================

# 1. Server configurations

SERVERS = [
    {"name": "Small", "capacity": 300, "cost": 10},
    {"name": "Medium", "capacity": 700, "cost": 20},
    {"name": "Large", "capacity": 1200, "cost": 35}
]

ACTIONS = ["Small", "Medium", "Large"]

# 2. Training configuration

LEARNING_RATE = 0.8
DISCOUNT_FACTOR = 0.9
INITIAL_EPSILON = 0.2
EPISODES = 1000
STEPS_PER_EPISODE = 20

TRAINING_WORKLOADS = [100, 200, 300, 500, 700, 900, 1100]

SUCCESS_REWARD = 10
OVERLOAD_PENALTY = -100

# 3. Initialize Q-table

Q_TABLE = {
    "Low": [0.0, 0.0, 0.0],
    "Medium": [0.0, 0.0, 0.0],
    "High": [0.0, 0.0, 0.0]
}


# 4. Identify workload state

def get_state(workload):
    if workload <= 300:
        return "Low"
    elif workload <= 700:
        return "Medium"
    return "High"


# 5. Identify valid server actions

def get_valid_actions(workload):
    return [
        index
        for index, server in enumerate(SERVERS)
        if workload <= server["capacity"]
    ]


# 6. Calculate deployment reward

def calculate_reward(workload, server):

    if workload > server["capacity"]:
        return OVERLOAD_PENALTY

    utilization = workload / server["capacity"]

    cost_penalty = server["cost"] * 0.2
    utilization_bonus = utilization * 5

    return SUCCESS_REWARD + utilization_bonus - cost_penalty


# 7. Select action using epsilon-greedy policy

def choose_action(state, valid_actions, epsilon):

    if random.random() < epsilon:
        return random.choice(valid_actions)

    highest_value = max(
        Q_TABLE[state][index]
        for index in valid_actions
    )

    best_actions = [
        index for index in valid_actions
        if Q_TABLE[state][index] == highest_value
    ]

    return random.choice(best_actions)


# 8. Initialize training history

training_history = []


# 9. Train the agent

def train_agent():

    global training_history

    training_history = []

    epsilon = INITIAL_EPSILON

    for episode in range(EPISODES):

        total_reward = 0

        # Start with a random workload
        workload = random.choice(TRAINING_WORKLOADS)

        for step in range(STEPS_PER_EPISODE):

            state = get_state(workload)

            valid_actions = get_valid_actions(workload)

            # Choose an action
            action_index = choose_action(
                state,
                valid_actions,
                epsilon
            )

            selected_server = SERVERS[action_index]

            # Calculate immediate reward
            reward = calculate_reward(
                workload,
                selected_server
            )

            # Simulate the next workload state
            next_workload = random.choice(
                TRAINING_WORKLOADS
            )

            next_state = get_state(next_workload)

            next_valid_actions = get_valid_actions(
                next_workload
            )

            # Calculate maximum future Q-value
            future_value = max(
                Q_TABLE[next_state][index]
                for index in next_valid_actions
            )

            # Q-learning update
            old_value = Q_TABLE[state][action_index]

            new_value = old_value + LEARNING_RATE * (
                reward
                + DISCOUNT_FACTOR * future_value
                - old_value
            )

            Q_TABLE[state][action_index] = new_value

            total_reward += reward

            # Move to next workload
            workload = next_workload

        # Save average reward for this episode
        average_episode_reward = (
            total_reward / STEPS_PER_EPISODE
        )

        training_history.append(
            round(average_episode_reward, 4)
        )

        # Gradually reduce exploration
        epsilon = max(0.01, epsilon * 0.995)

        if (episode + 1) % 100 == 0:
            print(
                f"Episode {episode + 1} | "
                f"Average Reward: {average_episode_reward:.2f} | "
                f"Epsilon: {epsilon:.3f}"
            )

    save_results()

    return Q_TABLE


# 10. Save Q-table and training history

def save_results():

    with open("q_table.json", "w") as file:
        json.dump(Q_TABLE, file, indent=4)

    with open("training_history.json", "w") as file:
        json.dump(training_history, file, indent=4)

    print("\nQ-table saved successfully!")
    print("Training history saved successfully!")


# 11. Deployment testing

def test_deployments():

    test_workloads = [100, 500, 900, 1100]

    print("\n========== DEPLOYMENT TESTING ==========")

    for workload in test_workloads:

        state = get_state(workload)

        valid_actions = get_valid_actions(workload)

        best_action = max(
            valid_actions,
            key=lambda index: Q_TABLE[state][index]
        )

        server = SERVERS[best_action]

        utilization = (
            workload / server["capacity"]
        ) * 100

        latency = 50 + (
            workload / server["capacity"]
        ) * 100

        print(f"\nWorkload: {workload}")
        print(f"State: {state}")
        print(f"Server: {server['name']}")
        print(f"Cost: {server['cost']}")
        print(f"Utilization: {utilization:.2f}%")
        print(f"Estimated Latency: {latency:.2f} ms")


# 12. Main execution

if __name__ == "__main__":

    print("===================================")
    print("       SMARTDEPLOY TRAINING")
    print("===================================")

    train_agent()

    print("\n========== LEARNED Q-TABLE ==========")

    for state, values in Q_TABLE.items():
        print(
            state,
            [round(value, 2) for value in values]
        )

    test_deployments()

    print("\nTraining completed successfully!")
