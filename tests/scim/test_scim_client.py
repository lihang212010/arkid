'''
test scim client sync
'''
from unittest import mock
from django.test import TestCase

from tenant.models import Tenant
from inventory.models import Group, User
from app.models import App
from provisioning.models import Config
from provisioning.constants import ProvisioningStatus, ProvisioningType, AuthenticationType


class UserTestCase(TestCase):
    '''
    test user
    '''
    def setUp(self):    # pylint: disable=invalid-name, missing-function-docstring
        # create tenant
        self.tenant = Tenant.objects.create(name='first tenant')

        # create app
        self.app = App.objects.create(
            tenant=self.tenant,
            name='First App',
            type='App',
            url='http://test.com',
            description='Test App',
        )

        # create config
        self.config = Config.objects.create(
            app=self.app,
            sync_type=ProvisioningType.downstream.value,
            auth_type=AuthenticationType.token.value,
            base_url='http://test.com/auth',
            token='token',
            status=ProvisioningStatus.Enabled.value,
        )

    @mock.patch('tasks.tasks.provision_user')
    def test_provision_user(self, provision_user):
        """
        Test django model signal
        """
        # create user
        ford = User.objects.create(
            first_name='Robert',
            last_name='Ford',
            username='rford',
            email='rford@ww.com',
        )

        ford.tenants.add(self.tenant)

        ford.save()

        provision_user.assert_called_with(self.tenant.uuid, ford.id)

    @mock.patch('tasks.tasks.provision_app_user')
    def test_provision_app_user(self, provision_app_user):
        """
        Test provision app user
        """
        # create user
        ford = User.objects.create(
            first_name='Robert',
            last_name='Ford',
            username='rford',
            email='rford@ww.com',
        )

        ford.tenants.add(self.tenant)

        ford.save()

        provision_app_user.assert_called_with(self.tenant.uuid, self.app.id, self.config.id, ford.id)

    @mock.patch('tasks.tasks.deprovision_app_user')
    def test_deprovision_app_user(self, deprovision_app_user):
        """
        Test deprovision app user
        """
        # create user
        ford = User.objects.create(
            first_name='Robert',
            last_name='Ford',
            username='rford',
            email='rford@ww.com',
        )

        ford.tenants.add(self.tenant)

        # ford.save()

        User.objects.filter(username='rford').delete()

        deprovision_app_user.assert_called_with(self.tenant.uuid, self.app.id, self.config.id, ford.id)

    @mock.patch('tasks.tasks.create_user')
    @mock.patch('tasks.tasks.user_exists')
    def test_create_user(self, user_exists, create_user):
        """
        Test create user
        """
        # patch where the func is used not imported
        # doc: https://docs.python.org/3/library/unittest.mock.html#where-to-patch
        user_exists.return_value = (False, None)

        # create user
        ford = User.objects.create(
            first_name='Robert',
            last_name='Ford',
            username='rford',
            email='rford@ww.com',
        )

        ford.tenants.add(self.tenant)

        ford.save()

        create_user.assert_called()

    @mock.patch('tasks.tasks.update_user')
    @mock.patch('tasks.tasks.user_exists')
    def test_update_user(self, user_exists, update_user):
        """
        Test update user
        """
        user_exists.return_value = (True, '1234')

        # create user
        ford = User.objects.create(
            first_name='Robert',
            last_name='Ford',
            username='rford',
            email='rford@ww.com',
        )

        ford.tenants.add(self.tenant)

        ford.save()

        update_user.assert_called()

    @mock.patch('tasks.tasks.delete_user')
    @mock.patch('tasks.tasks.user_exists')
    def test_delete_user(self, user_exists, delete_user):
        """
        Test delete user
        """
        user_exists.return_value = (True, '1234')

        # create user
        ford = User.objects.create(
            first_name='Robert',
            last_name='Ford',
            username='rford',
            email='rford@ww.com',
        )

        ford.tenants.add(self.tenant)

        # ford.save()

        User.objects.filter(username='rford').delete()

        delete_user.assert_called()


