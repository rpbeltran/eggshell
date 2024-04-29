#pragma once

#include <concepts>
#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

namespace Instructions {

using refid_t = uint32_t;
using number_t = int64_t;

class Argument {

  size_t width;

 public:
  explicit Argument(uint8_t _width) : width(_width) {};

  virtual void read_from(const std::vector<uint8_t> & buffer, size_t pos) = 0;
  virtual void write_to(std::vector<uint8_t> & buffer) const = 0;
  [[nodiscard]] virtual auto display() const -> std::string = 0;

  [[nodiscard]] auto get_width() const -> size_t { return width; }

  virtual ~Argument() = default;
};

// Concept IsAnArgument: type 'T' derives `Argument`.
template <typename T>
concept IsAnArgument = std::derived_from<T, Argument>;

class NameArgument : public Argument {
  const static size_t WIDTH = sizeof(refid_t);
  refid_t ref_id;

 public:
  explicit NameArgument() : ref_id(0), Argument(WIDTH) {}

  explicit NameArgument(const refid_t _ref_id)
      : ref_id(_ref_id), Argument(WIDTH) {}

  void read_from(const std::vector<uint8_t> & buffer, size_t pos) override;
  void write_to(std::vector<uint8_t> & buffer) const override;
  [[nodiscard]] auto display() const -> std::string override;

  [[nodiscard]] static auto get_width() -> size_t { return WIDTH; }

  [[nodiscard]] auto get_refid() const -> refid_t { return ref_id; }

  void set_refid(refid_t new_refid) { ref_id = new_refid; }
};

class StringArgument : public Argument {
  const static size_t WIDTH = sizeof(refid_t);
  refid_t ref_id;

 public:
  explicit StringArgument() : ref_id(0), Argument(WIDTH) {}

  explicit StringArgument(const refid_t _ref_id)
      : ref_id(_ref_id), Argument(WIDTH) {}

  void read_from(const std::vector<uint8_t> & buffer, size_t pos) override;
  void write_to(std::vector<uint8_t> & buffer) const override;
  [[nodiscard]] auto display() const -> std::string override;

  [[nodiscard]] static auto get_width() -> size_t { return WIDTH; }

  [[nodiscard]] auto get_refid() const -> refid_t { return ref_id; }

  void set_refid(refid_t new_refid) { ref_id = new_refid; }
};

class NumberArgument : public Argument {
  number_t val;

 protected:
  const static size_t WIDTH = sizeof(number_t);

 public:
  explicit NumberArgument() : val(0), Argument(WIDTH) {}

  explicit NumberArgument(const number_t _val) : val(_val), Argument(WIDTH) {}

  void read_from(const std::vector<uint8_t> & buffer, size_t pos) override;
  void write_to(std::vector<uint8_t> & buffer) const override;
  [[nodiscard]] auto display() const -> std::string override;

  [[nodiscard]] static auto get_width() -> size_t { return WIDTH; }

  [[nodiscard]] auto get_val() const -> number_t { return val; }

  void set_val(number_t new_val) { val = new_val; }
};

class BooleanArgument : public NumberArgument {
 public:
  explicit BooleanArgument() = default;

  explicit BooleanArgument(const bool _val)
      : NumberArgument(static_cast<Instructions::number_t>(_val)) {}

  [[nodiscard]] auto display() const -> std::string override;

  [[nodiscard]] static auto get_width() -> size_t { return WIDTH; }
};

}  // namespace Instructions