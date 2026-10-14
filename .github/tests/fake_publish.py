"""Run the real publisher with the existing filesystem AWS command boundary.

Transport-specific tests exercise the real SDK separately against local HTTP.
"""
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import publish


class CommandS3(publish.S3):
    def enable_transfers(self, workers=32):
        pass

    def upload(self, path, key):
        subprocess.run(['aws', 's3', 'cp', str(path), self.target + '/' + key,
                        '--only-show-errors', '--metadata', 'sha256=' + publish.file_integrity(path)[1]], check=True)

    def head(self, key):
        result = subprocess.run(['aws', 's3api', 'head-object', '--bucket', self.bucket,
                                 '--key', self.object_key(key), '--output', 'json'], capture_output=True, text=True)
        if result.returncode:
            if re.search(r'\((?:404|NoSuchKey|NotFound)\) when calling the HeadObject operation', result.stderr):
                return None
            raise ValueError('Cannot HEAD target S3 object: ' + result.stderr.strip())
        return json.loads(result.stdout)


if __name__ == '__main__':
    publish.S3 = CommandS3
    try:
        publish.main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print('Publish failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
