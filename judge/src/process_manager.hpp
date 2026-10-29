#ifndef PROCESS_MANAGER_HPP
#define PROCESS_MANAGER_HPP
#include "types.hpp"
#include <chrono>
#include <string>
#include <vector>
enum class RunStatus
{
    Exited, // program ended by itself; exitCode is valid
    Signaled, // killed by the OS (segfault, abort, CPU limit); termSignal is valid
    WallTimeout, // judge killed it: real time ran out
    OutputLimit, // judge killed it: it printed more than outputBytes
    InternalError, // judge-side failure (fork/pipe/poll/wait); see `error`
};
struct RunResult
{
    RunStatus status = RunStatus::InternalError; // default is failure, never "success by accident"
    int exitCode = -1; // valid only if status == Exited
    int termSignal = 0; // valid only if status == Signaled
    std::chrono::milliseconds wallTime{0};
    std::chrono::milliseconds cpuTime{0};
    long peakMemoryKb = 0;
    std::string stdoutData;
    std::string stderrData;
    std::string error; // valid only if status == InternalError
};
// argv[0] is looked up in PATH. No shell is involved, so nothing can be injected.
RunResult run(const std::vector<std::string>& argv,const std::string& stdinData,const Limits& limits);
#endif // PROCESS_MANAGER_HPP