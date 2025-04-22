#include <iostream>
#include "vector_set.h"
int main() {
    VectorSet<int> vs;
    vs.insert(10);
    vs.insert(20);
    vs.insert(30);

    // Standard iterator loop now works!
    for (auto it = vs.begin(); it != vs.end(); ++it) {
        std::cout << *it << " ";  // Output: 10 20 30
    }

    return 0;
}