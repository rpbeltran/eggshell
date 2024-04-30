#pragma once

#include <algorithm>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

#include "../instruction/instructionArgs.h"
#include "../instruction/instructions.h"

#include "./flags.h"

namespace YolkParser {

template <Instructions::IsAnInstruction instruction_t>
class InstructionParser {
  std::shared_ptr<std::vector<Flag>> required_flags;
  std::shared_ptr<std::vector<Flag>> optional_flags;

 public:
  explicit InstructionParser(
      const std::shared_ptr<std::vector<Flag>> & _required_flags,
      const std::shared_ptr<std::vector<Flag>> & _optional_flags)
      : required_flags(_required_flags), optional_flags(_optional_flags) {}

  auto parse(const std::vector<std::string> & args)
      -> std::optional<std::shared_ptr<instruction_t>> {
    auto flags = collect_flags(args);
    if (flags.has_value()) {
      return parse_flags(flags.value());
    }
    return {};
  }

  virtual auto parse_flags(
      std::unordered_map<std::string, std::optional<FlagValue>> & flags)
      -> std::shared_ptr<instruction_t> = 0;

  virtual ~InstructionParser() = default;

  InstructionParser(const InstructionParser & copyFrom) = delete;
  auto operator=(const InstructionParser & copyFrom) -> InstructionParser & = delete;
  InstructionParser(InstructionParser &&) = delete;
  auto operator=(InstructionParser &&) -> InstructionParser & = delete;

 private:
  auto collect_flags(const std::vector<std::string> & args)
      -> std::optional<
          std::unordered_map<std::string, std::optional<FlagValue>>> {
    std::unordered_map<std::string, std::optional<FlagValue>> flags;
    std::string flag_name;
    bool has_unpublished = false;
    for (const auto & arg : args) {
      if (arg.starts_with("--")) {
        if (has_unpublished) {
          flags[flag_name] = {};
        }
        has_unpublished = true;
        flag_name = arg.substr(2);
      } else if (has_unpublished) {
        FlagValue val{};
        if (arg.starts_with('<') && arg.ends_with('>')) {
          try {
            auto inner = arg.substr(1, arg.size() - 2);
            val.value = std::stoi(inner);
            val.is_reference = true;
          } catch (...) {
            return {};
          }
        } else if (arg == "true") {
          val.value = 1;
          val.is_reference = false;
        } else if (arg == "false") {
          val.value = 0;
          val.is_reference = false;
        } else {
          try {
            val.value = std::stoi(arg);
            val.is_reference = false;
          } catch (...) {
            return {};
          }
        }
        flags[flag_name] = val;
        has_unpublished = false;
      } else {
        return {};
      }
    }
    if (has_unpublished) {
      flags[flag_name] = {};
    }
    if (!validate_flags(flags)) {
      return {};
    }
    return flags;
  }

  auto validate_flag(
      const std::pair<std::string, std::optional<FlagValue>> & flag) -> bool {
    for (auto req : *required_flags) {
      if (flag.first == req.get_name()) {
        return req.validate(flag.second);
      }
    }
    for (auto opt : *optional_flags) {
      if (flag.first == opt.get_name()) {
        return opt.validate(flag.second);
      }
    }
    return false;
  }

  auto validate_flags(
      const std::unordered_map<std::string, std::optional<FlagValue>> & flags)
      -> bool {
    // Contains all required flags
    auto has_all_required =
        std::ranges::all_of(*required_flags, [&flags](const Flag & flag) {
          return flags.contains(flag.get_name());
        });

    // All flags given are expected and have the proper type
    auto all_are_valid = std::ranges::all_of(
        flags,
        [this](const std::pair<std::string, std::optional<FlagValue>> & flag) {
          return validate_flag(flag);
        });

    return (has_all_required and all_are_valid);
  }
};
}  // namespace YolkParser
