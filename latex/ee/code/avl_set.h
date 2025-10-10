#include <vector>
#include <algorithm>
#include <memory>
#include <list>
#include <functional>
#include <stack>
#ifdef DEBUG
#include <assert.h>
#endif

template <typename T, typename Compare = std::less<T>>
class AVLSet {
private:
    struct Node {
        T key;
        Node* left;
        Node* right;
        int height;
        
        template <typename... Args>
        Node(Args&&... args) 
            : key(std::forward<Args>(args)...), 
              left(nullptr), 
              right(nullptr), 
              height(1) {}
    };

    Node* root;
    size_t size;
    Compare comp_;

    // Helper functions for merging
    int height(Node* node) const {
        return node ? node->height : 0;
    }

    Node* create_node(const T& key) {
        ++size;
        return new Node(key);
    }

    Node* create_node(T&& key) {
        ++size;
        return new Node(std::move(key));
    }

    // Generates a balanced subtree in O(n) time out from a ordered sequence.
    // Returns the root node pointer.
    // *Preconditions
    //  keys have to be ordered
    //  _RandAccIt is the random access iterator
    //  (*bg) and (*ed) should be of type T

    template<typename _RandAccIt>
    Node* build(const _RandAccIt& bg, const _RandAccIt& ed){
        if(bg == ed) return nullptr;
        auto it = bg;
        if(++it == ed) return create_node(*bg);
        it = bg + (ed - bg) / 2; // The same as (bg + ed)/2 but avoids overflow problems
        auto cur = create_node(*it);
        cur->left = build(bg, it);
        cur->right = build(it + 1, ed); 
        update_height(cur);
        return cur;
    }

    void update_height(Node* node) {
        node->height = 1 + std::max(height(node->left), height(node->right));
    }

    void delete_tree(Node* node) {
        if (!node) return;
        delete_tree(node->left);
        delete_tree(node->right);
        --size;
        delete node;
    }

    Node* rotate_right(Node* y) {
        Node* x = y->left;
        Node* T2 = x->right;

        x->right = y;
        y->left = T2;

        update_height(y);
        update_height(x);

        return x;
    }

    Node* rotate_left(Node* x) {
        Node* y = x->right;
        Node* T2 = y->left;

        y->left = x;
        x->right = T2;

        update_height(x);
        update_height(y);

        return y;
    }

    int balance_factor(Node* node) const {
        return node ? height(node->left) - height(node->right) : 0;
    }

    Node* balance(Node* node) {
        update_height(node);
        int bf = balance_factor(node);

        // Left Heavy
        if (bf > 1) {
            if (balance_factor(node->left) < 0)
                node->left = rotate_left(node->left);
            return rotate_right(node);
        }
        // Right Heavy
        if (bf < -1) {
            if (balance_factor(node->right) > 0)
                node->right = rotate_right(node->right);
            return rotate_left(node);
        }
        return node;
    }

    template <typename Func>
    void traverse_in_order(Node* node, Func f) const {
        if (!node) return;
        std::stack<Node*> stack;
        Node* current = node;
        while (current || !stack.empty()) {
            while (current) {
                stack.push(current);
                current = current->left;
            }
            current = stack.top();
            stack.pop();
            f(current->key);
            current = current->right;
        }
    }

    Node* insert(Node* node, const T& key) {
        if (!node) {
            return create_node(key);
        }

        if (comp_(key, node->key)) {
            node->left = insert(node->left, key);
        } else if (comp_(node->key, key)) {
            node->right = insert(node->right, key);
        } else {
            return node;
        }

        return balance(node);
    }

public:
    AVLSet(Compare Comp = Compare()) : root(nullptr), size(0), comp_(Comp) {}
    Compare comparator() const { return comp_; }
    // Move operations
    AVLSet(AVLSet&& other) noexcept 
        : root(other.root), 
          size(other.size){
        other.root = nullptr;
        other.size = 0;
    }

    AVLSet& operator=(AVLSet&& other) noexcept {
        if (this != &other) {
            clear();
            root = other.root;
            size = other.size;
            other.root = nullptr;
            other.size = 0;
        }
        return *this;
    }

    // Disable copy operations
    AVLSet(const AVLSet&) = delete;
    AVLSet& operator=(const AVLSet&) = delete;

