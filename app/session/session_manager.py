import time
import uuid


class SessionManager:

    def __init__(self):

        self.session_id = str(
            uuid.uuid4()
        )[:8]

        self.start_time = (
            time.time()
        )

        self.query_count = 0

    def increment_queries(self):

        self.query_count += 1

    def uptime(self):

        return round(
            time.time()
            - self.start_time,
            2,
        )

    def get_info(self):

        return {

            "session_id": self.session_id,

            "queries": self.query_count,

            "uptime_seconds": self.uptime(),

        }