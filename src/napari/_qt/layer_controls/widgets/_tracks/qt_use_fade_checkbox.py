from qtpy.QtWidgets import (
    QCheckBox,
    QWidget,
)

from napari._qt.layer_controls.widgets.qt_widget_controls_base import (
    QtWidgetControlsBase,
    QtWrappedLabel,
)
from napari.layers import Tracks
from napari.utils.translations import trans


class QtUseFadeCheckBoxControl(QtWidgetControlsBase):
    """
    Class that wraps the connection of events/signals between the use_fade
    attribute and Qt widgets.

    Parameters
    ----------
    parent: qtpy.QtWidgets.QWidget
        An instance of QWidget that will be used as widgets parent
    layer : napari.layers.Tracks
        An instance of a napari Tracks layer.

    Attributes
    ----------
    use_fade_checkbox : qtpy.QtWidgets.QCheckBox
        Checkbox controlling if tracks should fade over time.
    use_fade_checkbox_label : napari._qt.layer_controls.widgets.qt_widget_controls_base.QtWrappedLabel
        Label for showing the use_fade chooser widget.
    """

    def __init__(self, parent: QWidget, layer: Tracks) -> None:
        super().__init__(parent, layer)
        # Setup layer
        self._layer.events.use_fade.connect(self._on_use_fade_change)

        # Setup widgets
        self.use_fade_checkbox = QCheckBox()
        self.use_fade_checkbox.setChecked(self._layer._use_fade)
        self.use_fade_checkbox.setToolTip(
            trans._('Enable fading of track tails over time')
        )
        self.use_fade_checkbox.stateChanged.connect(self.change_use_fade)

        self.use_fade_checkbox_label = QtWrappedLabel(trans._('fade tracks:'))

    def change_use_fade(self, state) -> None:
        """Change the use_fade state of the layer.

        Parameters
        ----------
        state : int
            Integer value of Qt.CheckState that indicates the check state of use_fade_checkbox
        """
        self._layer.use_fade = self.use_fade_checkbox.isChecked()

    def _on_use_fade_change(self) -> None:
        """Update the checkbox when the layer's use_fade changes."""
        with self._layer.events.use_fade.blocker():
            self.use_fade_checkbox.setChecked(self._layer._use_fade)

    def get_widget_controls(self) -> list[tuple[QtWrappedLabel, QWidget]]:
        return [(self.use_fade_checkbox_label, self.use_fade_checkbox)]