from __future__ import print_function

import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import jinja2

NAMES = ("issa_server_a_host", "issa_server_a_port", "issa_server_b_host", "issa_server_b_port", "issa_server_c_host",
         "issa_server_c_port")


def render(tpl_path, **kwargs):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')).get_template(filename).render(**kwargs)


def parser_vars_into_globals(filename):
    parser = configparser.ConfigParser()
    parser.read(filename)
    for name in NAMES:
        globals()[name] = parser.get('DEFAULT', name)
        """获取指点section下指点option的值"""


def main():
    parser_vars_into_globals('base.cfg')
    with open('pass_service1.xml', 'w') as f:
        f.write(render('pass_service1_template.xml', **globals()))

    with open('pass_service2.xml', 'w') as f:
        f.write(render('pass_service2_template.xml', **globals()))


if __name__ == '__main__':
    main()

"""ConfigParser 是用来读取配置文件的包
   括号“[ ]”内包含的为section。紧接着section 为类似于key-value 的options 的配置内容。
   使用ConfigParser 首选需要初始化实例，并读取配置文件
   import configparser
   config = configparser.ConfigParser()
   config.read("ini", encoding="utf-8")
"""
