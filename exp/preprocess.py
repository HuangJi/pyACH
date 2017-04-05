from gcoin import *

BANK_LIST = [
    '6AB', 'A28', '46E', 'DD3', '822', 'CCC', '219',
    '18C', '170', 'B63', '62F', '5E0', '666', '519',
    'BA4', '5BD', '682', 'E07', 'B31', '0B1', 'FCB',
    'B89', '101', 'EDB', 'E75', '75D', 'A0D', '22D',
    'AB5', 'A1D', 'F73', 'C45', '481', '49A', 'EE0',
    '269', '7BA', '48C', 'E0C', 'CE3', '8DA', '552',
    '1F6', 'B30', '6D4', 'FB4', '4AD', '940', '838',
    'E15', 'F8E', '717', 'C72', '882', 'EA0'
]

def get_addr_list(bank_list):
    list = {}
    for bank in bank_list:
        priv = sha256(bank)
        pub = privtopub(priv)
        addr = pubtoaddr(pub)
        list[bank] = addr
    return list

print get_addr_list(BANK_LIST)
