#pragma once

#include <concepts>
#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

namespace Instructions {

    typedef uint32_t refid_t;
    typedef int64_t number_t;
    typedef uint8_t boolean_t;

    struct Argument {
        const uint8_t width;
        explicit Argument(uint8_t _width): width(_width) {};
        virtual void read_from (const std::vector<uint8_t> & buffer, uint8_t pos) = 0;
        virtual void write_to (std::vector<uint8_t> & buffer, uint8_t pos) = 0;
        virtual std::string display() = 0;
    };

    // Concept IsAnArgument: type 'T' derives `Argument`.
    template<typename T>
    concept IsAnArgument = std::derived_from<T, Argument>;

    struct NameArgument: Argument {
    private:
        const static uint8_t WIDTH = sizeof (refid_t);

    public:
        refid_t ref_id;

        explicit NameArgument () : ref_id(0), Argument(WIDTH) {}
        explicit NameArgument (const refid_t _ref_id) : ref_id(_ref_id), Argument(WIDTH) {}

        void read_from (const std::vector<uint8_t> & buffer, uint8_t pos) override;
        void write_to(std::vector<uint8_t> & buffer, uint8_t pos) override;
        auto display() -> std::string override;
    };

    struct StringArgument: Argument {
    private:
        const static uint8_t WIDTH = sizeof (refid_t);

    public:
        refid_t ref_id;

        explicit StringArgument () : ref_id(0), Argument(WIDTH) {}
        explicit StringArgument (const refid_t _ref_id) : ref_id(_ref_id), Argument(WIDTH) {}

        void read_from (const std::vector<uint8_t> & buffer, uint8_t pos) override;
        void write_to(std::vector<uint8_t> & buffer, uint8_t pos) override;
        auto display() -> std::string override;
    };

    struct NumberArgument: Argument {
    private:
        const static uint8_t WIDTH = sizeof (number_t);

    public:
        number_t val;

        explicit NumberArgument () : val(0), Argument(WIDTH) {}
        explicit NumberArgument (const number_t _val) : val(_val), Argument(WIDTH) {}

        void read_from (const std::vector<uint8_t> & buffer, uint8_t pos) override;
        void write_to(std::vector<uint8_t> & buffer, uint8_t pos) override;
        auto display() -> std::string override;
    };

    struct BooleanArgument: Argument {
    private:
        const static uint8_t WIDTH = sizeof (boolean_t);

    public:
        boolean_t val;

        explicit BooleanArgument () : val(0), Argument(WIDTH) {}
        explicit BooleanArgument (const boolean_t _val) : val(_val), Argument(WIDTH) {}

        void read_from (const std::vector<uint8_t> & buffer, uint8_t pos) override;
        void write_to(std::vector<uint8_t> & buffer, uint8_t pos) override;
        auto display() -> std::string override;
    };
} // namespace Instructions