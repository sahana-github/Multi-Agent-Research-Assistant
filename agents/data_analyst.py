import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from pydantic import BaseModel, Field
from typing import List, Dict, Any
from utils.llm_client import get_llm
from langchain_core.prompts import ChatPromptTemplate


class DataAnalysis(BaseModel):
    """Results of data analysis"""
    findings: List[str] = Field(description="Key findings from analysis")
    trends: List[str] = Field(description="Identified trends or patterns")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Relevant statistics")
    insights: str = Field(description="Overall insights and interpretation")
    recommendations: List[str] = Field(description="Actionable recommendations")


class DataAnalystAgent:
    """Agent that analyzes data and identifies patterns"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.3)
    
    def analyze_findings(self, research_data: List[Dict[str, Any]], context: str = "") -> DataAnalysis:
        """Analyze research findings and extract insights"""
        
        print("📊 Analyzing research data...")
        
        # Prepare data summary
        data_summary = self._prepare_data_summary(research_data)
        
        prompt = ChatPromptTemplate.from_template(
            """You are an expert data analyst. Analyze the following research data and provide comprehensive insights.

Context: {context}

Research Data:
{data_summary}

Provide a detailed analysis including:
1. Key findings (5-7 important discoveries)
2. Trends and patterns observed
3. Relevant statistics or metrics
4. Overall insights and interpretation
5. Actionable recommendations based on the data

Format as JSON with keys: findings (list), trends (list), statistics (dict), insights (string), recommendations (list)"""
        )
        
        response = self.llm.invoke(
            prompt.format(context=context or "General research analysis", data_summary=data_summary)
        )
        
        # Parse response
        content = response.content
        
        try:
            import json
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                data = json.loads(json_str)
                
                return DataAnalysis(
                    findings=data.get('findings', []),
                    trends=data.get('trends', []),
                    statistics=data.get('statistics', {}),
                    insights=data.get('insights', ''),
                    recommendations=data.get('recommendations', [])
                )
        except Exception as e:
            print(f"⚠️ Parsing issue: {e}")
        
        # Fallback
        return DataAnalysis(
            findings=["Analysis completed"],
            trends=["See insights for details"],
            statistics={},
            insights=content[:500],
            recommendations=["Further analysis recommended"]
        )
    
    def _prepare_data_summary(self, research_data: List[Dict[str, Any]]) -> str:
        """Prepare a summary of research data for analysis"""
        summary_parts = []
        
        for i, item in enumerate(research_data, 1):
            summary_parts.append(f"\nData Point {i}:")
            for key, value in item.items():
                if isinstance(value, (str, int, float)):
                    summary_parts.append(f"  {key}: {value}")
                elif isinstance(value, list) and len(value) > 0:
                    summary_parts.append(f"  {key}: {', '.join(str(v) for v in value[:3])}")
        
        return '\n'.join(summary_parts)
    
    def compare_sources(self, source1: Dict, source2: Dict) -> str:
        """Compare two data sources"""
        
        prompt = ChatPromptTemplate.from_template(
            """Compare these two data sources and identify:
1. Common themes
2. Contradictions or differences
3. Complementary information

Source 1:
{source1}

Source 2:
{source2}

Provide a brief comparison (3-4 sentences)."""
        )
        
        response = self.llm.invoke(
            prompt.format(source1=str(source1), source2=str(source2))
        )
        
        return response.content
    
    def display_analysis(self, analysis: DataAnalysis):
        """Pretty print data analysis"""
        print("\n" + "="*60)
        print("📊 DATA ANALYSIS RESULTS")
        print("="*60)
        
        print("\n🔍 Key Findings:")
        for i, finding in enumerate(analysis.findings, 1):
            print(f"   {i}. {finding}")
        
        print("\n📈 Trends & Patterns:")
        for i, trend in enumerate(analysis.trends, 1):
            print(f"   {i}. {trend}")
        
        if analysis.statistics:
            print("\n📊 Statistics:")
            for key, value in analysis.statistics.items():
                print(f"   {key}: {value}")
        
        print(f"\n💡 Insights:\n{analysis.insights}")
        
        print("\n✅ Recommendations:")
        for i, rec in enumerate(analysis.recommendations, 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "="*60 + "\n")


# Test the agent
if __name__ == "__main__":
    print("Testing Data Analyst Agent...\n")
    
    analyst = DataAnalystAgent()
    
    # Sample research data
    sample_data = [
        {
            "source": "Healthcare AI Report 2024",
            "finding": "78% of hospitals use AI diagnostics",
            "impact": "45% reduction in diagnostic errors"
        },
        {
            "source": "Medical Journal Study",
            "finding": "AI improved patient outcomes by 32%",
            "impact": "Faster treatment decisions"
        },
        {
            "source": "FDA Report Q1 2024",
            "finding": "23 new AI medical devices approved",
            "impact": "Expanded AI capabilities in healthcare"
        }
    ]
    
    # Analyze data
    analysis = analyst.analyze_findings(
        sample_data, 
        context="AI impact on healthcare in 2024"
    )
    
    analyst.display_analysis(analysis)
    
    # Test comparison
    print("\nTEST 2: Comparing Sources")
    comparison = analyst.compare_sources(sample_data[0], sample_data[1])
    print(f"\n📋 Comparison Result:\n{comparison}")