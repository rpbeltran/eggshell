#include <cstdint>
#include <fstream>
#include <iostream>
#include <iterator>
#include <memory>
#include <string>
#include <vector>

#include "../instruction/instructions.h"
#include "../parser/parser.h"
#include "./cli.h"

namespace CLI {

auto read_file_lines(const std::string & path) -> std::vector<std::string> {
  std::fstream file;
  file.open(path, std::ios::in);

  std::vector<std::string> lines;
  std::string line;
  while (getline(file, line)) {
    lines.push_back(line);
  }
  return lines;
}

auto read_file_bytes(const std::string & path) -> std::vector<uint8_t> {
  std::ifstream stream(path, std::ios::in | std::ios::binary);
  std::vector<uint8_t> buffer((std::istreambuf_iterator<char>(stream)),
                              std::istreambuf_iterator<char>());
  return buffer;
}

void write_buffer_to_file(const std::vector<uint8_t> & buffer,
                          const std::string & path) {
  std::ofstream outfile;
  outfile.open(path, std::ios::binary | std::ios::out);
  outfile.write(reinterpret_cast<const char *>(buffer.data()),
                static_cast<int64_t>(buffer.size()));
}

void compile(const std::string & input, const std::string & output) {
  auto lines = read_file_lines(input);
  YolkParser::Parser parser(lines);

  if (parser.has_error()) {
    std::cout << "Compilation failed.. \n";
    for (const auto & err : parser.get_errors()) {
      std::cout << err.get_message() << "\n";
    }
    return;
  }

  std::vector<uint8_t> buffer;
  for (const auto & instruction : parser.get_instructions()) {
    instruction->serialize_to(buffer);
  }
  write_buffer_to_file(buffer, output);
}

void decompile(const std::string & input, const std::string & output) {
  auto buffer = read_file_bytes(input);

  std::vector<std::unique_ptr<Instructions::Instruction>> instructions;

  int read_from = 0;
  while (read_from < buffer.size()) {
    instructions.push_back(Instructions::deserialize(buffer, read_from));
    read_from += instructions.at(instructions.size() - 1).get()->width();
  }

  std::ofstream output_stream;
  output_stream.open(output);
  for (const auto & instruction : instructions) {
    output_stream << instruction->to_psuedoyolk() << "\n";
  }
  output_stream.close();
}
}  // namespace CLI