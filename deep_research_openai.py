import asyncio
import streamlit as st
from typing import Dict, Any, List
from agents import Agent, Runner, trace, set_default_openai_key, set_groq_key, set_provider
from firecrawl import FirecrawlApp
from agents import function_tool
from datetime import datetime
import time
import json

# Set page configuration
st.set_page_config(
    page_title="AI Deep Research Agent",
    page_icon="📘",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background: #f0f2f6;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #667eea;
}
.progress-container {
    background: #f0f2f6;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for API keys if not exists
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""
if "firecrawl_api_key" not in st.session_state:
    st.session_state.firecrawl_api_key = ""
if "selected_provider" not in st.session_state:
    st.session_state.selected_provider = "OpenAI"
if "research_history" not in st.session_state:
    st.session_state.research_history = []
if "current_research" not in st.session_state:
    st.session_state.current_research = None

# Sidebar for API keys
with st.sidebar:
    st.title("API Configuration")
    
    # Provider selection
    provider = st.selectbox(
        "Choose AI Provider",
        ["OpenAI", "Groq"],
        index=0 if st.session_state.selected_provider == "OpenAI" else 1,
        help="Select your preferred AI provider"
    )
    st.session_state.selected_provider = provider
    
    # Set the provider in the agents module
    set_provider(provider)
    
    st.markdown("---")
    
    if provider == "OpenAI":
        st.header("OpenAI Configuration")
        openai_api_key = st.text_input(
            "OpenAI API Key", 
            value=st.session_state.openai_api_key,
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys"
        )
        if openai_api_key:
            st.session_state.openai_api_key = openai_api_key
            set_default_openai_key(openai_api_key)
    
    elif provider == "Groq":
        st.header("Groq Configuration")
        groq_api_key = st.text_input(
            "Groq API Key", 
            value=st.session_state.groq_api_key,
            type="password",
            help="Get your API key from https://console.groq.com/keys"
        )
        if groq_api_key:
            st.session_state.groq_api_key = groq_api_key
            set_groq_key(groq_api_key)
    
    # Firecrawl API key (common for both providers)
    st.header("Firecrawl Configuration")
    firecrawl_api_key = st.text_input(
        "Firecrawl API Key (Optional)", 
        value=st.session_state.firecrawl_api_key,
        type="password",
        help="Get your API key from https://firecrawl.dev"
    )
    if firecrawl_api_key:
        st.session_state.firecrawl_api_key = firecrawl_api_key
    
    # Debug mode
    debug_mode = st.checkbox("Debug Mode", help="Show detailed error messages and API responses")
    if debug_mode:
        st.session_state.debug_mode = True
    else:
        st.session_state.debug_mode = False
    
    # Research Templates
    st.markdown("---")
    st.header("🔧 Research Settings")
    
    template = st.selectbox(
        "Research Template",
        ["Academic Research", "Market Analysis", "Technical Deep Dive", "News Summary", "Custom"],
        help="Choose a research template for better results"
    )
    
    # Research Parameters
    st.subheader("Research Parameters")
    max_depth = st.slider("Research Depth", 1, 5, 3, help="How deep to search (1=shallow, 5=very deep)")
    time_limit = st.slider("Time Limit (minutes)", 1, 10, 3, help="Maximum research time")
    max_urls = st.slider("Max Sources", 5, 20, 10, help="Maximum number of sources to analyze")
    
    # Store parameters in session state
    st.session_state.research_params = {
        "template": template,
        "max_depth": max_depth,
        "time_limit": time_limit * 60,  # Convert to seconds
        "max_urls": max_urls
    }

# Main content
st.markdown('<div class="main-header"><h1>📘 AI Deep Research Agent</h1></div>', unsafe_allow_html=True)
st.markdown(f"This AI Agent performs deep research on any topic using {provider} and Firecrawl")

# Research topic input with better styling
research_topic = st.text_input(
    "Enter your research topic:", 
    placeholder="e.g., Latest developments in AI, Market analysis of electric vehicles, etc.",
    help="Be specific for better research results"
)

# Research History
if st.session_state.research_history:
    with st.expander(f"📚 Research History ({len(st.session_state.research_history)} items)"):
        for i, research in enumerate(reversed(st.session_state.research_history)):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{research['topic']}**")
                st.caption(f"Research completed: {research['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            with col2:
                if st.button(f"View {i+1}", key=f"view_{i}"):
                    st.session_state.current_research = research
                    st.rerun()

# Keep the original deep_research tool
@function_tool
async def deep_research(query: str, max_depth: int, time_limit: int, max_urls: int) -> Dict[str, Any]:
    """
    Perform comprehensive web research using Firecrawl's deep research endpoint.
    """
    try:
        # Initialize FirecrawlApp with the API key from session state
        firecrawl_app = FirecrawlApp(api_key=st.session_state.firecrawl_api_key)
        
        # Set up a callback for real-time updates with progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def on_activity(activity):
            activity_type = activity.get('type', 'info')
            message = activity.get('message', 'Processing...')
            
            # Update progress based on activity type
            if 'searching' in activity_type.lower():
                progress_bar.progress(25)
            elif 'analyzing' in activity_type.lower():
                progress_bar.progress(50)
            elif 'synthesizing' in activity_type.lower():
                progress_bar.progress(75)
            elif 'complete' in activity_type.lower():
                progress_bar.progress(100)
            
            status_text.text(f"[{activity_type.upper()}] {message}")
            st.write(f"🔍 [{activity_type}] {message}")
        
        # Run deep research with updated v1 API format
        with st.spinner("Performing deep research..."):
            results = firecrawl_app.deep_research(
                query=query,
                maxDepth=max_depth,
                timeLimit=time_limit,
                maxUrls=max_urls,
                on_activity=on_activity
            )
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        return {
            "success": True,
            "final_analysis": results['data']['finalAnalysis'],
            "sources_count": len(results['data']['sources']),
            "sources": results['data']['sources']
        }
    except Exception as e:
        st.error(f"Deep research error: {str(e)}")
        return {"error": str(e), "success": False}

# Keep the original agents
def get_template_instructions(template: str) -> str:
    """Get template-specific instructions for the research agent."""
    base_instructions = """You are a research assistant that can perform deep web research on any topic.

    When given a research topic or question:
    1. Use the deep_research tool to gather comprehensive information
       - Always use these parameters:
         * max_depth: {max_depth} (for appropriate depth)
         * time_limit: {time_limit} (in seconds)
         * max_urls: {max_urls} (sufficient sources)
    2. The tool will search the web, analyze multiple sources, and provide a synthesis
    3. Review the research results and organize them into a well-structured report
    4. Include proper citations for all sources
    5. Highlight key findings and insights
    """
    
    template_specific = {
        "Academic Research": """
    6. Focus on academic rigor and scholarly sources
    7. Include methodology, findings, and implications
    8. Use formal academic language and structure
    9. Provide comprehensive literature review
        """,
        "Market Analysis": """
    6. Focus on market trends, competitors, and opportunities
    7. Include market size, growth potential, and key players
    8. Provide actionable business insights
    9. Include SWOT analysis and recommendations
        """,
        "Technical Deep Dive": """
    6. Focus on technical specifications and implementation details
    7. Include code examples, architecture diagrams, and technical comparisons
    8. Provide practical implementation guidance
    9. Include performance metrics and benchmarks
        """,
        "News Summary": """
    6. Focus on recent developments and breaking news
    7. Include timeline of events and key stakeholders
    8. Provide context and background information
    9. Include expert opinions and public reactions
        """,
        "Custom": """
    6. Adapt the research approach based on the specific topic
    7. Use appropriate sources and methodology for the subject
    8. Provide comprehensive analysis tailored to the query
    9. Include relevant examples and case studies
        """
    }
    
    return base_instructions + template_specific.get(template, template_specific["Custom"])

research_agent = Agent(
    name="research_agent",
    instructions=get_template_instructions(st.session_state.get('research_params', {}).get('template', 'Custom')),
    tools=[deep_research]
)

elaboration_agent = Agent(
    name="elaboration_agent",
    instructions="""You are an expert content enhancer specializing in research elaboration.

    When given a research report:
    1. Analyze the structure and content of the report
    2. Enhance the report by:
       - Adding more detailed explanations of complex concepts
       - Including relevant examples, case studies, and real-world applications
       - Expanding on key points with additional context and nuance
       - Adding visual elements descriptions (charts, diagrams, infographics)
       - Incorporating latest trends and future predictions
       - Suggesting practical implications for different stakeholders
    3. Maintain academic rigor and factual accuracy
    4. Preserve the original structure while making it more comprehensive
    5. Ensure all additions are relevant and valuable to the topic
    """
)

async def run_research_process(topic: str):
    """Run the complete research process."""
    start_time = time.time()
    
    # Get research parameters
    params = st.session_state.get('research_params', {
        'max_depth': 3,
        'time_limit': 180,
        'max_urls': 10,
        'template': 'Custom'
    })
    
    # Update research agent with current parameters
    research_agent.instructions = get_template_instructions(params['template']).format(
        max_depth=params['max_depth'],
        time_limit=params['time_limit'],
        max_urls=params['max_urls']
    )
    
    # Step 1: Initial Research
    with st.spinner("Conducting initial research..."):
        research_result = await Runner.run(research_agent, topic)
        initial_report = research_result.final_output
    
    # Display initial report in an expander
    with st.expander("View Initial Research Report"):
        st.markdown(initial_report)
    
    # Step 2: Enhance the report
    with st.spinner("Enhancing the report with additional information..."):
        elaboration_input = f"""
        RESEARCH TOPIC: {topic}
        TEMPLATE: {params['template']}
        
        INITIAL RESEARCH REPORT:
        {initial_report}
        
        Please enhance this research report with additional information, examples, case studies, 
        and deeper insights while maintaining its academic rigor and factual accuracy.
        """
        
        elaboration_result = await Runner.run(elaboration_agent, elaboration_input)
        enhanced_report = elaboration_result.final_output
    
    # Calculate research metrics
    end_time = time.time()
    research_time = end_time - start_time
    
    return {
        "enhanced_report": enhanced_report,
        "initial_report": initial_report,
        "research_time": research_time,
        "topic": topic,
        "params": params
    }

# Check if required API keys are available
def check_api_keys():
    if st.session_state.selected_provider == "OpenAI":
        return bool(st.session_state.openai_api_key)
    elif st.session_state.selected_provider == "Groq":
        return bool(st.session_state.groq_api_key)
    return False

def test_groq_connection():
    """Test Groq API connection with a simple request."""
    try:
        import requests
        
        headers = {
            "Authorization": f"Bearer {st.session_state.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "user", "content": "Hello! Please respond with 'Connection successful'."}
            ],
            "max_tokens": 50
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if st.session_state.get('debug_mode', False):
                st.json(result)
            return True, "Connection successful"
        else:
            return False, f"API Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

# Main research process
if st.button("Start Research", disabled=not (check_api_keys() and research_topic)):
    if not check_api_keys():
        st.warning(f"Please enter your {st.session_state.selected_provider} API key in the sidebar.")
    elif not research_topic:
        st.warning("Please enter a research topic.")
    else:
        try:
            # Test Groq connection if using Groq
            if st.session_state.selected_provider == "Groq":
                with st.spinner("Testing Groq API connection..."):
                    success, message = test_groq_connection()
                    if not success:
                        st.error(f"Groq API test failed: {message}")
                        st.stop()
                    else:
                        st.success("Groq API connection successful!")
            
            # Create placeholder for the final report
            report_placeholder = st.empty()
            
            # Run the research process
            research_result = asyncio.run(run_research_process(research_topic))
            
            # Display research metrics
            st.markdown("### 📊 Research Metrics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Research Time", f"{research_result['research_time']:.1f}s")
            with col2:
                st.metric("Template Used", research_result['params']['template'])
            with col3:
                st.metric("Search Depth", research_result['params']['max_depth'])
            with col4:
                st.metric("Max Sources", research_result['params']['max_urls'])
            
            # Display the enhanced report
            st.markdown("## 📋 Enhanced Research Report")
            st.markdown(research_result["enhanced_report"])
            
            # Add to research history
            st.session_state.research_history.append({
                "topic": research_topic,
                "timestamp": datetime.now(),
                "report": research_result["enhanced_report"],
                "metrics": {
                    "research_time": research_result['research_time'],
                    "template": research_result['params']['template'],
                    "max_depth": research_result['params']['max_depth'],
                    "max_urls": research_result['params']['max_urls']
                }
            })
            
            # Export options
            st.markdown("### 📤 Export Options")
            export_col1, export_col2, export_col3 = st.columns(3)
            
            with export_col1:
                st.download_button(
                    "📄 Download Markdown",
                    research_result["enhanced_report"],
                    file_name=f"{research_topic.replace(' ', '_')}_report.md",
                    mime="text/markdown"
                )
            
            with export_col2:
                # Generate HTML version
                html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Research Report: {research_topic}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #667eea; }}
        .metadata {{ background: #f0f2f6; padding: 15px; border-radius: 8px; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>Research Report: {research_topic}</h1>
    <div class="metadata">
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Template:</strong> {research_result['params']['template']}</p>
        <p><strong>Research Time:</strong> {research_result['research_time']:.1f} seconds</p>
    </div>
    {research_result["enhanced_report"].replace(chr(10), '<br>')}
</body>
</html>"""
                st.download_button(
                    "🌐 Download HTML",
                    html_content,
                    file_name=f"{research_topic.replace(' ', '_')}_report.html",
                    mime="text/html"
                )
            
            with export_col3:
                # Generate JSON export with metadata
                json_export = {
                    "topic": research_topic,
                    "timestamp": datetime.now().isoformat(),
                    "template": research_result['params']['template'],
                    "metrics": {
                        "research_time": research_result['research_time'],
                        "max_depth": research_result['params']['max_depth'],
                        "max_urls": research_result['params']['max_urls']
                    },
                    "report": research_result["enhanced_report"]
                }
                st.download_button(
                    "📊 Download JSON",
                    json.dumps(json_export, indent=2),
                    file_name=f"{research_topic.replace(' ', '_')}_report.json",
                    mime="application/json"
                )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            if st.session_state.get('debug_mode', False):
                st.exception(e)
            
            # Add retry button
            if st.button("🔄 Retry Research"):
                st.rerun()

# Display current research if available
if st.session_state.current_research:
    st.markdown("---")
    st.markdown("## 📖 Current Research")
    st.markdown(f"**Topic:** {st.session_state.current_research['topic']}")
    st.markdown(f"**Completed:** {st.session_state.current_research['timestamp'].strftime('%Y-%m-%d %H:%M')}")
    
    if 'metrics' in st.session_state.current_research:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Research Time", f"{st.session_state.current_research['metrics']['research_time']:.1f}s")
        with col2:
            st.metric("Template", st.session_state.current_research['metrics']['template'])
        with col3:
            st.metric("Search Depth", st.session_state.current_research['metrics']['max_depth'])
    
    st.markdown(st.session_state.current_research['report'])
    
    if st.button("Clear Current Research"):
        st.session_state.current_research = None
        st.rerun()

# Footer
st.markdown("---")
st.markdown(f"Powered by {provider} and Firecrawl")

# Provider information
with st.expander("Provider Information"):
    if st.session_state.selected_provider == "OpenAI":
        st.markdown("""
        ### OpenAI
        - **Cost**: Pay-per-use
        - **Models**: GPT-4, GPT-3.5-turbo
        - **Speed**: Fast
        - **Quality**: Excellent
        - **Setup**: https://platform.openai.com/api-keys
        """)
    elif st.session_state.selected_provider == "Groq":
        st.markdown("""
        ### Groq
        - **Cost**: Pay-per-use (often cheaper than OpenAI)
        - **Models**: Llama 3.1, Mixtral, Gemma
        - **Speed**: Very fast (optimized for speed)
        - **Quality**: Good
        - **Setup**: https://console.groq.com/keys
        """) 