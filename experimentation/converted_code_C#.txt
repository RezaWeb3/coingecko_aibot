```csharp
using System;

class Program
{
    static void Main()
    {
        Console.WriteLine(MakeSeries(100000000, 4, 1));
    }

    static double MakeSeries(int iterations, int param1, int param2)
    {
        var start = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
        double result = 0;
        for (int i = 1; i < iterations; i++)
        {
            int j = i * param1 - param2;
            result -= 1.0 / j;
            j = i * param1 + param2;
            result += 1.0 / j;
        }
        Console.WriteLine(result);
        var end = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
        return (end - start) / 1000.0;
    }
}
```