#ifndef __STUDENT_H_
#define __STUDENT_H_

#include "stack.h"
#include <vector>

// can include other libs or write util funtion here
template <typename T>
void CP::stack<T>::push(const T& value) {
    if (!mSize || mSize == 1) {
        mData.push_back({value});
        mSize++;
        return;
    }

    size_t prevSize = mData[mData.size() - 2].size();
    if (mData.back().size() < prevSize + 1) mData.back().push_back(value);
    else mData.push_back({value});
    mSize++;
}

template <typename T>
void CP::stack<T>::pop() {
    if (size() == 0) throw std::out_of_range("index of out range") ;
	
    mData.back().pop_back();
    if (mData.back().empty()) mData.pop_back();
    mSize--;
}

template <typename T>
size_t CP::stack<T>::size() const {
    //write your code here
    return mSize;
}

template <typename T>
const T&  CP::stack<T>::top() const {
    //write your code here
    if (size() == 0) throw std::out_of_range("index of out range") ;
    return mData.back().back();
}

/*
Push and pop with steady hand,
or tears may fall from teacher’s stand.
*/

#endif