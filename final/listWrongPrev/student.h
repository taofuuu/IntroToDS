#ifndef __STUDENT_H__
#define __STUDENT_H__

#include "list.h"

template<typename T>
size_t CP::list<T>::fix_wrong() {
  size_t count = 0;
  node *n = mHeader->next;
  for (size_t i = 0; i <= mSize; ++i) {
    if (n->next->prev != n) {
      count++;
      n->next->prev = n;
    }
    n = n->next;
  }
  return count;
}

#endif