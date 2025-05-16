#include <vector>
#include <algorithm>
#include <memory>
#include <list>
#include <functional>
#include <stack>

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
    Compare comp;
    
    // Memory pool management
    std::list<Node> node_storage;
    std::vector<Node*> free_nodes;

    // Memory pool operations
    Node* create_node(const T& key) {
        if (!free_nodes.empty()) {
            Node* node = free_nodes.back();
            free_nodes.pop_back();
            *node = Node(key);
            return node;
        }
        node_storage.emplace_back(key);
        return &node_storage.back();
    }

    Node* create_node(T&& key) {
        if (!free_nodes.empty()) {
            Node* node = free_nodes.back();
            free_nodes.pop_back();
            *node = Node(std::move(key));
            return node;
        }
        node_storage.emplace_back(std::move(key));
        return &node_storage.back();
    }

    void recycle_node(Node* node) {
        free_nodes.push_back(node);
    }

    // Helper functions for merging
    int height(Node* node) const {
        return node ? node->height : 0;
    }

    void update_height(Node* node) {
        node->height = 1 + std::max(height(node->left), height(node->right));
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
        traverse_in_order(node->left, f);
        f(node->key);
        traverse_in_order(node->right, f);
    }

    void insert_merge(const T& key) {
        if (!root) {
            root = create_node(key);
            size++;
            return;
        }

        std::vector<Node*> path;
        std::vector<Node*> successor;
        Node* current = root;
        bool inserted = false;

        // Climb up to find the insertion path
        while (true) {
            path.push_back(current);
            if (comp(key, current->key)) {
                if (!current->left) break;
                successor.push_back(current);
                current = current->left;
            } else if (comp(current->key, key)) {
                if (!current->right) break;
                current = current->right;
            } else {
                // Duplicate, do not insert
                return;
            }
        }

        // Insert the new node
        Node* newNode = create_node(key);
        if (comp(key, current->key)) {
            current->left = newNode;
        } else {
            current->right = newNode;
        }
        size++;

        // Retrace the path to update heights and balance
        while (!path.empty()) {
            Node* node = path.back();
            path.pop_back();
            node = balance(node);

            if (!path.empty()) {
                if (path.back()->left == node) {
                    path.back()->left = node;
                } else {
                    path.back()->right = node;
                }
            } else {
                root = node;
            }
        }
    }

public:
    AVLSet() : root(nullptr), size(0), comp(Compare()) {}
    
    // Move operations
    AVLSet(AVLSet&& other) noexcept 
        : root(other.root), 
          size(other.size),
          node_storage(std::move(other.node_storage)),
          free_nodes(std::move(other.free_nodes)) {
        other.root = nullptr;
        other.size = 0;
    }

    AVLSet& operator=(AVLSet&& other) noexcept {
        if (this != &other) {
            clear();
            root = other.root;
            size = other.size;
            node_storage = std::move(other.node_storage);
            free_nodes = std::move(other.free_nodes);
            other.root = nullptr;
            other.size = 0;
        }
        return *this;
    }

    // Disable copy operations
    AVLSet(const AVLSet&) = delete;
    AVLSet& operator=(const AVLSet&) = delete;

    void clear() {
        node_storage.clear();
        free_nodes.clear();
        root = nullptr;
        size = 0;
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

    void merge(AVLSet&& other) {
        if (other.empty()) return;

        if (size < other.size) {
            // Swap to merge smaller into larger
            std::swap(root, other.root);
            std::swap(size, other.size);
            std::swap(node_storage, other.node_storage);
            std::swap(free_nodes, other.free_nodes);
        }

        // Insert all elements from the smaller tree (now 'other') into this
        other.traverse_in_order([this](const T& key) {
            this->insert_merge(key);
        });

        other.clear();
    }
    
    private:
    // Example of modified insert implementation
    Node* insert(Node* node, const T& key) {
        if (!node) {
            size++;
            return create_node(key);
        }

        if (comp(key, node->key)) {
            node->left = insert(node->left, key);
        } else if (comp(node->key, key)) {
            node->right = insert(node->right, key);
        } else {
            return node;
        }

        return balance(node);
    }

    // Example of modified remove implementation
    Node* remove(Node* node, const T& key) {
        if (!node) return nullptr;

        if (comp(key, node->key)) {
            node->left = remove(node->left, key);
        } else if (comp(node->key, key)) {
            node->right = remove(node->right, key);
        } else {
            // Node deletion with recycling
            if (!node->left || !node->right) {
                Node* temp = node->left ? node->left : node->right;
                recycle_node(node);
                size--;
                node = temp;
            } else {
                Node* temp = findMin(node->right);
                node->key = std::move(temp->key);
                node->right = remove(node->right, temp->key);
            }
        }

        return node ? balance(node) : nullptr;
    }

    public:
    void insert(const T& val){
        insert(root, val);
    }
    void remove(const T& val){
        remove(root, val);
    }
};

