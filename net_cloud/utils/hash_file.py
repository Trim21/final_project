import hashlib
from pathlib import Path
from typing import Union


def md5(file_content: Union[bytes, str] = None,
        file_path: Union[Path, str] = None, ):
    if file_content is None:
        if file_path is None:
            raise ValueError('file_content and file_path can\'t be both None')
        file_content = Path(file_path).read_bytes()
    return _md5(file_content)


def _md5(content: bytes):
    m = hashlib.md5(content)
    return m.hexdigest()


if __name__ == '__main__':
    filepath = Path(
        r'C:\Users\Trim21\proj\final_project\sync_dir\qweqwe'
    ).absolute()
    h = md5(file_path=filepath)
    print(h)
