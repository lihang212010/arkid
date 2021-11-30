import re
import copy
import json
import pypinyin
import ldap3
from ldap3 import Server, Connection
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups
from ldap3.extend.microsoft.removeMembersFromGroups import ad_remove_members_from_groups

from common.logger import logger
from qiye_weixin.utils import get_weixin_client, load_textcard_url
from .utils_client import gen_password


class SyncClient:
    def sync(self):
        pass


class SyncClientAD(SyncClient):
    user_object_class = 'user'
    group_object_class = 'group'
    ou_object_class = 'organizationalUnit'

    def __init__(self, **settings):
        self.host = settings['host']
        self.port = settings['port']
        self.use_tls = settings['use_tls']
        self.bind_dn = settings['bind_dn']
        self.bind_password = settings['bind_password']
        self.root_dn = settings['root_dn']
        dc = self.root_dn[self.root_dn.replace('dc=','DC=').find('DC='):]
        mail_suffix = '@' + '.'.join((',' + dc).split(',DC='))[1:]
        self.mail_suffix = settings['mail_suffix'] \
                                if 'group_name_prefix' in settings \
                                 else mail_suffix
        self.group_name_prefix = settings['group_name_prefix'] \
                                 if 'group_name_prefix' in settings \
                                 else self.root_dn.split(',',1)[0].split('=', 1)[1] + '_'
        self.search_base = settings['search_base'] \
                                 if 'search_base' in settings \
                                 else self.root_dn[self.root_dn.replace('dc=','DC=').find('DC='):]
        self.exclude_groups = settings.get('exclude_groups', [])
        self.connect_timeout = settings.get('connect_timeout')
        self.receive_timeout = settings.get('receive_timeout')

        self.conn = self.get_connection()

        self.users = settings['users']
        self.groups = settings['groups']

        self.user_search_clients = [self]

    def get_connection(self):
        server = Server(
            host=self.host,
            port=self.port,
            use_ssl=self.use_tls,
            # get_info=ldap3.NONE,
            connect_timeout=self.connect_timeout,
        )
        conn = Connection(
            server,
            user=self.bind_dn,
            password=self.bind_password,
            auto_bind=True,
            # raise_exceptions=False,
            receive_timeout=self.receive_timeout,
        )
        return conn

    def add_user(self, user: json):
        object_class = self.user_object_class
        attributes = copy.copy(user['attributes'])
        if not attributes.get('homePhone'):
            mail = self.gen_user_email(user)
            attributes['homePhone'] = mail
        cn, dn = user['ldap_cn'], user['ldap_dn']

        attributes['cn'] = cn
        attributes = {k:v for k,v in attributes.items() if v}

        # add user
        res = self.conn.add(dn=dn, object_class=object_class, attributes=attributes)
        logger.debug(f"add user {res and 'success' or 'failed'}: dn: {dn}, object_class: {object_class}, attributes: {attributes}, error: {res and 'None' or self.conn.result}")

        # set initial password
        user_password = self.gen_user_password()
        logger.debug(f"password: {user_password} generated for user: {attributes['name']} id: {attributes['userPrincipalName']}")
        self.set_user_password(dn, user_password)
        self.enable_user(dn)

        # notify user
        try:
            self.notify_user_created(attributes, user_password)
        except Exception as e:
            logger.error(e)
        logger.debug("notify user success")

    def notify_user_created(self, attributes, user_password):
        client = get_weixin_client()
        textcard_url = load_textcard_url(client)
        if not textcard_url:
            logger.error('No textcard url return')
        logger.info(textcard_url)
        title = f"{attributes['displayName']}，您好："
        description = f"""欢迎加入孚能科技，我们是您IT的同事，我们准备了以下关于IT方面的相关资讯，便于您更好的开展工作：
                        a，您的电脑登录账户是：{attributes['SamAccountName']}，登录随机密码是：{user_password}；
                        b，您的邮箱号是：{attributes['homePhone']}，密码与电脑密码相同或者Farasis@1234；"""
        touser=attributes.get('employeeID')
        res = client.send_textcard(touser, title, description, textcard_url, '更多内容')
        logger.debug(f"weixin notify {touser} result: {res}")

    def gen_user_password(self):
        return gen_password(10)

    def set_user_password(self, user_dn: str, user_password: str):
        # set password
        self.conn.extend.microsoft.modify_password(user_dn,
                new_password=user_password, old_password=None)
        # User must change password at next logon
        password_expire = {"pwdLastSet": [(ldap3.MODIFY_REPLACE, [0])]}
        self.conn.modify(dn=user_dn, changes=password_expire)

    def enable_user(self, dn):
        self.conn.modify(dn, {'userAccountControl': [(ldap3.MODIFY_REPLACE, 512)]})

    def gen_user_email(self, user: json):
        attrs = user['attributes']
        name = attrs['name']
        givenName = attrs['givenName']
        sn = attrs['sn']
        givenNamePinyin = pypinyin.lazy_pinyin(givenName)
        snPinyin = pypinyin.lazy_pinyin(sn)
        # 吴家亮 jlwu
        email_prefix = ''.join([x[0] for x in givenNamePinyin] + snPinyin)
        email_prefix = re.sub("[^a-zA-Z]+", "", email_prefix)
        email = email_prefix + self.mail_suffix
        if not self.exists_email(email):
            return email
        logger.debug(f'email: {email} exists for {name}')

        # 吴家亮 jialiangwu
        email_prefix = ''.join(givenNamePinyin + snPinyin)
        email_prefix = re.sub("[^a-zA-Z]+", "", email_prefix)
        email = email_prefix + self.mail_suffix
        if not self.exists_email(email):
            return email
        logger.debug(f'email: {email} exists for {name}')

        # 吴家亮 jialiangwu1、jialiangwu2、jialiangwu3
        max_n = 1000
        mail = email_prefix
        for n in range(1, max_n):
            email = mail + str(n) + self.mail_suffix
            if not self.exists_email(email):
                return email
            logger.debug(f'email: {email} exists for {name}')

        raise Exception("more than {max_n} duplicate email: {mail} exists for {name} {user['id']}")

    def gen_user_dn_in_ou(self, user: json, ou: str):
        user_cn = user['name']
        user_dn = f"cn={user_cn},{ou}"
        return_flag = False
        if not self.exists_user_dn(user_dn):
            return_flag = True

        if not return_flag:
            ldap_user = self.get_user_from_ldap_by_id(user['id'])
            if ldap_user:
                ldap_user_dn = ldap_user['dn']
                _, ldap_user_ou = ldap_user_dn.split(',', 1)
                if ldap_user_ou.lower() == ou.lower():
                    return_flag = True

        if not return_flag:
            max_n = 1000
            cn = user_cn
            for n in range(1, max_n, 2):
                user_cn = cn + str(n)
                user_dn = f"cn={user_cn},{ou}"
                if not self.exists_user_dn(user_dn):
                    return_flag = True
                    break
                # logger.info(f"user_cn: {user_cn} exists for {user['name']}")

        if not return_flag:
            raise Exception("more than {max_n} duplicate email: {mail} exists for {user['name']}")

        user['ldap_cn'] = user_cn
        user['ldap_dn'] = user_dn
        # logger.debug(f"{user_dn} generated for user {user['name']} user_id{user['id']}")

    def gen_group_dn(self, group: json, parent_group: json):
        group['ldap_cn'] = self.group_name_prefix + group['name']
        if parent_group:
            group_last_name = group['ldap_cn'].split('_')[-1]
            group['ldap_ou'] = f"ou={group_last_name},{parent_group['ldap_ou']}"
        else:
            group['ldap_ou'] = f"ou={group['name']},{self.root_dn}"
        group['ldap_dn'] = f"cn={group['ldap_cn']},{group['ldap_ou']}"

    def exists_user_dn(self, dn: str):
        search_base = dn
        search_filter = f'(objectclass={self.user_object_class})'
        res = self.conn.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=ldap3.SUBTREE,
        )
        if not res or not json.loads(self.conn.response_to_json())['entries']:
            return False
        return True

    def exists_group_dn(self, dn: str):
        search_base = dn
        search_filter = f'(objectclass={self.group_object_class})'
        res = self.conn.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=ldap3.SUBTREE,
        )
        if not res or not json.loads(self.conn.response_to_json())['entries']:
            return False
        return True

    def exists_ou_dn(self, dn: str):
        search_base = dn
        search_filter = f'(objectclass={self.ou_object_class})'
        res = self.conn.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=ldap3.SUBTREE,
        )
        if not res or not json.loads(self.conn.response_to_json())['entries']:
            return False
        return True

    def exists_email(self, mail: str):
        for client in self.user_search_clients:
            search_base = client.search_base
            search_filter = f'(&(objectclass={client.user_object_class})(homePhone={mail}))'
            res = client.conn.search(
                    search_base=search_base,
                    search_filter=search_filter,
                    search_scope=ldap3.SUBTREE,
            )
            if res and json.loads(client.conn.response_to_json())['entries']:
                return True
        return False

    def get_user_from_ldap_by_id(self, user_id: str):
        for client in self.user_search_clients:
            search_base = client.search_base
            search_filter = f'(&(objectclass={client.user_object_class})(employeeID={user_id}))'
            res = client.conn.search(
                    search_base=search_base,
                    search_filter=search_filter,
                    search_scope=ldap3.SUBTREE,
                    attributes=ldap3.ALL_ATTRIBUTES,
                    size_limit=1,
            )
            if res:
                entries = json.loads(client.conn.response_to_json())['entries']
                if entries:
                    result = entries[0]
                    result['host_port'] = client.host + str(client.port)
                    return result
        return None

    def get_group_from_ldap_by_id(self, group_id: str):
        search_base = self.search_base
        search_filter = f'(&(objectclass={self.group_object_class})(sAMAccountName={group_id}))'
        res = self.conn.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=ldap3.SUBTREE,
                attributes=ldap3.ALL_ATTRIBUTES,
                size_limit=1,
        )
        if not res:
            return None
        entries = json.loads(self.conn.response_to_json())['entries']
        if not entries:
            return None
        return entries[0]

    def get_group_under_ou(self, ou: str):
        search_base = ou
        search_filter = f'(objectclass={self.group_object_class})'
        res = self.conn.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=ldap3.LEVEL,
                size_limit=1,
        )
        if not res:
            return None
        entries = json.loads(self.conn.response_to_json())['entries']
        if not entries:
            return None
        return entries[0]

    def get_all_ou_from_ldap(self):
        search_base = self.root_dn
        search_filter = f'(objectclass={self.ou_object_class})'
        res = self.conn.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=ldap3.SUBTREE,
        )
        if not res:
            return []
        all_ou = json.loads(self.conn.response_to_json())['entries']
        all_ou_dn = [x['dn'] for x in all_ou]
        index = [x.lower() for x in all_ou_dn].index(self.root_dn.lower())
        del all_ou_dn[index]
        return all_ou_dn

    def move_user(self, source_dn, destination_dn):
        relative_dn, new_superior = destination_dn.split(',', 1)
        res = self.conn.modify_dn(
            dn=source_dn,
            relative_dn=relative_dn,
            delete_old_dn=True,
            new_superior=new_superior,
        )
        logger.debug(f"move user {res and 'success' or 'failed'} from {source_dn} to {destination_dn}, error: {res and 'None' or self.conn.result}")

    def move_group(self, source_dn, destination_dn):
        relative_dn, new_superior = destination_dn.split(',', 1)
        res = self.conn.modify_dn(
            dn=source_dn,
            relative_dn=relative_dn,
            delete_old_dn=True,
            new_superior=new_superior,
        )
        logger.debug(f"move group {res and 'success' or 'failed'} from {source_dn} to {destination_dn}, error: {res and 'None' or self.conn.result}")

    def move_user_to_ou(self, user: json, source_dn, dest_ou: str):
        _, source_ou = source_dn.split(',', 1)
        if source_ou.lower() != dest_ou.lower():
            self.gen_user_dn_in_ou(user, dest_ou)
            user_dn = user['ldap_dn']
            self.move_user(source_dn=source_dn, destination_dn=user_dn)

    def compare_user(self, user: json, ldap_user: json):
        user_attributes = user['attributes']
        ldap_user_attributes = ldap_user['attributes']
        new_value = {}
        old_value = {}
        compare_keys = ['givenName', 'sn', 'displayName', 'title', 'department', 'company', 'pager']
        for k in compare_keys:
            if user_attributes[k] and user_attributes[k] != ldap_user_attributes.get(k):
                new_value[k] = user_attributes[k]
                old_value[k] = ldap_user_attributes.get(k)

        for k in ['homePhone']:
            # if ldap_user_attributes.get('mail') and not ldap_user_attributes.get(k):
            #     ldap_user_attributes[k] = ldap_user_attributes['mail']
            #     new_value[k] = ldap_user_attributes[k]
            #     old_value[k] = ''
            # if user_attributes[k] and \
            #         user_attributes[k].split('@')[0] != ldap_user_attributes.get(k, '').split('@')[0]:
            if user_attributes[k]:
                new_value[k] = user_attributes[k]
                old_value[k] = ldap_user_attributes.get(k)
            elif not ldap_user_attributes.get(k):
                mail = self.gen_user_email(user)
                logger.debug(f"email: {mail} generated for user: {user['name']} id: {user['id']}")
                new_value[k] = mail
                old_value[k] = ''

        return new_value, old_value

    def update_user(self, user_dn: str, new_value: json, old_value: json):
        changes = {}
        for k,v in new_value.items():
            changes[k] = [(ldap3.MODIFY_REPLACE, v)]
        res = self.conn.modify(dn=user_dn, changes=changes)
        logger.info(f"updating user {res and 'success' or 'failed'}: {user_dn}, updated_data: {new_value}, old_data: {old_value}, error: {res and 'None' or self.conn.result}")

    def add_group(self, group: json):
        cn = group['ldap_cn']
        dn = group['ldap_dn']
        group_id = group['id']
        if len(cn) > 64:
            logger.info(f'group {group_id} name: {cn} too long, more than 64')
            return

        object_class = self.group_object_class
        attributes = {
            'cn': cn,
            'groupType':'-2147483646',
            'sAMAccountName': group_id,
            }
        res = self.conn.add(dn=dn, object_class=object_class, attributes=attributes)
        logger.debug(f"add group {res and 'success' or 'failed'}: dn: {dn}, object_class: {object_class}, attributes: {attributes}, error: {res and 'None' or self.conn.result}")

    def add_ou(self, dn: str):
        object_class = self.ou_object_class
        attributes = None
        res = self.conn.add(dn=dn, object_class=object_class, attributes=attributes)
        logger.debug(f"add ou {res and 'success' or 'failed'}: dn: {dn}, object_class: {object_class}, attributes: {attributes}, error: {res and 'None' or self.conn.result}")

    def set_ou_manager(self, ou_dn: str, manager_id: str):
        manager = self.user_dict.get(manager_id)
        if not manager:
            return
        if manager["status"] == 'enabled':
            changes = {"managedBy": [(ldap3.MODIFY_REPLACE, [manager["ldap_dn"]])]}
        else:
            changes = {"managedBy": [(ldap3.MODIFY_DELETE, [])]}
        self.conn.modify(dn=ou_dn, changes=changes)

    def get_user_group(self, user):
        group_id = user['group_id']
        group = self.group_dict.get(group_id)
        return group

    def get_user_ou(self, user):
        group = self.get_user_group(user)
        if not group:
            logger.debug(f"user_id {user['id']} does not belong to a group")
            ou = self.root_dn
        elif group['status'] == 'disabled':
            logger.debug(f"user_id {user['id']} is in deleted group group_id {group['id']}")
            ou = self.root_dn
        else:
            ou = group['ldap_ou']
        user['ldap_ou'] = ou
        return ou

    def add_group_member(self, dn, group_dn):
        res = self.conn.extend.microsoft.add_members_to_groups(dn, group_dn)
        if not res:
            logger.error(f"add dn: {dn} to group: {group_dn} failed, error: {self.conn.result}")

    def remove_group_member(self, dn, group_dn):
        res = self.conn.extend.microsoft.remove_members_from_groups(dn, group_dn)
        if not res:
            logger.error(f"remove dn: {dn} from group: {group_dn} failed, error: {self.conn.result}")

    def remove_member_of_attr(self, ldap_object):
        # remove user or group from group by ldap memberOf attribute
        attrs = ldap_object.get('attributes', {})
        dn = attrs.get('distinguishedName','')
        if not dn:
            return

        groups_dn = attrs.get('memberOf', [])
        for group_dn in groups_dn:
            if self.exists_group_dn(group_dn) and group_dn not in self.exclude_groups:
                self.remove_group_member(dn, group_dn)

    def remove_member_of_group(self, ldap_object):
        # remove user or group from group by ldap member attribute
        attrs = ldap_object.get('attributes', {})
        dn = attrs.get('distinguishedName','')
        if not dn:
            return

        members_dn = attrs.get('member', [])
        self.remove_group_member(members_dn, dn)

    def get_root_groups(self):
        none_root_groups = set()
        for group in self.groups:
            if group['status'] == 'enabled':
                members = group.get('members',[])
                for member in members:
                    none_root_groups.add(member['value'])

        root_groups = [group for group in self.groups if group['status']=='enabled' and group['id'] not in none_root_groups]
        return root_groups

    def sync_groups_from_root(self, group, parent_group=None):
        self.gen_group_dn(group, parent_group)

        if parent_group:
            group['parent'] = parent_group

        if not self.exists_ou_dn(group['ldap_ou']):
            self.add_ou(group['ldap_ou'])

        ldap_group = self.get_group_from_ldap_by_id(group['id'])
        if not ldap_group:
            # add new group
            self.add_group(group)
        else:
            # move existing group
            group_dn = group['ldap_dn']
            ldap_group_dn = ldap_group['dn']
            if group_dn.lower() != ldap_group_dn.lower():
                self.move_group(source_dn=ldap_group_dn, destination_dn=group_dn)
                # remove group from parent group
                self.remove_member_of_attr(ldap_group)

        # add group to parent
        if parent_group:
            if self.exists_group_dn(group['ldap_dn']) and self.exists_group_dn(parent_group['ldap_dn']):
                self.add_group_member(group['ldap_dn'], parent_group['ldap_dn'])

        parent_group = group
        for member in group.get('members',[]):
            child_group_id = member['value']
            child_group = self.group_dict[child_group_id]
            if child_group['status'] == 'enabled':
                self.sync_groups_from_root(child_group, parent_group=parent_group)

    def sync_groups(self):
        logger.info('syncing groups')
        self.group_dict = {group['id']: group for group in self.groups}

        # sync from root group to leaf group
        root_groups = self.get_root_groups()
        logger.info(f"root_groups found: {[group['id'] for group in root_groups]}")
        for root_group in root_groups:
            logger.info(f"syncing group from root_group: {root_group['id']}")
            self.sync_groups_from_root(root_group)

    def delete_ou(self, ou_dn):
        # 递归删除 ou
        search_base = ou_dn
        search_filter = '(objectclass=*)'
        attributes=['objectClass']
        res = self.conn.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=ldap3.LEVEL,
                attributes=attributes,
        )

        # ou 不存在或已被删除或到了叶子节点
        if not res:
            # 叶子节点
            if ou_dn not in self.deleted_ou_dn:
                res = self.conn.delete(ou_dn)
                self.deleted_ou_dn.add(ou_dn)
                logger.debug(f"delete ou {res and 'success' or 'failed'}: dn: {ou_dn}, error: {res and 'None' or self.conn.result}")
            return

        entries = json.loads(self.conn.response_to_json())['entries']
        for entry in entries:
            if self.ou_object_class in entry['attributes']['objectClass'] and entry['dn'] in self.delete_ou_dn:
                self.delete_ou(entry['dn'])
            if self.group_object_class in entry['attributes']['objectClass']:
                res = self.conn.delete(entry['dn'])
                logger.debug(f"delete group {res and 'success' or 'failed'}: dn: {entry['dn']}, error: {res and 'None' or self.conn.result}")
            if self.user_object_class in entry['attributes']['objectClass']:
                logger.debug(f"move user {entry['dn']} out of deleted ou")
                user = {'id': entry['attributes']['employeeID'], 'name': entry['attributes']['name']}
                self.move_user_to_ou(user, source_dn=entry['dn'], dest_ou=self.root_dn)

        if ou_dn not in self.deleted_ou_dn:
            res = self.conn.delete(ou_dn)
            self.deleted_ou_dn.add(ou_dn)
            logger.debug(f"delete ou {res and 'success' or 'failed'}: dn: {ou_dn}, error: {res and 'None' or self.conn.result}")

    def delete_group(self, group):
        logger.info(f"deleting group {group['id']}")
        ldap_group = self.get_group_from_ldap_by_id(group['id'])
        if not ldap_group:
            logger.warning(f"disabling group {group['id']}, but group {group['id']} does not exist in ldap")
            return
        ldap_group_dn = ldap_group['dn']
        res = self.conn.delete(ldap_group_dn)
        logger.debug(f"delete group {res and 'success' or 'failed'}: dn: {ldap_group_dn}, group_id: {group['id']}, error: {res and 'None' or self.conn.result}")

    def delete_groups(self):
        logger.info('syncing disabled groups')
        for group in self.groups:
            if group['status'] == 'disabled':
                self.delete_group(group)

    def delete_ous(self):
        logger.info('deleting orgnazationalUnits')
        all_ou_dn = self.get_all_ou_from_ldap()

        enabled_ou_dn = [group['ldap_ou'].replace('ou=','OU=').replace('dc=','DC=') for group in self.groups if group['status']=='enabled']
        self.delete_ou_dn = set(all_ou_dn) - set(enabled_ou_dn)
        self.deleted_ou_dn = set()
        logger.info(f'ou to be deleted: {self.delete_ou_dn}')
        for dn in self.delete_ou_dn:
            self.delete_ou(dn)

    def sync_users(self):
        logger.info('syncing users')
        self.user_dict = {user['id']: user for user in self.users}

        # generate user attributes
        # for user in self.users:
        #     self.gen_user_attributes(user)
        self.users.sort(key=lambda x:x['id'])

        # sync users
        for user in self.users:
            if user['status'] == 'enabled':
                # username may confict in the same ou
                ou = self.get_user_ou(user)
                self.gen_user_dn_in_ou(user, ou)

                ldap_user = self.get_user_from_ldap_by_id(user['id'])
                if not ldap_user:
                    # add new user
                    self.add_user(user)
                elif ldap_user['host_port'] == self.host + str(self.port):
                    # same ad domain
                    # move existing user
                    user_dn = user['ldap_dn']
                    ldap_user_dn = ldap_user['dn']
                    _, source_ou = ldap_user_dn.split(',', 1)
                    if source_ou.lower() != ou.lower():
                        self.move_user(source_dn=ldap_user_dn, destination_dn=user_dn)
                        # search group under this ou and remove user from this ou
                        group = self.get_group_under_ou(source_ou)
                        if group:
                            self.remove_group_member(ldap_user_dn, group['dn'])
                    else:
                        user['ldap_dn'] = ldap_user_dn
                    new_value, old_value = self.compare_user(user, ldap_user)
                    if new_value:
                        self.update_user(user['ldap_dn'], new_value, old_value)
                else:
                    # not the domain
                    pass

        logger.info('syncing user manager')
        for user in self.users:
            if user['status'] == 'enabled':
                self.add_user_manager(user)

        logger.info('syncing user group')
        for user in self.users:
            if user['status'] == 'enabled':
                self.add_user_to_group(user)

    def add_user_to_group(self, user):
        user_dn = user['ldap_dn']
        group = self.get_user_group(user)
        while group:
            group_dn = group['ldap_dn']
            if self.exists_user_dn(user_dn) and self.exists_group_dn(group_dn):
                self.add_group_member(user_dn, group_dn)
                return
            group = group.get('parent')
        logger.warning(f"add user {user['id']} to group {user.get('group_id','')} failed, group or user does not exist")

    def add_user_manager(self, user):
        manager_id = user['manager_id']
        manager = self.user_dict.get(manager_id)
        if not manager:
            return
        if manager["status"] == 'enabled':
            changes = {"manager": [(ldap3.MODIFY_REPLACE, [manager["ldap_dn"]])]}
        else:
            changes = {"manager": [(ldap3.MODIFY_DELETE, [])]}
        self.conn.modify(dn=user["ldap_dn"], changes=changes)

    def delete_users(self):
        logger.info('syncing disabled users')
        for user in self.users:
            if user['status'] == 'disabled':
                self.disable_user(user)

    def disable_user(self, user):
        logger.info(f"disabling user: id {user['id']} name user['name']")
        ldap_user = self.get_user_from_ldap_by_id(user['id'])
        if not ldap_user:
            logger.warning(f"disabling user {user['id']}, but {user['id']} does not exist in ldap")
            return
        ldap_user_dn = ldap_user['dn']

        # disable user
        # userAccountControl: 512 normal user, 514 disabled user
        self.conn.modify(ldap_user_dn, {'userAccountControl': [(ldap3.MODIFY_REPLACE, 514)]})

        # delete user attributes
        changes = {}
        keys = set(user['attributes'].keys())
        delete_keys = set([
            #常规属性名称
            "givenName",
            "sn",
            "initials",
            "description",
            "physicalDeliveryOfficeName",
            "telephoneNumber",
            "otherTelephone",
            "mail",
            "wwwHomePage",
            "url",
            #地址属性名称
            "streetAddress",
            "postOfficeBox",
            "l",
            "st",
            "postalCode",
            "c",
            "co",
            #组织属性名称
            "title",
            "department",
            "company",
            #电话相关属性名称
            "telephoneNumber",
            "otherTelephone",
            "pager",
            "mobile",
            "otherMobile",
            "facsimileTelephoneNumber",
            "otherFacsimileTelephoneNumber",
            "ipPhone",
            "otherIpPhone",
            "info",
        ])
        for k in keys & delete_keys:
            changes[k] = [(ldap3.MODIFY_REPLACE, [' '])]
        res = self.conn.modify(dn=ldap_user_dn, changes=changes)
        if not res:
            logger.error(f"deleting user attributes failed: {user['id']}, dn={ldap_user_dn}, changes={changes}, error: {self.conn.result}")

        # delete user manger
        changes = {"manager": [(ldap3.MODIFY_DELETE, [])]}
        self.conn.modify(dn=ldap_user_dn, changes=changes)

        # remove user from group
        self.remove_member_of_attr(ldap_user)

        # move user to new ou if group changed
        group = self.get_user_group(user)
        if not group or group['status'] == 'disabled':
            dest_ou = self.root_dn
            logger.error(f"disable user: moving disabled user_id {user['id']} to group_id {group['id']}, but {group['id']} is deleted, so move disabled {user['id']} to deleted users ou {ou} ")
        else:
            dest_ou = group['ldap_ou']

        self.move_user_to_ou(user, source_dn=ldap_user_dn, dest_ou=dest_ou)

    def sync_ou_manager(self):
        logger.info('syncing ou manager')
        for group in self.groups:
            if group['status'] == 'enabled':
                self.set_ou_manager(group['ldap_ou'], group['manager_id'])

    def sync(self):
        self.sync_groups()
        self.sync_users()
        self.sync_ou_manager()
        self.delete_users()
        self.delete_groups()
        self.delete_ous()
