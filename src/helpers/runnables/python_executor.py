from __future__ import annotations
from libs.PythonLibrary.utils import debug_text
from typing import List, Optional
import subprocess
import shlex
import json
from src.models.signal import Signal


class PythonExecutor:
    def __init__(self, path: str, options: List[str] = []) -> None:
        self.command = 'python3 {} {}'.format(path, ' '.join(options))

    def run(self) -> PythonExecutor:
        self.proc = subprocess.Popen(shlex.split(self.command), stdout=subprocess.PIPE)
        return self

    def output(self) -> str:
        out = ''
        first = True
        while True:
            line = self.proc.stdout.readline().decode('utf-8')
            if not line:
                break
            if first:
                first = False
            else:
                out += '\n'
            out += line.rstrip()
        return out
    
    def parse_signals(self) -> List[Signal]:
        output = json.loads(self.output())
        signals = []
        for signal_data in output:
            # debug_text('DATA: %', signal_data)
            signals.append(Signal(
                name=signal_data["name"],
                gain=signal_data["gain"],
                life=signal_data["life"],
                time=signal_data["time"],
                market=signal_data["market"],
                status=signal_data["status"]
            ))
        return signals
