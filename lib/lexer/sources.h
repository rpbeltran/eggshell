#pragma once
#include <cstdint>

class SourceSlice {

  const uintptr_t offset;
  const uintptr_t length;

 public:
  SourceSlice(uintptr_t _offset, uintptr_t _length):
        offset(_offset), length(_length)
  {}

  const uintptr_t get_offset() {
    return offset;
  }

  const uintptr_t get_length() {
    return length;
  }
};
