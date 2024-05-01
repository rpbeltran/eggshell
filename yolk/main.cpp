#include <exception>
#include <iostream>
#include <string>

#include "argparse/argparse.hpp"

#include "./cli/cli.h"

// NOLINTNEXTLINE(bugprone-exception-escape)
auto main(int argc, char * argv[]) -> int {
  argparse::ArgumentParser program("yolk");

  argparse::ArgumentParser compile_command("compile");
  compile_command.add_description(
      "Convert .psuedoyolk file to binary .yolk format.");
  compile_command.add_argument("input").help("Psuedoyolk file to compile");
  compile_command.add_argument("-o", "--output")
      .help("Name of output file")
      .nargs(1)
      .default_value("output.yolk");

  argparse::ArgumentParser decompile_command("decompile");
  decompile_command.add_description(
      "Convert binary .yolk file to human readable .psuedoyolk format.");
  decompile_command.add_argument("input").help("Yolk file to decompile");
  decompile_command.add_argument("-o", "--output")
      .help("Name of output file")
      .nargs(1)
      .default_value("output.psuedoyolk");

  program.add_subparser(compile_command);
  program.add_subparser(decompile_command);

  try {
    program.parse_args(argc, argv);
  } catch (const std::exception & err) {
    std::cerr << err.what() << '\n';
    std::cerr << program;
    return 1;
  }

  if (program.is_subcommand_used(compile_command)) {
    CLI::compile(compile_command.get<std::string>("input"),
                 compile_command.get<std::string>("--output"));
  } else if (program.is_subcommand_used(decompile_command)) {
    CLI::decompile(decompile_command.get<std::string>("input"),
                   decompile_command.get<std::string>("--output"));
  }

  return 0;
}