import ntplib
import datetime

from datetime import datetime, timezone
from __init__ import logger


class Timer:
    def __init__(self):
        self.ntp_server = 'pool.ntp.org'
        self.client = ntplib.NTPClient()

    def get_current_time_h_m_s(self):
        """
        Retrieves the current time in 'HH:MM:SS' format from the NTP server.

        Returns:
            str: The current time in 'HH:MM:SS' format if successful; otherwise, None.

        Logs:
            - Success: Logs the retrieved time.
            - TimeoutError or ConnectionError: Logs an error if unable to reach the server.
            - Exception: Logs any unexpected errors that may occur.
        """
        try:
            c = ntplib.NTPClient()
            response = c.request('pool.ntp.org')
            time_object = datetime.fromtimestamp(response.tx_time, timezone.utc)
            current_time = time_object.strftime("%H:%M:%S")
            logger.info("Successfully requested current time from the ntp server.")
            return current_time
        except TimeoutError or ConnectionError:
            logger.error("Connection or Timeout error occurred while trying to reach the NTP server.")
        except Exception as e:
            logger.critical("An unexpected error occurred: %s", e)

    def get_current_time_y_m_d(self):
        """
        Retrieves the current date in 'YYYY-MM-DD' format from the NTP server.

        Returns:
            str: The current date in 'YYYY-MM-DD' format if successful; otherwise, None.

        Logs:
            - Success: Logs the retrieved date.
            - TimeoutError or ConnectionError: Logs an error if unable to reach the server.
            - Exception: Logs any unexpected errors that may occur.
        """
        try:
            c = ntplib.NTPClient()
            response = c.request('pool.ntp.org')
            time_object = datetime.fromtimestamp(response.tx_time, timezone.utc)
            current_time = time_object.strftime("%Y-%m-%d")
            logger.info("Successfully requested current time from the ntp server.")
            return current_time
        except TimeoutError or ConnectionError:
            logger.error("Connection or Timeout error occurred while trying to reach the NTP server.")
        except Exception as e:
            logger.critical("An unexpected error occurred: %s", e)
