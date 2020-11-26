# Minimum version of CMake required to build this project
cmake_minimum_required(VERSION 3.0)

# Name of the project
project(Project)

# Include Conan dependencies
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

# This will setup conan environment. Without this, including our dependencies
# would fail
conan_basic_setup()

# Compile main.cpp
add_executable(project src/main.cpp)

# Link the dependencies with our binary
target_link_libraries(project ${CONAN_LIBS})


