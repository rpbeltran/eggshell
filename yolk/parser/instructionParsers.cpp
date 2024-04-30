#include <cassert>
#include <memory>
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
    -> std::shared_ptr<Instructions::StartInstruction> {
  assert(flags.empty());
  return std::make_shared<Instructions::StartInstruction>();
}

auto EvalParser::parse_flags(
    std::unordered_map<std::string, std::optional<FlagValue>> & flags)
    -> std::shared_ptr<Instructions::EvalInstruction> {
  auto eval_ptr = std::make_shared<Instructions::EvalInstruction>();
  eval_ptr->get_discard().set_val(
      static_cast<Instructions::number_t>(flags.contains("discard")));
  return eval_ptr;
}

std::vector<Flag> EvalParser::_optional_flags = {Flag("discard", None)};

auto PushNameParser::parse_flags(
    std::unordered_map<std::string, std::optional<FlagValue>> & flags)
    -> std::shared_ptr<Instructions::PushName> {
  auto push_ptr = std::make_shared<Instructions::PushName>();
  push_ptr->get_val().set_refid(flags["ref"].value().value);
  return push_ptr;
}

std::vector<Flag> PushNameParser::_required_flags = {Flag("ref", RefID)};

auto PushNumParser::parse_flags(
    std::unordered_map<std::string, std::optional<FlagValue>> & flags)
    -> std::shared_ptr<Instructions::PushNum> {
  auto push_ptr = std::make_shared<Instructions::PushNum>();
  push_ptr->get_val().set_val(flags["val"].value().value);
  return push_ptr;
}

std::vector<Flag> PushNumParser::_required_flags = {Flag("val", Num)};

auto PushStringParser::parse_flags(
    std::unordered_map<std::string, std::optional<FlagValue>> & flags)
    -> std::shared_ptr<Instructions::PushString> {
  auto push_ptr = std::make_shared<Instructions::PushString>();
  push_ptr->get_val().set_refid(flags["ref"].value().value);
  return push_ptr;
}

std::vector<Flag> PushStringParser::_required_flags = {Flag("ref", RefID)};

auto PushBoolParser::parse_flags(
    std::unordered_map<std::string, std::optional<FlagValue>> & flags)
    -> std::shared_ptr<Instructions::PushBool> {
  auto push_ptr = std::make_shared<Instructions::PushBool>();
  push_ptr->get_val().set_val(flags["val"].value().value);
  return push_ptr;
}

std::vector<Flag> PushBoolParser::_required_flags = {Flag("val", Bool)};

}  // namespace YolkParser
