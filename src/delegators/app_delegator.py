from __future__ import annotations
import os
from src.helpers.config.config_reader import ConfigReader
from src.helpers.runnables.python_executor import PythonExecutor
from src.models.event_types import EventTypes
from src.models.signal_statuses import SignalStatuses
from libs.PythonLibrary.utils import debug_text
from libs.PythonLibrary.utils import TerminalProcess

class App:
    def __init__(self) -> None:
        pass

    def read_config(self) -> App:
        self.config = ConfigReader()
        return self

    def collect_signals(self) -> App:
        debug_text('Collecting Signals')
        tp = TerminalProcess(len(self.config.get('markets')))
        exec_path = os.path.join(self.config.get('signal-detector.path'), 'main.py')
        self.signals = []
        for market in self.config.get('markets'):
            signals = PythonExecutor(exec_path, [
                *self.config.get('signal-detector.options'),
                "--market {}".format(market),
                "--past_days {}".format(self.config.get('past-candles'))
            ]) \
            .run() \
            .parse_signals()
            self.signals = [*self.signals, *signals]
            tp.hit()
        return self

    def run(self) -> App:
        signal_events = []
        iteration = 0
        for signal in self.signals:
            if signal.status != SignalStatuses.PENDING:
                signal_events.append((signal.time, EventTypes.ENTRY, iteration))
                signal_events.append((signal.time + signal.life, EventTypes.EXIT, iteration))
                iteration += 1
        signal_events.sort()
        alive_set = set()
        alive_markets = set()
        gains = []
        balance = self.config.get('initial-balance')
        hold = 0
        for event in signal_events:
            if event[1] == EventTypes.ENTRY:
                # enter event
                if balance > self.config.get('trade-chunk') and self.signals[event[2]].market not in alive_markets:
                    balance -= self.config.get('trade-chunk')
                    hold += self.config.get('trade-chunk')
                    alive_set.add(event[2])
                    alive_markets.add(self.signals[event[2]].market)
                    debug_text('in ({:01d}->{:02d}): {}/{}'.format(len(alive_set), event[2], self.signals[event[2]].market, self.signals[event[2]].name))
            else:
                # exit event
                if event[2] in alive_set:
                    balance += self.config.get('trade-chunk') * (1 + self.signals[event[2]].gain)
                    hold -= self.config.get('trade-chunk')
                    alive_set.remove(event[2])
                    alive_markets.remove(self.signals[event[2]].market)
                    gains.append((event[0], hold + balance))
                    debug_text('out({:01d}->{:02d}): {}/{} gain: {:03f}'.format(len(alive_set), event[2], self.signals[event[2]].market, self.signals[event[2]].name, self.signals[event[2]].gain))
        self.result = {
            "gains": gains,
            "total": balance
        }
        return self

    def plot_figures(self) -> App:
        return self

    def output_results(self) -> App:
        debug_text(self.result)
        return self
