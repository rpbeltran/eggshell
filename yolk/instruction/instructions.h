#pragma once

#include <concepts>
#include <cstddef>
#include <cstdint>
#include <format>
#include <vector>

#include "instructionArgs.h"

namespace Instructions {

    enum InstructionLabel {
        START=0,
        PUSH_NAME, PUSH_NUM, PUSH_STR, PUSH_BOOL,
        EVAL,
    };

    struct Instruction {
        virtual void serialize_to(std::vector<uint8_t> & buffer) = 0;
        virtual void deserialize(const std::vector<uint8_t> & buffer) = 0;
        virtual auto to_psuedoyolk() -> std::string = 0;
        virtual auto width() -> uint8_t = 0;

        std::vector<uint8_t> serialize();
    };

    // Concept IsAnInstruction: type 'T' derives `Instruction`.
    template<typename T>
    concept IsAnInstruction = std::derived_from<T, Instruction>;

    struct StartInstruction : Instruction {
        void serialize_to(std::vector<uint8_t> & buffer) override;
        void deserialize(const std::vector<uint8_t> & buffer) override;
        auto to_psuedoyolk() -> std::string override;
        auto width() -> uint8_t override;
    };

    struct EvalInstruction : Instruction {
        BooleanArgument discard; // todo: make private and add getter
        void serialize_to(std::vector<uint8_t> & buffer) override;
        void deserialize(const std::vector<uint8_t> & buffer) override;
        auto to_psuedoyolk() -> std::string override;
        auto width() -> uint8_t override;
    };

    template<InstructionLabel label, IsAnArgument arg_t>
    struct PushInstruction : Instruction {
        arg_t val;
        void serialize_to(std::vector<uint8_t> & buffer) override {
            buffer.at(0) = label;
            val.write_to(buffer, 1);
        }

        void deserialize(const std::vector<uint8_t> & buffer) override {
            val.read_from(buffer, 1);
        }

        auto to_psuedoyolk() -> std::string override {
            switch (label) {
                case InstructionLabel::PUSH_NAME:
                    return std::format("push --name {0}", val.display());
                case InstructionLabel::PUSH_STR:
                    return std::format("push --string {0}", val.display());
                case InstructionLabel::PUSH_NUM:
                    return std::format("push --num {0}", val.display());
                case InstructionLabel::PUSH_BOOL:
                    return std::format("push --bool {0}", val.display());
            }
            std::unreachable();
        }

        auto width() -> uint8_t override {
            return 1 + val.width;
        }
    };
} // namespace Instructions
