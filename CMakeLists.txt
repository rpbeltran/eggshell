cmake_minimum_required(VERSION 3.27)
project(egg)

set(CMAKE_CXX_STANDARD 23)

include(FetchContent)
FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_executable(yolk yolk/main.cpp)

add_executable(yolk-test yolk/main-test.cpp)

target_link_libraries(
        yolk-test
        GTest::gtest_main
)
