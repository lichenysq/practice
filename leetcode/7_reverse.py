#-*-coding:utf-8-*-
# 给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。
#
# 示例 1:
#
# 输入: 123
# 输出: 321
#  示例 2:
#
# 输入: -123
# 输出: -321
# 示例 3:
#
# 输入: 120
# 输出: 21
# 注意:
#
# 假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [−231,  231 − 1]。请根据这个假设，如果反转后整数溢出那么就返回 0。

class Solution:
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        strx = str(x)
        if len(strx) == 1:
            return x

        rever_strx = strx[::-1]
        for i in range(len(rever_strx)):
            if rever_strx[0] == "0":
                rever_strx = rever_strx[1:]
        if rever_strx[-1] == "-":
            rever_strx = rever_strx[:-1]
            rever_strx = "-" + rever_strx

        rever_x = int(rever_strx)
        if rever_x > 2**31 - 1 or rever_x < -(2**31):
            return 0
        else:
            return rever_x




a = Solution()
print(a.reverse(123))