#!/usr/bin/env python3
"""
Streamlit Web UI for Agno Agents

This creates a beautiful, interactive web interface for chatting with your Agno agents.
Features multiple agent types, conversation history, and real-time streaming responses.
"""

import streamlit as st
import os
import sys
import pathlib
from datetime import datetime
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.db.sqlite import SqliteDb
from model_config import get_configured_model, get_reasoning_model, print_model_info

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Agno Agent Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .agent-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .user-message {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        border: none;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_agents():
    """Initialize all agent types with caching for performance."""
    try:
        agents = {}
        
        # Basic Chat Agent
        agents["Chat Assistant"] = Agent(
            name="Chat Assistant",
            model=get_configured_model(),
            instructions=[
                "You are a helpful AI assistant.",
                "Provide clear, accurate, and concise responses.",
                "Be friendly and engaging in your conversations.",
                "If you're unsure about something, say so rather than guessing.",
            ],
            description="A friendly conversational AI assistant for general questions and discussions.",
            markdown=True,
            add_datetime_to_context=True,
        )
        
        # Research Agent with Tools
        agents["Research Assistant"] = Agent(
            name="Research Assistant",
            model=get_configured_model(),
            tools=[DuckDuckGoTools()],
            instructions=[
                "You are a research assistant with access to web search.",
                "Use the search tool to find current information when needed.",
                "Always cite your sources and provide accurate information.",
                "Be thorough in your research but concise in your responses.",
            ],
            description="An AI research assistant that can search the web for current information.",
            markdown=True,
            add_datetime_to_context=True,
        )
        
        # Reasoning Agent
        agents["Reasoning Expert"] = Agent(
            name="Reasoning Expert",
            model=get_reasoning_model(),
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "You are an expert problem-solving assistant with strong analytical skills.",
                "Always break down complex problems into component parts.",
                "Use step-by-step reasoning and show your thought process.",
                "Consider multiple perspectives and evaluate evidence.",
                "Identify assumptions and highlight areas of uncertainty.",
            ],
            description="An AI expert specialized in structured reasoning and complex problem analysis.",
            markdown=True,
            add_datetime_to_context=True,
            stream_intermediate_steps=True,
        )
        
        # Memory Agent
        db = SqliteDb(db_file="streamlit_agent_memory.db")
        agents["Memory Assistant"] = Agent(
            name="Memory Assistant",
            model=get_configured_model(),
            db=db,
            enable_agentic_memory=True,
            instructions=[
                "You are a personal assistant with memory capabilities.",
                "Remember important information about users and conversations.",
                "Refer to previous conversations when relevant.",
                "Build context over time to provide better assistance.",
                "Ask clarifying questions to better understand user needs.",
            ],
            description="An AI assistant with persistent memory that remembers conversations across sessions.",
            markdown=True,
            add_datetime_to_context=True,
        )
        
        return agents
    except Exception as e:
        st.error(f"Error initializing agents: {e}")
        return {}

def display_agent_info(agent_name, agents):
    """Display information about the selected agent."""
    if agent_name in agents:
        agent = agents[agent_name]
        
        st.markdown(f"""
        <div class="agent-card">
            <h4>🤖 {agent_name}</h4>
            <p><strong>Description:</strong> {agent.description}</p>
            <p><strong>Model:</strong> {os.getenv('DEFAULT_MODEL', 'GPT-4o-mini')}</p>
            <p><strong>Provider:</strong> {"Azure OpenAI" if os.getenv('AZURE_OPENAI_API_KEY') else "OpenAI"}</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Agno Agent Chat Interface</h1>
        <p>Interact with specialized AI agents powered by Azure OpenAI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize agents
    agents = initialize_agents()
    
    if not agents:
        st.error("Failed to initialize agents. Please check your configuration.")
        st.stop()
    
    # Sidebar for agent selection and info
    with st.sidebar:
        st.header("🎯 Agent Selection")
        
        agent_names = list(agents.keys())
        selected_agent = st.selectbox(
            "Choose an AI agent:",
            agent_names,
            index=0,
            help="Select different agents for different capabilities"
        )
        
        st.markdown("---")
        
        # Display agent information
        display_agent_info(selected_agent, agents)
        
        st.markdown("---")
        
        # Configuration info
        st.header("⚙️ Configuration")
        model_name = os.getenv('DEFAULT_MODEL', 'GPT-4o-mini')
        provider = "Azure OpenAI" if os.getenv('AZURE_OPENAI_API_KEY') else "OpenAI"
        
        st.success(f"✅ {provider}")
        st.info(f"🔧 Model: {model_name}")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            if f"messages_{selected_agent}" in st.session_state:
                del st.session_state[f"messages_{selected_agent}"]
            st.rerun()
    
    # Main chat interface
    st.header(f"💬 Chat with {selected_agent}")
    
    # Initialize chat history for the selected agent
    if f"messages_{selected_agent}" not in st.session_state:
        st.session_state[f"messages_{selected_agent}"] = []
    
    # Display chat history
    messages = st.session_state[f"messages_{selected_agent}"]
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input(f"Ask {selected_agent} anything..."):
        # Add user message to chat history
        messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        
        # Get agent response
        try:
            agent = agents[selected_agent]
            
            # Display assistant message with streaming
            with chat_container:
                with st.chat_message("assistant"):
                    with st.spinner(f"{selected_agent} is thinking..."):
                        # Get response from agent
                        response = agent.run(prompt)
                        
                        # Display the response
                        if hasattr(response, 'content') and response.content:
                            response_text = response.content
                        else:
                            response_text = str(response)
                        
                        st.markdown(response_text)
                        
                        # Add assistant response to chat history
                        messages.append({"role": "assistant", "content": response_text})
                        
        except Exception as e:
            st.error(f"Error getting response from {selected_agent}: {e}")
            
            # Add error message to chat history
            error_msg = f"Sorry, I encountered an error: {e}"
            messages.append({"role": "assistant", "content": error_msg})
    
    # Example prompts section
    st.markdown("---")
    st.header("💡 Example Prompts")
    
    example_prompts = {
        "Chat Assistant": [
            "Hello! Tell me about yourself.",
            "What can you help me with today?",
            "Explain quantum computing in simple terms.",
        ],
        "Research Assistant": [
            "What are the latest developments in AI?",
            "Search for recent news about renewable energy.",
            "Find information about the current stock market trends.",
        ],
        "Reasoning Expert": [
            "Should companies adopt a 4-day work week? Analyze pros and cons.",
            "How would you solve traffic congestion in major cities?",
            "What are the ethical implications of AI in healthcare?",
        ],
        "Memory Assistant": [
            "My name is [Your Name] and I work in [Your Field].",
            "Remember that I prefer detailed explanations.",
            "What did we discuss in our last conversation?",
        ]
    }
    
    if selected_agent in example_prompts:
        st.write(f"**Try these with {selected_agent}:**")
        cols = st.columns(len(example_prompts[selected_agent]))
        
        for i, example in enumerate(example_prompts[selected_agent]):
            with cols[i]:
                if st.button(f"💬 {example[:30]}...", key=f"example_{i}"):
                    # Add example to chat input (this will trigger the chat flow)
                    st.session_state.chat_input = example
                    st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚀 Powered by <strong>Agno Framework</strong> & <strong>Azure OpenAI</strong></p>
        <p>💡 Switch between different agents using the sidebar</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()