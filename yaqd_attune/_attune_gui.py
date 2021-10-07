from qtpy import QtWidgets, QtCore  # type: ignore

import yaqc_qtpy  # type: ignore


class AttuneGUI(QtWidgets.QWidget):

    def __init__(self, client: yaqc_qtpy.QClient):
        super().__init__()
        self._create_main_frame()

    def _create_main_frame(self):
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel("this widget provided by yaqd-attune"))
        self.setLayout(hbox)
