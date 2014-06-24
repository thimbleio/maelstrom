from flask import session
from uuid import uuid4
from base import Base
from db_utils import get_time


class Account(Base):
    defaults = {
        'id': uuid4(),
        'follower_count': 0,
        'following_count': 0,
        'stars_count': 0,
        'school_id': uuid4(),
        'login_count': 0,
        'permission': 0,
        'state': 0,
        'email_authorized': False,
        'account_suspended': False,
        'email': '',
        'password_hash': '',
        'password_salt': '',
        'current_login_ip': '',
        'last_login_ip': '',
        'school': '',
        'username': '',
        'name': '',
        'major': '',
        'grade': '',
        'city_name': '',
        'state_name': '',
        'bio_text': '',
        'avatar_url': '',
        'following_url': '',
        'follower_url': '',
        'last_login_at': get_time(),
        'updated_at': get_time(),
        'created_at': get_time(),
        'birthday': get_time(),
        'trophies': [uuid4()],
        'organizations': [uuid4()],
        'comments': [uuid4()],
        'likes': [uuid4()],
        'tags': [uuid4()],
        'subscribed': [uuid4()],
        'subscribers': [uuid4()],
        'following_projects': [uuid4()],
        'projects': [uuid4()]
    }

    lookups = ['username', 'email']
    search_terms = ['username', 'name', 'email']

    __tablename__ = 'users'

    def __init__(self, *args, **kwargs):
        self.update_data(**self.defaults)
        Base.__init__(self, *args, **kwargs)

    def is_authenticated(self):
        return self.email_authorized

    def is_active(self):
        return not self.account_suspended

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @property
    def trophy_count(self):
        return len(self.trophies)

    @property
    def following_count(self):
        return len(self.subscribed)

    @property
    def followers_count(self):
        return len(self.subscribers)

    def get_id(self):
        return self.id

    # TODO
    def is_following_user(self, account_id):
        return account_id in self.subscribed

    # TODO
    def is_subscribed_project(self, project_id):
        return project_id in self.following_projects

    # TODO
    def Projects(self):
        from gf.models.project import Project

        projects = Project.multi_get_by_id(self.projects)
        project_list = []
        for project in projects:
            project_list.append(project)
        return project_list
