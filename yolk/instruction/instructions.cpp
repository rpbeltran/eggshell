#include <cstdint>
#include <format>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "instructionArgs.h"
#include "instructions.h"

namespace Instructions {

auto deserialize(const std::vector<uint8_t> & buffer,
                 size_t from) -> std::unique_ptr<Instruction> {
  auto label = static_cast<InstructionType>(buffer.at(from));
  if (label == START) {
    auto instruction = std::make_unique<StartInstruction>();
    instruction.get()->deserialize(buffer, from);
    return instruction;
  }
  if (label == PUSH_NAME) {
    auto instruction = std::make_unique<PushName>();
    instruction.get()->deserialize(buffer, from);
    return instruction;
  }
  if (label == PUSH_NUM) {
    auto instruction = std::make_unique<PushNum>();
    instruction.get()->deserialize(buffer, from);
    return instruction;
  }
  if (label == PUSH_STR) {
    auto instruction = std::make_unique<PushString>();
    instruction.get()->deserialize(buffer, from);
    return instruction;
  }
  if (label == PUSH_BOOL) {
    auto instruction = std::make_unique<PushBool>();
    instruction.get()->deserialize(buffer, from);
    return instruction;
  }
  if (label == EVAL) {
    auto instruction = std::make_unique<EvalInstruction>();
    instruction.get()->deserialize(buffer, from);
    return instruction;
  }
  std::unreachable();
}

void Instruction::serialize_to(std::vector<uint8_t> & buffer) const {
  switch (instruction_type) {
    case START:
      dynamic_cast<const StartInstruction *>(this)->serialize_to(buffer);
      break;
    case PUSH_NAME:
      dynamic_cast<const PushName *>(this)->serialize_to(buffer);
      break;
    case PUSH_NUM:
      dynamic_cast<const PushNum *>(this)->serialize_to(buffer);
      break;
    case PUSH_STR:
      dynamic_cast<const PushString *>(this)->serialize_to(buffer);
      break;
    case PUSH_BOOL:
      dynamic_cast<const PushBool *>(this)->serialize_to(buffer);
      break;
    case EVAL:
      dynamic_cast<const EvalInstruction *>(this)->serialize_to(buffer);
      break;
  }
  std::unreachable();
}

auto Instruction::to_psuedoyolk() const -> std::string {
  switch (instruction_type) {
    case START:
      return dynamic_cast<const StartInstruction *>(this)->to_psuedoyolk();
    case PUSH_NAME:
      return dynamic_cast<const PushName *>(this)->to_psuedoyolk();
    case PUSH_NUM:
      return dynamic_cast<const PushNum *>(this)->to_psuedoyolk();
    case PUSH_STR:
      return dynamic_cast<const PushString *>(this)->to_psuedoyolk();
    case PUSH_BOOL:
      return dynamic_cast<const PushBool *>(this)->to_psuedoyolk();
    case EVAL:
      return dynamic_cast<const EvalInstruction *>(this)->to_psuedoyolk();
  }
  std::unreachable();
}

auto Instruction::width() const -> uint8_t {

  switch (instruction_type) {
    case START:
      return StartInstruction::width();
    case PUSH_NAME:
      return PushName::width();
    case PUSH_NUM:
      return PushNum::width();
    case PUSH_STR:
      return PushString::width();
    case PUSH_BOOL:
      return PushBool::width();
    case EVAL:

      return EvalInstruction::width();
  }
  std::unreachable();
}

auto Instruction::serialize() const -> std::vector<uint8_t> {
  std::vector<uint8_t> buffer;
  serialize_to(buffer);
  return buffer;
}

// start-expression

void StartInstruction::serialize_to(std::vector<uint8_t> & buffer) const {
  buffer.push_back(InstructionType::START);
}

void StartInstruction::deserialize(const std::vector<uint8_t> & buffer,
                                   size_t from) {}

auto StartInstruction::to_psuedoyolk() const -> std::string {
  return "start-expression";
}

auto StartInstruction::width() -> uint8_t {
  return 1;
}

// eval

void EvalInstruction::serialize_to(std::vector<uint8_t> & buffer) const {
  buffer.push_back(InstructionType::EVAL);
  discard.write_to(buffer);
}

void EvalInstruction::deserialize(const std::vector<uint8_t> & buffer,
                                  size_t from) {
  discard.read_from(buffer, from + 1);
}

auto EvalInstruction::to_psuedoyolk() const -> std::string {
  if (discard.get_val() != 0) {
    return "eval --discard";
  }
  return "eval";
}

auto EvalInstruction::width() -> uint8_t {
  return 1 + BooleanArgument::get_width();
}

// push

void PushName::serialize_to(std::vector<uint8_t> & buffer) const {
  buffer.push_back(PUSH_NAME);
  val.write_to(buffer);
}

void PushName::deserialize(const std::vector<uint8_t> & buffer, size_t from) {
  val.read_from(buffer, from + 1);
}

auto PushName::to_psuedoyolk() const -> std::string {
  return std::format("push-name --ref {0}", val.display());
}

auto PushName::width() -> uint8_t {
  return 1 + NameArgument::get_width();
}

void PushNum::serialize_to(std::vector<uint8_t> & buffer) const {
  buffer.push_back(PUSH_NUM);
  val.write_to(buffer);
}

void PushNum::deserialize(const std::vector<uint8_t> & buffer, size_t from) {
  val.read_from(buffer, from + 1);
}

auto PushNum::to_psuedoyolk() const -> std::string {
  return std::format("push-num --val {0}", val.display());
}

auto PushNum::width() -> uint8_t {
  return 1 + NumberArgument::get_width();
}

void PushString::serialize_to(std::vector<uint8_t> & buffer) const {
  buffer.push_back(PUSH_STR);
  val.write_to(buffer);
}

void PushString::deserialize(const std::vector<uint8_t> & buffer, size_t from) {
  val.read_from(buffer, from + 1);
}

auto PushString::to_psuedoyolk() const -> std::string {
  return std::format("push-str --ref {0}", val.display());
}

auto PushString::width() -> uint8_t {
  return 1 + StringArgument::get_width();
}

void PushBool::serialize_to(std::vector<uint8_t> & buffer) const {
  buffer.push_back(PUSH_BOOL);
  val.write_to(buffer);
}

void PushBool::deserialize(const std::vector<uint8_t> & buffer, size_t from) {
  val.read_from(buffer, from + 1);
}

auto PushBool::to_psuedoyolk() const -> std::string {
  return std::format("push-bool --val {0}", val.display());
}

auto PushBool::width() -> uint8_t {
  return 1 + BooleanArgument::get_width();
}

}  // namespace Instructions
