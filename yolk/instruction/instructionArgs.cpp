#include <cstddef>
#include <cstdint>
#include <cstring>
#include <format>
#include <string>
#include <vector>

// Correct htonl import depends on platform.
// Also clang-tidy doesn't seem to know how to map this one.
#ifdef _WIN32
#include <winsock.h> // NOLINT(misc-include-cleaner)
#else
#include <arpa/inet.h> // NOLINT(misc-include-cleaner)
#endif

#include "instructionArgs.h"

namespace Instructions {

template <typename int_val_t>
auto read_from_generic(const std::vector<uint8_t> & buffer,
                       size_t pos) -> int_val_t {
  int_val_t val = 0;
  for (int i = 0; i < sizeof(int_val_t); i++) {
    val <<= 8;  // NOLINT(*-magic-numbers)
    val += buffer.at(pos + i);
  }
  return val;
}

void NameArgument::read_from(const std::vector<uint8_t> & buffer, size_t pos) {
  ref_id = read_from_generic<refid_t>(buffer, pos);
}

void NameArgument::write_to(std::vector<uint8_t> & buffer) const {
  refid_t id_network = htonl(ref_id); // NOLINT(misc-include-cleaner)
  auto old_size = buffer.size();
  buffer.resize(buffer.size() + WIDTH);
  std::memcpy(&buffer.at(old_size), &id_network, WIDTH);
}

auto NameArgument::display() const -> std::string {
  return std::format("<{0}>", ref_id);
}

// String Arguments

void StringArgument::read_from(const std::vector<uint8_t> & buffer,
                               size_t pos) {
  ref_id = read_from_generic<refid_t>(buffer, pos);
}

void StringArgument::write_to(std::vector<uint8_t> & buffer) const {
  refid_t id_network = htonl(ref_id); // NOLINT(misc-include-cleaner)
  auto old_size = buffer.size();
  buffer.resize(buffer.size() + WIDTH);
  std::memcpy(&buffer.at(old_size), &id_network, WIDTH);
}

[[nodiscard]] auto StringArgument::display() const -> std::string {
  return std::format("<{0}>", ref_id);
}

// Number Arguments

void NumberArgument::read_from(const std::vector<uint8_t> & buffer,
                               size_t pos) {
  val = read_from_generic<number_t>(buffer, pos);
}

void NumberArgument::write_to(std::vector<uint8_t> & buffer) const {
  number_t val_network = htonll(val); // NOLINT(misc-include-cleaner)
  auto old_size = buffer.size();
  buffer.resize(buffer.size() + WIDTH);
  std::memcpy(&buffer.at(old_size), &val_network, WIDTH);
}

[[nodiscard]] auto NumberArgument::display() const -> std::string {
  return std::format("{0}", val);
}

// Boolean Arguments

[[nodiscard]] auto BooleanArgument::display() const -> std::string {
  if (get_val() == 0) {
    return "false";
  }
  return "true";
}

}  // namespace Instructions