cmake_minimum_required(VERSION 3.27)
project(egg)

set(CMAKE_CXX_STANDARD 23)
include_directories(extern/pybind11/include)

include(FetchContent)
FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)


# search for clang-tidy
find_program(CLANG_TIDY_EXE NAMES "clang-tidy" REQUIRED)

# setup clang-tidy command from executable + options
set(CLANG_TIDY_COMMAND "${CLANG_TIDY_EXE}")

add_executable(yolk yolk/main.cpp
        yolk/instruction/instructions.h
        yolk/instruction/instructions.cpp
        yolk/instruction/instructionArgs.h
        yolk/instruction/instructionArgs.cpp)

add_executable(yolk-test yolk/main-test.cpp
        yolk/instruction/instructions.h
        yolk/instruction/instructions.cpp
        yolk/instruction/instructionArgs.h
        yolk/instruction/instructionArgs.cpp
        yolk/instruction/instructionsTest.cpp
        yolk/utils/testUtils.h)

target_link_libraries(
        yolk-test
        GTest::gtest_main
)

target_include_directories(yolk PRIVATE extern/pybind11/include)
target_include_directories(yolk-test PRIVATE extern/pybind11/include)


set_target_properties(yolk PROPERTIES CXX_CLANG_TIDY "${CLANG_TIDY_COMMAND}")
set_target_properties(yolk-test PROPERTIES CXX_CLANG_TIDY "${CLANG_TIDY_COMMAND}")
