__all__ = ["Attune"]

import asyncio
from typing import Dict, Any, List

import attune
import yaqc
from yaqd_core import ContinuousHardware


class Attune(ContinuousHardware):
    _kind = "attune"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._instrument = attune.load(name)
        self._setables = {k: yaqc.Client(v) for k, v in config["setables"].items()}

    def _set_position(self, position):
        self.set_position_except(position)

    def set_position_except(self, position, exceptions=None):
        self._busy = True
        self._state["destination"] = position
        if exceptions is None:
            exceptions = []
        for name, set_pos in self._instrument(position, self._state["arrangement"]).items():
            if name in exceptions:
                continue
            self._setables[name].set_position(set_pos)
        self._state["position"] = position

    def get_instrument(self):
        return self._instrument.as_dict()

    def set_instrument(self, instrument):
        self._instrument = attune.Instrument(**instrument)
        attune.store(self._instrument)
        self.shutdown(restart=True)

    def get_arrangement(self):
        return self._state["arrangement"]

    def set_arrangement(self, arrangement):
        self._state["arrangement"] = arrangement

    def get_all_arrangements(self):
        return list(self._instrument.arrangements.keys())

    def get_setable_yaq_params(self):
        return self._config["setables"]

    def get_setable_names(self):
        return list(self._setables.keys())

    def set_setable_positions(self, setables):
        for name, set_pos in setables.items():
            self._setables[name].set_position(set_pos)

    def get_setable_positions(self):
        return {k: v.get_position() for k, v in self._setables.items()}

    def home_setables(self, setables):
        for name in setables:
            if hasattr(self._setables[name], "home"):
                self._setables[name].home()

    def home(self):
        self.home_setables(self._setables.keys())

    async def update_state(self):
        """Continually monitor and update the current daemon state."""
        while True:
            self._busy = any([sa.busy() for sa in self._setables.values()])
            if self._busy:
                await asyncio.sleep(0.1)
            else:
                await self._busy_sig.wait()
