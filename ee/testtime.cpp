#include <algorithm>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <vector>
void slow_motion()
{
    std::vector<int> a;
    for(int i = 1; i <= 10; i++)
        a.push_back(i);
    //static int a[]{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
    // Generate Γ(13) == 12! permutations:
    while (std::next_permutation(a.begin(), a.end())) {}
}
 
int main()
{
    using namespace std::literals; // enables literal suffixes, e.g. 24h, 1ms, 1s.

    const std::chrono::time_point<std::chrono::steady_clock> start =
        std::chrono::steady_clock::now();
    
    std::cout << "Test" << std::endl;
    slow_motion();
 
    const auto end = std::chrono::steady_clock::now();
    std::cout
        << "Slow calculations took "
        << (end - start) / 1ms << "ms";
}