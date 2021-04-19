import os
import time
import subprocess
import argparse
import shutil


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

BINARY_NAME = 'shellcopy'


def find_files_by_extension(inpath: str, inext: str, outlist: list):
    if os.path.isfile(inpath):
        _, ext = os.path.splitext(inpath)
        if ext.lower() == inext:
            outlist.append(inpath)
    elif os.path.isdir(inpath):
        fns = os.listdir(inpath)
        for fn in fns:
            fpath = os.path.join(inpath, fn)
            find_files_by_extension(
                inpath=fpath,
                inext=inext,
                outlist=outlist,
            )


def shell(
    args,
    cwd=None,
    timeout=5,
):
    ps = subprocess.Popen(
        args=args,
        cwd=cwd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = ps.communicate(timeout=timeout)
    if len(stdout) != 0:
        print('stdout')
        print(stdout.decode('ascii'))
    if len(stderr) != 0:
        print('stderr')
        print(stderr.decode('ascii'))
    return ps.returncode

if os.path.exists(CLASSES_DIR):
    shutil.rmtree(CLASSES_DIR)

if not os.path.exists(CLASSES_DIR):
    os.makedirs(CLASSES_DIR)

java_filepaths = []
find_files_by_extension(
    inpath=CWD,
    inext='.java',
    outlist=java_filepaths,
)

compile_java_command = (
    f'javac -bootclasspath "{ANDROID_JAR_PATH}" ' +
    f'-d {CLASSES_DIR} -source 1.8 -target 1.8 ' +
    ' '.join(java_filepaths)
)

print(compile_java_command)
print('returncode', shell(
    args=compile_java_command,
    cwd=CWD,
))

compile_dex_command = (
    f'{DX_PATH} --dex ' +
    f'--output {BINARY_NAME}.dex ' +
    CLASSES_DIR
)

print(compile_dex_command)
print('returncode', shell(
    args=compile_dex_command,
    cwd=CWD,
))
