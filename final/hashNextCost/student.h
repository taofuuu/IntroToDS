#ifndef __STUDENT_H_
#define __STUDENT_H_

#include "unordered_map.h"

namespace CP {

template <typename KeyT,
          typename MappedT,
          typename HasherT,
          typename EqualT>
size_t CP::unordered_map<KeyT, MappedT, HasherT, EqualT>::next_cost(iterator it) {
    size_t count = 0;

    if (it == end()) return count;

    int curBucket = hash_to_bucket(it->first);
    ValueIterator curVal_it = find_in_bucket(mBuckets[curBucket], it->first);

    ++curVal_it;
    ++count;
    if (curVal_it != mBuckets[curBucket++].end()) return count;

    while (curBucket < mBuckets.size()) {
        if (!mBuckets[curBucket++].empty()) break;
        count++;
    }
    return count + 1;
}
}

#endif


