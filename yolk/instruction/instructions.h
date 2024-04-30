#pragma once

#include <cassert>
#include <concepts>
#include <cstddef>
#include <cstdint>
#include <format>
#include <memory>
#include <utility>
#include <vector>

#include "instructionArgs.h"

namespace Instructions {

enum InstructionType : std::uint8_t {
  START = 0,
  PUSH_NAME,
  PUSH_NUM,
  PUSH_STR,
  PUSH_BOOL,
  EVAL,
};

class Instruction {
  InstructionType instruction_type;

 public:
  virtual void serialize_to(std::vector<uint8_t> & buffer) const;

  virtual void deserialize(const std::vector<uint8_t> & _buffer,
                           size_t _from) = 0;

  [[nodiscard]] virtual auto to_psuedoyolk() const -> std::string;
  [[nodiscard]] auto width() const -> uint8_t;

  [[nodiscard]] auto serialize() const -> std::vector<uint8_t>;

  [[nodiscard]] auto get_instruction_type() const -> InstructionType {
    return instruction_type;
  };

  explicit Instruction(InstructionType _type) : instruction_type(_type) {}

  virtual ~Instruction() = default;

  Instruction(const Instruction & copyFrom) = delete;
  auto operator=(const Instruction & copyFrom) -> Instruction & = delete;
  Instruction(Instruction &&) = delete;
  auto operator=(Instruction &&) -> Instruction & = delete;
};

// Concept IsAnInstruction: type `T` derives `Instruction`.
template <typename T>
concept IsAnInstruction = std::derived_from<T, Instruction>;

struct StartInstruction : public Instruction {
  void serialize_to(std::vector<uint8_t> & buffer) const override;
  void deserialize(const std::vector<uint8_t> & buffer, size_t from) override;
  [[nodiscard]] auto to_psuedoyolk() const -> std::string override;
  [[nodiscard]] static auto width() -> uint8_t;

  StartInstruction() : Instruction(START) {}
};

class EvalInstruction : public Instruction {
  BooleanArgument discard;

 public:
  void serialize_to(std::vector<uint8_t> & buffer) const override;
  void deserialize(const std::vector<uint8_t> & buffer, size_t from) override;
  [[nodiscard]] auto to_psuedoyolk() const -> std::string override;
  [[nodiscard]] static auto width() -> uint8_t;

  EvalInstruction() : Instruction(EVAL) {}

  [[nodiscard]] auto get_discard() -> BooleanArgument & { return discard; }
};

class PushName : public Instruction {
  NameArgument val;

 public:
  void serialize_to(std::vector<uint8_t> & buffer) const override;
  void deserialize(const std::vector<uint8_t> & buffer, size_t from) override;
  [[nodiscard]] auto to_psuedoyolk() const -> std::string override;
  [[nodiscard]] static auto width() -> uint8_t;

  PushName() : Instruction(PUSH_NAME) {}

  [[nodiscard]] auto get_val() -> NameArgument & { return val; }
};

class PushNum : public Instruction {
  NumberArgument val;

 public:
  // todo: refactor instructions to have a vector of arguments to serialize in order
  void serialize_to(std::vector<uint8_t> & buffer) const override;
  void deserialize(const std::vector<uint8_t> & buffer, size_t from) override;
  [[nodiscard]] auto to_psuedoyolk() const -> std::string override;
  [[nodiscard]] static auto width() -> uint8_t;

  PushNum() : Instruction(PUSH_NUM) {}

  [[nodiscard]] auto get_val() -> NumberArgument & { return val; }
};

class PushString : public Instruction {
  StringArgument val;

 public:
  void serialize_to(std::vector<uint8_t> & buffer) const override;
  void deserialize(const std::vector<uint8_t> & buffer, size_t from) override;
  [[nodiscard]] auto to_psuedoyolk() const -> std::string override;
  [[nodiscard]] static auto width() -> uint8_t;

  PushString() : Instruction(PUSH_STR) {}

  [[nodiscard]] auto get_val() -> StringArgument & { return val; }
};

class PushBool : public Instruction {
  BooleanArgument val;

 public:
  void serialize_to(std::vector<uint8_t> & buffer) const override;
  void deserialize(const std::vector<uint8_t> & buffer, size_t from) override;
  [[nodiscard]] auto to_psuedoyolk() const -> std::string override;
  [[nodiscard]] static auto width() -> uint8_t;

  PushBool() : Instruction(PUSH_BOOL) {}

  [[nodiscard]] auto get_val() -> BooleanArgument & { return val; }
};

auto deserialize(const std::vector<uint8_t> & buffer,
                 size_t from) -> std::unique_ptr<Instruction>;

}  // namespace Instructions
