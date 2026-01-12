import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from agents.research_planner import ResearchPlannerAgent
from agents.web_searcher import WebSearcherAgent
from agents.document_analyzer import DocumentAnalyzerAgent
from agents.data_analyst import DataAnalystAgent
from agents.report_compiler import ReportCompilerAgent


class ResearchState(TypedDict):
    """State that flows through the workflow"""
    query: str
    research_plan: Dict[str, Any]
    search_results: List[Dict[str, Any]]
    document_insights: List[Dict[str, Any]]
    data_analysis: Dict[str, Any]
    final_report: Dict[str, Any]
    current_step: str


class MultiAgentResearchWorkflow:
    """Multi-agent research workflow orchestrator"""
    
    def __init__(self):
        # Initialize all agents
        self.planner = ResearchPlannerAgent()
        self.searcher = WebSearcherAgent()
        self.doc_analyzer = DocumentAnalyzerAgent()
        self.analyst = DataAnalystAgent()
        self.compiler = ReportCompilerAgent()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the graph
        workflow = StateGraph(ResearchState)
        
        # Add nodes (each agent is a node)
        workflow.add_node("plan_research", self.plan_research_node)
        workflow.add_node("search_web", self.search_web_node)
        workflow.add_node("analyze_data", self.analyze_data_node)
        workflow.add_node("compile_report", self.compile_report_node)
        
        # Define the flow
        workflow.set_entry_point("plan_research")
        workflow.add_edge("plan_research", "search_web")
        workflow.add_edge("search_web", "analyze_data")
        workflow.add_edge("analyze_data", "compile_report")
        workflow.add_edge("compile_report", END)
        
        return workflow.compile()
    
    def plan_research_node(self, state: ResearchState) -> ResearchState:
        """Node 1: Create research plan"""
        print("\n" + "="*60)
        print("🎯 STEP 1: PLANNING RESEARCH")
        print("="*60)
        
        plan = self.planner.create_plan(state["query"])
        self.planner.display_plan(plan)
        
        state["research_plan"] = plan.model_dump()
        state["current_step"] = "plan_complete"
        
        return state
    
    def search_web_node(self, state: ResearchState) -> ResearchState:
        """Node 2: Search the web for information"""
        print("\n" + "="*60)
        print("🔍 STEP 2: WEB SEARCH")
        print("="*60)
        
        # Get keywords from research plan
        keywords = state["research_plan"].get("keywords", [])
        
        # Search for top 3 keywords
        all_results = []
        for keyword in keywords[:3]:
            results = self.searcher.search(keyword, max_results=3)
            self.searcher.display_results(results)
            all_results.append(results.model_dump())
        
        state["search_results"] = all_results
        state["current_step"] = "search_complete"
        
        return state
    
    def analyze_data_node(self, state: ResearchState) -> ResearchState:
        """Node 3: Analyze collected data"""
        print("\n" + "="*60)
        print("📊 STEP 3: DATA ANALYSIS")
        print("="*60)
        
        # Prepare data for analysis
        analysis_data = []
        
        # Convert search results to analysis format
        for search_result in state["search_results"]:
            for result in search_result.get("results", []):
                analysis_data.append({
                    "source": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", "")
                })
        
        # Analyze the data
        analysis = self.analyst.analyze_findings(
            analysis_data,
            context=state["query"]
        )
        
        self.analyst.display_analysis(analysis)
        
        state["data_analysis"] = analysis.model_dump()
        state["current_step"] = "analysis_complete"
        
        return state
    
    def compile_report_node(self, state: ResearchState) -> ResearchState:
        """Node 4: Compile final report"""
        print("\n" + "="*60)
        print("📝 STEP 4: COMPILING REPORT")
        print("="*60)
        
        # Compile the final report
        report = self.compiler.compile_report(
            topic=state["query"],
            research_plan=state["research_plan"],
            search_results=state["search_results"],
            document_insights=state.get("document_insights", []),
            data_analysis=state["data_analysis"]
        )
        
        self.compiler.display_report(report)
        
        # Save report
        filename = f"research_report_{state['research_plan'].get('topic', 'report').replace(' ', '_')[:30]}.md"
        self.compiler.save_report(report, filename)
        
        state["final_report"] = report.model_dump()
        state["current_step"] = "complete"
        
        return state
    
    def run(self, query: str) -> Dict[str, Any]:
        """Run the complete research workflow"""
        
        print("\n" + "🚀"*30)
        print("MULTI-AGENT RESEARCH SYSTEM STARTING")
        print("🚀"*30)
        print(f"\nResearch Query: {query}\n")
        
        # Initialize state
        initial_state = ResearchState(
            query=query,
            research_plan={},
            search_results=[],
            document_insights=[],
            data_analysis={},
            final_report={},
            current_step="started"
        )
        
        # Run the workflow
        final_state = self.workflow.invoke(initial_state)
        
        print("\n" + "✅"*30)
        print("RESEARCH COMPLETE!")
        print("✅"*30)
        
        return final_state


# Test the workflow
if __name__ == "__main__":
    # Create the workflow
    workflow = MultiAgentResearchWorkflow()
    
    # Run research
    query = "What are the latest AI innovations in healthcare for 2024?"
    
    result = workflow.run(query)
    
    print("\n📊 WORKFLOW SUMMARY:")
    print(f"Query: {result['query']}")
    print(f"Final Status: {result['current_step']}")
    print(f"Report Generated: {bool(result['final_report'])}")