"""Check release downloads against the upstream SHA512 manifest."""
import hashlib
import sys
from pathlib import Path

lines = Path(sys.argv[1]).read_text().splitlines()
checksums = {}
for line in lines:
    parts = line.split()
    if len(parts) == 2:
        checksums[parts[1].lstrip('*')] = parts[0]
for local, upstream in zip(sys.argv[2::2], sys.argv[3::2]):
    actual = hashlib.file_digest(open(local, 'rb'), 'sha512').hexdigest()
    if checksums.get(upstream) != actual:
        raise SystemExit(f'Checksum mismatch: {upstream}')
    print(f'Verified {upstream}')
