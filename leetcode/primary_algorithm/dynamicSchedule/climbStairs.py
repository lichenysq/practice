class Solution:
    #递归
    def climbStairs1(self, n: int) -> int:
        if n == 1:
            return 1
        elif n ==2:
            return 2
        else:
            sum1 = self.climbStairs1(n - 1)
            sum2 = self.climbStairs1(n - 2)
            return sum1 + sum2

    #动态规划
    def climbStairs2(self, n: int) -> int:
        result = [1,2,3]
        if n <= 3:
            return  n
        else:
            for i in range(3,n):
                result.append(result[i - 1]+result[i-2])
            return result[-1]

import datetime
starttime = datetime.datetime.now()
s = Solution()
print(s.climbStairs2(30))
endtime = datetime.datetime.now()
print((endtime - starttime).microseconds)
