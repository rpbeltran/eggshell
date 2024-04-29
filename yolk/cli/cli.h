#pragma once

#include <string>

#include "../parser/parser.h"

namespace CLI {

void compile(const std::string & input, const std::string & output);
void decompile(const std::string & input, const std::string & output);

}  // namespace CLI
