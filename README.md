# 🧩 8-Puzzle AI Solver & Interactive Streamlit Game

![8-Puzzle App Screenshot](dog.png)

A **search-algorithm powered AI project** that solves the classic **8-puzzle problem** using both **uninformed** and **informed** search techniques.  
This project combines **Artificial Intelligence fundamentals** with an **interactive Streamlit interface**, allowing users to test different algorithms, compare performance, and even turn an uploaded image into a solvable 8-puzzle experience.

---

## 🌟 Why This Project Matters

### 🧠 For AI & Computer Science Students
- Understand the practical difference between **uninformed search** and **informed search**.  
- See how **BFS, DFS, and A\*** behave on the exact same puzzle state.  
- Compare heuristics and observe how they affect the number of expanded nodes and solving efficiency.  
- Learn how state-space search is implemented using real data structures such as **queues, stacks, and priority queues**.

### 🎓 For Academic Use
- Matches the core requirements of the 8-puzzle assignment, including **BFS, DFS, A\***, traceable solution output, and performance metrics.  
- Provides a clearer and more visual way to demonstrate how the algorithms operate step by step.  
- Helps in writing reports by exposing important outputs such as path, cost, depth, and runtime.

### 💡 Project Value
- Turns a classic textbook AI problem into an **interactive application**.  
- Connects theory with practice through both a **Jupyter Notebook explanation** and a **Streamlit app**.  
- Adds a creative bonus feature by transforming any uploaded image into a puzzle board that the agent can solve.

---

## ✨ Features & Highlights

| Feature | Description |
|---------|-------------|
| 🔍 Multiple Search Algorithms | Solve the puzzle using **BFS**, **DFS**, **A* Manhattan**, and **A* Euclidean**. |
| 📊 Performance Metrics | Displays **cost of path, nodes expanded, search depth, running time,** and **max frontier size**. |
| 🧾 Full Trace Output | Shows the full sequence of states from the initial configuration to the goal. |
| 🖼️ Image-Based Upgrade | Upload any image, split it into puzzle tiles, scramble it, and solve it as an 8-puzzle. |
| 🎮 Interactive Streamlit UI | Test numeric puzzles and image puzzles in a clean visual interface. |
| 📘 Notebook Version | Includes a clear Jupyter Notebook version for explanation, testing, and academic presentation. |

---

## 🚀 How to Use This Project

### 1) Prerequisites
- Python 3.9+
- pip

### 2) Clone the Repository
```bash
git clone <YOUR_REPOSITORY_LINK>
cd <YOUR_PROJECT_FOLDER>
```

### 3) Install Dependencies
```bash
pip install -r requirements.txt
```

### 4) Run the Streamlit App
```bash
streamlit run app.py
```

### 5) Use the App
- Enter a numeric puzzle state such as:
```text
1,2,5,3,4,0,6,7,8
```
- Choose the algorithm:
  - BFS
  - DFS
  - A* (Manhattan)
  - A* (Euclidean)
- View the solution trace and performance metrics.
- Or upload an image and let the app generate a visual 8-puzzle version.

---

## 🛠️ Technical Details

### Algorithms Implemented
- **BFS (Breadth-First Search)**
- **DFS (Depth-First Search)**
- **A\*** with **Manhattan Distance**
- **A\*** with **Euclidean Distance**

### Data Structures Used
- **Queue** for BFS
- **Stack** for DFS
- **Min-Heap / Priority Queue** for A\*
- **Sets and dictionaries** for explored states, parent tracking, and path reconstruction

### Output Metrics
- Path to goal
- Cost of path
- Nodes expanded
- Search depth
- Running time
- Max frontier size

### Goal State
```text
0,1,2,3,4,5,6,7,8
```

---

## 📚 Project Structure

```bash
.
├── 8_PUZZLE.ipynb      # Notebook explanation and testing
├── solver.py           # Core search algorithms and helpers
├── app.py              # Streamlit interface
├── cli.py              # Command-line execution (optional)
├── README.md
└── requirements.txt
```

---

## 🧪 Example Algorithms Comparison

This project makes it easy to compare how different search strategies behave on the same puzzle instance.
Typically, **Manhattan A\*** is more informed for 4-direction tile movement and often expands fewer nodes than Euclidean in this problem setting.

---

## 📞 Contact & Portfolio

Connect with me or explore more of my work:

- 🌐 **Portfolio:** https://mohamed-ashraf-github-io.vercel.app/
- 🔗 **LinkedIn:** https://www.linkedin.com/in/mohamed--ashraff
- 🐙 **GitHub:** https://github.com/MohamedAshraf-DE

### Freelance Profiles
- 💼 Upwork: https://www.upwork.com/freelancers/~0190a07e5b17474f9f?mp_source=share
- 💼 Mostaql: https://mostaql.com/u/MohamedA_Data
- 💼 Khamsat: https://khamsat.com/user/mohamed_ashraf124
- 💼 Freelancer: https://www.freelancer.com/dashboard
- 💼 Outlier: https://app.outlier.ai/profile

---

## 🏁 Final Note

This project is more than a simple puzzle solver. It is a practical demonstration of how **AI search algorithms** can be implemented, analyzed, visualized, and turned into an engaging interactive experience.
