#!/usr/bin/env python3

import time
from pprint import pprint

import requests
import keycloak
#from keycloak.realm import KeycloakRealm


def get_access_token(server, username, password):
    #url = server + '/' + 'auth' + '/' + 'realms' + '/' + realm 
    url = server + '/' + 'auth' + '/' + 'realms' + '/' + 'master'
    #url = server + '/' + 'auth' + '/' + 'admin' + '/' + 'realms'
    print(url)
    rr = requests.get(url, verify=False)
    print(rr)
    print(rr.text)
    print(rr.json())
    jdata = rr.json()
    pprint(jdata)

    # get a token ... ?
    token_service = jdata['token-service']
    rr = requests.post(
            token_service + '/token',
            #token_service,
            auth=(username, password),
            headers={
                #'Content-Type': 'application/json'
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={'grant_type': 'password', 'username': username, 'password': password, 'client_id': 'admin-cli'},
            verify=False
        )
    print(rr)
    print(rr.text)

    access_token = rr.json()['access_token']
    print(access_token)
    #import epdb; epdb.st()
    return access_token


def get_mapper(attribute, mtype='String'):
    mapper = {
        'name': attribute,
        'id': attribute,
        'protocol': 'openid-connect',
        'protocolMapper': 'oidc-usermodel-attribute-mapper',
        'consentRequired': False,
        'config': {
            'userinfo.token.claim': True,
            'user.attribute': attribute,
            'id.token.claim': True,
            'access.token.claim': True,
            'claim.name': attribute,
            'jsonType.label': mtype
        } 
    }
    return mapper


def main():
    username = 'admin'
    password = 'password'
    server = "https://172.19.0.2:8443"
    realm = "redhat-external"

    '''
    #ro = KeycloakRealm(server_url=server, realm_name=realm)
    #def __init__(self, server_url, username=None, password=None, realm_name='master', client_id='admin-cli', verify=True,
    #             client_secret_key=None, custom_headers=None, user_realm_name=None, auto_refresh_token=None):
    admin = keycloak.KeycloakAdmin(server, realm_name=realm, username=username, password=password, verify=False )
    import epdb; epdb.st()
    '''

    '''
    #url = server + '/' + 'auth' + '/' + 'realms' + '/' + realm 
    url = server + '/' + 'auth' + '/' + 'realms' + '/' + 'master'
    print(url)
    rr = requests.get(url, verify=False)
    print(rr)
    print(rr.text)
    print(rr.json())
    jdata = rr.json()
    pprint(jdata)

    # get a token ... ?
    token_service = jdata['token-service']
    rr = requests.post(
            token_service + '/token',
            #token_service,
            auth=(username, password),
            headers={
                #'Content-Type': 'application/json'
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={'grant_type': 'password', 'username': username, 'password': password, 'client_id': 'admin-cli'},
            verify=False
        )
    print(rr)
    print(rr.text)

    access_token = rr.json()['access_token']
    print(access_token)
    import epdb; epdb.st()
    '''

    '''
    access_token = get_access_token(server, username, password)

    URL_ADMIN_SERVER_INFO = "admin/serverinfo"
    #url = server + '/' + URL_ADMIN_SERVER_INFO
    #url = server + f'/realms/master/users'
    url = server + f'/admin/realms/{realm}'
    print(url)
    rr = requests.get(
        url,
        auth=(username, password),
        headers={
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        },
        verify=False
    )
    print(rr)
    import epdb; epdb.st()
    '''
    admin = keycloak.KeycloakAdmin(server + '/auth/', username=username, password=password, verify=False )
    realms = admin.get_realms()
    for _realm in realms:
        pprint(_realm)

    try:
        admin.delete_realm('redhat-external')
    except Exception as e:
        print(e)

    resp = admin.create_realm({'realm': 'redhat-external', 'enabled': True})
    time.sleep(1)
    
    realmids = {}
    realms = admin.get_realms()
    for idr,_realm in enumerate(realms):
        print('------------------------------------')
        print('# REALM: %s' % _realm['realm'])
        print('# ID: %s' % _realm['id'])
        print('------------------------------------')
        realmids[_realm['realm']] = _realm['id']
    #import epdb; epdb.st()

    admin2 = keycloak.KeycloakAdmin(
            server + '/auth/',
            realm_name='redhat-external',
            user_realm_name='master',
            username=username,
            password=password,
            verify=False
        )

    '''
    identity: {
        account_number: token.account_number,
        type: token.type,
        user: {
            username: token.username,
            email: token.email,
            first_name: token.first_name,
            last_name: token.last_name,
            is_active: token.is_active,
            is_org_admin: token.is_org_admin,
            is_internal: token.is_internal,
            locale: token.locale
        },
        internal: {
            org_id: token.org_id,
            account_id: token.account_id
        }
    '''

    protocol_mappers = [
        get_mapper('account_number', mtype='int'),
        get_mapper('account_id', mtype='int'),
        get_mapper('org_id', mtype='int'),
        get_mapper('username', mtype='String'),
        get_mapper('email', mtype='String'),
        get_mapper('first_name', mtype='String'),
        get_mapper('last_name', mtype='String')
    ]

    # TODO: service accouts enabled == True, authorization enabled = True
    admin2.create_client({
            'clientId': 'cloud-services',
            'enabled': True,
            'bearerOnly': False,
            'publicClient': True,
            'rootUrl': 'https://prod.foo.redhat.com:1337',
            'baseUrl': 'https://prod.foo.redhat.com:1337',
            'redirectUris': ['https://prod.foo.redhat.com:1337/*'],
            'protocolMappers': protocol_mappers
        })
    time.sleep(1)


    # need client scope on each attribute and then add to client's client scopes?

    '''
    clientids = {}
    clients = admin2.get_clients()
    for _client in clients:
        print(_client['clientId'])
        print(_client.get('id'))
        clientids[_client['clientId']] = _client['id']
        
    cs_client = admin2.get_client(clientids['cloud-services'])
    '''


    #admin2.create_user({'username': 'bbarker', 'first_name': 'bob', 'last_name': 'barker', 'email': 'bbarker@redhat.com', 'org_id': 1 })
    admin2.create_user({
        'enabled': True,
        'username': 'bbarker',
        'firstName': 'bob',
        'lastName': 'barker',
        'email': 'bbarker@redhat.com',
        'attributes': {
            'first_name': 'bob',
            'last_name': 'barker',
            'account_id': 111111,
            'account_number': 111111,
            'org_id': 1
        },
        'credentials': [{
            'temporary': False,
            'type': 'password',
            'value': 'redhat1234'
        }]
    })

    import epdb; epdb.st()


if __name__ == "__main__":
    main()
