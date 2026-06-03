import time
import logging
from django.utils.deprecation import MiddlewareMixin

# Initialize a standard Python logger targeting a local file
logger = logging.getLogger('django.request_metrics')

class RequestMetricsLoggerMiddleware:
    """
    Custom Django Middleware to log request analytics:
    Execution Time, Client IP address, and User-Agent.
    """
    
    def __init__(self, get_response):
        # One-time configuration and initialization
        self.get_response = get_response

    def __call__(self, request):
        # 1. PRE-PROCESSING: Code executed before the view is called
        start_time = time.perf_counter()

        # 2. PASS-THROUGH: Hand off request to the next middleware/view
        response = self.get_response(request)

        # 3. POST-PROCESSING: Code executed on the response outbound path
        duration = time.perf_counter() - start_time

        # Capture Client IP Address (Handles direct connections or reverse proxies like Nginx)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')

        # Capture Browser/Client User Agent
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown-Agent')
        path = request.path
        method = request.method
        status_code = response.status_code

        # Format our structural log entry
        log_message = (
            f"METHOD: {method} | PATH: {path} | STATUS: {status_code} | "
            f"DURATION: {duration:.4f}s | IP: {ip} | USER_AGENT: {user_agent}"
        )

        # Write out to our dedicated metrics log file
        logger.info(log_message)

        return response