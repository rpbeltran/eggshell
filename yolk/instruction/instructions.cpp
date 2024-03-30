#include <cassert>
#include <cstddef>
#include <cstdint>
#include <format>
#include <array>
#include <string>
#include <utility>


#include "instructions.h"
#include "instructionArgs.h"

namespace Instructions {
    auto Instruction::serialize() -> std::vector<uint8_t> {
        auto buffer = std::vector<uint8_t>(width());
        serialize_to(buffer);
        return buffer;
    }

    // start-expression

    void StartInstruction::serialize_to(std::vector<uint8_t> & buffer) {
        buffer.at(0) = InstructionLabel::START;
    }

    void StartInstruction::deserialize(const std::vector<uint8_t> & buffer) {}

    auto StartInstruction::to_psuedoyolk() -> std::string {
        return "start-expression";
    }

    auto StartInstruction::width() -> uint8_t {
        return 1;
    }

    // eval

    void EvalInstruction::serialize_to(std::vector<uint8_t> & buffer) {
        buffer.at(0) = InstructionLabel::EVAL;
        discard.write_to(buffer, 1);
    }

    void EvalInstruction::deserialize(const std::vector<uint8_t> & buffer) {
        discard.read_from(buffer, 1);
    }

    auto EvalInstruction::to_psuedoyolk() -> std::string {
        if (discard.val != 0) {
            return "eval --discard";
        }
        return "eval";
    }

    auto EvalInstruction::width() -> uint8_t {
        return 1 + discard.width;
    }

} // namespace Instructions
