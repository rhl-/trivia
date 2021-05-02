
import distutils.text_file
from pathlib import Path
from typing import List

def _parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(filename))).readlines()

setup(name='trivia game',
      version='0.1',
      description='Uses OpenTDB+darkslide to generate a trivia game'
      url='http://github.com/rhl-/trivia',
      author='Ryan H. Lewis',
      author_email='me@ryanlewis.net',
      license='BSD-3',
      packages=['trivia_game'],
      install_requires=_parse_requirements('requirements.txt'),
      zip_safe=False)
