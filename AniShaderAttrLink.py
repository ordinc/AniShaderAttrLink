#coding: utf-8
import re
import collections
import pymel.core as pm
import mgear.core.attribute as attribute


def get_count_repetitions(long_name_list):
    """列表统计重复次数。.

    统计列表中重复元素和重复元素次数并返回一个新的列表。

    Args:
        long_name_list (list): 要统计的列表。

    Returns:
        list: 返回的新的列表。For example: [repeated element (str), number of repetitions (int)]

    """
    list = []
    dic = collections.Counter(long_name_list)
    for i in dic:
        list.append([i, dic[i]])

    return list


def get_sou_udAttr(sou_list):
    """获取链接属性源物体的用户自定义属性.

    获取链接属性源物体的以数字索引为结尾的用户自定义属性，并返回一个新的列表。

    Args:
        sou_list (list): 要获取的链接源物体列表。

    Returns:
        list: 返回的获取到的自定义属性的列表。

    """
    list = [x for x in sou_list if re.match('.*\d$', x)]

    return list


def get_sou_string_udAttr(sou_list):
    """获取链接属性源物体的不包含数字的用户自定义属性.

    获取链接属性源物体的不包含数字的用户自定义属性，并返回一个新的列表。

    Args:
        sou_list (list): 要获取的链接源物体列表。

    Returns:
        list: 返回的获取到的自定义属性的列表。

    """
    list = []
    for x in sou_list:
        pattern = re.compile('[0-9]+')
        match = pattern.findall(x)
        if not match:
            list.append(x)

    return list


def get_des_attrs(key_attr, link, nameSpace=None):
    """获取链接属性目的地物体的多属性.

    获取链接属性目的地物体的多属性，并返回一个新的列表。

    Args:
        key_attr (list): 用户自定义重复属性的属性名称列表。
        link (str): 要获取的链接属性目的地物体名称。
        nameSpace (boolean):  是否存在namespace命名空间。
    Returns:
        list: 返回的获取到的多属性的列表。

    """
    des = []
    if nameSpace:
        des_attrs = pm.listAttr(
            nameSpace + link.split("AniShaderAttrLink__")[1], multi=True)
    else:
        des_attrs = pm.listAttr(link.split(
            "AniShaderAttrLink__")[1], multi=True)
    for a in key_attr:
        for t in des_attrs:
            if re.match('.*%s$' % a, t):
                des.append(t)

    return des


def connect_multi(node, nameSpace=False, getValue=True):
    """链接属性目的地物体的多属性.

    Args:
        node (str): 链接属性目的地物体的名称。
        nameSpace (boolean):  是否存在namespace命名空间。
        getValue (boolean): 是否获取原始属性的数值。
    """
    if node:
        shaderLink = pm.ls("{}".format(node))
    else:
        shaderLink = pm.ls('*:AniShaderAttrLink__*')
    if shaderLink:
        for link in shaderLink:
            attr = get_sou_udAttr(pm.listAttr(link, ud=True))
            key_attr = set([x.split('_')[1] for x in attr])
            if nameSpace:
                nameSpace = (link.split(':AniShaderAttrLink__')[
                    0].replace('rig', 'shd')).split('__')[0] + '_:'
                des = get_des_attrs(key_attr, link, nameSpace)
                for i, t in enumerate(attr):
                    base_link = pm.listConnections('{}.{}'.format(link.split("AniShaderAttrLink__")[1],des[i]), d=False, s=True,p=True)
                    if getValue:
                        pm.connectAttr('{}.{}'.format(
                            nameSpace + link.split("AniShaderAttrLink__")[1], des[i]), '{}.{}'.format(link, t), f=True)
                        pm.disconnectAttr('{}.{}'.format(
                            nameSpace + link.split("AniShaderAttrLink__")[1], des[i]), '{}.{}'.format(link, t))
                        pm.connectAttr('{}.{}'.format(link, t), '{}.{}'.format(
                            nameSpace + link.split("AniShaderAttrLink__")[1], des[i]), f=True)
                    else:
                        pm.connectAttr('{}.{}'.format(link, t), '{}.{}'.format(
                            nameSpace + link.split("AniShaderAttrLink__")[1], des[i]), f=True)
                    if base_link:
                        pm.connectAttr('{}'.format(base_link[0]), '{}.{}'.format(node, t), f=True)
            else:
                des = get_des_attrs(key_attr, link, nameSpace=None)
                for i, t in enumerate(attr):
                    base_link = pm.listConnections('{}.{}'.format(link.split("AniShaderAttrLink__")[1],des[i]), d=False, s=True,p=True)
                    if getValue:
                        pm.connectAttr('{}.{}'.format(link.split("AniShaderAttrLink__")[
                                       1], des[i]), '{}.{}'.format(link, t), f=True)
                        pm.disconnectAttr('{}.{}'.format(link.split("AniShaderAttrLink__")[
                                          1], des[i]), '{}.{}'.format(link, t))
                        pm.connectAttr('{}.{}'.format(link, t), '{}.{}'.format(
                            link.split("AniShaderAttrLink__")[1], des[i]), f=True)
                    else:
                        pm.connectAttr('{}.{}'.format(link, t), '{}.{}'.format(
                            link.split("AniShaderAttrLink__")[1], des[i]), f=True)
                    if base_link:
                        pm.connectAttr('{}'.format(base_link[0]), '{}.{}'.format(node, t), f=True)

