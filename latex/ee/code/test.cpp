#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <fstream>
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

const std::string methodnames[] = {"Insertion-based", "In-order trasversal", "Brown and Tarjan's"};

std::tuple<double, size_t> testmerge(int type, std::mt19937_64& rnd, size_t q1 = 5e5, size_t q2 = 5e5) {
    CounterPtr sharecounter = std::make_shared<std::size_t>(0);
    auto comp = SharedCountingComp(sharecounter);
    std::vector<int> vec(q1 + q2);
    iota(vec.begin(), vec.end(), 0);
    std::shuffle(vec.begin(), vec.end(), rnd);
    auto s1 = AVLSet<int, SharedCountingComp>(comp), s2 = AVLSet<int, SharedCountingComp>(comp);
    sort(vec.begin()+0, vec.begin()+q1); 
    s1.construct(vec.begin() + 0, vec.begin() + q1);
    sort(vec.begin() + q1 + 1, vec.begin() + q1 + q2);
    s2.construct(vec.begin() + q1 + 1, vec.begin() + q1 + q2);
    const auto t1 = std::chrono::steady_clock::now();
    if(type == 1)
        s1.simplemerge(std::move(s2));
    else if (type == 2)
        s1.linearmerge(std::move(s2));
    else if (type == 3)
        s1.brownmerge(std::move(s2));
    const auto t2 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t2 - t1).count();
    return std::make_tuple(ms, s1.comparator().getcount());
}

int main() {
    auto seedx = std::chrono::steady_clock::now().time_since_epoch().count();
    std::mt19937_64 rnd(seedx);

    std::ofstream outfile("results.csv");
    outfile << "method,alpha,N,trial,time_ms,comparisons\n"; // CSV header

    for (int type : {1, 2, 3}) {
        for (int alpha : {1, 1<<3, 1<<6, 1<<9, 1<<12}) {
            for (long long n : {1<<12, 1<<13, 1<<14, 1<<15, 1<<16, 1<<17, 1<<18, 1<<19, 1<<20}) {
                for (int trial = 1; trial <= 20; trial++) {
                    auto [time, comp] = testmerge(type, rnd, n, n / alpha);
                    outfile << methodnames[type - 1] << ","
                            << alpha << ","
                            << n << ","
                            << trial << ","
                            << time << ","
                            << comp << "\n";
                }
            }
        }
    }

    outfile.close();
    std::cout << "seed = " << seedx << std::endl;
    return 0;
}