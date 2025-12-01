#include "priority_queue.h"
#include <utility>
#include <queue>

template <typename T,typename Comp>
void CP::priority_queue<T, Comp>::child_swap(size_t k) {
  if (!mSize || mSize == 1 || k >= mSize) return;

  size_t lc = k*2 + 1;
  size_t rc = k*2 + 2;

  size_t count = 1;
  while (rc < mSize) {
    size_t tmp_lc = lc;
    size_t tmp_rc = rc;

    for (size_t i = 0; i < count; ++i) {
      std::swap(mData[tmp_lc++], mData[tmp_rc++]);
    }

    lc = lc*2 + 1;
    rc = rc*2 + 1;
    count *= 2;
  }
   
  return;
}