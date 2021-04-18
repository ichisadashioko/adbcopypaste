import os
import sys
import datetime
import subprocess

module_parent = os.path.dirname(os.path.abspath(__file__))
built_apk_filepath = 'app/build/outputs/apk/debug/app-debug.apk'

if not os.path.exists(built_apk_filepath):
    raise Exception('Cannot find ' + built_apk_filepath)

binary_basename = 'adbcopypaste'


def get_short_commit_hash():
    command = 'git rev-parse --short HEAD'
    print(command)
    cwd = module_parent
    print('cwd', cwd)
    ps = subprocess.Popen(
        args=command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
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
print('short_commit_hash', short_commit_hash)

built_time_float = os.path.getmtime(built_apk_filepath)
print('built_time_float', built_time_float)

# TODO check if timezone will affect the parsing
built_time_str = datetime.datetime.fromtimestamp(built_time_float).strftime('%Y%m%d')

# TODO hack on the update-artifact codebase to update the apk without being zipped the second time as an apk file is a zip archive
artifact_name = f'{binary_basename}-{built_time_str}-{short_commit_hash}'
artifact_filename = f'{artifact_name}.apk'
artifact_filepath = os.path.join(module_parent, artifact_filename)
os.rename(built_apk_filepath, artifact_filepath)

if 'GITHUB_ENV' in os.environ:
    github_env_setter_filepath = os.environ['GITHUB_ENV']
    print('GITHUB_ENV', github_env_setter_filepath)
    # TODO write artifact file name / path to GITHUB_ENV
    with open(github_env_setter_filepath, mode='ab') as outfile:
        outfile.write(
            (
                f'ADBCOPYPASTE_ARTIFACT_NAME={artifact_name}\n' +
                f'ADBCOPYPASTE_ARTIFACT_FILENAME={artifact_filename}'
            ).encode('utf-8')
        )
else:
    print('Cannot find GITHUB_ENV variable. Probably not running in Github Actions environment')
