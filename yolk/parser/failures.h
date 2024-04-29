#pragma once

#include <format>
#include <string>

namespace YolkParser {
class YolkError {
  int yolk_line;
  std::string message;

 public:
  YolkError(const int _yolk_line, const std::string & msg)
      : yolk_line(_yolk_line) {
    message = std::format("Instruction {0}: {1}", yolk_line, msg);
  }

  [[nodiscard]] auto get_message() const -> const std::string & {
    return message;
  }
};

struct UnknownInstruction : YolkError {
  UnknownInstruction(const int _yolk_line, const std::string & instruction_name)
      : YolkError(_yolk_line, format_error(instruction_name)) {}

  static auto format_error(const std::string & instruction_name)
      -> std::string {
    return std::format("Unknown instruction {0}.", instruction_name);
  }
};

struct FailedToParseInstruction : YolkError {
  FailedToParseInstruction(const int _yolk_line,
                           const std::string & instruction_name)
      : YolkError(_yolk_line, format_error(instruction_name)) {}

  static auto format_error(const std::string & instruction_name)
      -> std::string {
    return std::format("Unable to parse instruction {0}.", instruction_name);
  }
};
}  // namespace YolkParser