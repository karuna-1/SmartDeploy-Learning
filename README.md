
# 🚀 SmartDeploy – Intelligent Deployment Optimization

**Reinforcement Learning-Based Intelligent Deployment Optimization using Python, Streamlit, and Docker.**

SmartDeploy is a mini-project that uses Reinforcement Learning (Q-Learning) to recommend suitable server configurations based on application workloads. It aims to balance server capacity, utilization, and deployment cost through a simulated environment.

## 📌 Project Overview

Selecting the right server for an application workload is important for efficient resource utilization and cost management.

SmartDeploy demonstrates how Reinforcement Learning can automate server selection by learning from simulated deployment scenarios.

The system trains an RL agent and provides deployment recommendations through an interactive Streamlit dashboard.

## ✨ Features

- **Reinforcement Learning:** Implements the Q-Learning algorithm.
- **Intelligent Server Selection:** Recommends suitable servers based on workload.
- **Workload Classification:** Classifies workloads into Low, Medium, and High states.
- **Cost Optimization:** Considers server cost in reward calculations.
- **Utilization Monitoring:** Displays server utilization percentages.
- **Training Analytics:** Visualizes reward progression during training.
- **Interactive Dashboard:** Provides a user-friendly Streamlit interface.
- **Docker Support:** Runs the application inside a Docker container.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Q-Learning | Reinforcement Learning algorithm |
| Streamlit | Interactive dashboard |
| Pandas | Data handling and visualization |
| Docker | Application containerization |
| Git | Version control |
| GitHub | Project hosting |

## 🧠 How It Works

1. The application receives a workload value.
2. The workload is classified into Low, Medium, or High.
3. The trained RL agent evaluates available server options.
4. The agent selects a suitable server using learned Q-values.
5. The dashboard displays the recommended server and deployment metrics.

### Reinforcement Learning Configuration

| Parameter | Value |
|---|---:|
| Algorithm | Q-Learning |
| Learning Rate | 0.8 |
| Discount Factor | 0.9 |
| Initial Epsilon | 0.2 |
| Training Episodes | 1,000 |
| Steps per Episode | 20 |

The agent uses an epsilon-greedy strategy to balance exploration and exploitation. Epsilon gradually decreases during training.

### Server Configurations

| Server | Capacity | Cost |
|---|---:|---:|
| Small | 300 | 10 |
| Medium | 700 | 20 |
| Large | 1200 | 35 |

### Workload Classification

| Workload | State |
|---|---|
| 1–300 | Low |
| 301–700 | Medium |
| 701–1200 | High |

## 📂 Project Structure

```text
SmartDeploy-Learning/
│
├── app.py                  # Streamlit dashboard
├── main.py                 # Q-Learning implementation
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image configuration
├── .dockerignore           # Docker build exclusions
├── .gitignore              # Git exclusions
├── q_table.json            # Saved Q-table
├── training_history.json   # Training reward history
└── README.md               # Project documentation
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/karuna-1/SmartDeploy-Learning.git
cd SmartDeploy-Learning
```

### 2. Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 3. Train the RL Agent

```bash
python3 main.py
```

This trains the agent and generates the following files:

- `q_table.json`
- `training_history.json`

### 4. Run the Streamlit Dashboard

```bash
streamlit run app.py
```

Open your browser and visit:

```text
http://localhost:8501
```

## 🐳 Run Using Docker

SmartDeploy can also be executed inside a Docker container.

### 1. Build the Docker Image

```bash
docker build -t smartdeploy .
```

### 2. Run the Docker Container

```bash
docker run -d -p 8501:8501 --name smartdeploy-container smartdeploy
```

### 3. Access the Application

Open:

```text
http://localhost:8501
```

### 4. Verify the Running Container

```bash
docker ps
```

### 5. View Container Logs

```bash
docker logs smartdeploy-container
```

### 6. Stop the Container

```bash
docker stop smartdeploy-container
```

### 7. Remove the Container

```bash
docker rm smartdeploy-container
```

## 📊 Dashboard Modules

SmartDeploy contains four main dashboard sections:

1. **Overview:** Displays project metrics and server configurations.
2. **Deploy Application:** Generates server recommendations based on workload.
3. **Q-Table:** Displays learned Q-values and server comparisons.
4. **Training Center:** Trains the RL agent and displays reward analytics.

## 🔬 Current Scope and Limitations

- The deployment environment is simulated.
- Workload transitions are randomly generated during training.
- Server capacities, costs, and latency values are illustrative.
- The application does not currently provision real cloud infrastructure.
- Training results should not be interpreted as production performance guarantees.

## 🚀 Future Enhancements

- Integrate real-time workload monitoring.
- Explore Kubernetes-based deployment.
- Integrate Azure cloud infrastructure.
- Implement Prometheus and Grafana monitoring.
- Improve workload simulation.
- Introduce CI/CD automation using GitHub Actions.

## 👩‍💻 Author

**Karuna Sugirayya Amargolmath**

- GitHub: [@karuna-1](https://github.com/karuna-1)
- Project Repository: [SmartDeploy-Learning](https://github.com/karuna-1/SmartDeploy-Learning)

## 📄 License

No open-source license has been added to this repository yet.

---

⭐ If you find this project interesting, consider giving the repository a star!
