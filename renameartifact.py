import os
import sys
import subprocess

built_apk_filepath = 'app/build/outputs/apk/debug/app-debug.apk'

if not os.path.exists(built_apk_filepath):
    raise Exception('Cannot find ' + built_apk_filepath)

binary_basename = 'adbcopypaste'


def get_short_commit_hash():
    command = f'git rev-parse --short HEAD'
    ps = subprocess.Popen(
        command,
        cwd=os.path.dirname(__file__),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = ps.communicate(timeout=2)

    log = {
        'returncode': ps.returncode,
        'stdout': stdout,
        'stderr': stderr,
    }

    if ps.returncode != 0:
        print(log, file=sys.stderr)
        raise Exception('git did not return 0')
    elif len(stderr) != 0:
        print(log, file=sys.stderr)
        raise Exception('there is something in stderr')
    elif len(stdout) == 0:
        print(log, file=sys.stderr)
        raise Exception('stdout is empty')

    stdout_str = stdout.decode('ascii')
    return stdout_str.strip()


short_commit_hash = get_short_commit_hash()
built_time = os.path.getmtime(built_apk_filepath)
print('short_commit_hash', short_commit_hash)
print('built_time', built_time)
print('GITHUB_ENV', os.environ['GITHUB_ENV'])
