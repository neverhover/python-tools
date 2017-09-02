import re

sym = 'FDXABDHZK'
codes = [ord(s) for s in sym]
print(codes)
print(re.sub("_","-", "ipv4_address"))

user = {'name': "Trey", 'website': "http://treyhunner.com"}
defaults = {'name': "Anonymous User", 'page_name': "Profile Page"}
context = {}
context.update(defaults)
context.update(user)
print(context)

my_dict = {'key': 'iftype', 'type': 'string', 'default': 'ethernet'}
my_dict