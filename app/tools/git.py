"""
 github helpers for peach-blog
 auto push files to github repo
"""
from github import Github

class GitHelper:

    __slots__ = ['user_name', 'password', 'access_token', 'logger', 'repo', 'repo_name' , 'git_config']
    
    def __init__(self, app = None):

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        
        self.user_name = app.config['USER_NAME'] or None
        self.password = app.config['PASSWORD'] or None
        self.access_token = app.config['ACCESS_TOKEN'] or None
        self.repo_name = app.config['GIT_REPO_NAME'] or None

        self.logger = app.logger

        if self.user_name and self.password:
            self.git_config = 'account'
        elif self.access_token:
            self.git_config = 'token'
        else:
            self.git_config = False
            self.logger.warning("git config was not set, peach-blog will not push files to github repo !")

        if self.git_config:
            self.init_repo()

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['git_helper'] = self

    def init_repo(self):
        if self.git_config == 'account':
            github = Github(self.user_name,self.password)
        else:
            github = Github(self.access_token)
        self.repo = github.get_user().get_repo(self.repo_name)