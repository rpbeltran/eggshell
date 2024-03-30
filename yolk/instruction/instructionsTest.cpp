#include <vector>

#include "gtest/gtest.h"

#include "../utils/testUtils.h"
#include "instructions.h"

using namespace Instructions;

template<IsAnInstruction instruction_t>
[[nodiscard]] testing::AssertionResult testInstruction(
        instruction_t instruction, std::string expected_psuedoyolk, std::vector<uint8_t> expected_buffer) {
    if (instruction.width() != expected_buffer.size()) {
         return (testing::AssertionFailure()
            << "instruction.width() is: " << (int) instruction.width() << ". Expected: " << expected_buffer.size());
    }
    if (instruction.to_psuedoyolk() != expected_psuedoyolk) {
         return (testing::AssertionFailure()
            << "instruction.to_psuedoyolk() is: '" << instruction.to_psuedoyolk() << "'. Expected: '"
            << expected_psuedoyolk << "'");
    }
    auto buffer = instruction.serialize();
    auto vector_check = testUtils::VectorsEqual(buffer, expected_buffer);
    if (!vector_check) {
        return vector_check;
    }
    IsAnInstruction auto instruction2 = instruction_t();
    instruction2.deserialize(buffer);
    if (instruction2.width() != expected_buffer.size()) {
         return (testing::AssertionFailure()
            << "After serializing and then deserializing, width() is: "
            << (int) instruction2.width() << ". Expected: " << expected_buffer.size());
    }
    if (instruction2.to_psuedoyolk() != expected_psuedoyolk) {
         return (testing::AssertionFailure()
            << "After serializing and then deserializing, to_psuedoyolk() is: '"
            << instruction2.to_psuedoyolk() << "'. Expected: '" << expected_psuedoyolk) << "'";
    }
    auto buffer2 = instruction2.serialize();
    auto vector_check2 = testUtils::VectorsEqual(buffer2, expected_buffer);
    if (!vector_check2) {
        return testing::AssertionFailure() << "After serializing and then deserializing, " << vector_check2.message();
    }
    return testing::AssertionSuccess();
}


// StartInstruction

TEST(StartInstructionTest, BasicAssertions) {
    auto start = StartInstruction();

    auto expected_psuedo = "start-expression";
    auto expected_buffer = std::vector<uint8_t> { InstructionLabel::START};

    EXPECT_TRUE(testInstruction<StartInstruction>(
        start, expected_psuedo, expected_buffer));
}

// EvalInstruction

TEST(EvalInstructionTest, BasicAssertions) {
    auto eval = EvalInstruction();
    eval.discard.val = false;

    auto expected_psuedo = "eval";
    auto expected_buffer = std::vector<uint8_t> { InstructionLabel::EVAL, 0};

    EXPECT_TRUE(testInstruction<EvalInstruction>(
        eval, expected_psuedo, expected_buffer));
}

TEST(EvalDiscardInstructionTest, BasicAssertions) {
    auto eval = EvalInstruction();
    eval.discard.val = true;

    auto expected_psuedo = "eval --discard";
    auto expected_buffer = std::vector<uint8_t> { InstructionLabel::EVAL, 1};

    EXPECT_TRUE(testInstruction<EvalInstruction>(
        eval, expected_psuedo, expected_buffer));
}

TEST(PushNameInstructionTest, BasicAssertions) {
    auto push = PushInstruction<InstructionLabel::PUSH_NAME, NameArgument>();
    push.val.ref_id = 37 + (27 << 8) + (17 << 16) + (9 << 24); // 152116005

    auto expected_psuedo = "push --name <152116005>";
    auto expected_buffer = std::vector<uint8_t> { InstructionLabel::PUSH_NAME, 9,17,27,37};

    auto pushNameResult = testInstruction<PushInstruction<InstructionLabel::PUSH_NAME, NameArgument>>(
        push, expected_psuedo, expected_buffer);

    EXPECT_TRUE(pushNameResult);
}

TEST(PushStringInstructionTest, BasicAssertions) {
    auto push = PushInstruction<InstructionLabel::PUSH_STR, StringArgument>();
    push.val.ref_id = 37 + (27 << 8) + (17 << 16) + (9 << 24); // 152116005

    auto expected_psuedo = "push --string <152116005>";
    auto expected_buffer = std::vector<uint8_t> { InstructionLabel::PUSH_STR, 9,17,27,37};

    auto pushStrResult = testInstruction<PushInstruction<InstructionLabel::PUSH_STR, StringArgument>>(
        push, expected_psuedo, expected_buffer);

    EXPECT_TRUE(pushStrResult);
}

TEST(PushNumInstructionTest, BasicAssertions) {
    auto push = PushInstruction<InstructionLabel::PUSH_NUM, NumberArgument>();
    push.val.val = 37 + (27 << 8) + (17 << 16) + (9 << 24) + ((uint64_t) 211 << 40); // 231997105576741

    auto expected_psuedo = "push --num 231997105576741";
    auto expected_buffer = std::vector<uint8_t> { InstructionLabel::PUSH_NUM, 0,0,211,0,9,17,27,37};

    auto pushNumResult = testInstruction<PushInstruction<InstructionLabel::PUSH_NUM, NumberArgument>>(
        push, expected_psuedo, expected_buffer);

    EXPECT_TRUE(pushNumResult);
}

TEST(PushNumInstructionNegativeTest, BasicAssertions) {
    auto push = PushInstruction<InstructionLabel::PUSH_NUM, NumberArgument>();
    push.val.val = -37 - (27 << 8) - (17 << 16) - (9 << 24) - ((int64_t) 211 << 40); // -231997105576741

    auto expected_psuedo = "push --num -231997105576741";

    // Assume twos compliment integers
    auto expected_buffer = std::vector<uint8_t> { InstructionLabel::PUSH_NUM, 255,255,44,255,246,238,228,219};

    auto pushNumResult = testInstruction<PushInstruction<InstructionLabel::PUSH_NUM, NumberArgument>>(
        push, expected_psuedo, expected_buffer);

    EXPECT_TRUE(pushNumResult);
}

TEST(PushBoolInstructionTest, BasicAssertions) {
    auto push = PushInstruction<InstructionLabel::PUSH_BOOL, BooleanArgument>();
    push.val.val = 1;

    auto expected_psuedo = "push --bool true";
    auto expected_buffer = std::vector<uint8_t> { InstructionLabel::PUSH_BOOL, 1};

    auto pushBoolResult = testInstruction<PushInstruction<InstructionLabel::PUSH_BOOL, BooleanArgument>>(
        push, expected_psuedo, expected_buffer);

    EXPECT_TRUE(pushBoolResult);
}
