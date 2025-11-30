#include <iostream>

using namespace std;

int n;
int buckets[2005];

int quadraticProbing(int start, int count) {
    return (start + count*count) % n;
}

int findSpace(int val, int mode = 0) {
    int col = 0;
    while (buckets[quadraticProbing(val, col)] >= 0) {
        ++col;
    }
    return mode ? col : quadraticProbing(val, col);
}

int findValue(int val, int mode = 0) {
    int col = 0;
    while (buckets[quadraticProbing(val, col)] != (mode ? -1 : val)) {
        if (buckets[quadraticProbing(val, col)] == -1) return -1;
        ++col;
    }
    return mode ? col : quadraticProbing(val, col);
}

int main() {
    int m, a, b;
    cin >> n >> m;
    for (int i = 0; i < n; ++i) buckets[i] = -1;
    
    while (m--) {
        cin >> a >> b;
        if (a == 1) {
            buckets[findSpace(b)] = b;
        } else {
            int pos = findValue(b);
            if (pos == -1) continue;
            buckets[pos] = -2;
        }
    }

    int q1 = -1, q2 = -1;

    for (int i = 0; i < n; ++i) {
        q1 = max(q1, findSpace(i, 1));
        q2 = max(q2, findValue(i, 1));
    }

    cout << q1 + 1 << " " << q2 + 1;
}