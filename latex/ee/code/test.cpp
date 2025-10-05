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

void print_tset(AVLSet<int, SharedCountingComp>& s){
    auto items = s.items();
    for(size_t i = 0; i < s.get_size()-1; i++){
        if(items[i] > items[i+1]) {std::cout << "wow bad\n"; break;}
    }
    std::cout << "[there are" << s.get_size() << " items]" << std::endl;
    for(size_t i = 0; i < s.get_size(); i++){
        std::cout << items[i] << " \n"[i==s.get_size()-1];
    }
}

const std::string methodnames[] = {"linear", "simple", "brown"};
void testmerge(int type, std::mt19937_64& rnd, size_t q1 = 5e5, size_t q2 = 5e5){
    CounterPtr sharecounter = std::make_shared<std::size_t>(0);
    auto s1 = random_tset(q1, rnd, sharecounter), s2 = random_tset(q2, rnd, sharecounter);

    const auto t1 = std::chrono::steady_clock::now();
    std::cout << "merging avlset" << std::endl;
    if(type == 1)
        s1.linearmerge(std::move(s2));
    else if (type == 2)
        s1.simplemerge(std::move(s2));
    else if (type == 3)
        s1.brownmerge(std::move(s2));
    const auto t2 = std::chrono::steady_clock::now();
    using namespace::std::literals; // millisecond literals
    std::cout << "Time for "<< methodnames[type-1] << " merging is " << (t2-t1)/1ms << "ms" << std::endl;
    std::cout << "Number of comparisons: " << s1.comparator().getcount() << std::endl;
    if(q1+q2 <= 20) print_tset(s1);
}


int main() {
    size_t seedx;
    std::cout << "The seed is:" << std::endl;
    std::cin >> seedx;
    unsigned int s1, s2, ty;
    std::mt19937_64 rnd(seedx);
    while(std::cout << "size, size, type:" << std::endl, std::cin >> s1 >> s2 >> ty){
        if(s1 == 0 || s2 == 0 || ty < 1 || ty > 3) {std::cout<< "test ended" << std::endl; break;}
        else testmerge(ty, rnd, s1, s2);
    }
    return 0;
}
/*
    cd D:\code\latex\ee\code && g++ test.cpp -std=c++17 -o test.exe && .\test.exe
*/