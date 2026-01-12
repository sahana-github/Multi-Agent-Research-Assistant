import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from utils.llm_client import get_llm
from langchain_core.prompts import ChatPromptTemplate
import json


class ResearchReport(BaseModel):
    """Complete research report"""
    title: str = Field(description="Report title")
    executive_summary: str = Field(description="Executive summary")
    introduction: str = Field(description="Introduction section")
    methodology: str = Field(description="Research methodology")
    findings: str = Field(description="Key findings section")
    analysis: str = Field(description="Analysis and discussion")
    conclusions: str = Field(description="Conclusions")
    recommendations: str = Field(description="Recommendations")
    references: List[str] = Field(default_factory=list, description="List of sources")
    generated_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))


class ReportCompilerAgent:
    """Agent that compiles research into comprehensive reports"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.5)
    
    def _flatten_value(self, value):
        """Convert nested structures to strings"""
        if isinstance(value, str):
            return value
        elif isinstance(value, list):
            return '\n'.join(f"- {item}" for item in value)
        elif isinstance(value, dict):
            parts = []
            for k, v in value.items():
                if isinstance(v, list):
                    parts.append(f"{k.replace('_', ' ').title()}:")
                    parts.extend(f"- {item}" for item in v)
                else:
                    parts.append(f"{k.replace('_', ' ').title()}: {v}")
            return '\n'.join(parts)
        else:
            return str(value)
    
    def compile_report(
        self,
        topic: str,
        research_plan: dict,
        search_results: List[dict],
        document_insights: List[dict],
        data_analysis: dict
    ) -> ResearchReport:
        """Compile all research into a final report"""
        
        print("📝 Compiling final research report...")
        
        # Prepare context
        context = self._prepare_context(
            topic, research_plan, search_results, document_insights, data_analysis
        )
        
        prompt = ChatPromptTemplate.from_template(
            """You are an expert research report writer. Compile a comprehensive research report.

Topic: {topic}

Research Context:
{context}

Create a professional research report. Return ONLY a valid JSON object with these keys:
- title: string (clear and descriptive title)
- executive_summary: string (2-3 paragraph summary)
- introduction: string (background and objectives)
- methodology: string (how research was conducted)
- findings: string (key discoveries in paragraph form)
- analysis: string (interpretation and implications)
- conclusions: string (summary of main points)
- recommendations: string (actionable next steps in paragraph form)
- references: array of strings (list of sources)

Important: All values except 'references' must be plain strings, not nested objects or arrays. Write in full paragraphs."""
        )
        
        response = self.llm.invoke(
            prompt.format(topic=topic, context=context)
        )
        
        # Parse response
        content = response.content
        
        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                data = json.loads(json_str)
                
                # Flatten nested structures
                flattened_data = {
                    'title': self._flatten_value(data.get('title', f'Research Report: {topic}')),
                    'executive_summary': self._flatten_value(data.get('executive_summary', '')),
                    'introduction': self._flatten_value(data.get('introduction', '')),
                    'methodology': self._flatten_value(data.get('methodology', '')),
                    'findings': self._flatten_value(data.get('findings', '')),
                    'analysis': self._flatten_value(data.get('analysis', '')),
                    'conclusions': self._flatten_value(data.get('conclusions', '')),
                    'recommendations': self._flatten_value(data.get('recommendations', '')),
                    'references': data.get('references', []) if isinstance(data.get('references'), list) else []
                }
                
                return ResearchReport(**flattened_data)
                
        except Exception as e:
            print(f"⚠️ Parsing issue: {e}")
            print(f"Response preview: {content[:200]}...")
        
        # Fallback
        return ResearchReport(
            title=f"Research Report: {topic}",
            executive_summary="This report provides a comprehensive analysis of the research topic based on multi-agent AI research.",
            introduction=f"This research examines {topic} using an automated multi-agent system.",
            methodology="Research conducted using AI-powered web search, document analysis, and data synthesis.",
            findings=content[:600] if len(content) > 600 else content,
            analysis="Analysis based on aggregated research data from multiple sources.",
            conclusions="The research provides valuable insights into the topic.",
            recommendations="Further investigation recommended. Review findings for detailed next steps.",
            references=[]
        )
    
    def _prepare_context(
        self,
        topic: str,
        research_plan: dict,
        search_results: List[dict],
        document_insights: List[dict],
        data_analysis: dict
    ) -> str:
        """Prepare context from all research components"""
        
        context_parts = [f"Topic: {topic}\n"]
        
        # Add research plan
        if research_plan:
            context_parts.append(f"\nResearch Objectives: {research_plan.get('objectives', [])}")
        
        # Add search results summary
        if search_results:
            context_parts.append(f"\nWeb Search Found: {len(search_results)} sources")
            for result in search_results[:3]:
                context_parts.append(f"- {result.get('title', 'Source')}")
        
        # Add document insights
        if document_insights:
            context_parts.append(f"\nDocument Analysis: {len(document_insights)} documents analyzed")
        
        # Add data analysis
        if data_analysis:
            context_parts.append(f"\nKey Findings: {data_analysis.get('findings', [])}")
            context_parts.append(f"\nInsights: {data_analysis.get('insights', '')}")
        
        return '\n'.join(context_parts)
    
    def save_report(self, report: ResearchReport, filename: str = "research_report.md"):
        """Save report to markdown file"""
        
        markdown = f"""# {report.title}

**Generated:** {report.generated_date}

---

## Executive Summary

{report.executive_summary}

---

## Introduction

{report.introduction}

---

## Methodology

{report.methodology}

---

## Key Findings

{report.findings}

---

## Analysis

{report.analysis}

---

## Conclusions

{report.conclusions}

---

## Recommendations

{report.recommendations}

---

## References

"""
        
        for i, ref in enumerate(report.references, 1):
            markdown += f"{i}. {ref}\n"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"✅ Report saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving report: {e}")
    
    def display_report(self, report: ResearchReport):
        """Pretty print the report"""
        print("\n" + "="*60)
        print(f"📄 {report.title}")
        print("="*60)
        print(f"Generated: {report.generated_date}\n")
        
        print("📋 EXECUTIVE SUMMARY")
        print("-" * 60)
        print(report.executive_summary)
        
        print("\n📖 KEY FINDINGS")
        print("-" * 60)
        print(report.findings)
        
        print("\n💡 CONCLUSIONS")
        print("-" * 60)
        print(report.conclusions)
        
        print("\n✅ RECOMMENDATIONS")
        print("-" * 60)
        print(report.recommendations)
        
        print("\n" + "="*60 + "\n")


# Test the agent
if __name__ == "__main__":
    print("Testing Report Compiler Agent...\n")
    
    compiler = ReportCompilerAgent()
    
    # Sample data
    sample_plan = {
        "objectives": ["Understand AI impact", "Identify trends", "Evaluate adoption"]
    }
    
    sample_search = [
        {"title": "AI in Healthcare 2024", "content": "Major adoption trends"}
    ]
    
    sample_insights = [
        {"summary": "78% hospital AI adoption"}
    ]
    
    sample_analysis = {
        "findings": ["Significant AI adoption", "45% error reduction"],
        "insights": "AI transforming healthcare diagnostics"
    }
    
    # Compile report
    report = compiler.compile_report(
        topic="Impact of AI on Healthcare in 2024",
        research_plan=sample_plan,
        search_results=sample_search,
        document_insights=sample_insights,
        data_analysis=sample_analysis
    )
    
    compiler.display_report(report)
    compiler.save_report(report, "test_report.md")