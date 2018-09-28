__author__ = 'amir'
import os
import fnmatch


def getPack(path):
    Jclass = os.path.splitext(os.path.basename(path))[0]
    with open(path, "r") as f:
        for line in f:
            if "package " in line and ";" in line:
                pack = line.split(";")[0].split("package ")[1]
                return pack, "{0}.{1}".format(pack, Jclass)
    return "", Jclass


def projectPathPacks(path):
    matches = {}
    for dirName, subdirList, fileList in os.walk(path):
        for filename in fnmatch.filter(fileList, '*.java'):
            pathToJava = os.path.join(dirName, filename)
            pack, classpath = getPack(pathToJava)
            matches[classpath] = pathToJava[len(path) + 1:]
    return matches
