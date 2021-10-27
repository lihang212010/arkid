from re import X
import requests


def get_data(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return {}


def gen_user_password(len=9):
    from password_generator import PasswordGenerator

    pwo = PasswordGenerator()
    pwo.minlen = len
    pwo.maxlen = len
    pwo.minuchars = 1
    pwo.minlchars = 1
    pwo.minnumbers = 1
    pwo.minschars = 1
    return pwo.generate()


def gen_user_attributes(user):
    data = {
        'cn': '',
        'givenName': user['name']['givenName'],
        'sn': user['name']['familyName'],
        'name': user['name']['formatted'].replace(',',''),
        'displayName': user['name']['formatted'].replace(',',''),
        'mail':  user.get('mail', ''), # generate_mail_func or mail_str or update_mail_func
        'userPrincipalName': user['id'],
        'sAMAccountName': user['id'],
        # 'userPassword': '', # generate_pwd_func and notify_by_api
        'employeeID': user['id'],
        'title': user['title'],
        'department': user['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User']['department'],
        'company': user['urn:ietf:params:scim:schemas:extension:hr:2.0:User']['FCOMP'],
        # 'manager': user['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User']['manager']['value'],
        'pager': str(user['phoneNumbers'][0]['value']),
    }
    result = {}
    result['raw_data'] = user
    result['id'] = user['id']
    result['name'] = data['name']
    result['mail'] = data.get('mail','')
    status = user['urn:ietf:params:scim:schemas:extension:hr:2.0:User']['FSTATUS']
    result['status'] = 'enabled' if str(status) == '1' else 'disabled'
    result['group_id'] = user['urn:ietf:params:scim:schemas:extension:hr:2.0:User']['FDEPT_ID']
    result['manager_id'] = user['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User']['manager']['value']
    result['attributes'] = data
    result['company_name'] = user['urn:ietf:params:scim:schemas:extension:hr:2.0:User']['FCOMP']
    result['company_id'] = user['urn:ietf:params:scim:schemas:extension:hr:2.0:User']['FCOMP_ID']
    return result


def gen_group_attributes(group):
    result = {}
    result['raw_data'] = group
    result['id'] = group['id']
    status= group['urn:ietf:params:scim:schemas:extension:hr:2.0:Group']['FSTATUS']
    result['status'] = 'enabled' if str(status) == '3' else 'disabled'
    result['name'] = group['displayName'].strip().replace('/','_')
    result['members'] = group.get('members',[])
    result['company_name'] = group['urn:ietf:params:scim:schemas:extension:hr:2.0:Group']['FCOMP']
    result['company_id'] = group['urn:ietf:params:scim:schemas:extension:hr:2.0:Group']['FCOMP_ID']
    return result