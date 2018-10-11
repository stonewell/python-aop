# package initialize
import sys

from aop_module_importer import AopModuleImporter


def install():
    sys.meta_path = [AopModuleImporter()]

def uninstall():
    pass
