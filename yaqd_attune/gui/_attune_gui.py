from qtpy import QtWidgets, QtCore  # type: ignore
import qtypes

import yaqc_qtpy  # type: ignore
from yaqc_qtpy import _plot  # noqa
import WrightTools as wt
import attune


class AttuneGUI(QtWidgets.QWidget):
    def __init__(self, qclient: yaqc_qtpy.QClient):
        super().__init__()
        self.units = "nm"  # TODO synchronous getter calls at startup?
        self.plot_widget = yaqc_qtpy._plot.Plot1D()
        self.plot_v_line = self.plot_widget.add_infinite_line(angle=90, hide=False)
        self.arrangement_enum = qtypes.Enum()
        self.tune_enum = qtypes.Enum()
        allowed_values = ["wn"] + list(wt.units.get_valid_conversions("wn"))
        self.plot_units = qtypes.Enum(initial_value=self.units, allowed_values=allowed_values)
        self.low_energy_limit_display = qtypes.Number(units=self.units, display=True)
        self.high_energy_limit_display = qtypes.Number(units=self.units, display=True)
        self.qclient = qclient
        self.qclient.get_instrument.finished.connect(self.on_get_instrument)
        self.qclient.get_instrument()
        self.qclient.get_limits.finished.connect(self.on_get_limits)
        self.qclient.get_position.finished.connect(self.on_get_position)
        self.qclient.get_limits()
        self._create_main_frame()

    def _create_main_frame(self):
        hbox = QtWidgets.QHBoxLayout()
        self.setLayout(hbox)
        # container widget
        display_container_widget = QtWidgets.QWidget()
        display_container_widget.setLayout(QtWidgets.QVBoxLayout())
        display_layout = display_container_widget.layout()
        display_layout.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(display_container_widget)
        # plot
        self.plot_widget.plot_object.setMouseEnabled(False, False)
        self.plot_curve = self.plot_widget.add_scatter()
        # self.plot_h_line = self.plot_widget.add_infinite_line(angle=0, hide=False)
        display_layout.addWidget(self.plot_widget)
        # vertical line
        line = qtypes.widgets.Line("V")
        hbox.addWidget(line)
        # container widget / scroll area
        settings_container_widget = QtWidgets.QWidget()
        settings_scroll_area = qtypes.widgets.ScrollArea()
        settings_scroll_area.setWidget(settings_container_widget)
        settings_scroll_area.setMinimumWidth(500)
        settings_scroll_area.setMaximumWidth(500)
        settings_container_widget.setLayout(QtWidgets.QVBoxLayout())
        settings_layout = settings_container_widget.layout()
        settings_layout.setContentsMargins(5, 5, 5, 5)

        hbox.addWidget(settings_scroll_area)
        # opa properties
        input_table = qtypes.widgets.InputTable()
        settings_layout.addWidget(input_table)
        # plot control
        input_table = qtypes.widgets.InputTable()
        input_table.append(None, "Display")
        self.tune_enum.updated.connect(self.update_plot)
        input_table.append(self.tune_enum, "Tune")
        self.plot_units.updated.connect(self.update_plot)
        input_table.append(self.plot_units, "Units")
        settings_layout.addWidget(input_table)
        # curves
        input_table = qtypes.widgets.InputTable()
        # input_table.append(None, "Curves")
        self.arrangement_enum.updated.connect(self.on_arrangement_updated)
        input_table.append(self.arrangement_enum, "Arrangement")
        # limits
        input_table.append(self.low_energy_limit_display, "Low Limit")
        input_table.append(self.high_energy_limit_display, "High Limit")
        settings_layout.addWidget(input_table)
        self.home_all_button = qtypes.widgets.PushButton("HOME ALL")
        settings_layout.addWidget(self.home_all_button)
        self.home_all_button.clicked.connect(self.on_home_all)
        # stretch
        settings_layout.addStretch(1)
        # finish
        self.update()
        self.update_plot()

    def update_plot(self):
        if not hasattr(self, "instrument"):
            return
        arr = self.arrangement_enum.get()
        motor_name = self.tune_enum.get()
        tune = self.instrument.arrangements[arr][motor_name]
        if not isinstance(tune, attune.Tune):
            return
        # units
        units = self.plot_units.get()
        # xi
        colors = tune.independent
        xi = wt.units.converter(colors, tune.ind_units, units)
        # yi
        yi = tune.dependent
        self.plot_widget.set_labels(xlabel=units, ylabel=motor_name)
        self.plot_curve.clear()
        try:
            self.plot_curve.setData(xi, yi)
        except ValueError:
            pass
        self.plot_widget.graphics_layout.update()
        self.update()

    def on_get_instrument(self, json):
        self.instrument = attune.Instrument(**json)
        self.arrangement_enum.set_allowed_values(self.instrument.arrangements.keys())
        self.tune_enum.set_allowed_values(self.instrument[self.arrangement_enum.get()].keys())
        self.update_plot()

    def on_home_all(self):
        self.qclient.home()

    def on_get_limits(self, limits):
        low_energy_limit, high_energy_limit = limits
        self.low_energy_limit_display.set(low_energy_limit, self.units)
        self.high_energy_limit_display.set(high_energy_limit, self.units)

    def on_arrangement_updated(self):
        arr = self.arrangement_enum.get()
        self.qclient.set_arrangement(arr)
        self.qclient.get_limits()
        self.tune_enum.set_allowed_values(self.instrument[arr].keys())
        self.update_plot()

    def on_get_position(self, pos):
        self.plot_v_line.setValue(wt.units.convert(pos, self.units, self.plot_units.get()))
