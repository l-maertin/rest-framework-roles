import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.test import TestCase  # needed for override_settings to work

from ..roles import is_admin, is_user, is_anon
from ..permissions import is_self
from ..patching import is_django_configured
from .fixtures import admin, user, anon
from .utils import assert_allowed, assert_disallowed, BaseUserViewSet


# -------------------------------- Recipe --------------------------------------


from rest_framework import routers
import rest_framework as drf
from django.contrib.auth.models import User
from django.urls import path, include


roles = {
    'admin': is_admin,
    'user': is_user,
    'anon': is_anon,
}
permissions = [{
  'view': 'rest_framework_roles.tests.test_permissions.UserViewSet',
  'permissions': {
    'user': {
        'retrieve': is_self,
    },
    'anon': {
        'create': True,
    },
    'admin': {
        'list': True,
    },
  }
}]

class UserViewSet(BaseUserViewSet):
    view_permissions = {}

router = drf.routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = [
    path('', include(router.urls)),
]


# ------------------------------------------------------------------------------


def test_view_permissions_can_be_applied_directl_at_view():
    pass


def test_view_permissions_can_be_applied_at_settings():
    pass


@pytest.mark.urls(__name__)
class TestUserAPI():

    def test_only_admin_can_list_users(self, user, anon, admin):
        assert_allowed(admin, get='/users/')
        assert_disallowed(user, get='/users/')
        assert_disallowed(anon, get='/users/')

    def test_user_can_retrieve_only_self(self, user, anon, admin):
        other_user = User.objects.create(username='mrother')
        other_user_url = f'/users/{other_user.id}/'
        all_users_url = '/users/'
        assert_allowed(admin, get=other_user_url)
        assert_disallowed(user, get=other_user_url)
        assert_disallowed(anon, get=other_user_url)
        assert_allowed(admin, get=f'/users/{admin.id}/')
        assert_allowed(user, get=f'/users/{user.id}/')


def test_view_redirectios_dont_omit_checks():
    pass