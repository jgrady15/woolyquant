cmake_minimum_required(VERSION 3.4)
project(smart-pairs)
set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} "/path/to/pybind11") 
set(pybind11_DIR "/path/to/pybind11/lib/cmake/pybind11")
find_package(pybind11 REQUIRED)
pybind11_add_module(stockPair stockPair.cc)

