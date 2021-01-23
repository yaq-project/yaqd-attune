__all__ = ["Attune"]

import asyncio
from typing import Dict, Any, List

import attune  # type: ignore
import yaqc  # type: ignore
from yaqd_core import HasLimits, IsHomeable, HasPosition, IsDaemon


class Attune(HasLimits, IsHomeable, HasPosition, IsDaemon):
    _kind = "attune"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._instrument = attune.load(name)
        self._setables = {k: yaqc.Client(v) for k, v in config["setables"].items()}
        self._set_limits()

    def _set_position(self, position):
        self.set_position_except(position)

    def set_position_except(self, position, exceptions=None):
        self._busy = True
        self._state["destination"] = position
        self._state["position"] = position
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
        self._busy = True
        self._instrument = attune.Instrument(**instrument)
        attune.store(self._instrument)
        self.shutdown(restart=True)

    def get_arrangement(self):
        return self._state["arrangement"]

    def set_arrangement(self, arrangement):
        if arrangement is not None and arrangement not in self._instrument.arrangements.keys():
            raise ValueError("Arrangement not found")
        self._busy = True
        self._state["arrangement"] = arrangement
        self._set_limits()

    def get_all_arrangements(self):
        return list(self._instrument.arrangements.keys())

    def get_setable_yaq_params(self):
        return self._config["setables"]

    def get_setable_names(self):
        return list(self._setables.keys())

    def set_setable_positions(self, setables):
        self._busy = True
        for name, set_pos in setables.items():
            self._setables[name].set_position(set_pos)

    def get_setable_positions(self):
        return {k: v.get_position() for k, v in self._setables.items()}

    def home_setables(self, setables):
        self._busy = True
        for name in setables:
            if hasattr(self._setables[name], "home"):
                self._setables[name].home()

    def home(self):
        self._busy = True
        self.home_setables(self._setables.keys())

    def _set_limits(self):
        if self._state["arrangement"] is None:
            min_ = min(x.ind_min for x in self._instrument.arrangements.values())
            max_ = max(x.ind_max for x in self._instrument.arrangements.values())
            self._state["hw_limits"] = (min_, max_)
        else:
            self._state["hw_limits"] = (
                float(self._instrument.arrangements[self._state["arrangement"]].ind_min),
                float(self._instrument.arrangements[self._state["arrangement"]].ind_max),
            )

    async def update_state(self):
        """Continually monitor and update the current daemon state."""
        while True:
            self._busy = any(sa.busy() for sa in self._setables.values())
            if self._busy:
                await asyncio.sleep(0.1)
            else:
                await self._busy_sig.wait()
