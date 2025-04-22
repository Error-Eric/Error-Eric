#include <functional>
#include <vector>
#include <algorithm>

template <typename T, typename Cmp = std::less<T> >
class AbstractSet {
public:
    virtual ~AbstractSet() = default;

    virtual void insert(const T& x) = 0;
    virtual void erase(const T& x) = 0;
    virtual size_t count(const T& x) = 0;
    virtual size_t size() const noexcept = 0;

    // Standard iterator interface (non-virtual)
    class iterator {
    public:
        virtual ~iterator() = default;
        virtual T& operator*() const = 0;
        virtual iterator& operator++() = 0;
        virtual bool operator!=(const iterator& other) const = 0;
    };

    virtual iterator begin() = 0;
    virtual iterator end() = 0;

    virtual void insert_set(const AbstractSet<T, Cmp>& friend_set) = 0;
    virtual AbstractSet<T, Cmp>& operator+=(const AbstractSet<T, Cmp>& friend_set) = 0;
};
