import time
from rest_framework.throttling import BaseThrottle

# Simple in-memory throttle (It will reset upon server restart)
VISIT_RECORD = {}

class SimpleIPThrottle(BaseThrottle):
    """
    Allows a maximum of `max_requests` per `duration` seconds per IP.
    """
    max_requests = 10
    duration = 180  # seconds (3 minutes)

    def allow_request(self, request, view):
        ip = self.get_ident(request)
        now = time.time()
        history = VISIT_RECORD.get(ip, [])

        # Remove old requests outside the duration window
        history = [timestamp for timestamp in history if now - timestamp < self.duration]

        if len(history) >= self.max_requests:
            return False  # Block request

        # Record this request
        history.append(now)
        VISIT_RECORD[ip] = history
        return True

    def wait(self):
        """Optional: return number of seconds until next request is allowed"""
        return self.duration
