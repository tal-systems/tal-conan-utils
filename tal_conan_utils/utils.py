from conans import ConanFile, CMake, tools
import os


def get_version():
    git = tools.Git()
    try:
        tag = git.get_tag()
        if tag:
            return tag
        return git.get_branch()
    except:
        return None


def make_conan(lib_name, requirements):
    class TalConan(ConanFile):
        name = f"tal.{lib_name}"
 #       version = get_version()
        license = ""
        author = ""
        url = f"https://github.com/tal-systems/tal.{lib_name}"
        description = ""
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}
        generators = "cmake"
        requires = requirements

        def config_options(self):
            if self.settings.os == "Windows":
                del self.options.fPIC

        def _configure_cmake(self):
            cmake = CMake(self)
            cmake.configure(source_folder=f"tal.{lib_name}")
            return cmake

        def source(self):
            self.run(f"git clone --depth 1 --branch {self.version} git@github.com:tal-systems/tal.{lib_name}.git")

        def build(self):
            cmake = self._configure_cmake()
            cmake.build()

        def package(self):
            cmake = self._configure_cmake()
            cmake.install()

        def layout(self):
            self.cpp_info.requires = requirements
            self.cpp.source.includedirs = ["lib/include"]
            self.cpp.build.libdirs = ["build/lib"]
            self.cpp.build.libs = [f"tal_{lib_name}"]
            self.cpp.package.libs = [f"tal_{lib_name}"]
    return TalConan


def make_test_conan(lib_name, requirements=[]):
    class TalTestConan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        generators = "cmake"
        requires = requirements

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def imports(self):
            self.copy("*.dll", dst="bin", src="bin")
            self.copy("*.dylib*", dst="bin", src="lib")
            self.copy('*.so*', dst='bin', src='lib')

        def test(self):
            if not tools.cross_building(self):
                os.chdir("bin")
                self.run(".%stest_app" % os.sep)
    return TalTestConan

