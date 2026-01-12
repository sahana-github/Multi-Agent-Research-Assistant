import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PyPDF2 import PdfReader
from pydantic import BaseModel, Field
from typing import List, Optional
from utils.llm_client import get_llm
from langchain_core.prompts import ChatPromptTemplate
import io


class DocumentInsight(BaseModel):
    """Insights extracted from a document"""
    summary: str = Field(description="Brief summary of the document")
    key_points: List[str] = Field(description="Main points from the document")
    relevant_data: List[str] = Field(description="Relevant data points or statistics")
    sources_cited: List[str] = Field(default_factory=list, description="Sources mentioned in the document")


class DocumentAnalyzerAgent:
    """Agent that analyzes documents and extracts insights"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.2)  # Lower temp for factual extraction
    
    def read_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            reader = PdfReader(file_path)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            print(f"✅ Extracted {len(text)} characters from PDF")
            return text
        
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return ""
    
    def read_text_file(self, file_path: str) -> str:
        """Read plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            print(f"✅ Read {len(text)} characters from text file")
            return text
        
        except Exception as e:
            print(f"❌ Error reading text file: {e}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = 3000) -> List[str]:
        """Split text into manageable chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    def analyze_text(self, text: str, context: str = "") -> DocumentInsight:
        """Analyze text and extract insights"""
        
        # Chunk if text is too long
        if len(text) > 4000:
            print(f"📄 Text is long ({len(text)} chars), analyzing first 4000 characters...")
            text = text[:4000]
        
        prompt = ChatPromptTemplate.from_template(
            """You are an expert document analyst. Analyze the following text and extract key insights.

Context: {context}

Text to analyze:
{text}

Provide:
1. A brief summary (2-3 sentences)
2. Key points (3-5 main takeaways)
3. Relevant data, statistics, or facts mentioned
4. Any sources or references cited

Format your response as JSON with keys: summary, key_points (list), relevant_data (list), sources_cited (list)"""
        )
        
        response = self.llm.invoke(
            prompt.format(context=context or "General analysis", text=text)
        )
        
        # Parse response (simplified - in production use structured output)
        content = response.content
        
        # Try to extract structured info (basic parsing)
        try:
            import json
            # Try to find JSON in response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                data = json.loads(json_str)
                
                return DocumentInsight(
                    summary=data.get('summary', ''),
                    key_points=data.get('key_points', []),
                    relevant_data=data.get('relevant_data', []),
                    sources_cited=data.get('sources_cited', [])
                )
        except:
            pass
        
        # Fallback: parse from plain text
        lines = content.split('\n')
        return DocumentInsight(
            summary=content[:300],
            key_points=["Analysis completed - see summary"],
            relevant_data=[],
            sources_cited=[]
        )
    
    def analyze_document(self, file_path: str, context: str = "") -> Optional[DocumentInsight]:
        """Analyze a document file (PDF or text)"""
        
        print(f"\n📄 Analyzing document: {file_path}")
        
        # Read document based on file type
        if file_path.endswith('.pdf'):
            text = self.read_pdf(file_path)
        elif file_path.endswith('.txt'):
            text = self.read_text_file(file_path)
        else:
            print(f"❌ Unsupported file type")
            return None
        
        if not text:
            return None
        
        # Analyze
        print("🤖 Analyzing content...")
        insights = self.analyze_text(text, context)
        
        return insights
    
    def display_insights(self, insights: DocumentInsight):
        """Pretty print document insights"""
        print("\n" + "="*60)
        print("📊 DOCUMENT INSIGHTS")
        print("="*60)
        
        print(f"\n📝 Summary:\n{insights.summary}")
        
        print("\n🔑 Key Points:")
        for i, point in enumerate(insights.key_points, 1):
            print(f"   {i}. {point}")
        
        if insights.relevant_data:
            print("\n📈 Relevant Data:")
            for i, data in enumerate(insights.relevant_data, 1):
                print(f"   {i}. {data}")
        
        if insights.sources_cited:
            print("\n📚 Sources Cited:")
            for i, source in enumerate(insights.sources_cited, 1):
                print(f"   {i}. {source}")
        
        print("\n" + "="*60 + "\n")


# Test the agent
if __name__ == "__main__":
    print("Testing Document Analyzer Agent...\n")
    
    analyzer = DocumentAnalyzerAgent()
    
    # Test with sample text
    print("TEST 1: Analyzing Sample Text")
    
    sample_text = """
    Artificial Intelligence in Healthcare: 2024 Report
    
    The healthcare industry has seen remarkable AI adoption in 2024. 
    Key findings include:
    - 78% of hospitals now use AI-powered diagnostic tools
    - AI reduced diagnostic errors by 45% in radiology
    - Predictive analytics improved patient outcomes by 32%
    
    Major implementations include:
    1. IBM Watson Health deployed in 500+ hospitals
    2. Google's Med-PaLM 2 achieved 85% accuracy in medical exams
    3. FDA approved 23 new AI medical devices in Q1 2024
    
    Sources: Journal of Medical AI, Healthcare Technology Review 2024
    """
    
    insights = analyzer.analyze_text(sample_text, context="AI healthcare impact analysis")
    analyzer.display_insights(insights)
    
    # If you have a PDF file, uncomment this:
    # print("\nTEST 2: Analyzing PDF Document")
    # pdf_insights = analyzer.analyze_document("path/to/your/file.pdf", context="Research paper analysis")
    # if pdf_insights:
    #     analyzer.display_insights(pdf_insights)