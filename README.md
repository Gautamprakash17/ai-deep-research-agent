# ai-deep-research-agent

A powerful, feature-rich research assistant that leverages OpenAI's Agents SDK or Groq API along with Firecrawl's deep research capabilities to perform comprehensive web research on any topic with advanced customization and professional reporting.

[![Research Agent](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()
[![Python](https://img.shields.io/badge/Python-3.8+-blue)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-orange)]()

> Maintained by [Gautam Prakash](https://github.com/Gautamprakash17)  
> Company Repository: [Elint-Agents](https://github.com/Elint-Agents)

## ✨ Key Features

### 🎯 **Multi-Provider AI Support**
- **OpenAI**: High-quality results with GPT-4 and GPT-3.5-turbo
- **Groq**: Cost-effective, ultra-fast processing with Llama 3.1 and Mixtral
- **Easy Switching**: Toggle between providers seamlessly

### 🔧 **Advanced Research Customization**
- **Research Templates**: Academic, Market Analysis, Technical Deep Dive, News Summary, Custom
- **Parameter Control**: Adjustable search depth, time limits, and source counts
- **Template-Specific Instructions**: Optimized prompts for different research types

### 📊 **Professional Reporting & Analytics**
- **Real-time Progress Tracking**: Visual progress bars and status updates
- **Research Metrics Dashboard**: Time tracking, template usage, search depth metrics
- **Multiple Export Formats**: Markdown, HTML (styled), JSON (with metadata)
- **Research History**: Session-based history with easy access to previous reports

### 🎨 **Enhanced User Experience**
- **Modern UI**: Professional gradient styling and intuitive layout
- **Interactive Elements**: Expandable sections, collapsible reports
- **Error Handling**: Graceful error recovery with retry functionality
- **Debug Mode**: Detailed error messages and API responses for troubleshooting

### 🔍 **Deep Web Research Capabilities**
- **Firecrawl Integration**: Advanced web scraping and content extraction
- **Multi-Source Analysis**: Comprehensive coverage from diverse sources
- **Content Synthesis**: AI-powered analysis and synthesis of findings
- **Citation Management**: Automatic source tracking and citation generation

## 🏗️ Architecture

The application uses a sophisticated multi-agent architecture:

```
User Input → Provider Selection → Research Agent → Firecrawl → 
Content Extraction → Initial Report → Elaboration Agent → 
Enhanced Report → Export Options → History Storage
```

### Agent System
1. **Research Agent**: Performs deep web research using Firecrawl
2. **Elaboration Agent**: Enhances reports with additional context and insights

## 📋 Requirements

- **Python**: 3.8 or higher
- **API Keys**: 
  - OpenAI API key OR Groq API key (required)
  - Firecrawl API key (optional, for web research)
- **Dependencies**: See `requirements.txt`

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   # Personal Repository
   git clone https://github.com/Gautamprakash17/ai-deep-research-agent.git
   
   # Company Repository
   git clone https://github.com/Elint-Agents/ai-deep-research-agent-.git
   
   cd ai-deep-research-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run deep_research_openai.py
   ```

## 🎮 Usage Guide

### 1. **Initial Setup**
- Open the Streamlit app in your browser
- Configure API keys in the sidebar
- Choose your preferred AI provider

### 2. **Research Configuration**
- **Select Template**: Choose from 5 research templates
- **Adjust Parameters**:
  - **Research Depth**: 1-5 (shallow to very deep)
  - **Time Limit**: 1-10 minutes
  - **Max Sources**: 5-20 sources to analyze

### 3. **Conduct Research**
- Enter your research topic
- Click "Start Research"
- Monitor real-time progress
- View research metrics upon completion

### 4. **Export & Share**
- Download in multiple formats:
  - 📄 **Markdown**: For documentation
  - 🌐 **HTML**: Styled web-ready format
  - 📊 **JSON**: With metadata for analysis

## 📊 Provider Comparison

| Feature | OpenAI | Groq |
|---------|--------|------|
| **Cost** | Pay-per-use | Pay-per-use (often cheaper) |
| **Speed** | Fast | Very fast (optimized for speed) |
| **Quality** | Excellent | Good |
| **Models** | GPT-4, GPT-3.5-turbo | Llama 3.1, Mixtral, Gemma |
| **Best For** | High-quality results | Cost-effective, fast processing |
| **Setup** | [OpenAI API Keys](https://platform.openai.com/api-keys) | [Groq Console](https://console.groq.com/keys) |

## 🎯 Research Templates

### 📚 **Academic Research**
- Scholarly sources and academic rigor
- Methodology, findings, and implications
- Formal academic language and structure
- Comprehensive literature review

### 📈 **Market Analysis**
- Market trends, competitors, and opportunities
- Market size, growth potential, and key players
- Actionable business insights
- SWOT analysis and recommendations

### 🔧 **Technical Deep Dive**
- Technical specifications and implementation details
- Code examples, architecture diagrams, and comparisons
- Practical implementation guidance
- Performance metrics and benchmarks

### 📰 **News Summary**
- Recent developments and breaking news
- Timeline of events and key stakeholders
- Context and background information
- Expert opinions and public reactions

### 🎨 **Custom**
- Adaptable approach based on topic
- Appropriate sources and methodology
- Comprehensive analysis tailored to query
- Relevant examples and case studies

## 📝 Example Research Topics

### Academic Research
- "Impact of climate change on marine biodiversity"
- "Machine learning applications in healthcare"
- "Quantum computing developments and implications"

### Market Analysis
- "Electric vehicle market trends 2024"
- "AI startup ecosystem analysis"
- "Renewable energy investment opportunities"

### Technical Deep Dive
- "Kubernetes orchestration best practices"
- "Blockchain consensus mechanisms comparison"
- "Microservices architecture patterns"

### News Summary
- "Latest developments in space exploration"
- "Global economic policy changes 2024"
- "Breakthroughs in renewable energy technology"

## 🔧 Advanced Features

### 📊 **Research Metrics Dashboard**
- Research completion time
- Template used
- Search depth achieved
- Number of sources analyzed

### 📚 **Research History**
- Session-based storage of previous research
- Quick access to past reports
- Metadata preservation
- Easy comparison between studies

### 🎨 **Professional Export Options**
- **Markdown**: Clean, formatted documentation
- **HTML**: Styled web-ready reports with metadata
- **JSON**: Structured data with research metrics

### 🔄 **Error Recovery**
- Automatic retry functionality
- Graceful error handling
- Debug mode for troubleshooting
- Connection testing for APIs

## 🛠️ Technical Implementation

### Core Components
- **Streamlit Frontend**: Modern, responsive UI
- **Agent Framework**: OpenAI Agents SDK integration
- **Firecrawl API**: Advanced web research capabilities
- **Session Management**: Persistent state and history
- **Export System**: Multiple format support

### Performance Optimizations
- **Caching**: Session-based caching for improved performance
- **Progress Tracking**: Real-time updates during research
- **Error Handling**: Robust error recovery mechanisms
- **Memory Management**: Efficient session state handling

## 🔑 API Setup

### OpenAI Setup
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create account and add payment method
3. Generate API key
4. Add key to the app sidebar

### Groq Setup
1. Visit [Groq Console](https://console.groq.com/keys)
2. Create account (free tier available)
3. Generate API key
4. Add key to the app sidebar

### Firecrawl Setup (Optional)
1. Visit [Firecrawl](https://firecrawl.dev)
2. Create account and get API key
3. Add key for enhanced web research capabilities

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/Gautamprakash17/ai-deep-research-agent.git
cd ai-deep-research-agent

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run deep_research_openai.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for the Agents SDK and GPT models
- Groq for fast AI processing capabilities
- Firecrawl for advanced web research capabilities
- Streamlit for the amazing web framework
- The open-source community for inspiration and tools

---

**Ready to revolutionize your research workflow?** 🚀

Start exploring with your first research topic today!