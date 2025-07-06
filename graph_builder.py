"""
Project Knowledge Graph Builder
SPACEAI APP - Python Developer Assignment
Author: Ayaan

This script models project dependencies in Neo4j and identifies critical paths using Cypher queries.
"""

from neo4j import GraphDatabase
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProjectGraphBuilder:
    def __init__(self, uri, username, password):
        """Initialize Neo4j connection"""
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        logger.info("Connected to Neo4j database")
    
    def close(self):
        """Close the database connection"""
        self.driver.close()
        logger.info("Database connection closed")
    
    def clear_database(self):
        """Clear existing data for fresh start"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Database cleared")
    
    def create_project_structure(self):
        """Create the project and task nodes with relationships"""
        
        # Cypher statements for graph creation
        create_queries = [
            # Create project node
            "CREATE (p:Project {name: 'AI Dashboard Implementation'})",
            
            # Create task nodes
            """CREATE (t1:Task {id: 'T1', name: 'Data Pipeline', duration: 3, status: 'Completed'}),
                      (t2:Task {id: 'T2', name: 'UI Design', duration: 2, status: 'In Progress'}),
                      (t3:Task {id: 'T3', name: 'Model Integration', duration: 4, status: 'Not Started'}),
                      (t4:Task {id: 'T4', name: 'Testing', duration: 3, status: 'Not Started'}),
                      (t5:Task {id: 'T5', name: 'Deployment', duration: 1, status: 'Not Started'})""",
            
            # Create project-task relationships
            """MATCH (p:Project {name: 'AI Dashboard Implementation'}),
                     (t1:Task {id: 'T1'}), (t2:Task {id: 'T2'}), (t3:Task {id: 'T3'}),
                     (t4:Task {id: 'T4'}), (t5:Task {id: 'T5'})
               CREATE (p)-[:CONTAINS]->(t1),
                      (p)-[:CONTAINS]->(t2),
                      (p)-[:CONTAINS]->(t3),
                      (p)-[:CONTAINS]->(t4),
                      (p)-[:CONTAINS]->(t5)""",
            
            # Create task dependencies
            """MATCH (t1:Task {id: 'T1'}), (t2:Task {id: 'T2'}), (t3:Task {id: 'T3'}),
                     (t4:Task {id: 'T4'}), (t5:Task {id: 'T5'})
               CREATE (t3)-[:DEPENDS_ON]->(t1),
                      (t4)-[:DEPENDS_ON]->(t2),
                      (t4)-[:DEPENDS_ON]->(t3),
                      (t5)-[:DEPENDS_ON]->(t4)"""
        ]
        
        with self.driver.session() as session:
            for query in create_queries:
                session.run(query)
                logger.info(f"Executed: {query[:50]}...")
        
        logger.info("Project structure created successfully")
    
    def find_critical_path(self):
        """Find the critical path using Cypher query"""
        
        critical_path_query = """
        MATCH path = (start:Task)-[:DEPENDS_ON*]->(end:Task)
        WHERE NOT ()-[:DEPENDS_ON]->(start)
        AND NOT (end)-[:DEPENDS_ON]->()
        WITH path,
        REDUCE(total = 0, t IN nodes(path) | total + t.duration) AS path_duration
        ORDER BY path_duration DESC
        LIMIT 1
        RETURN [t IN nodes(path) | t.name] AS critical_path, path_duration
        """
        
        with self.driver.session() as session:
            result = session.run(critical_path_query)
            record = result.single()
            
            if record:
                return record['critical_path'], record['path_duration']
            else:
                return None, 0
    
    def get_all_paths(self):
        """Get all possible paths for analysis"""
        
        all_paths_query = """
        MATCH path = (start:Task)-[:DEPENDS_ON*]->(end:Task)
        WHERE NOT ()-[:DEPENDS_ON]->(start)
        AND NOT (end)-[:DEPENDS_ON]->()
        WITH path,
        REDUCE(total = 0, t IN nodes(path) | total + t.duration) AS path_duration
        ORDER BY path_duration DESC
        RETURN [t IN nodes(path) | t.name] AS path, path_duration
        """
        
        with self.driver.session() as session:
            result = session.run(all_paths_query)
            return [(record['path'], record['path_duration']) for record in result]
    
    def get_project_overview(self):
        """Get project overview with task details"""
        
        overview_query = """
        MATCH (p:Project)-[:CONTAINS]->(t:Task)
        RETURN p.name AS project_name, 
               t.id AS task_id, 
               t.name AS task_name, 
               t.duration AS duration, 
               t.status AS status
        ORDER BY t.id
        """
        
        with self.driver.session() as session:
            result = session.run(overview_query)
            return [(record['project_name'], record['task_id'], record['task_name'], 
                    record['duration'], record['status']) for record in result]

def main():
    """Main execution function"""
    
  
    URI = "bolt://18.205.2.119"  
    USERNAME = "neo4j"
    PASSWORD = "sidewalks-ratings-tanks" 
    
    # For local Neo4j instance, use:
    # URI = "bolt://localhost:7687"
    # USERNAME = "neo4j"
    # PASSWORD = "your_local_password"
    
    try:
        # Initialize the graph builder
        graph_builder = ProjectGraphBuilder(URI, USERNAME, PASSWORD)
        
        print("🚀 SPACEAI APP - Project Knowledge Graph Builder")
        print("=" * 50)
        
        # Clear existing data and create fresh structure
        graph_builder.clear_database()
        graph_builder.create_project_structure()
        
        # Get project overview
        print("\n📊 Project Overview:")
        overview = graph_builder.get_project_overview()
        for project, task_id, task_name, duration, status in overview:
            print(f"  {task_id}: {task_name} (Duration: {duration} days, Status: {status})")
        
        # Find and display critical path
        print("\n🔍 Critical Path Analysis:")
        critical_path, total_duration = graph_builder.find_critical_path()
        
        if critical_path:
            print(f"Critical Path: {critical_path}")
            print(f"Total Duration: {total_duration} days")
            
            # Display all paths for comparison
            print("\n📈 All Possible Paths:")
            all_paths = graph_builder.get_all_paths()
            for i, (path, duration) in enumerate(all_paths, 1):
                marker = "🔥 CRITICAL" if duration == total_duration else "  "
                print(f"  Path {i}: {path} (Duration: {duration} days) {marker}")
        
        else:
            print("No critical path found!")
        
        print("\n✅ Assignment completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error occurred: {e}")
        print("\n💡 Setup Instructions:")
        print("1. Create a free Neo4j Sandbox at https://sandbox.neo4j.com/")
        print("2. Update the URI, USERNAME, and PASSWORD variables in the script")
        print("3. Install Neo4j driver: pip install neo4j")
        print("4. Run the script again")
        
    finally:
        try:
            graph_builder.close()
        except:
            pass

if __name__ == "__main__":
    main()