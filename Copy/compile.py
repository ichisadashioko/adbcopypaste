import os
import time
import subprocess
import argparse


CWD = os.getcwd()
ANDROID_SDK_ROOT = os.environ['ANDROID_SDK_ROOT']
ANDROID_BUILD_TOOLS_VERSION = '30.0.3'
ANDROID_PLATFORM_VERSION = 30

ANDROID_BUILD_TOOLS_ROOT = os.path.join(
    ANDROID_SDK_ROOT,
    'build-tools',
    ANDROID_BUILD_TOOLS_VERSION,
)

DX_PATH = os.path.join(ANDROID_BUILD_TOOLS_ROOT, 'dx')

ANDROID_JAR_PATH = os.path.join(
    ANDROID_SDK_ROOT,
    'platforms',
    f'android-{ANDROID_PLATFORM_VERSION}',
    'android.jar',
)


CLASSES_DIR = os.path.join(CWD, 'classes')


def find_all_java_files(inpath: str, outlist: list):
    if os.path.isfile(inpath):
        _, ext = os.path.splitext(inpath)
        if ext.lower() == '.java':
            outlist.append(inpath)
    elif os.path.isdir(inpath):
        fns = os.listdir(inpath)
        for fn in fns:
            fpath = os.path.join(inpath, fn)
            find_all_java_files(
                inpath=fpath,
                outlist=outlist,
            )


if not os.path.exists(CLASSES_DIR):
    os.makedirs(CLASSES_DIR)

java_filepaths = []
find_all_java_files(
    inpath=CWD,
    outlist=java_filepaths,
)

compile_java_command = (
    f'javac -bootclasspath "{ANDROID_JAR_PATH}" ' +
    f'-d {CLASSES_DIR} -source 1.8 -target 1.8 ' +
    ' '.join(java_filepaths)
)

print(compile_java_command)
