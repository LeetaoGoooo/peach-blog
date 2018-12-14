"""
utils for peach blog
"""

import hashlib
import time
import datetime

class Tools:

    @staticmethod
    def init_app(app):
        @app.template_global('md5')
        def md5(email):
            return hashlib.md5(email.encode('utf-8')).hexdigest()
        
        @app.template_global("total_views")
        def total_views(postviews):
            total_views = 0
            for postview in postviews:
                total_views += postview.views
            return total_views

