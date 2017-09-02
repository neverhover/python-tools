from xml.dom.minidom import Document
import json
import re

### 全局属性集合
nodeAttrs = ({
    "type",
    "default",
    "item_type",
    "item_length",
    "range",
    "length",
    "key",
    "show",
    "required",
    "range",
    "maxitems",
    "item_range"
})
### 全局层级替换，即缩减为上一级
nodeLevels = ({
    "spec",
    "default"
})

### 全局忽略
nodeIgnore = ({
    "$template",
    "$parent",
    "$selector"
})

def writeToFile(self, filename, encoding='utf-8'):
    with open(filename, "w", encoding=encoding) as f:
        self.writexml(f, addindent='  ', newl='\n', encoding=encoding)
        # f.write(doc.toprettyxml(indent="  "))


def loadJsonToMem(filename, encoding='utf-8'):
    with open(filename, "r", encoding=encoding) as f:
        data = json.load(f)
        return data

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def transDictToXML(obj, parentObj, doc):
    for key, val in obj.items():

        if isinstance(key, str) and isinstance(val, list):
            ## 遍历为数组的情况
            for li_idx, li_val in enumerate(val):
                print(key, ": ", "index: ", li_idx, li_val)
                li_key = key

                if li_key in nodeIgnore:
                    if li_key == "$template":
                        parentObj.setAttribute("type", "list")
                    continue
                ## 如果key是list，则转化名称
                if li_key == "list":
                    li_key="option"

                ## 检测其是否含有$parent以及$selector
                ## 并将新节点挂到其节点上
                li_key = re.sub("_", "-", li_key)
                tmp_obj = doc.createElement(li_key)
                found = False
                if  isinstance(li_val, list) or  isinstance(li_val, dict):
                    pnode = li_val.get("$parent", 'not exist')
                    snode = li_val.get("$selector", 'not exist')

                    if pnode != 'not exist' and snode != 'not exist':
                        pc_list = parentObj.childNodes
                        for pck in pc_list:
                            if pck.nodeName == pnode:
                                print("zzzzzzz", pck)

                                for sck in pck.childNodes:
                                    print("ssssss", sck)
                                    if sck.getAttribute("value") == snode:
                                        print("cccc", sck.nodeValue)
                                    if getText(sck.childNodes) == snode:
                                        print("oooooo", sck)
                                        sck.setAttribute("value", snode)
                                        sck.removeChild(sck.childNodes[0])
                                        sck.appendChild(tmp_obj)
                                        found = True
                                break


                #
                #
                #                     if sck.getAttribute("value") == snode:
                #                         print("cccc", sck)
                #                 pck.appendChild(tmp_obj)
                #                 break
                #
                if not found:
                    parentObj.appendChild(tmp_obj)


                if li_key == "option":
                    parentObj.setAttribute("type", "choice")
                    tmp_val = doc.createTextNode(str(li_val))
                    tmp_obj.appendChild(tmp_val)
                    continue

                if not isinstance(li_val, list) and not isinstance(li_val, dict):
                    if li_val in nodeAttrs:
                        parentObj.setAttribute(li_key, li_val)
                    else:
                        tmp_val = doc.createTextNode(str(li_val))
                        tmp_obj.appendChild(tmp_val)
                else:
                    transDictToXML(li_val, tmp_obj, doc)

                # tmp_obj = doc.createElement(key)
                # parentObj.appendChild(tmp_obj)
                #

        elif isinstance(key, str) and isinstance(val, dict):
            ### 遍历为dict节点的情况
            # print("jump ", key)
            if key in nodeLevels:
                transDictToXML(val, parentObj, doc)
            elif key == "range" or key == "item_range":
                parentObj.setAttribute(key, "%d..%d" % (val["min"], val["max"]))
            else:
                # print("dict key create:", key)
                ## 创建之前需要判断一下key的属性key的值是否与key相等
                key = val.get("key", key)
                key = re.sub("_", "-", key)
                tmp_obj = doc.createElement(key)
                parentObj.appendChild(tmp_obj)
                transDictToXML(val, tmp_obj, doc)

        elif isinstance(key, str) and not isinstance(val, dict):
            ### 遍历为非dict 非list节点的情况
            if key in nodeIgnore:
                if key == "$template":
                    parentObj.setAttribute("type", "list")
                continue
            ### 转换属性
            t_val = str(val)
            key = re.sub("_","-", key)
            if isinstance(val, bool):
                t_val = str.lower(t_val)
            if key in nodeAttrs:
                if key != "key":
                    parentObj.setAttribute(key, t_val)
            else:
                # print("text key create:", key)
                tmp_obj = doc.createElement(key)
                parentObj.appendChild(tmp_obj)
                tmp_val = doc.createTextNode(t_val)
                tmp_obj.appendChild(tmp_val)

        else:
            print("------ start ------")
            print(key)
            print(val)
            print(type(val))
            print("------ end ------")


doc = Document()

notes = doc.createComment("This document is writen by Zhangleyi@ligowave.com")
doc.appendChild(notes)

root = doc.createElement("device")
doc.appendChild(root)
#
# aperson = doc.createElement("person")
# root.appendChild(aperson)
#
# name = doc.createElement("name")
# aperson.appendChild(name)
#
# personname = doc.createTextNode("Annie")
# name.appendChild(personname)
# name.setAttribute("type", "string")



filename = "data.xml"

json_obj = loadJsonToMem("data2.json")
print(json_obj['wireless']['scenario'])

transDictToXML(json_obj, root, doc)
writeToFile(doc, filename)

# json_str = json.dumps(data)
# print(json_str)
