#include <vector>
#include <algorithm>

template <typename T>
class VectorSet {
private:
    std::vector<T> elements;

public:
    VectorSet() = default;
    VectorSet(const std::vector<T>& vec){
        elements = vec;
    }

    // Inserts an element into the set if not already present
    void insert(const T& value) {
        auto it = std::lower_bound(elements.begin(), elements.end(), value);
        if (it == elements.end() || *it != value) {
            elements.insert(it, value);
        }
    }

    // Removes an element from the set if present
    void erase(const T& value) {
        auto it = std::lower_bound(elements.begin(), elements.end(), value);
        if (it != elements.end() && *it == value) {
            elements.erase(it);
        }
    }

    // Checks if an element exists in the set
    bool contains(const T& value) const {
        return std::binary_search(elements.begin(), elements.end(), value);
    }

    // Returns the number of elements in the set
    size_t size() const {
        return elements.size();
    }

    // Checks if the set is empty
    bool empty() const {
        return elements.empty();
    }

    // Allows iteration over the elements (read-only)
    typename std::vector<T>::const_iterator begin() const {
        return elements.begin();
    }

    typename std::vector<T>::const_iterator end() const {
        return elements.end();
    }

    // Optional: Clear all elements from the set
    void clear() {
        elements.clear();
    }

     // Merge another VectorSet into this one (union operation)
     void merge(const VectorSet<T>& other) {
        std::vector<T> merged;
        merged.reserve(elements.size() + other.elements.size());
        
        auto it1 = elements.begin(), end1 = elements.end();
        auto it2 = other.elements.begin(), end2 = other.elements.end();

        while (it1 != end1 && it2 != end2) {
            if (*it1 < *it2) {
                merged.push_back(*it1);
                ++it1;
            } else if (*it2 < *it1) {
                merged.push_back(*it2);
                ++it2;
            } else { // Equal elements
                merged.push_back(*it1);
                ++it1;
                ++it2;
            }
        }

        // Add remaining elements from either vector
        merged.insert(merged.end(), it1, end1);
        merged.insert(merged.end(), it2, end2);
        
        elements = std::move(merged);
    }

    // Merge-and-assign operator
    VectorSet<T>& operator+=(const VectorSet<T>& other) {
        merge(other);
        return *this;
    }
};