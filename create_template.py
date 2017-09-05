import os
import json,yaml,re
from functools import partial
import json_gen as y2j

def walk_files(dirname):
    files = []
    for name in os.listdir(dirname):

        path = os.path.join(dirname, name)
        obj = {}
        # print(path)
        # print("{} in {}".format(name, dirname))
        if name == 'md5sum':
            continue
        if os.path.isfile(path):
            obj = {
                'fname': name,
                'full_name': path
            }
            files.append(obj)
        else:
            files.extend(walk_files(path))
        # yield  obj
    return files

def create_dist(files, dirname, temp_dir_name):
    if not os.access(dirname, os.F_OK):
        os.makedirs(dirname)
    for file in iter(files):
        print("Produce file >>>>>>>>>>>>", file)
        user_yaml = file['full_name']
        (json_fname, extension) = os.path.splitext(file['fname'])
        user_target_json = os.path.join(dirname, "%s.json" % json_fname)

        ## 读取产品的yaml模版
        with open(user_yaml, 'r', encoding='utf-8') as yaml_file:
            pro_data = yaml.load(yaml_file)
            print(pro_data)
        ## 获得该产品的yaml模版对象
        pro_temp_name = pro_data.get('template_name')
        if pro_temp_name == None:
            print("Error file %s does not contain a template name" % file['full_name'])
            return
        template_yaml = os.path.join(temp_dir_name, "%s.yaml" % pro_temp_name)
        print("Produce template file >>>>>>>>>>>>", template_yaml)

        ## 读取默认的yaml模版
        with open(template_yaml, 'r', encoding='utf-8') as yaml_file:
            default_data = yaml.load(yaml_file)
            print(default_data)
        ## 合并dict

        tmp_data = dict(default_data)
        y2j.merge2(tmp_data, pro_data)
        # # tmp_data.update(pro_data)
        # # tmp_data['device']['wireless']['radio']
        # # tmp_data['device']['wireless']['teest']= 'abc'
        print(tmp_data)
        #
        ## 合并完成后修复数据
        y2j.fix_data(tmp_data, pro_data)
        #
        ## python data --> json
        with open(user_target_json, 'w', encoding='utf-8') as json_file:
            json.dump(tmp_data['device'], json_file, separators=(',', ': '), skipkeys=True, sort_keys=True, indent=2)

if __name__ == '__main__':
    templates = walk_files(dirname='src/template')
    print("Template yamls:",templates)
    ligos = walk_files(dirname='src/LigoWave')
    print("LigoWave yamls:",ligos)
    create_dist(ligos, dirname='dist/LigoWave', temp_dir_name='src/template')