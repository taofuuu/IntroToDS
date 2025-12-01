#ifndef __STUDENT_H_
#define __STUDENT_H_

// You can include library here
#include "map_avl.h"
#include <vector>

template <typename KeyT,
          typename MappedT,
          typename CompareT>
void CP::map_avl<KeyT, MappedT, CompareT>::my_recur(node* node, iterator it, std::vector<size_t> &balance) const { 
    // Get Balance
    if (!node) return;
    
    if (node->left && node->right) {
        balance[node->right->height - node->left->height + 1]++;
        my_recur(node->left, it, balance);
        my_recur(node->right, it, balance);
    } else if (!node->left && !node->right) {
        balance[1]++;
        return;
    } else if (!node->left){
        balance[2]++;
        my_recur(node->right, it, balance);
    } else {
        balance[0]++;
        my_recur(node->left, it, balance);
    }

    return;
}

template <typename KeyT,
          typename MappedT,
          typename CompareT>
void CP::map_avl<KeyT, MappedT, CompareT>::my_recur_2(node* node, iterator it, std::vector<size_t> &balance) const {
    // Get Height
    
}

template <typename KeyT,
          typename MappedT,
          typename CompareT>
std::vector<size_t> CP::map_avl<KeyT, MappedT, CompareT>::balance_values(iterator it) const  {
    // Write your code here
    std::vector<size_t> balance = {0, 0, 0};
    my_recur(it.ptr, it, balance);
    return balance;
}

#endif