import tests.test_users_and_auth_routers as t
r = t.client.get('/users/notfound')
print('status', r.status_code)
print('body', r.text)
