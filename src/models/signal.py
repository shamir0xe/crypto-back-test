class Signal:
    def __init__(
        self,
        name: str,
        gain: float,
        life: int,
        time: int,
        market: str,
        status: str
    ) -> None:
        self.name = name
        self.gain = gain
        self.life = life
        self.time = time
        self.market = market
        self.status = status
