from typing import Dict


class PtzAPIMixin:
    """
    API for PTZ functions.
    """
    def get_ptz_check_state(self, channel: int = 0) -> Dict:
        """
        Get PTZ Check State Information that indicates whether calibration is required (0) running (1) or done (2)
        Value is contained in response[0]["value"]["PtzCheckState"].
        See examples/response/GetPtzCheckState.json for example response data.
        :param channel: channel id
        :return: response json
        """
        body = [{"cmd": "GetPtzCheckState", "action": 1, "param": { "channel": channel}}]
        return self._execute_command('GetPtzCheckState', body)

    def get_ptz_presets(self, channel: int = 0) -> Dict:
        """
        Get ptz presets
        See examples/response/GetPtzPresets.json for example response data.
        :param channel: channel id
        :return: response json
        """

        body = [{"cmd": "GetPtzPreset", "action": 1, "param": { "channel": channel}}]
        return self._execute_command('GetPtzPreset', body)

    def perform_calibration(self, channel: int = 0) -> Dict:
        """
        Do the calibration (like app -> ptz -> three dots -> calibration). Moves camera to all end positions.
        If not calibrated, your viewpoint of presets might drift. So before setting new presets, or moving to preset,
        check calibration status (get_ptz_check_state -> 2 = calibrated) and perform calibration if not yet calibrated.
        As of 2024-01-23 (most recent firmware 3.1.0.1711_23010700 for E1 Zoom) does not do this on startup.
        Method blocks while calibrating.
        See examples/response/PtzCheck.json for example response data.
        :param channel: channel id
        :return: response json
        """
        data = [{"cmd": "PtzCheck", "action": 0, "param": {"channel": channel}}]
        return self._execute_command('PtzCheck', data)

    def _send_operation(self, operation: str, speed: float, index: float = None, channel: int = 0) -> Dict:
        # Refactored to reduce redundancy
        param = {"channel": channel, "op": operation, "speed": speed}
        if index is not None:
            param['id'] = index
        data = [{"cmd": "PtzCtrl", "action": 0, "param": param}]
        return self._execute_command('PtzCtrl', data)

    def _send_noparm_operation(self, operation: str, channel: int = 0) -> Dict:
        data = [{"cmd": "PtzCtrl", "action": 0, "param": {"channel": channel, "op": operation}}]
        return self._execute_command('PtzCtrl', data)

    def _send_set_preset(self, enable: float, preset: float = 1, name: str = 'pos1', channel: int = 0) -> Dict:
        data = [{"cmd": "SetPtzPreset", "action": 0, "param": { "PtzPreset": {
            "channel": channel, "enable": enable, "id": preset, "name": name}}}]
        return self._execute_command('PtzCtrl', data)

    def go_to_preset(self, speed: float = 60, index: float = 1, channel: int = 0) -> Dict:
        """
        Move the camera to a preset location
        :param channel: channel id
        :return: response json
        """
        return self._send_operation('ToPos', speed=speed, index=index, channel=channel)

    def add_preset(self, preset: float = 1, name: str = 'pos1', channel: int = 0) -> Dict:
        """
        Adds the current camera position to the specified preset.
        :param channel: channel id
        :return: response json
        """
        return self._send_set_preset(enable=1, preset=preset, name=name, channel=channel)

    def remove_preset(self, preset: float = 1, name: str = 'pos1', channel: int = 0) -> Dict:
        """
        Removes the specified preset
        :param channel: channel id
        :return: response json
        """
        return self._send_set_preset(enable=0, preset=preset, name=name, channel=channel)

    def move_right(self, speed: float = 25, channel: int = 0) -> Dict:
        """
        Move the camera to the right
        The camera moves self.stop_ptz() is called.
        :param channel: channel id
        :return: response json
        """
        return self._send_operation('Right', speed=speed, channel=channel)

    def move_right_up(self, speed: float = 25, channel: int = 0) -> Dict:
        """
        Move the camera to the right and up
        The camera moves self.stop_ptz() is called.
        :param channel: channel id
        :return: response json
        """
        return self._send_operation('RightUp', speed=speed, channel=channel)

    def move_right_down(self, speed: float = 25, channel: int = 0) -> Dict:
        """
        Move the camera to the right and down
        The camera moves self.stop_ptz() is called.
        :param channel: channel id
        :return: response json
        """
        return self._send_operation('RightDown', speed=speed, channel=channel)

    def move_left(self, speed: float = 25, channel: int = 0) -> Dict:
        """
        Move the camera to the left
        The camera moves self.stop_ptz() is called.
        :param channel: channel id
        :return: response json
        """
        return self._send_operation('Left', speed=speed, channel=channel)

    def move_left_up(self, speed: float = 25, channel: int = 0) -> Dict:
        """
        Move the camera to the left and up
        The camera moves self.stop_ptz() is called.
        :param channel: channel id
        :return: response json
        """
        return self._send_operation('LeftUp', speed=speed, channel=channel)

    def move_left_down(self, speed: float = 25, channel: int = 0) -> Dict:
        """
        Move the camera to the left and down
        The camera moves self.stop_ptz() is called.
        :param channel: channel id
        :return: response json
        """
        return self._send_operation('LeftDown', speed=speed, channel=channel)

    def move_up(self, speed: float = 25, channel: int = 0) -> Dict:
        """
        Move the camera up.
        The camera moves self.stop_ptz() is called.
        :param channel: channel id
        :return: response json
        """
        return self._send_operation('Up', speed=speed, channel=channel)

    def move_down(self, speed: float = 25, channel: int = 0) -> Dict:
        """
        Move the camera down.
        The camera moves self.stop_ptz() is called.
        :param channel: channel id
        :return: response json
        """
        return self._send_operation('Down', channel=channel, speed=speed)

    def stop_ptz(self, channel: int = 0) -> Dict:
        """
        Stops the cameras current action.
        :param channel: channel id
        :return: response json
        """
        return self._send_noparm_operation('Stop', channel=channel)

    def auto_movement(self, speed: float = 25, channel: int = 0) -> Dict:
        """
        Move the camera in a clockwise rotation.
        The camera moves self.stop_ptz() is called.
        :param channel: channel id
        :return: response json
        """
        return self._send_operation('Auto', speed=speed, channel=channel)