def connect_single(node, nameSpace=False, getValue=True):
    """链接属性目的地物体的单属性.

    Args:
        node (str): 链接属性目的地物体的名称。
        nameSpace (boolean):  是否存在namespace命名空间。
        getValue (boolean): 是否获取原始属性的数值。
    """
    if node:
        shaderLink = pm.ls("{}".format(node))
    else:
        shaderLink = pm.ls('*:AniShaderAttrLink__*')
    if shaderLink:
        for link in shaderLink:
            attr = get_sou_string_udAttr(pm.listAttr(link, ud=True))
            key_attr = set([x.split('link_')[1] for x in attr])
            for index, attr in enumerate(key_attr):
                base_link = pm.listConnections('{}.{}'.format(link.split("AniShaderAttrLink__")[1],attr), d=False, s=True,p=True)
                if nameSpace:
                    nameSpace = (link.split(':AniShaderAttrLink__')[
                        0].replace('rig', 'shd')).split('__')[0] + '_:'
                    if getValue:
                        pm.connectAttr('{}.{}'.format(nameSpace + link.split("AniShaderAttrLink__")[
                                       1], attr), '{}.{}'.format(link, '{}_{}'.format("link", attr)), f=True)
                        pm.disconnectAttr('{}.{}'.format(nameSpace + link.split("AniShaderAttrLink__")[
                                          1], attr), '{}.{}'.format(link, '{}_{}'.format("link", attr)))
                        pm.connectAttr('{}.{}'.format(link, '{}_{}'.format("link", attr)), '{}.{}'.format(
                            nameSpace + link.split("AniShaderAttrLink__")[1], attr), f=True)
                    else:
                        pm.connectAttr('{}.{}'.format(link, '{}_{}'.format("link", attr)), '{}.{}'.format(
                            nameSpace + link.split("AniShaderAttrLink__")[1], attr), f=True)
                else:
                    if getValue:
                        pm.connectAttr('{}.{}'.format(link.split("AniShaderAttrLink__")[
                                       1], attr), '{}.{}'.format(link, '{}_{}'.format("link", attr)), f=True)
                        pm.disconnectAttr('{}.{}'.format(link.split("AniShaderAttrLink__")[
                                          1], attr), '{}.{}'.format(link, '{}_{}'.format("link", attr)))
                        pm.connectAttr('{}.{}'.format(link, '{}_{}'.format("link", attr)), '{}.{}'.format(
                            link.split("AniShaderAttrLink__")[1], attr), f=True)
                    else:
                        pm.connectAttr('{}.{}'.format(link, '{}_{}'.format("link", attr)), '{}.{}'.format(
                            link.split("AniShaderAttrLink__")[1], attr), f=True)
                if base_link:
                    pm.connectAttr('{}'.format(base_link[0]), '{}.link_{}'.format(node, attr), f=True)

def create_AniShaderAttrLink_node(node_name, long_name_list,nameSpace=False, getValue=True):
    """创建具有链接属性的代理物体，并链接到相关目的地的节点属性上.

    Args:
        node_name (str): 链接属性目的地物体的名称。
        long_name_list (list): 链接属性的长名称列表。

    """
    proxy_gp_name = '{}__{}'.format("AniShaderAttrLink", node_name)
    if not pm.objExists(proxy_gp_name):
        proxy_grp = pm.group(em=1, n=proxy_gp_name)
        attribute.lockAttribute(proxy_grp, attributes=[
                                'tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
    for value in get_count_repetitions(long_name_list):
        if value[1] > 1:
            for index in range(value[1]):
                if value[0] == 'color':
                    if not pm.PyNode(proxy_gp_name).hasAttr('{}_{}_{}'.format("link", value[0], index)):
                        attribute.addColorAttribute(pm.PyNode(proxy_gp_name), '{}_{}_{}'.format(
                            "link", value[0], index), value=None, niceName=None, shortName=None, keyable=True, readable=True, storable=True, writable=True)
                else:
                    if not pm.PyNode(proxy_gp_name).hasAttr('{}_{}_{}'.format("link", value[0], index)):
                        attribute.addAttribute(pm.PyNode(proxy_gp_name), '{}_{}_{}'.format(
                            "link", value[0], index), "float", value=None, niceName=None, shortName=None, minValue=None, maxValue=None, keyable=True, readable=True, storable=True, writable=True, channelBox=False)
        if value[1] == 1:
            if not pm.PyNode(proxy_gp_name).hasAttr('{}_{}'.format("link", value[0])):
                attribute.addAttribute(pm.PyNode(proxy_gp_name), '{}_{}'.format(
                    "link", value[0]), "float", value=None, niceName=None, shortName=None, minValue=None, maxValue=None, keyable=True, readable=True, storable=True, writable=True, channelBox=False)

    connect_multi(proxy_gp_name, nameSpace, getValue)
    connect_single(proxy_gp_name, nameSpace, getValue)


###################################################

'''
node_name = "ramp1"
long_name_list = ['color', 'color', 'noise',
                  'uWave', 'vWave', 'position', 'position']
create_AniShaderAttrLink_node(node_name, long_name_list)

connect_multi(None , nameSpace = True, getValue=False)
connect_single(None , nameSpace = True, getValue=False)
'''
