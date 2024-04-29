#pragma once

#include <cstdint>
#include <optional>
#include <string>
#include <utility>

namespace YolkParser {

enum arg_type_t : uint8_t { None = 0, RefID, Num, Bool };

struct FlagValue {
  int64_t value;
  bool is_reference;
};

class Flag {
  std::string name;
  arg_type_t arg_type;

 public:
  explicit constexpr Flag(std::string _name, arg_type_t _arg_type)
      : name(std::move(_name)), arg_type(_arg_type) {}

  [[nodiscard]] auto get_name() const -> const std::string & { return name; }

  [[nodiscard]] auto get_arg_type() const -> const arg_type_t & {
    return arg_type;
  }

  [[nodiscard]] auto validate(const std::optional<FlagValue> & value) -> bool {
    if (!value.has_value()) {
      return arg_type == None;
    }
    switch (arg_type) {
      case None:
        return false;
      case RefID:
        return value->is_reference;
      case Num:
      case Bool:
        return !(value->is_reference);
    }
    std::unreachable();
  }
};

}  // namespace YolkParser
