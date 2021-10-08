from setuptools import setup


setup(name="tal_conan_utils",
      version="0.0.1",
      description="Helpers to create conanfiles",
      author="Tal Systems",
      url="https://github.com/tal-systems/tal-conan-utils",
      packages=["tal_conan_utils.py"],
      install_requires=['conan >= 1.40.0'],
      license="MIT"
)

