"""
Generate json from yaml

See http://yaml.readthedocs.io/en/latest/install.html

Use yaml 1.1 by PyYAML
See http://pyyaml.org/wiki/PyYAMLDocumentation
"""
from ruamel.yaml import YAML
import yaml, json, re
from collections import defaultdict
import collections

### 全局属性集合
mergeAttrs = ({
    "hardware"
})

ignoreAttrs = ({
    "$yaml_template",
    "max-radios",
    "template_name"
})

delAttrs = ({
    "max-radios"
})


def merge2(tmpdata, user):
    # print("type t ", type(tmpdata), " type user", type(user))
    print("")

    ## 判断参数的数据类型
    it = None
    if isinstance(user, dict):
        it = user.items()
    elif isinstance(user, list):
        it = enumerate(user)
    else:
        print("Error found type(p1)=%s, type(p2)=%s" % (type(tmpdata), type(user)))
        return
    ## 开始遍历
    for key, val in it:
        print("Loop >>>>>>>>>> user key =", key, ",val =", val)
        print("Input tmp_data is ", type(tmpdata))

        if key in ignoreAttrs:
            print("Ignore user attr ", key)
            continue


        tmp_obj = None
        if isinstance(tmpdata, list):
            if len(tmpdata) - 1 < key:
                ### 表示user list个数比defaults要多
                tmpdata.append(val)
                continue
            else:
                tmp_obj = tmpdata[key]
                # tmp_obj = copy.copy(tmpdata[key])
                print(tmpdata)
        elif isinstance(tmpdata, dict):
            tmp_obj = tmpdata.get(key, 'not exist')

        print("tmp_data['%s'] = %s" % (key, tmp_obj))
        if not isinstance(tmp_obj, dict) and not isinstance(tmp_obj, list):
            ## 此时已经是一个叶子节点，其节点下为字符串，则直接复制
            print("Copy user node attr ['%s']='%s' to default node" % (key, val))
            print("But current default is '%s' to default node" % (tmpdata))
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

def fix_data(tmpdata, user):
    ## 删除多余的radio
    user_radios = user.get('device',{}).get('wireless',{}).get('max-radios')
    default_radios = tmpdata.get('device', {}).get('wireless', {}).get('radio')
    dradio_len = len(default_radios)
    if user_radios != dradio_len and user_radios != None and default_radios != None:
        for i in range(user_radios, dradio_len, 1):
            print("Delete default radio %d, start=%d, totoal=%d" % (i, user_radios, dradio_len))
            if i < dradio_len:
                default_radios.pop()

if __name__ == '__main__':
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

    ## 合并完成后修复数据
    fix_data(tmp_data, pro_data)

    ## python data --> json
    with open(json_fname, 'w', encoding='utf-8') as json_file:
        json.dump(tmp_data['device'], json_file, separators=(',', ': '), skipkeys=True, sort_keys=True, indent=2)
    #     # print(json.dumps(tmp_data, separators=(',',': '), skipkeys=True, sort_keys=True, indent=2))

    ## python data  -- > yaml
    with open("dist/%s" % pro_2ac, 'w', encoding='utf-8') as target_file:
        yaml.dump(tmp_data['device'], target_file)
        # print(json.dumps(tmp_data, separators=(',',': '), skipkeys=True, sort_keys=True, indent=2))

    ## json -- > yaml
    with open("data2.json", 'r', encoding='utf-8') as json_file:
        with open("dist/template.yaml",'w', encoding='utf-8') as target_file:
            dev_json=dict()
            loaded_json = json.load(json_file)
            dev_json['device'] = loaded_json
            yaml.dump(dev_json, target_file, default_flow_style=False)