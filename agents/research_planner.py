import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from utils.llm_client import get_llm


class ResearchPlan(BaseModel):
    """Research plan output structure"""
    topic: str = Field(description="Main research topic")
    objectives: List[str] = Field(description="Research objectives")
    subtasks: List[str] = Field(description="Specific research subtasks")
    keywords: List[str] = Field(description="Key search terms")
    estimated_time: str = Field(description="Estimated completion time")


class ResearchPlannerAgent:
    """Agent that creates structured research plans"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.3)
        self.parser = PydanticOutputParser(pydantic_object=ResearchPlan)
        
    def create_plan(self, research_query: str) -> ResearchPlan:
        """Create a research plan from a query"""
        
        prompt = ChatPromptTemplate.from_template(
            """You are an expert research planner. Create a detailed research plan for the following query.

Research Query: {query}

Your plan should:
1. Identify clear research objectives
2. Break down into specific, actionable subtasks
3. Identify key search terms and keywords
4. Estimate realistic completion time

{format_instructions}

Provide a comprehensive but focused plan."""
        )
        
        chain = prompt | self.llm | self.parser
        
        result = chain.invoke({
            "query": research_query,
            "format_instructions": self.parser.get_format_instructions()
        })
        
        return result
    
    def display_plan(self, plan: ResearchPlan):
        """Pretty print the research plan"""
        print("\n" + "="*60)
        print("📋 RESEARCH PLAN")
        print("="*60)
        print(f"\n🎯 Topic: {plan.topic}")
        print(f"\n⏱️  Estimated Time: {plan.estimated_time}")
        
        print("\n📌 Objectives:")
        for i, obj in enumerate(plan.objectives, 1):
            print(f"   {i}. {obj}")
        
        print("\n✅ Subtasks:")
        for i, task in enumerate(plan.subtasks, 1):
            print(f"   {i}. {task}")
        
        print("\n🔍 Keywords:")
        print(f"   {', '.join(plan.keywords)}")
        print("\n" + "="*60 + "\n")


# Test the agent
if __name__ == "__main__":
    print("Testing Research Planner Agent...\n")
    
    planner = ResearchPlannerAgent()
    
    query = "Research the impact of AI on healthcare in 2024"
    
    print(f"Query: {query}\n")
    print("Generating research plan...")
    
    plan = planner.create_plan(query)
    
    planner.display_plan(plan)
    
    print("Raw Plan Data:")
    print(plan.model_dump_json(indent=2))