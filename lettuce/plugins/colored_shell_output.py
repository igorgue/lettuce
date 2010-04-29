# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import re
import sys
from lettuce.terrain import after
from lettuce.terrain import before

def wrap_file_and_line(string, start, end):
    return re.sub(r'([#] [^:]+[:]\d+)', '%s\g<1>%s' % (start, end), string)

def wp(l):
    if l.startswith("\033[1;32m"):
        l = l.replace(" |", "\033[1;37m |\033[1;32m")
    if l.startswith("\033[1;30m"):
        l = l.replace(" |", "\033[1;37m |\033[1;30m")

    return l

def write_out(what):
    sys.stdout.write(wp(what))

@before.each_step
def print_step_running(step):
    string = step.represent_string(step.sentence)
    string = wrap_file_and_line(string, '\033[1;30m', '\033[0m')
    write_out("\033[1;30m%s" % string)
    if step.data_list:
        for line in step.represent_data_list().splitlines():
            write_out("\033[1;30m%s\033[0m\n" % line)

@after.each_step
def print_step_ran(step):
    if step.data_list:
        write_out("\033[A" * (len(step.data_list) + 1))

    string = step.represent_string(step.sentence)

    string = wrap_file_and_line(string, '\033[1;30m', '\033[0m')

    if step.failed:
        color = "\033[0;31m"
    else:
        color = "\033[1;32m"

    write_out("\033[A%s%s" % (color, string))

    if step.data_list:
        for line in step.represent_data_list().splitlines():
            write_out("%s%s\033[0m\n" % (color, line))

    if step.failed:
        sys.stdout.write(color)
        pspaced = lambda x: sys.stdout.write("%s%s" % (" " * step.indentation, x))
        lines = step.why.traceback.splitlines()

        for pindex, line in enumerate(lines):
            pspaced(line)
            if pindex + 1 < len(lines):
                sys.stdout.write("\n")

        sys.stdout.write("\033[0m\n")

@before.each_scenario
def print_scenario_running(scenario):
    string = scenario.represented()
    string = wrap_file_and_line(string, '\033[1;30m', '\033[0m')
    write_out("\033[1;37m%s" % string)

@before.each_feature
def print_feature_running(feature):
    string = feature.represented()
    lines = string.splitlines()

    write_out("\n")
    for line in lines:
        line = wrap_file_and_line(line, '\033[1;30m', '\033[0m')
        write_out("\033[1;37m%s\n" % line)

    write_out("\n")

@after.all
def print_end(total):
    write_out("\n")

    word = total.features_ran > 1 and "features" or "feature"
    write_out("\033[1;37m%d %s (\033[1;32m%d passed\033[1;37m)\033[0m\n" % (
        total.features_ran,
        word,
        total.features_passed
        )
    )

    word = total.scenarios_ran > 1 and "scenarios" or "scenario"
    write_out("\033[1;37m%d %s (\033[1;32m%d passed\033[1;37m)\033[0m\n" % (
        total.scenarios_ran,
        word,
        total.scenarios_passed
        )
    )

    word = total.steps > 1 and "steps" or "step"
    write_out("\033[1;37m%d %s (\033[1;32m%d passed\033[1;37m)\033[0m\n" % (
        total.steps,
        word,
        total.steps_passed
        )
    )

def print_no_features_found(where):
    where = os.path.relpath(where)
    if not where.startswith(os.sep):
        where = '.%s%s' % (os.sep, where)

    write_out('\033[1;31mOops!\033[0m\n')
    write_out(
        '\033[1;37mcould not find features at '
        '\033[1;33m%s\033[0m\n' % where
    )