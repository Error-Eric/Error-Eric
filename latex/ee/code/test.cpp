#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include "avl_set.h"

AVLSet<int> random_tset(size_t want_size, std::mt19937_64& rnd) noexcept {
    AVLSet<int> ans;
    std::vector<int> vec;
    for(size_t i = 1, q = 0; i <= want_size; i++, q += rnd()%100)
        vec.push_back(q);
    ans.construct(vec.begin(), vec.end());
    std::cout << "set of size " << ans.get_size() << " randomly constructed" << std::endl;
    return ans;
}


const std::string methodnames[] = {"linear", "simple"};
void testmerge(int type, std::mt19937_64& rnd, size_t q1 = 5e5, size_t q2 = 5e5){
    auto s1 = random_tset(q1, rnd), s2 = random_tset(q2, rnd);

    const auto t1 = std::chrono::steady_clock::now();
    std::cout << "merging avlset" << std::endl;
    if(type == 1)
        s1.linearmerge(std::move(s2));
    else if (type == 2)
        s1.simplemerge(std::move(s2));
    const auto t2 = std::chrono::steady_clock::now();
    using namespace::std::literals; // millisecond literals
    std::cout << "Time for "<< methodnames[type] << " merging is " << (t2-t1)/1ms << "ms" << std::endl;
}

int main() {
    int a[10] = {0, 3, 5, 7, 8, 9, 13, 14, 18, 20};
    int b[10] = {1, 2, 6, 11, 12, 15, 17, 19, 30, 31};
    AVLSet<int> u, v;
    u.construct(a, a + 10), v.construct(b, b+10);
    u.simplemerge(std::move(v));
    u.traverse_in_order([](int x){std::cout << x << std::endl;});
    return 0;
    size_t seedx;
    std::cout << "The seed is" << std::endl;
    std::cin >> seedx;
    unsigned int s1, s2, ty;
    std::mt19937_64 rnd(seedx);
    while(std::cout << "size, size, type", std::cin >> s1 >> s2 >> ty){
        if(s1 == 0 || s2 == 0 || ty < 1 || ty > 2) break;
        else testmerge(ty, rnd, s1, s2);
    }
    return 0;
}