#include <array>
#include <cstddef>
#include <cstdint>
#include <format>
#include <span>
#include <string>
#include <vector>

#include "instructionArgs.h"

namespace Instructions {

    template <typename int_val_t>
    int_val_t read_from_generic (const std::vector<uint8_t> & buffer, uint8_t pos) {
        int_val_t val = 0;
        for (int i = 0; i < sizeof (int_val_t); i++) {
            val <<= 8;
            val += buffer.at(pos + i);
        }
        return val;
    }

    void NameArgument::read_from (const std::vector<uint8_t> & buffer, uint8_t pos) {
        ref_id = read_from_generic<refid_t>(buffer, pos);
    }

    void NameArgument::write_to(std::vector<uint8_t> & buffer, uint8_t pos) {
        refid_t id_network = htonl(ref_id);
        std::memcpy(&buffer.at(pos), &id_network, WIDTH);
    }

    auto NameArgument::display() -> std::string {
        return std::format("<{0}>", ref_id);
    }

    // String Arguments

    void StringArgument::read_from (const std::vector<uint8_t> & buffer, uint8_t pos) {
        ref_id = read_from_generic<refid_t>(buffer, pos);
    }

    void StringArgument::write_to(std::vector<uint8_t> & buffer, uint8_t pos) {
        refid_t id_network = htonl(ref_id);
        std::memcpy(&buffer.at(pos), &id_network, WIDTH);
    }

    auto StringArgument::display() -> std::string {
        return std::format("<{0}>", ref_id);
    }

    // Number Arguments

    void NumberArgument::read_from (const std::vector<uint8_t> & buffer, uint8_t pos) {
        val = read_from_generic<number_t>(buffer, pos);
    }

    void NumberArgument::write_to(std::vector<uint8_t> & buffer, uint8_t pos) {
        number_t val_network = htonll(val);
        std::memcpy(&buffer.at(pos), &val_network, WIDTH);
    }

    auto NumberArgument::display() -> std::string {
        return std::format("{0}", val);
    }

    // Boolean Arguments

    void BooleanArgument::read_from (const std::vector<uint8_t> & buffer, uint8_t pos) {
        val = buffer.at(pos);
    }

    void BooleanArgument::write_to(std::vector<uint8_t> & buffer, uint8_t pos) {
        buffer.at(pos) = val;
    }

    auto BooleanArgument::display() -> std::string {
        if (val == 0) {
            return "false";
        }
        return "true";
    }
} // namespace Instructions