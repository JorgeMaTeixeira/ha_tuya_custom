import time

from .base import TuyaDevice


class TuyaSwitch(TuyaDevice):
    def state(self):
        state = self.data.get("state")
        if state is None:
            return None
        return state

    def turn_on(self):
        self.api.device_control(self.obj_id, "turnOnOff", {"value": "1"})
        if self.data:
            self.data["state"] = True
            self.api.update_device_data(self.obj_id, self.data)

    def turn_off(self):
        self.api.device_control(self.obj_id, "turnOnOff", {"value": "0"})
        if self.data:
            self.data["state"] = False
            self.api.update_device_data(self.obj_id, self.data)

    # workaround for https://github.com/PaulAnnekov/tuyaha/issues/3
    def update(self):
        """Avoid get cache value after control."""
        time.sleep(0.5)
        devices = self.api.discovery()
        if not devices:
            return
        for device in devices:
            if device["id"] == self.obj_id:
                self.data = device["data"]
                return True
