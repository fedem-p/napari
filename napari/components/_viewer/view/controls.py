from qtpy.QtWidgets import QHBoxLayout, QStackedWidget, QWidget
from qtpy.QtCore import QSize


class QtControls(QStackedWidget):
    def __init__(self, viewer):
        super().__init__()

        self.viewer = viewer

        self.setMouseTracking(True)
        self.setMinimumSize(QSize(40, 40))
        self.empty_widget = QWidget()
        self.addWidget(self.empty_widget)
        self._display(None)

        self.viewer.layers.events.added.connect(self._add)
        self.viewer.layers.events.removed.connect(self._remove)
        self.viewer.events.active_layer.connect(self._display)

    def _display(self, event):
        """Change the displayed controls to be those of the target layer.

        Parameters
        ----------
        event : Event
            Event with the target layer at `event.item`.
        """
        if event is None:
            layer = None
        else:
            layer = event.item

        if layer is None or layer._qt_controls is None:
            self.setCurrentWidget(self.empty_widget)
        else:
            self.setCurrentWidget(layer._qt_controls)

    def _add(self, event):
        """Add the controls target layer to the list of control widgets.

        Parameters
        ----------
        event : Event
            Event with the target layer at `event.item`.
        """
        layer = event.item
        if layer._qt_controls is not None:
            self.addWidget(layer._qt_controls)

    def _remove(self, event):
        """Remove the controls target layer from the list of control widgets.

        Parameters
        ----------
        event : Event
            Event with the target layer at `event.item`.
        """
        layer = event.item
        if layer._qt_controls is not None:
            self.removeWidget(layer._qt_controls)
            layer._qt_controls.deleteLater()
            layer._qt_controls = None