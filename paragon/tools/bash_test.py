#!/usr/bin/env python3
import pytest 

from bash import BashTool, ToolError

@pytest.fixture
def bash_tool():
    return BashTool

@pytest.mark.asyncio
async def test_bash_tool_run_command(bash_tool):
    result = await bash_tool(command="echo 'Hello, World!'")
    assert result.output.strip() == "Hello, World!"
    assert result.error == ""

print("run_command test finished.")
    
@pytest.mark.asyncio
async def test_bash_tool_session_creation(bash_tool):
    result = await bash_tool(command="echo 'Session created'")
    assert bash_tool._session is not None   
    assert "Session created" in result.output
    
print("session_creation test finished.")
    
@pytest.mark.asyncio
async def test_bash_tool_timeout(bash_tool):
    await bash_tool(command="echo 'Hello World!'")
    bash_tool._session._timeout = 0.1
    with pytest.raises(
        ToolError,
        match="timed out: bash has not returned in 0.1 seconds and must be restarted"
    ):
        await bash_tool(command="sleep 1")

print("timeout test finished.")
        
        
@pytest.mark.asyncio
async def test_bash_tool_no_command(bash_tool):
    with pytest.raises(ToolError, match="no command provided."):
        await bash_tool()

print("no command test finished.")