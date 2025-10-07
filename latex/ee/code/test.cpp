#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <fstream>      // <--- for file output
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

const std::string methodnames[] = {"Insertion-based", "In-order trasversal", "Brown and Tarjan's"};

std::tuple<double, size_t> testmerge(int type, std::mt19937_64& rnd, size_t q1 = 5e5, size_t q2 = 5e5, bool printinfo = false) {
    CounterPtr sharecounter = std::make_shared<std::size_t>(0);
    auto s1 = random_tset(q1, rnd, sharecounter), s2 = random_tset(q2, rnd, sharecounter);

    const auto t1 = std::chrono::steady_clock::now();
    if(printinfo) std::cout << "merging avlset" << std::endl;
    if(type == 1)
        s1.simplemerge(std::move(s2));
    else if (type == 2)
        s1.linearmerge(std::move(s2));
    else if (type == 3)
        s1.brownmerge(std::move(s2));
    const auto t2 = std::chrono::steady_clock::now();
    //using namespace::std::literals;
    double ms = std::chrono::duration<double, std::milli>(t2 - t1).count();
    if(printinfo) std::cout << "Time for "<< methodnames[type-1] << " merging is " << ms << "ms" << std::endl;
    if(printinfo) std::cout << "Number of comparisons: " << s1.comparator().getcount() << std::endl;
    return std::make_tuple(ms, s1.comparator().getcount());
}

int main() {
    auto seedx = std::chrono::steady_clock::now().time_since_epoch().count();
    std::mt19937_64 rnd(seedx);

    std::ofstream outfile("results.csv");
    outfile << "method,alpha,N,trial,time_ms,comparisons\n"; // CSV header

    for (int type : {1, 2, 3}) {
        std::cout <<"type = " << type << std::endl;
        for (int alpha : {1, 1<<3, 1<<6, 1<<9, 1<<12}) {
            std::cout << "alpha = " << alpha << std::endl;
            for (long long n : {1<<12, 1<<13, 1<<14, 1<<15, 1<<16, 1<<17, 1<<18, 1<<19, 1<<20}) {
                std::cout << "n = " << n << std::endl;
                for (int trial = 1; trial <= 20; trial++) {
                    auto [time, comp] = testmerge(type, rnd, n, n / alpha, false);
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
    std::cout << "Results saved to merge_results.csv\n";
    std::cout << "seed = " << seedx << std::endl;
    return 0;
}