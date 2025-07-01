```cpp
#include <iostream>
#include <chrono>

double make_series(int iterations, int param1, int param2) {
    auto start = std::chrono::high_resolution_clock::now();
    double result = 0.0;
    for (int i = 1; i < iterations; ++i) {
        double j = static_cast<double>(i * param1 - param2);
        result -= 1.0 / j;
        j = static_cast<double>(i * param1 + param2);
        result += 1.0 / j;
    }
    std::cout << result << std::endl;
    auto end = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double>(end - start).count();
}

int main() {
    std::cout << make_series(100000000, 4, 1) << std::endl;
    return 0;
}
```