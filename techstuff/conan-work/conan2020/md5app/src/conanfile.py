from conans import ConanFile, CMake, tools

class Md5appConan(ConanFile):
    name = "md5app"
    version = "0.1"
    generators = "cmake"
    exports_sources = "src/*"
    
    def build(self):
        cmake = CMake(self)
        # The CMakeLists.txt file must be in `source_folder`
        cmake.configure(source_folder="src")
        cmake.build()
 
    def requirements(self):
        self.requires("poco/1.9.3")
        self.requires("zlib/1.2.8")

    def package(self):
        # Copy headers to the include folder and libraries to the lib folder
        self.copy("*.h", dst="include", src="src")
        self.copy("*.a", dst="lib", keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = ["md5app"]

