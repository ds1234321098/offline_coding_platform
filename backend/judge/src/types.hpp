#ifndef TYPES_HPP
#define TYPES_HPP
#include <chrono>
#include <cstddef>
#include <string>
enum class Verdict
{
    Accepted,
    WrongAnswer,
    TimeLimitExceeded,
    MemoryLimitExceeded,
    RuntimeError,
    CompilationError,
    OutputLimitExceeded,
    InternalError,
};
struct TestCase
{
    std::string input;
    std::string expectedOutput;
};
struct Limits
{
    std::chrono::milliseconds wallTime{2000}; // real elapsed time
    std::chrono::milliseconds cpuTime{1000}; // CPU time actually used
    std::size_t memoryBytes = 256ull << 20; // 256 MB
    std::size_t outputBytes = 1ull << 20; // 1 MB
};
#endif // TYPES_HPP