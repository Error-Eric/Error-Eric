#include<chrono>

int64_t time(){
    auto t0 = std::chrono::steady_clock::now();
    // do something
    auto t1 = std::chrono::steady_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0);
    
    return duration.count();
}