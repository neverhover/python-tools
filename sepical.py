import collections

WebSites = collections.namedtuple('WebSites', ['name', 'url', 'owner'])

class myWorld:
    names= 'sina 163 baidu'.split()
    urls = 'www.sina.com www.163.com www.baidu.com'.split()
    owners = '新浪 网易 百度'.split()
    def __init__(self):
        self._cards = [ WebSites(name, url, owner) for name in self.names
            for url in self.urls
            for owner in self.owners
            ]

    def __len__(self):
        return 11


    def __getitem__(self, item):
        return self._cards[item]

sogou = WebSites('sogou', 'www.sogou.com', '搜狗')
print(sogou.name)

world = myWorld()
print(repr(world))
