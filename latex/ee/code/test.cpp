#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include "avl_set.h"

typedef std::shared_ptr<std::size_t> CounterPtr;

struct SharedCountingComp {
    CounterPtr counter;

    SharedCountingComp() : counter(std::make_shared<std::size_t>(0)) {}
    SharedCountingComp(CounterPtr c) : counter(std::move(c)) {}

    bool operator()(int a, int b) const {
        ++(*counter);
        return a < b;
    }
    size_t getcount() const { return *counter; }
};

AVLSet<int, SharedCountingComp> random_tset(size_t n, std::mt19937_64& rng, const CounterPtr& counter) {
    std::vector<int> vec(n);
    for (size_t i = 0; i < n; i++) {
        vec[i] = rng();
    }
    std::sort(vec.begin(), vec.end());
    vec.erase(std::unique(vec.begin(), vec.end()), vec.end());

    AVLSet<int, SharedCountingComp> ans{SharedCountingComp(counter)};
    ans.construct(vec.begin(), vec.end());
    return ans;
}

const std::string methodnames[] = {"linear", "simple"};
void testmerge(int type, std::mt19937_64& rnd, size_t q1 = 5e5, size_t q2 = 5e5){
    CounterPtr sharecounter = std::make_shared<std::size_t>(0);
    auto s1 = random_tset(q1, rnd, sharecounter), s2 = random_tset(q2, rnd, sharecounter);

    const auto t1 = std::chrono::steady_clock::now();
    std::cout << "merging avlset" << std::endl;
    if(type == 1)
        s1.linearmerge(std::move(s2));
    else if (type == 2)
        s1.simplemerge(std::move(s2));
    //else if (type == 3)
    //    s1.fastmerge(std::move(s2));
    const auto t2 = std::chrono::steady_clock::now();
    using namespace::std::literals; // millisecond literals
    std::cout << "Time for "<< methodnames[type-1] << " merging is " << (t2-t1)/1ms << "ms" << std::endl;
    std::cout << "Number of comparisons: " << s1.comparator().getcount() << std::endl;
}

int main() {
    int a[8] = {0, 3, 5, 7, 8, 9, 13, 14};
    int b[10] = {1, 2, 6, 11, 12, 15, 17, 19, 30, 31};
    /*
    AVLSet<int> u, v;
    u.construct(a, a + 8), v.construct(b, b+10);
    std::cout << "constructed" << std::endl;
    u.simplemerge(std::move(v));
    u.traverse_in_order([](int x){std::cout << x << std::endl;});
    return 0;*/
    size_t seedx;
    std::cout << "The seed is:" << std::endl;
    std::cin >> seedx;
    unsigned int s1, s2, ty;
    std::mt19937_64 rnd(seedx);
    while(std::cout << "size, size, type:" << std::endl, std::cin >> s1 >> s2 >> ty){
        if(s1 == 0 || s2 == 0 || ty < 1 || ty > 3) break;
        else testmerge(ty, rnd, s1, s2);
    }
    return 0;
}
/*
    g++ test.cpp -std=c++14 -o test.exe && .\test.exe
*/