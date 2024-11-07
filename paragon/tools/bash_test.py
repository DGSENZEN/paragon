#!/usr/bin/env python3
import pytest
from bash import BashTool, ToolError


@pytest.fixture
def bash_tool():
    return BashTool()


@pytest.mark.asyncio
async def test_bash_tool_run_command(bash_tool):
    """Test basic command execution"""
    result = await bash_tool(command="echo 'Hello, World!'")
    print(f"\nCommand output: {result.output}")
    print(f"Command error: {result.error}")
    assert result.output.strip() == "Hello, World!"
    assert result.error == ""


@pytest.mark.asyncio
async def test_bash_tool_session_creation(bash_tool):
    """Test session creation"""

    result = await bash_tool(command="echo 'Session created'")
    print(f"\nSession ID: {id(bash_tool._session)}")
    print(f"Command output: {result.output}")
    assert bash_tool._session is not None
    assert "Session created" in result.output


@pytest.mark.asyncio
async def test_bash_tool_timeout(bash_tool):
    """Test timeout functionality"""

    await bash_tool(command="echo 'Hello World!'")

    bash_tool._session._timeout = 0.1

    print("\nTesting timeout with 0.1 seconds...")

    with pytest.raises(
        ToolError,
        match="timed out: bash has not returned in 0.1 seconds and has to be restarted",
    ):
        await bash_tool(command="sleep 1")


@pytest.mark.asyncio
async def test_bash_tool_no_command(bash_tool):
    """Test error handling for missing command"""

    print("\nTesting missing command...")

    with pytest.raises(ToolError, match="no command provided."):
        await bash_tool()

    """Test error handling for missing command"""

    print("\nTesting missing command...")

    with pytest.raises(ToolError, match="no command provided."):
        await bash_tool()


if __name__ == "__main__":
    # Run tests with detailed output

    pytest.main(
        [
            __file__,
            "-v",  # verbose output
            "-s",  # allow print statements
            "--tb=short",  # shorter traceback format
        ]
    )
