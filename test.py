

# Add sliders for research parameters
col1, col2, col3 = st.columns(3)
with col1:
    max_depth = st.slider("Research Depth", 1, 5, 3, help="How deep to search")
with col2:
    time_limit = st.slider("Time Limit (minutes)", 1, 10, 3, help="Maximum research time")
with col3:
    max_urls = st.slider("Max Sources", 5, 20, 10, help="Maximum number of sources") 

# Add progress bar and status updates
progress_bar = st.progress(0)
status_text = st.empty()
for i in range(100):
    progress_bar.progress(i + 1)
    status_text.text(f"Research progress: {i + 1}%")
    time.sleep(0.1) 

# Store research history
if "research_history" not in st.session_state:
    st.session_state.research_history = []

# Add to history after research
st.session_state.research_history.append({
    "topic": research_topic,
    "timestamp": datetime.now(),
    "report": enhanced_report
}) 

# Multiple export formats
export_col1, export_col2, export_col3 = st.columns(3)
with export_col1:
    st.download_button("📄 Download PDF", pdf_content, file_name="report.pdf")
with export_col2:
    st.download_button("📝 Download Word", docx_content, file_name="report.docx")
with export_col3:
    st.download_button("🌐 Download HTML", html_content, file_name="report.html") 

# Research templates
template = st.selectbox("Research Template", [
    "Academic Research",
    "Market Analysis", 
    "Technical Deep Dive",
    "News Summary",
    "Custom"
]) 

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
}
</style>
""", unsafe_allow_html=True) 

# Status dashboard
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Sources Found", sources_count)
with col2:
    st.metric("Research Time", f"{time_taken:.1f}s")
with col3:
    st.metric("Content Length", f"{len(report)} chars")
with col4:
    st.metric("Confidence Score", "85%") 

# Display sources with clickable links
st.subheader("📚 Sources")
for i, source in enumerate(sources):
    st.markdown(f"{i+1}. [{source['title']}]({source['url']})") 

# Better error handling
@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_research(topic, params):
    try:
        return perform_research(topic, params)
    except Exception as e:
        st.error(f"Research failed: {e}")
        if st.button("🔄 Retry"):
            return perform_research(topic, params) 

# Test all APIs before starting
def validate_all_apis():
    results = {}
    if st.session_state.openai_api_key:
        results["OpenAI"] = test_openai_connection()
    if st.session_state.groq_api_key:
        results["Groq"] = test_groq_connection()
    if st.session_state.firecrawl_api_key:
        results["Firecrawl"] = test_firecrawl_connection()
    return results 

# Quality assessment
def assess_research_quality(report, sources):
    metrics = {
        "completeness": len(report) / 1000,  # Normalized
        "source_diversity": len(set(s['domain'] for s in sources)),
        "recency": calculate_source_recency(sources),
        "credibility": assess_source_credibility(sources)
    }
    return metrics 

# Compare multiple research topics
if st.checkbox("Compare Multiple Topics"):
    topics = st.text_area("Enter topics (one per line)")
    if st.button("Compare Research"):
        results = []
        for topic in topics.split('\n'):
            results.append(perform_research(topic))
        display_comparison(results) 

# Auto-generate citations
def generate_citations(sources):
    citations = []
    for source in sources:
        citation = f"{source['title']}. {source['url']}. Accessed {datetime.now().strftime('%Y-%m-%d')}."
        citations.append(citation)
    return citations 

# Extract key insights
def extract_key_insights(report):
    # Use AI to extract key points
    insights = ai_extract_insights(report)
    return {
        "key_findings": insights["findings"],
        "trends": insights["trends"],
        "recommendations": insights["recommendations"]
    }
