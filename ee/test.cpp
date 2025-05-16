#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include "vector_set.h"
#include "avl_set.h"

VectorSet<int> random_vset(unsigned int want_size, std::mt19937_64& rnd) noexcept {
    VectorSet<int> ans;
    while(ans.size() < want_size)
        ans.insert(rnd());
    return ans;
}

AVLSet<int> random_tset(unsigned int want_size, std::mt19937_64& rnd) noexcept {
    AVLSet<int> ans;
    while(ans.get_size() < want_size)
        ans.insert(rnd());
    return ans;
}

void test(std::mt19937_64 rnd, unsigned int q1 = 5e5, unsigned int q2 = 5e5){
    VectorSet<int> vs1 = random_vset(q1, rnd), vs2 = random_vset(q2, rnd);
    AVLSet<int> as1 = random_tset(q1, rnd), as2 = random_tset(q2, rnd);

    const auto t0 = std::chrono::steady_clock::now();
    std::cout << "merging vectorset" << std::endl;
    vs1.merge(vs2);
    const auto t1 = std::chrono::steady_clock::now();
    std::cout << "merging avlset" << std::endl;
    as1.merge(std::move(as2));
    const auto t2 = std::chrono::steady_clock::now();
    
    using namespace::std::literals; // millisecond literals
    std::cout << "Time for vector merging is " << (t1-t0)/1ms << "ms\n"
              << "Time for avl merging is " << (t2-t1)/1ms << "ms\n";
}

int main() {
    size_t seedx;
    std::cin >> seedx;
    unsigned int s1, s2;
    std::mt19937_64 rnd(seedx);
    while(std::cin >> s1 >> s2){
        if(s1 == 0 || s2 == 0) break;
        else test(rnd, s1, s2);
    }
    return 0;
}