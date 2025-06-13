# Simple MCP Server Implementation
class MCPServer:
    def __init__(self):
        self.agents = {}
        self.message_queue = []
    
    def register_agent(self, agent_id, agent_instance):
        """Register a new agent with the MCP server"""
        self.agents[agent_id] = {
            'instance': agent_instance,
            'status': 'available',
            'capabilities': agent_instance.get_capabilities()
        }
        print(f"Agent {agent_id} registered successfully")
    
    def route_message(self, from_agent, to_agent, message):
        """Route messages between agents"""
        if to_agent in self.agents:
            if self.agents[to_agent]['status'] == 'available':
                result = self.agents[to_agent]['instance'].process_message(message)
                return result
            else:
                self.message_queue.append({
                    'from': from_agent,
                    'to': to_agent,
                    'message': message
                })
                return "Message queued - agent busy"
        else:
            return f"Error: Agent {to_agent} not found"
    
    def coordinate_task(self, task, required_agents):
        """Coordinate a complex task between multiple agents"""
        results = {}
        for agent_id in required_agents:
            if agent_id in self.agents:
                self.agents[agent_id]['status'] = 'busy'
                result = self.agents[agent_id]['instance'].execute_task(task)
                results[agent_id] = result
                self.agents[agent_id]['status'] = 'available'
        return results

# Example Agent Classes
class ResearchAgent:
    def get_capabilities(self):
        return ['web_search', 'data_analysis', 'fact_checking']
    
    def process_message(self, message):
        return f"Research completed: {message}"
    
    def execute_task(self, task):
        return f"Research results for: {task}"

class BudgetAgent:
    def get_capabilities(self):
        return ['cost_calculation', 'budget_planning', 'financial_analysis']
    
    def process_message(self, message):
        return f"Budget analysis: {message}"
    
    def execute_task(self, task):
        return f"Budget breakdown for: {task}"

# Usage Example
if __name__ == "__main__":
    # Initialize MCP Server
    mcp = MCPServer()
    
    # Create and register agents
    research_agent = ResearchAgent()
    budget_agent = BudgetAgent()
    
    mcp.register_agent("researcher", research_agent)
    mcp.register_agent("budgeter", budget_agent)
    
    # Coordinate a travel planning task
    task = "Plan 3-day Paris trip for 2 people, $2000 budget"
    results = mcp.coordinate_task(task, ["researcher", "budgeter"])
    
    print("Task Results:")
    for agent, result in results.items():
        print(f"{agent}: {result}")
