"""
Model Context Protocol (MCP) Agent for tool integration and communication
"""

import httpx
import os
from typing import Any, Dict, List, Optional

class MCPAgent:
    def __init__(self, mcp_server_url: str):
        """Initialize MCP Agent"""
        self.mcp_server_url = mcp_server_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.available_tools: List[Dict[str, Any]] = []
    
    async def discover_tools(self) -> List[Dict[str, Any]]:
        """Discover available tools from MCP server"""
        try:
            response = await self.client.get(
                f"{self.mcp_server_url}/tools",
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            self.available_tools = response.json().get("tools", [])
            return self.available_tools
        except Exception as e:
            raise Exception(f"Error discovering MCP tools: {str(e)}")
    
    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool via MCP"""
        try:
            response = await self.client.post(
                f"{self.mcp_server_url}/tools/{tool_name}/call",
                json={"parameters": parameters},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Error calling MCP tool '{tool_name}': {str(e)}")
    
    async def query(self, query: str) -> Dict[str, Any]:
        """
        Process a query using MCP tools
        
        Args:
            query: User query string
        
        Returns:
            Dictionary with answer and used tools
        """
        try:
            # First, discover available tools if not already done
            if not self.available_tools:
                await self.discover_tools()
            
            # Send query to MCP server for routing
            response = await self.client.post(
                f"{self.mcp_server_url}/query",
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            return {
                "answer": result.get("answer", ""),
                "tools_used": result.get("tools_used", []),
                "metadata": result.get("metadata", {})
            }
        except Exception as e:
            raise Exception(f"Error in MCP query: {str(e)}")
    
    async def get_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific tool"""
        try:
            response = await self.client.get(
                f"{self.mcp_server_url}/tools/{tool_name}",
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Error getting tool info: {str(e)}")
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()