    void clear() {
        delete_tree(root);
        root = nullptr;
    }

    bool empty() const {
        return size == 0;
    }

    size_t get_size() const {
        return size;
    }

    template <typename Func>
    void traverse_in_order(Func f) const {
        traverse_in_order(root, f);
    }

    std::vector<T> items() const {
        std::vector<T> result;
        traverse_in_order([&result](const T& key) {
            result.push_back(key);
        });
        return result;
    }


    void swap_with(AVLSet& other) {
        std::swap(root, other.root);
        std::swap(size, other.size);
    }

    void insert(const T& val){
        root = insert(root, val);
    }
    void remove(const T& val){
        root = remove(root, val);
    }
    template<typename RandAccIt>
    void construct(RandAccIt bg, RandAccIt ed){
        // Clear the current tree
        delete_tree(root);
        root = nullptr;
        // Build new tree
        root = build(bg, ed);
        size = static_cast<size_t>(ed - bg);
    }


    /** Merge two sets in O(N+M) time.
    *   Some additional space may be costed.
    *   But it does not affect the result of the experiment.
    *   @param other The AVLSet to be merged into this set.
    */

    void linearmerge(AVLSet&& other) {
        if (other.empty()) return;
        std::vector<T> q1 = items();
        std::vector<T> q2 = other.items();
        std::vector<T> all_elements;
        all_elements.reserve(q1.size() + q2.size());
        std::merge(q1.begin(), q1.end(), q2.begin(), q2.end(),
                  std::back_inserter(all_elements), comp_);
        delete_tree(root);
        delete_tree(other.root);
        root = nullptr;
        other.root = nullptr;
        root = build(all_elements.begin(), all_elements.end());
        size = all_elements.size();
    }

    /**
     *   Merge two sets in O(M log(N)) time.
     *   @param other The AVLSet to be merged into this set.
     */
    void simplemerge(AVLSet&& other) {
        if (other.empty()) return;
        if (size < other.size) { swap_with(other); }
        other.traverse_in_order([this](const T& key) {
            this->insert(key);
        });
        other.clear();
    }

    /**
     *   Merge two sets in O(M log(1+N/M)) time.
     *   @param other The AVLSet to be merged into this set.
     */
    void brownmerge(AVLSet&& other) {
        if (other.empty()) return;
        if (size < other.size) swap_with(other);

        std::vector<T> elems = other.items();
        other.clear();

        // stacks of pointers-to-links (Node**). Each points to some parent->left or parent->right or &root
        std::vector<Node**> path;
        std::vector<Node**> successor;

        path.push_back(&root);

        for (const T& x : elems) {
            while (!successor.empty() && !comp_(x, (*successor.back())->key)) {
                Node** succLink = successor.back();
                while (!path.empty() && path.back() != succLink) path.pop_back();
                successor.pop_back();
            }

            Node** curLink = path.empty() ? &root : path.back();
            Node* p = *curLink;
            if (!p) {
                *curLink = create_node(x);
                path.push_back(curLink);
            } else {
                for (;;) {
                    path.push_back(curLink); 
                    if (comp_(x, p->key)) {
                        if (p->left == nullptr) {
                            p->left = create_node(x);
                            path.push_back(&(p->left));
                            break;
                        } else {
                            successor.push_back(curLink);
                            curLink = &(p->left);
                            p = *curLink;
                        }
                    } else {
                        if (p->right == nullptr) {
                            p->right = create_node(x);
                            path.push_back(&(p->right));
                            break;
                        } else {
                            curLink = &(p->right);
                            p = *curLink;
                        }
                    }
                }
            }
            while (!path.empty()) {
                Node** link = path.back();
                Node* s = *link;
                path.pop_back();
                if (!successor.empty() && successor.back() == link) successor.pop_back();
                update_height(s);
                int bf = balance_factor(s);
                if (std::abs(bf) > 1) {
                    Node* newsub = balance(s);
                    *link = newsub;
                    while (!path.empty() && path.back() != link) path.pop_back();
                    break;
                }

                if (bf == 0) {
                    break;
                }
            }
        }
        #ifdef DEBUG
        auto items_after = items();
        for (size_t i = 1; i < items_after.size(); ++i) 
            assert(!comp_(items_after[i], items_after[i-1]));
        #endif
    }

};