from typing import Dict


class AlarmAPIMixin:
    """API calls for getting device alarm information."""

    def get_alarm_motion(self, channel: int = 0) -> Dict:
        """
        Gets the device alarm motion
        See examples/response/GetAlarmMotion.json for example response data.
        :param channel: channel id
        :return: response json
        """
        body = [{"cmd": "GetAlarm", "action": 1, "param": {"Alarm": {"channel": channel, "type": "md"}}}]
        return self._execute_command('GetAlarm', body)
