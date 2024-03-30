#pragma once

#include <vector>

#include "gtest/gtest.h"

namespace testUtils {

    template<typename t>
    [[nodiscard]] testing::AssertionResult VectorsEqual (std::vector<t> buffer, std::vector<t> expected_buffer) {
        if (buffer.size() != expected_buffer.size()) {
             return (testing::AssertionFailure()
                << "buffer.width() is: " << (int) buffer.size() << ". Expected: " << (int) expected_buffer.size());
        }
        for(auto i=0; i<buffer.size(); i++){
            if (buffer[i] != expected_buffer[i]) {
                 return (testing::AssertionFailure()
                    << "buffer[" << i << "] is: " << (int) buffer[i] << ". Expected: " << (int) expected_buffer[i]);
            }
        }
        return testing::AssertionSuccess();
    }

}