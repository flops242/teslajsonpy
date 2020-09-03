#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
from typing import Dict, Optional, Text

from teslajsonpy.const import RELEASE_NOTES_URL
from teslajsonpy.homeassistant.vehicle import VehicleDevice


class ShiftState(VehicleDevice):
    """Home-Assistant class of the shift state for a Tesla VehicleDevice."""

    def __init__(self, data: Dict, controller) -> None:
        """Initialize the Shift state sensor.

        Parameters
        ----------
        data : dict
            The charging parameters for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/chargestate
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.__shift_state = None
        self.type = "shiftstate sensor"
        self.measurement = None
        self.hass_type = "sensor"
        self._device_class: Optional[Text] = None
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 0xA

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the shift state."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        data = self._controller.get_drive_params(self._id)
        if data:
            self.__shift_state = (
                data["shift_state"] if data["shift_state"] else "P"
            )

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False

    def get_value(self):
        """Return the shift state."""
        return self.__shift_state

    @property
    def device_class(self) -> Text:
        """Return the HA device class."""
        return self._device_class

