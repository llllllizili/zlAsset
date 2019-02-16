#from django.test import TestCase
# Create your tests here.
str = [
    {
        'protocol': 'tcp',
        'pid': '10634',
        'localaddr': '192.168.1.250',
        'localport': '22',
        'foreignaddr': '192.168.1.250',
        'foreignport': '44334',
        'state': 'ESTABLISHED'
    },
    {
        'protocol': 'tcp',
        'pid': '8656',
        'localaddr': '192.168.1.250',
        'localport': '22',
        'foreignaddr': '10.1.1.251',
        'foreignport': '60643',
        'state': 'ESTABLISHED'
    },
    {
        'protocol': 'tcp',
        'pid': '10638',
        'localaddr': '192.168.1.250',
        'localport': '44334',
        'foreignaddr': '192.168.1.250',
        'foreignport': '22',
        'state': 'ESTABLISHED'
    },
    {
        'protocol': 'tcp',
        'pid': '9706',
        'localaddr': '192.168.1.250',
        'localport': '40786',
        'foreignaddr': '192.168.1.55',
        'foreignport': '22',
        'state': 'ESTABLISHED'
    },
    {
        'protocol': 'tcp',
        'pid': '9683',
        'localaddr': '192.168.1.250',
        'localport': '22',
        'foreignaddr': '10.1.1.251',
        'foreignport': '55431',
        'state': 'ESTABLISHED'
    },
    {
        'protocol': 'tcp',
        'pid': '8820',
        'localaddr': '192.168.1.250',
        'localport': '22',
        'foreignaddr': '10.1.1.251',
        'foreignport': '64183',
        'state': 'ESTABLISHED'
    },
    {
        'protocol': 'tcp',
        'pid': '8679',
        'localaddr': '192.168.1.250',
        'localport': '22',
        'foreignaddr': '10.1.1.251',
        'foreignport': '60644',
        'state': 'ESTABLISHED'
    },
    {
        'protocol': 'tcp',
        'pid': '8702',
        'localaddr': '192.168.1.250',
        'localport': '22',
        'foreignaddr': '10.1.1.251',
        'foreignport': '60645',
        'state': 'ESTABLISHED'
    },
    {
        'protocol': 'tcp',
        'pid': '10621',
        'localaddr': '192.168.1.250',
        'localport': '8888',
        'foreignaddr': '10.1.1.251',
        'foreignport': '56730',
        'state': 'ESTABLISHED'
    },
    {
        'protocol': 'tcp',
        'pid': '10621',
        'localaddr': '192.168.1.250',
        'localport': '51973',
        'foreignaddr': '192.168.1.123',
        'foreignport': '3306',
        'state': 'ESTABLISHED'
    },
    {
        'protocol': 'tcp',
        'pid': '10621',
        'localaddr': '192.168.1.250',
        'localport': '51976',
        'foreignaddr': '192.168.1.123',
        'foreignport': '3306',
        'state': 'ESTABLISHED'
    }
]

l =list()
for n,d in enumerate(str):
    n =dict()
    n['addr']=d['foreignaddr']
    n['port']=d['localport']
    l.append(n)
print(l)

print('=======')
print([dict(t) for t in set([tuple(d.items()) for d in l])])


# [dict(t) for t in set([tuple(d.items()) for d in str])]

# for d in str:
#     for t in set(d.items()):
#         print([tuple(d.items())])
