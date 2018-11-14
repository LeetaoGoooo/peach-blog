import pytest
from app import create_app

app = create_app('testing')

def test_get_post_content_without_meta():
    with open('tests/test.md','r',encoding='utf-8') as f:
        test_content = f.read()
        content = app.extensions['hexo'].get_post_content_without_meta(test_content)
        assert content is not None