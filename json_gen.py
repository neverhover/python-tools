"""
Generate json from yaml

See http://yaml.readthedocs.io/en/latest/install.html

Use yaml 1.1 by PyYAML
See http://pyyaml.org/wiki/PyYAMLDocumentation
"""
from ruamel.yaml import YAML
import yaml, json, re
from collections import defaultdict

### 全局属性集合
mergeAttrs = ({
    "hardware",
    "ethernet"
})


class Monster(yaml.YAMLObject):
    yaml_tag = u'!Monster'

    def __init__(self, name, hp, ac, attacks):
        self.kkkkkk = "222222222"
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attacks = attacks
    def __repr__(self):
        return "%s(name1=%r, hp1=%r, ac1=%r, attacks1=%r)" % (
            self.__class__.__name__, self.name, self.hp, self.ac, self.attacks)

class Radio(yaml.YAMLObject):
    yaml_tag = u'!Radio'
    fname = "radio.yaml"
    data = ""

    def __init__(self, **attrs):
        self.kkkkkk="111111111111"
        with open(self.fname, "r", encoding='utf-8') as sock:
            data = yaml.load(sock)
            print("---------------------", data)
        for key, value in data.items():
            stm = 'self.{key}={val}'.format(key=key, val=value)
            exec(stm)
        # for (key, value) in attrs.items():
        #     # stm = "self.%s = /" % s / "" % (key, value)
        #     stm = 'self.{key}={val}'.format(key= key, val= value)
        #     print("-------------------", stm)
        #     exec(stm)
    def __repr__(self):
        return "abc"


def convert_to_builtin_type(obj):
    # print("-x-x-x-x-x-", obj.kkkkkk)
    # print('default(', repr(obj), ')')
    d = {}
    d.update(obj.__dict__)

    return d


def add_yaml_resolver():
    pattern = re.compile(r'\$schema:(\w+)')
    # matchObj = re.search(patten, "$schema:vvvap")
    # if matchObj:
    #     print("Matched ", matchObj.group(1))
    # else:
    #     print("Not match")
    yaml.add_implicit_resolver(u'!dice', pattern)


def merge_hardware(tmpdata, user):
    tmpdata.update(user)


def merge_device(tmpdata, user):
    tmp_hard = tmpdata.get("hardware", 'not exist')
    user_hard = user.get("hardware", 'not exist')
    if user_hard != 'not exist':
        merge_hardware(tmp_hard, user_hard)


def merge(tmpdata, user):
    tmp_dev = tmpdata.get("device", 'not exist')
    user_dev = user.get("device", 'not exist')
    if user_dev != 'not exist':
        merge_device(tmp_dev, user_dev)


def merge2(tmpdata, user):
    # print("type t ", type(tmpdata), " type user", type(user))
    print("")

    it = None
    if isinstance(user, dict):
        it = user.items()
    elif isinstance(user, list):
        it = enumerate(user)
    else:
        print("Error found type(p1)=%s, type(p2)=%s" % (type(tmpdata), type(user)))
        return

    for key, val in it:
        print("Loop >>>>>>>>>> user key =", key)
        print("val is ", val)
        print("tmp_data is ", type(tmpdata))
        tmp_obj = None
        if isinstance(tmpdata, list):
            if len(tmpdata) - 1 < key:
                ### 表示user list个数比defaults要多
                tmpdata.append(val)
                continue
            else:
                tmp_obj = tmpdata[key]
        elif isinstance(tmpdata, dict):
            tmp_obj = tmpdata.get(key, 'not exist')

        print("tmp_data['%s'] = %s" % (key, tmp_obj))
        if isinstance(tmp_obj, str):
            ## 此时已经是一个叶子节点，其节点下为字符串，则直接复制
            print("Copy user node attr ['%s']='%s' to default node" % (key, val))
            tmpdata[key] = val
            continue
        if tmp_obj != 'not exist' and tmp_obj == None:
            ## default模版中这个节点为空，则直接复制
            print("Copy user node [%s] to default node" % key)
            tmpdata[key] = val
        elif tmp_obj != 'not exist' and key not in mergeAttrs:
            ## default模版中这个节点不在可以直接copy的列表中，需要再次迭代
            print("Jump to user node [%s] (%s) with default node" % (key, type(val)))
            merge2(tmp_obj, val)
        elif tmp_obj != 'not exist' and key in mergeAttrs:
            print("Merge user node [%s] to default node" % key)
            tmp_obj.update(val)
        elif tmp_obj == 'not exist' and key in mergeAttrs:
            print("Add user node [%s] to default node" % key)
            tmpdata[key] = val
        else:
            print("xxxxxxxxxxxxxxxxxx")
            print(tmp_obj, "key is ", key)
            print("tmpdata now is", tmpdata)
            print("xxxxxxxxxxxxxxxxxx")


add_yaml_resolver()
# Radio(sex="boy")

json_fname = 'dist/template.json'
yaml_fname = 'template.yaml'
pro_2ac = '2ac.yaml'
## 读取默认的yaml模版
with open(yaml_fname, 'r', encoding='utf-8') as yaml_file:
    default_data = yaml.load(yaml_file)
    # print(default_data)

## 读取产品的yaml模版
with open(pro_2ac, 'r', encoding='utf-8') as yaml_file:
    pro_data = yaml.load(yaml_file)
    # print(pro_data)

## 合并dict

tmp_data = dict(default_data)
merge2(tmp_data, pro_data)
# tmp_data.update(pro_data)
# tmp_data['device']['wireless']['radio']
# tmp_data['device']['wireless']['teest']= 'abc'
print(tmp_data)
# print(tmp_data['device']['wireless']['radio'][0])

with open(json_fname, 'w', encoding='utf-8') as json_file:
    json.dump(tmp_data, json_file, separators=(',', ': '), skipkeys=True, sort_keys=True, indent=2, default=convert_to_builtin_type)
#     # print(json.dumps(tmp_data, separators=(',',': '), skipkeys=True, sort_keys=True, indent=2))

with open("dist/%s" % pro_2ac, 'w', encoding='utf-8') as target_file:
    yaml.dump(tmp_data, target_file)
    # print(json.dumps(tmp_data, separators=(',',': '), skipkeys=True, sort_keys=True, indent=2))
