# middleware.py
import logging

class AdminActivityMiddleware:
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path.startswith('/admin/'):
            # Log user activity here
            logging.info(f"User {request.user} accessed {request.path}")

