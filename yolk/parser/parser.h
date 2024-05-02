#pragma once

#include <cstddef>
#include <memory>
#include <optional>
#include <sstream>
#include <string>
#include <vector>

#include "../instruction/instructions.h"

#include "./failures.h"
#include "./instructionParsers.h"

namespace YolkParser {

class Parser {
  std::vector<YolkError> errors;
  std::vector<std::shared_ptr<Instructions::Instruction>> instructions;

  int current_line;

  void parse_line(const std::string & line) {
    std::string arg_string;
    std::stringstream line_ss(line);
    std::string op_type;
    if (getline(line_ss, op_type, ' ')) {
      std::vector<std::string> args;
      while (getline(line_ss, arg_string, ' ')) {
        args.push_back(arg_string);
      }
      parse(op_type, args);
    }
  }

  void parse(const std::string & op_type,
             const std::vector<std::string> & args) {
    if (op_type == "start-expression") {
      StartExpressionParser parser;
      auto maybe = parser.parse(args);
      if (maybe.has_value()) {
        instructions.push_back(maybe.value());
      } else {
        errors.push_back(FailedToParseInstruction(current_line, op_type));
      }
    } else if (op_type == "eval") {
      EvalParser parser;
      auto maybe = parser.parse(args);
      if (maybe.has_value()) {
        instructions.push_back(maybe.value());
      } else {
        errors.push_back(FailedToParseInstruction(current_line, op_type));
      }
    } else if (op_type == "push-name") {
      PushNameParser parser;
      auto maybe = parser.parse(args);
      if (maybe.has_value()) {
        instructions.push_back(maybe.value());
      } else {
        errors.push_back(FailedToParseInstruction(current_line, op_type));
      }
    } else if (op_type == "push-num") {
      PushNumParser parser;
      auto maybe = parser.parse(args);
      if (maybe.has_value()) {
        instructions.push_back(maybe.value());
      } else {
        errors.push_back(FailedToParseInstruction(current_line, op_type));
      }
    } else if (op_type == "push-str") {
      PushStringParser parser;
      auto maybe = parser.parse(args);
      if (maybe.has_value()) {
        instructions.push_back(maybe.value());
      } else {
        errors.push_back(FailedToParseInstruction(current_line, op_type));
      }
    } else if (op_type == "push-bool") {
      PushBoolParser parser;
      auto maybe = parser.parse(args);
      if (maybe.has_value()) {
        instructions.push_back(maybe.value());
      } else {
        errors.push_back(FailedToParseInstruction(current_line, op_type));
      }
    } else {
      errors.push_back(UnknownInstruction(current_line, op_type));
    }
  }

 public:
  explicit Parser(const std::vector<std::string> & lines) {
    for (current_line = 0; current_line < lines.size(); current_line++) {
      parse_line(lines[current_line]);
    }
  }

  auto has_error() -> bool { return !errors.empty(); }

  [[nodiscard]] auto get_errors() const -> const std::vector<YolkError> & {
    return errors;
  }

  auto instruction_count() -> std::size_t { return instructions.size(); }

  [[nodiscard]] auto get_instructions() const
      -> const std::vector<std::shared_ptr<Instructions::Instruction>> & {
    return instructions;
  }
};

}  // namespace YolkParser