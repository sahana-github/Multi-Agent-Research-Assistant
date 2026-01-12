import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import streamlit as st
from workflows.research_workflow import MultiAgentResearchWorkflow
import time

# Page config
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 Multi-Agent Research Assistant")
st.markdown("*Powered by LangGraph, Groq, and 5 Specialized AI Agents*")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("""
    This system uses 5 AI agents:
    - 🎯 Research Planner
    - 🔍 Web Searcher
    - 📄 Document Analyzer
    - 📊 Data Analyst
    - 📝 Report Compiler
    
    They work together to automate deep research tasks!
    """)
    
    st.header("How it works")
    st.markdown("""
    1. Enter your research question
    2. AI agents collaborate automatically
    3. Get a comprehensive report in minutes
    """)

# Main interface
query = st.text_input(
    "Enter your research question:",
    placeholder="e.g., What are the latest AI innovations in healthcare for 2024?"
)

if st.button("🚀 Start Research", type="primary"):
    if query:
        # Create workflow
        workflow = MultiAgentResearchWorkflow()
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Container for results
        results_container = st.container()
        
        with results_container:
            # Step 1: Planning
            status_text.text("🎯 Planning research...")
            progress_bar.progress(20)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Research Plan")
                plan_placeholder = st.empty()
            
            with col2:
                st.subheader("🔍 Search Results")
                search_placeholder = st.empty()
            
            # Run workflow
            try:
                result = workflow.run(query)
                
                # Display plan
                if result.get("research_plan"):
                    plan = result["research_plan"]
                    with plan_placeholder:
                        st.write(f"**Topic:** {plan.get('topic', '')}")
                        st.write(f"**Estimated Time:** {plan.get('estimated_time', '')}")
                        with st.expander("View Objectives"):
                            for obj in plan.get('objectives', []):
                                st.write(f"- {obj}")
                
                progress_bar.progress(40)
                status_text.text("🔍 Searching the web...")
                
                # Display search results
                if result.get("search_results"):
                    with search_placeholder:
                        total_results = sum(len(sr.get('results', [])) for sr in result['search_results'])
                        st.write(f"Found **{total_results}** sources")
                
                progress_bar.progress(60)
                status_text.text("📊 Analyzing data...")
                
                # Display analysis
                if result.get("data_analysis"):
                    st.subheader("📊 Analysis Results")
                    analysis = result["data_analysis"]
                    
                    with st.expander("Key Findings"):
                        for finding in analysis.get('findings', []):
                            st.write(f"- {finding}")
                    
                    with st.expander("Insights"):
                        st.write(analysis.get('insights', ''))
                
                progress_bar.progress(80)
                status_text.text("📝 Compiling report...")
                
                time.sleep(1)
                
                progress_bar.progress(100)
                status_text.text("✅ Research complete!")
                
                # Display final report
                if result.get("final_report"):
                    st.success("🎉 Research Complete!")
                    
                    report = result["final_report"]
                    
                    st.header(report.get('title', 'Research Report'))
                    
                    st.subheader("Executive Summary")
                    st.write(report.get('executive_summary', ''))
                    
                    st.subheader("Key Findings")
                    st.write(report.get('findings', ''))
                    
                    st.subheader("Conclusions")
                    st.write(report.get('conclusions', ''))
                    
                    st.subheader("Recommendations")
                    st.write(report.get('recommendations', ''))
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Full Report",
                        data=str(report),
                        file_name="research_report.txt",
                        mime="text/plain"
                    )
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.exception(e)
    else:
        st.warning("Please enter a research question")

# Footer
st.markdown("---")
st.markdown("*Built with LangGraph, Groq LLM, and Tavily Search*")