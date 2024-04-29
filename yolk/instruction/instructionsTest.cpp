// NOLINTBEGIN(*-magic-numbers)
#include <cstdint>
#include <string>
#include <vector>

#include "gtest/gtest.h"

#include "../utils/testUtils.h"
#include "instructionArgs.h"
#include "instructions.h"

using namespace Instructions;

template <IsAnInstruction instruction_t>
[[nodiscard]] auto testInstructionHelper(
    instruction_t & instruction, std::string & expected_psuedoyolk,
    std::vector<uint8_t> & expected_buffer,
    std::string error_prefix) -> testing::AssertionResult {
  if (instruction.width() != expected_buffer.size()) {
    return (testing::AssertionFailure()
            << error_prefix << "instruction.width() is: "
            << static_cast<int>(instruction.width())
            << ". Expected: " << expected_buffer.size());
  }
  if (instruction.to_psuedoyolk() != expected_psuedoyolk) {
    return (testing::AssertionFailure()
            << error_prefix << "instruction.to_psuedoyolk() is: '"
            << instruction.to_psuedoyolk() << "'. Expected: '"
            << expected_psuedoyolk << "'");
  }
  auto buffer = instruction.serialize();
  auto vector_check =
      testUtils::VectorsEqual(buffer, expected_buffer, error_prefix);
  if (!vector_check) {
    return vector_check;
  }

  return testing::AssertionSuccess();
}

template <IsAnInstruction instruction_t>
[[nodiscard]] auto testInstruction(
    instruction_t instruction, std::string expected_psuedoyolk,
    std::vector<uint8_t> expected_buffer) -> testing::AssertionResult {
  auto test1 = testInstructionHelper(instruction, expected_psuedoyolk,
                                     expected_buffer, "");
  if (!test1) {
    return test1;
  }
  auto buffer = instruction.serialize();
  IsAnInstruction auto instruction2 = instruction_t();
  instruction2.deserialize(buffer, 0);

  auto test2 =
      testInstructionHelper(instruction2, expected_psuedoyolk, expected_buffer,
                            "After serializing and then deserializing, ");
  if (!test2) {
    return test2;
  }

  auto * instruction3 = dynamic_cast<Instruction *>(&instruction);

  auto test3 =
      testInstructionHelper(*instruction3, expected_psuedoyolk, expected_buffer,
                            "After casting to generic Instruction type, ");
  if (!test3) {
    return test3;
  }

  return testing::AssertionSuccess();
}

// StartInstruction

TEST(Instructions, Start) {
  auto start = StartInstruction();

  const std::string expected_psuedo = "start-expression";
  auto expected_buffer = std::vector<uint8_t>{InstructionType::START};

  EXPECT_TRUE(testInstruction<StartInstruction>(start, expected_psuedo,
                                                expected_buffer));
}

// EvalInstruction

TEST(Instructions, Eval) {
  auto eval = EvalInstruction();
  eval.get_discard().set_val(static_cast<number_t>(false));

  const std::string expected_psuedo = "eval";
  auto expected_buffer =
      std::vector<uint8_t>{InstructionType::EVAL, 0, 0, 0, 0, 0, 0, 0, 0};

  EXPECT_TRUE(
      testInstruction<EvalInstruction>(eval, expected_psuedo, expected_buffer));
}

TEST(Instructions, EvalDiscard) {
  auto eval = EvalInstruction();
  eval.get_discard().set_val(static_cast<number_t>(true));

  const std::string expected_psuedo = "eval --discard";
  auto expected_buffer =
      std::vector<uint8_t>{InstructionType::EVAL, 0, 0, 0, 0, 0, 0, 0, 1};

  EXPECT_TRUE(
      testInstruction<EvalInstruction>(eval, expected_psuedo, expected_buffer));
}

TEST(Instructions, PushName) {
  auto push = PushName();
  push.get_val().set_refid(37 + (27 << 8) + (17 << 16) +
                           (9 << 24));  // 152116005

  const std::string expected_psuedo = "push-name --ref <152116005>";
  auto expected_buffer =
      std::vector<uint8_t>{InstructionType::PUSH_NAME, 9, 17, 27, 37};

  auto pushNameResult =
      testInstruction<PushName>(push, expected_psuedo, expected_buffer);

  EXPECT_TRUE(pushNameResult);
}

TEST(Instructions, PushString) {
  auto push = PushString();
  push.get_val().set_refid(37 + (27 << 8) + (17 << 16) +
                           (9 << 24));  // 152116005

  const std::string expected_psuedo = "push-str --ref <152116005>";
  auto expected_buffer =
      std::vector<uint8_t>{InstructionType::PUSH_STR, 9, 17, 27, 37};

  auto pushStrResult =
      testInstruction<PushString>(push, expected_psuedo, expected_buffer);

  EXPECT_TRUE(pushStrResult);
}

TEST(Instructions, PushNum) {
  auto push = PushNum();
  push.get_val().set_val(
      37 + (27 << 8) + (17 << 16) + (9 << 24) +
      (static_cast<uint64_t>(211) << 40));  // 231997105576741

  const std::string expected_psuedo = "push-num --val 231997105576741";
  auto expected_buffer = std::vector<uint8_t>{
      InstructionType::PUSH_NUM, 0, 0, 211, 0, 9, 17, 27, 37};

  auto pushNumResult =
      testInstruction<PushNum>(push, expected_psuedo, expected_buffer);

  EXPECT_TRUE(pushNumResult);
}

TEST(Instructions, PushNumInstruct) {
  auto push = PushNum();
  push.get_val().set_val(
      -37 - (27 << 8) - (17 << 16) - (9 << 24) -
      (static_cast<int64_t>(211) << 40));  // -231997105576741

  const std::string expected_psuedo = "push-num --val -231997105576741";

  // Assume twos compliment integers
  auto expected_buffer = std::vector<uint8_t>{
      InstructionType::PUSH_NUM, 255, 255, 44, 255, 246, 238, 228, 219};

  auto pushNumResult =
      testInstruction<PushNum>(push, expected_psuedo, expected_buffer);

  EXPECT_TRUE(pushNumResult);
}

TEST(Instructions, PushBool) {
  auto push = PushBool();
  push.get_val().set_val(1);

  const std::string expected_psuedo = "push-bool --val true";
  auto expected_buffer =
      std::vector<uint8_t>{InstructionType::PUSH_BOOL, 0, 0, 0, 0, 0, 0, 0, 1};

  auto pushBoolResult =
      testInstruction<PushBool>(push, expected_psuedo, expected_buffer);

  EXPECT_TRUE(pushBoolResult);
}

TEST(Instructions, PushBoolFalse) {
  auto push = PushBool();
  push.get_val().set_val(0);

  const std::string expected_psuedo = "push-bool --val false";
  auto expected_buffer =
      std::vector<uint8_t>{InstructionType::PUSH_BOOL, 0, 0, 0, 0, 0, 0, 0, 0};

  auto pushBoolResult =
      testInstruction<PushBool>(push, expected_psuedo, expected_buffer);

  EXPECT_TRUE(pushBoolResult);
}

// NOLINTEND(*-magic-numbers)