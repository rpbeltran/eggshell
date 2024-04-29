#pragma once

#include <vector>

#include "gtest/gtest.h"

namespace testUtils {

template <typename t>
[[nodiscard]] auto VectorsEqual(
    std::vector<t> buffer, std::vector<t> expected_buffer,
    std::string & error_prefix) -> testing::AssertionResult {
  if (buffer.size() != expected_buffer.size()) {
    return (testing::AssertionFailure()
            << error_prefix
            << "buffer.width() is: " << static_cast<int>(buffer.size())
            << ". Expected: " << static_cast<int>(expected_buffer.size()));
  }
  for (auto i = 0; i < buffer.size(); i++) {
    if (buffer[i] != expected_buffer[i]) {
      return (testing::AssertionFailure()
              << error_prefix << "buffer[" << i
              << "] is: " << static_cast<int>(buffer[i])
              << ". Expected: " << static_cast<int>(expected_buffer[i]));
    }
  }
  return testing::AssertionSuccess();
}

}  // namespace testUtils