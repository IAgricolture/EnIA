#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage") #non usato al momento
use_plugin("python.distutils")


name = "EnIA"
default_task = "publish"


@init
def set_properties(project):
    project.set_property("dir_source_main_python", "src/logic")
    project.set_property("dir_source_main_scripts", "src/scripts")
    project.set_property("dir_docs", "Documents/docs")
    project.set_property('coverage_break_build', False) #Evita di far fallire la build per coverage inferiore al 70%

    #set one file for testing

    project.build_depends_on("flask")
    project.build_depends_on("flask_login")
    project.build_depends_on("flask_pymongo")
    project.build_depends_on("flask_cors")
    project.build_depends_on("pymongo")
    project.build_depends_on("requests")
    project.build_depends_on("mockito")
    project.build_depends_on("geopy")
    project.build_depends_on("selenium")
    project.build_depends_on("requests_mock")
