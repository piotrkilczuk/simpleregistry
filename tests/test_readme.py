import hashlib
import pathlib
import re
from typing import List

import pytest

README_PATH = pathlib.Path(__file__).parent.parent / "README.md"
README_CHECKSUM_ALLOWED = "78070471bde83adb7ca8b4f42b9fb40e"


@pytest.fixture
def python_snippets():
    readme_contents_bytes = README_PATH.read_bytes()

    hash_md5 = hashlib.md5(readme_contents_bytes)
    assert hash_md5.hexdigest() == README_CHECKSUM_ALLOWED

    code_snippets = re.findall(
        r"```python(.*?)```", readme_contents_bytes.decode(), re.DOTALL
    )
    yield code_snippets


def test_all_snippets_working(python_snippets: List[str]):
    for snippet in python_snippets:
        exec(snippet)
