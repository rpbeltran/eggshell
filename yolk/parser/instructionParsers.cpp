#include <cassert>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

#include "../instruction/instructionArgs.h"
#include "../instruction/instructions.h"
#include "./flags.h"
#include "./instructionParsers.h"

namespace YolkParser {

auto StartExpressionParser::parse_flags(
    std::unordered_map<std::string, std::optional<FlagValue>> & flags)
    -> Instructions::StartInstruction {
  assert(flags.empty());
  return {};
}

auto EvalParser::parse_flags(
    std::unordered_map<std::string, std::optional<FlagValue>> & flags)
    -> Instructions::EvalInstruction {
  Instructions::EvalInstruction eval;
  eval.get_discard().set_val(static_cast<Instructions::number_t>(flags.contains("discard")));
  return eval;
}

std::vector<Flag> EvalParser::_optional_flags = {Flag("discard", None)};

auto PushNameParser::parse_flags(
    std::unordered_map<std::string, std::optional<FlagValue>> & flags)
    -> Instructions::PushName {
  Instructions::PushName push;
  push.get_val().set_refid(flags["ref"].value().value);
  return push;
}

std::vector<Flag> PushNameParser::_required_flags = {Flag("ref", RefID)};

auto PushNumParser::parse_flags(
    std::unordered_map<std::string, std::optional<FlagValue>> & flags)
    -> Instructions::PushNum {
  Instructions::PushNum push;
  push.get_val().set_val(flags["val"].value().value);
  return push;
}

std::vector<Flag> PushNumParser::_required_flags = {Flag("val", Num)};

auto PushStringParser::parse_flags(
    std::unordered_map<std::string, std::optional<FlagValue>> & flags)
    -> Instructions::PushString {
  Instructions::PushString push;
  push.get_val().set_refid(flags["ref"].value().value);
  return push;
}

std::vector<Flag> PushStringParser::_required_flags = {Flag("ref", RefID)};

auto PushBoolParser::parse_flags(
    std::unordered_map<std::string, std::optional<FlagValue>> & flags)
    -> Instructions::PushBool {
  Instructions::PushBool push;
  push.get_val().set_val(flags["val"].value().value);
  return push;
}

std::vector<Flag> PushBoolParser::_required_flags = {Flag("val", Bool)};

}  // namespace YolkParser
