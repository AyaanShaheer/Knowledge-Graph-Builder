# 🚀 Project Knowledge Graph Builder

**SPACEAI APP - Python Developer Assignment**  
*Author: Ayaan*

A Python application that models project dependencies in Neo4j and identifies critical paths using Cypher queries for project management optimization.

## 📋 Overview

This project demonstrates the implementation of a knowledge graph system for project management, specifically designed to:
- Model project tasks and their dependencies in Neo4j
- Identify critical paths that could delay project completion
- Provide comprehensive project analysis and visualization

## 🏗️ Architecture

The system uses:
- **Neo4j Graph Database** for storing project structure and relationships
- **Python Neo4j Driver** for database connectivity and query execution
- **Cypher Query Language** for graph traversal and analysis

### Data Model

```
Project
├── name: String
└── CONTAINS → Task
    ├── id: String
    ├── name: String
    ├── duration: Integer
    ├── status: String
    └── DEPENDS_ON → Task
```

## 🎯 Features

- **Graph Creation**: Automated setup of project structure in Neo4j
- **Critical Path Analysis**: Identifies longest dependency chain
- **Multi-Path Analysis**: Compares all possible execution paths
- **Project Overview**: Comprehensive task status and duration reporting
- **Error Handling**: Robust connection and query error management

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- Neo4j Database (Sandbox or Local)
- pip package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AyaanShaheer/Knowledge-Graph-Builder
   cd graph_builder
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install neo4j
   ```

4. **Configure Neo4j connection:**
   - Create a free Neo4j Sandbox at https://sandbox.neo4j.com/
   - Update connection details in `project_graph_builder.py`:
     ```python
     URI = "neo4j+s://your-instance.databases.neo4j.io"
     USERNAME = "neo4j"
     PASSWORD = "your_password"
     ```

## 🚀 Usage

### Basic Execution

```bash
python graph_builder.py
```

### Expected Output

```
🚀 SPACEAI APP - Project Knowledge Graph Builder
==================================================

📊 Project Overview:
  T1: Data Pipeline (Duration: 3 days, Status: Completed)
  T2: UI Design (Duration: 2 days, Status: In Progress)
  T3: Model Integration (Duration: 4 days, Status: Not Started)
  T4: Testing (Duration: 3 days, Status: Not Started)
  T5: Deployment (Duration: 1 day, Status: Not Started)

🔍 Critical Path Analysis:
Critical Path: ['Data Pipeline', 'Model Integration', 'Testing', 'Deployment']
Total Duration: 11 days

📈 All Possible Paths:
  Path 1: ['Data Pipeline', 'Model Integration', 'Testing', 'Deployment'] (Duration: 11 days) 🔥 CRITICAL
  Path 2: ['UI Design', 'Testing', 'Deployment'] (Duration: 6 days)

✅ Assignment completed successfully!
==================================================
```

## 📊 Sample Data

The application creates the following project structure:

**Project:** AI Dashboard Implementation

**Tasks & Dependencies:**
- T1: Data Pipeline (3 days) → Completed
- T2: UI Design (2 days) → In Progress
- T3: Model Integration (4 days) → Depends on T1
- T4: Testing (3 days) → Depends on T2, T3
- T5: Deployment (1 day) → Depends on T4

## 🔍 Critical Path Analysis

The system identifies the critical path using advanced Cypher queries:

```cypher
MATCH path = (start:Task)-[:DEPENDS_ON*]->(end:Task)
WHERE NOT ()-[:DEPENDS_ON]->(start)
AND NOT (end)-[:DEPENDS_ON]->()
WITH path,
REDUCE(total = 0, t IN nodes(path) | total + t.duration) AS path_duration
ORDER BY path_duration DESC
LIMIT 1
RETURN [t IN nodes(path) | t.name] AS critical_path, path_duration
```

## 🏗️ Code Structure

```
project-knowledge-graph/
├── project_graph_builder.py    # Main application
├── README.md                   # Documentation
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
└── venv/                       # Virtual environment (ignored)
```

## 🔧 Configuration

### Local Neo4j Setup

For local development:

```python
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "your_local_password"
```

### Neo4j Sandbox Setup

For cloud development:

```python
URI = "neo4j+s://your-instance.databases.neo4j.io"
USERNAME = "neo4j"
PASSWORD = "your_sandbox_password"
```

## 🧪 Testing

The application includes comprehensive error handling and logging:

- Database connection validation
- Query execution monitoring
- Graceful failure handling
- Detailed error reporting

## 📈 Performance Considerations

- **Graph Traversal**: Optimized Cypher queries for efficient path finding
- **Memory Usage**: Minimal memory footprint with streaming results
- **Connection Management**: Proper driver lifecycle management
- **Scalability**: Designed to handle larger project structures

## 🔮 Future Enhancements

Potential improvements:
- **Resource Management**: Add resource allocation and capacity planning
- **Timeline Visualization**: Gantt chart generation
- **Risk Analysis**: Probability-based delay predictions
- **Multi-Project Support**: Portfolio-level critical path analysis
- **REST API**: Web service interface for integration

## 🐛 Troubleshooting

### Common Issues

1. **Connection Error**: Verify Neo4j credentials and network connectivity
2. **Import Error**: Ensure `neo4j` package is installed in virtual environment
3. **Query Timeout**: Check database performance and query optimization

### Debug Mode

Enable detailed logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📄 License

This project is created for the SPACEAI APP Python Developer position assignment.

## 👤 Author

**Ayaan**  
*Python Developer Candidate*  
*SPACEAI APP Assignment*

## 🤝 Contributing

This is an assignment project. For interview discussion and modifications, please contact the author.

---

*Built with ❤️ for SPACEAI APP*