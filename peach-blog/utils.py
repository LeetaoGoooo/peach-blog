"""
utils for peach blog
"""

import hashlib
import time
import datetime
import re


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

        @app.template_global("escape_html")
        def escape_html(html):
            '''
             将非字母或者非数字的字符替换为空格
             然后将空格替换为-
            '''
            html = re.sub("[^[\w]|[\u4e00-\u9fa5_a-zA-Z0-9]+]", " ", html)
            html = re.sub("\s+", "-", html)
            return html
