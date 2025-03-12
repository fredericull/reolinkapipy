from typing import Dict


class ZoomAPIMixin:
    """
    API for zooming and changing focus.
    Note that the API does not allow zooming/focusing by absolute
    values rather that changing focus/zoom for a given time.
    """
    def _start_operation(self, operation: str, speed: float, channel: int = 0) -> Dict:
        data = [{"cmd": "PtzCtrl", "action": 0, "param": {"channel": channel, "op": operation, "speed": speed}}]
        return self._execute_command('PtzCtrl', data)

    def _stop_zooming_or_focusing(self, channel: int = 0) -> Dict:
        """This command stops any ongoing zooming or focusing actions."""
        data = [{"cmd": "PtzCtrl", "action": 0, "param": {"channel": channel, "op": "Stop"}}]
        return self._execute_command('PtzCtrl', data)

    def get_zoom_focus(self, channel: int = 0) -> Dict:
        """This command returns the current zoom and focus values."""
        data = [{"cmd": "GetZoomFocus", "action": 0, "param": {"channel": channel}}]
        return self._execute_command('GetZoomFocus', data)

    def start_zoom_pos(self, position: float, channel: int = 0) -> Dict:
        """This command sets the zoom position."""
        data = [{"cmd": "StartZoomFocus", "action": 0, "param": {"ZoomFocus": {"channel": channel, "op": "ZoomPos", "pos": position}}}]
        return self._execute_command('StartZoomFocus', data)

    def start_focus_pos(self, position: float, channel: int = 0) -> Dict:
        """This command sets the focus position."""
        data = [{"cmd": "StartZoomFocus", "action": 0, "param": {"ZoomFocus": {"channel": channel, "op": "FocusPos", "pos": position}}}]
        return self._execute_command('StartZoomFocus', data)

    def get_auto_focus(self, channel: int = 0) -> Dict:
        """This command returns the current auto focus status."""
        data = [{"cmd": "GetAutoFocus", "action": 0, "param": {"channel": channel}}]
        return self._execute_command('GetAutoFocus', data)
    
    def set_auto_focus(self, disable: bool, channel: int = 0) -> Dict:
        """This command sets the auto focus status."""
        data = [{"cmd": "SetAutoFocus", "action": 0, "param": {"AutoFocus": {"channel": channel, "disable": 1 if disable else 0}}}]
        return self._execute_command('SetAutoFocus', data)

    def start_zooming_in(self, speed: float = 60, channel: int = 0) -> Dict:
        """
        The camera zooms in until self.stop_zooming() is called.
        :param channel: channel id
        :return: response json
        """
        return self._start_operation('ZoomInc', speed=speed, channel=channel)

    def start_zooming_out(self, speed: float = 60, channel: int = 0) -> Dict:
        """
        The camera zooms out until self.stop_zooming() is called.
        :param channel: channel id
        :return: response json
        """
        return self._start_operation('ZoomDec', speed=speed, channel=channel)

    def stop_zooming(self, channel: int = 0) -> Dict:
        """
        Stop zooming.
        :param channel: channel id
        :return: response json
        """
        return self._stop_zooming_or_focusing(channel=channel)

    def start_focusing_in(self, speed: float = 32, channel: int = 0) -> Dict:
        """
        The camera focuses in until self.stop_focusing() is called.
        :param channel: channel id
        :return: response json
        """
        return self._start_operation('FocusInc', speed=speed, channel=channel)

    def start_focusing_out(self, speed: float = 32, channel: int = 0) -> Dict:
        """
        The camera focuses out until self.stop_focusing() is called.
        :param channel: channel id
        :return: response json
        """
        return self._start_operation('FocusDec', speed=speed, channel=channel)

    def stop_focusing(self, channel: int = 0) -> Dict:
        """
        Stop focusing.
        :param channel: channel id
        :return: response json
        """
        return self._stop_zooming_or_focusing(channel=channel)
