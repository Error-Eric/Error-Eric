#include"abstract_set.h"

template <typename T, typename Cmp = std::less<T> >
class VectorSet : public AbstractSet<T, Cmp> {
private:
    std::vector<T> data;
    Cmp cmp;

public:
    // Concrete iterator implementation
    class Iterator : public AbstractSet<T, Cmp>::iterator {
        typename std::vector<T>::iterator vec_it;
    public:
        Iterator(typename std::vector<T>::iterator it) : vec_it(it) {}
        T& operator*() const override { return *vec_it; }
        Iterator& operator++() override { ++vec_it; return *this; }
        bool operator!=(const typename AbstractSet<T, Cmp>::iterator& other) const override {
            const Iterator* other_it = dynamic_cast<const Iterator*>(&other);
            return (other_it == nullptr) || (vec_it != other_it->vec_it);
        }
    };

    // Overridden virtual methods
    void insert(const T& x) override {
        if (std::find(data.begin(), data.end(), x) == data.end()) {
            data.push_back(x);
        }
    }

    void erase(const T& x) override {
        auto it = std::find(data.begin(), data.end(), x);
        if (it != data.end()) data.erase(it);
    }

    size_t count(const T& x) override { 
        return (std::find(data.begin(), data.end(), x) != data.end()) ? 1 : 0;
    }

    size_t size() const noexcept override { return data.size(); }

    // Return concrete iterators
    Iterator begin() override { return Iterator(data.begin()); }
    Iterator end() override { return Iterator(data.end()); }

    // Other methods
    void insert_set(const AbstractSet<T, Cmp>& friend_set) override {
        for (auto it = friend_set.begin(); it != friend_set.end(); ++it) {
            this->insert(*it);
        }
    }

    AbstractSet<T, Cmp>& operator+=(const AbstractSet<T, Cmp>& friend_set) override {
        insert_set(friend_set);
        return *this;
    }
};