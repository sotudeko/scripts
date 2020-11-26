from conans import ConanFile, CMake, tools


class DemoappIncConan(ConanFile):
    name = "demoapp_inc"
    version = "0.1"
    exports_sources = "src/*"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="src")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="src")
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["demoapp_inc"]