class GroupTestCase(TestCase):
    '''
    test group
    '''
    def setUp(self):
        # create tenant
        self.tenant = Tenant.objects.create(name='first tenant')

        # create app
        self.app = App.objects.create(
            tenant=self.tenant,
            name='First App',
            type='App',
            url='http://test.com',
            description='Test App',
        )

        # create config
        self.config = Config.objects.create(
            app=self.app,
            sync_type=ProvisioningType.downstream.value,
            auth_type=AuthenticationType.token.value,
            base_url='http://test.com/auth',
            token='token',
            status=ProvisioningStatus.Enabled.value,
        )

    @mock.patch('tasks.tasks.provision_group')
    def test_provision_group(self, provision_group):
        """
        Test django model signal
        """
        # create group
        behavior = Group.objects.create(name='Behavior Group', tenant=self.tenant)

        behavior.save()

        provision_group.assert_called_with(self.tenant.uuid, behavior.id)

    @mock.patch('tasks.tasks.provision_app_group')
    def test_provision_app_group(self, provision_app_group):
        """
        Test provision app group
        """
        # create group
        behavior = Group.objects.create(name='Behavior Group', tenant=self.tenant)

        behavior.save()

        provision_app_group.assert_called_with(self.tenant.uuid, self.app.id, self.config.id, behavior.id)

    @mock.patch('tasks.tasks.provision_app_group')
    @mock.patch('tasks.tasks.deprovision_app_group')
    def test_deprovision_app_group(self, deprovision_app_group, provision_app_group):
        """
        Test deprovision app group
        """
        # create group
        behavior = Group.objects.create(name='Behavior Group', tenant=self.tenant)

        behavior.save()

        provision_app_group.assert_called_with(self.tenant.uuid, self.app.id, self.config.id, behavior.id)

        Group.objects.filter(name='Behavior Group').delete()

        deprovision_app_group.assert_called_with(self.tenant.uuid, self.app.id, self.config.id, behavior.id)

    @mock.patch('tasks.tasks.create_group')
    @mock.patch('tasks.tasks.group_exists')
    def test_create_group(self, group_exists, create_group):
        """
        Test create group
        """
        # patch where the func is used not imported
        # doc: https://docs.python.org/3/library/unittest.mock.html#where-to-patch
        group_exists.return_value = (False, '1234')

        # create group
        behavior = Group.objects.create(name='Behavior Group', tenant=self.tenant)

        behavior.save()

        create_group.assert_called()

    @mock.patch('tasks.tasks.update_group')
    @mock.patch('tasks.tasks.group_exists')
    def test_update_group(self, group_exists, update_group):
        """
        Test update group
        """
        group_exists.return_value = (True, '1234')

        # create group
        behavior = Group.objects.create(name='Behavior Group', tenant=self.tenant)

        behavior.save()

        update_group.assert_called()

    @mock.patch('tasks.tasks.provision_app_group')
    @mock.patch('tasks.tasks.delete_group')
    @mock.patch('tasks.tasks.group_exists')
    def test_delete_group(self, group_exists, delete_group, provision_app_group):
        """
        Test delete group
        """
        group_exists.return_value = (True, '1234')

        # create group
        behavior = Group.objects.create(name='Behavior Group', tenant=self.tenant)

        behavior.save()

        provision_app_group.assert_called_with(self.tenant.uuid, self.app.id, self.config.id, behavior.id)

        Group.objects.filter(name='Behavior Group').delete()

        delete_group.assert_called()

    @mock.patch('tasks.tasks.provision_app_group')
    @mock.patch('tasks.tasks.patch_group')
    @mock.patch('tasks.tasks.get_user_group_uuid')
    def test_patch_group(self, get_user_group_uuid, patch_group, provision_app_group):
        """
        Test patch group
        """
        get_user_group_uuid.return_value = ('1234', '5678')

        # create group
        behavior = Group.objects.create(name='Behavior Group', tenant=self.tenant)

        behavior.save()

        provision_app_group.assert_called_with(self.tenant.uuid, self.app.id, self.config.id, behavior.id)

        # create user
        ford = User.objects.create(
            first_name='Robert',
            last_name='Ford',
            username='rford',
            email='rford@ww.com',
        )

        ford.tenants.add(self.tenant)

        # ford.save()

        ford.scim_groups.add(behavior)

        patch_group.assert_called()
