#pragma once

#include <memory>
#include <unordered_map>

#include "../instruction/instructionArgs.h"
#include "../instruction/instructions.h"

#include "./instructionParser.h"

namespace YolkParser {

class StartExpressionParser
    : public InstructionParser<Instructions::StartInstruction> {
  static const constexpr std::vector<Flag> _required_flags = {};
  static const constexpr std::vector<Flag> _optional_flags = {};

  auto parse_flags(std::unordered_map<std::string, std::optional<FlagValue>> &
                       flags) -> Instructions::StartInstruction override;

 public:
  explicit StartExpressionParser()
      : InstructionParser<Instructions::StartInstruction>(
            std::make_shared<std::vector<Flag>>(_required_flags),
            std::make_shared<std::vector<Flag>>(_optional_flags)) {}
};

class EvalParser : public InstructionParser<Instructions::EvalInstruction> {
  static const constexpr std::vector<Flag> _required_flags = {};
  static std::vector<Flag> _optional_flags;

  auto parse_flags(std::unordered_map<std::string, std::optional<FlagValue>> &
                       flags) -> Instructions::EvalInstruction override;

 public:
  explicit EvalParser()
      : InstructionParser<Instructions::EvalInstruction>(
            std::make_shared<std::vector<Flag>>(_required_flags),
            std::make_shared<std::vector<Flag>>(_optional_flags)) {}
};

class PushNameParser : public InstructionParser<Instructions::PushName> {
  static std::vector<Flag> _required_flags;
  static const constexpr std::vector<Flag> _optional_flags = {};

  auto parse_flags(std::unordered_map<std::string, std::optional<FlagValue>> &
                       flags) -> Instructions::PushName override;

 public:
  explicit PushNameParser()
      : InstructionParser<Instructions::PushName>(
            std::make_shared<std::vector<Flag>>(_required_flags),
            std::make_shared<std::vector<Flag>>(_optional_flags)) {}
};

class PushNumParser : public InstructionParser<Instructions::PushNum> {
  static std::vector<Flag> _required_flags;
  static const constexpr std::vector<Flag> _optional_flags = {};

  auto parse_flags(std::unordered_map<std::string, std::optional<FlagValue>> &
                       flags) -> Instructions::PushNum override;

 public:
  explicit PushNumParser()
      : InstructionParser<Instructions::PushNum>(
            std::make_shared<std::vector<Flag>>(_required_flags),
            std::make_shared<std::vector<Flag>>(_optional_flags)) {}
};

class PushStringParser : public InstructionParser<Instructions::PushString> {
  static std::vector<Flag> _required_flags;
  static const constexpr std::vector<Flag> _optional_flags = {};

  auto parse_flags(std::unordered_map<std::string, std::optional<FlagValue>> &
                       flags) -> Instructions::PushString override;

 public:
  explicit PushStringParser()
      : InstructionParser<Instructions::PushString>(
            std::make_shared<std::vector<Flag>>(_required_flags),
            std::make_shared<std::vector<Flag>>(_optional_flags)) {}
};

class PushBoolParser : public InstructionParser<Instructions::PushBool> {
  static std::vector<Flag> _required_flags;
  static const constexpr std::vector<Flag> _optional_flags = {};

  auto parse_flags(std::unordered_map<std::string, std::optional<FlagValue>> &
                       flags) -> Instructions::PushBool override;

 public:
  explicit PushBoolParser()
      : InstructionParser<Instructions::PushBool>(
            std::make_shared<std::vector<Flag>>(_required_flags),
            std::make_shared<std::vector<Flag>>(_optional_flags)) {}
};

};  // namespace YolkParser
