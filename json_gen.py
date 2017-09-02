"""
Generate json from yaml

See http://yaml.readthedocs.io/en/latest/install.html

Use yaml 1.1 by PyYAML
See http://pyyaml.org/wiki/PyYAMLDocumentation
"""
from ruamel.yaml import YAML
import yaml,json
from collections import defaultdict

### 全局属性集合
mergeAttrs = ({
    "hardware",
    "ethernet"
})

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
        print("Loop >>>>>>>>>> user key =" , key)
        print("val is ", val)
        print("tmp_data is ", type(tmpdata))
        tmp_obj = None
        if isinstance(tmpdata, list):
            tmp_obj = tmpdata[key]
        elif isinstance(tmpdata, dict):
            tmp_obj = tmpdata.get(key, 'not exist')

        print("tmp_data['%s'] = %s" % (key, tmp_obj))
        if isinstance(tmp_obj, str):
            ## 此时已经是一个叶子节点，其节点下为字符串，则直接复制
            print("Copy user node attr ['%s']='%s' to default node" % (key, val) )
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

json_fname = 'template.json'
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

tmp_data=dict(default_data)
merge2(tmp_data, pro_data)
# tmp_data.update(pro_data)
# tmp_data['device']['wireless']['radio']
# tmp_data['device']['wireless']['teest']= 'abc'
print(tmp_data)
# print(tmp_data['device']['wireless']['radio'][0])

with open(json_fname, 'w', encoding='utf-8') as json_file:
    json.dump(tmp_data, json_file, separators=(',',': '), skipkeys=True, sort_keys=True, indent=2)
    # print(json.dumps(tmp_data, separators=(',',': '), skipkeys=True, sort_keys=True, indent=2))
