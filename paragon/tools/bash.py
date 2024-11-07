import asyncio
import os
from typing import ClassVar, Literal

from alpha_tool_bash_param import AlphaToolBashParam
from base import  BaseParagonTool, CLIResult, ToolError, ToolResult

class _BashSession:
    """Session of a bash shell."""
    
    _started: bool 
    _process: asyncio.subprocess.Process
    
    command: str = "/bin/bash"
    _output_delay: float = 0.2
    _timeout: float = 120.0
    _sentinel: str = "<<exit>>"
    
    def __init__(self):
        self.__started = False
        self.__timed_out = False
        
    async def start(self):
        if self._started:
            return
        
        self._process = await asyncio.create_subprocess_shell(
            self.command,
            preexec_fn=os.setsid,
            shell=True,
            bufsize=0,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        self.__started = True
        
    def stop(self):
        """Terminate bash shell."""
        if not self.__started:
            raise ToolError("Session has not started.")
        if self._process.returncode is not None:
            return
        self._process.terminate()
        
    async def run(self, command: str):
        """Execute a command in the bash shell."""
        if not self._started:
            raise ToolError("Session has not started.")
        if self._process.returncode is not None:
            return ToolResult(
                system="tool must be restarted",
                error=f"bash has exited with returncode {self._process.returncode}"
            )
        if self.__timed_out:
            raise ToolError(
                f"timed out: bash has not returned in {self.__timed_out} seconds and must be restarted",
            )
        assert self._process.stdin
        assert self._process.stdout
        assert self._process.stderr
        
        self._process.stdin.write(
            command.encode() + f"; echo '{self._sentinel}'\n".encode()
        )
        await self._process.stdin.drain()
        
        try:
            async with asyncio.timeout(self._timeout):
                while True:
                    await asyncio.sleep(self._output_delay)
                    #StreamReader buffer is faster than directly from stdout/stderr
                    output = self._process.stdout._buffer.decode()
                    if self._sentinel in output:
                        output = output[: output.index(self._sentinel)]
                        break
        except asyncio.TimeoutError:
            self.__timed_out = True
            raise ToolError(
                f"timed out: bash has not returned in {self._timeout} seconds and has to be restarted"
            ) from None
            
        if output.endswith('\n'):
            output = output[:-1]
            
        error = self._process.stderr._buffer.decode()
        if error.endswith('\n'):
            error = error[:-1]
            
        self._process.stdout._buffer.clear()
        self._process.stderr._buffer.clear()
        
        return CLIResult(output=output, error=error)
    


class BashTool(BaseParagonTool):
    """Tool that will allow the agent to run bash commands."""
    name: ClassVar[Literal["bash"]] = "bash"
    api_type: ClassVar[Literal["bash_20241106"]] = "bash_20241106"
    
    def __init__(self):
        self._session = None
        super().__init__()
        
    async def __call__(
        self, command: str | None = None, restart: bool = False, **kwargs):
        if restart:
            if self._session:
                self._session.stop()
            self._session = _BashSession()
            await self._session.start()
            
            return ToolResult(system="tool has been restarted.")
        
        if self._session is None:
            self._session = _BashSession()
            await self._session.start()
            
        if command is not None:
            return await self._session.run(command)
        
        raise ToolError("no command provided.")
    
    def to_params(self) -> AlphaToolBashParam:
        return {
            "type": self.api_type,
            "name": self.name,
        }