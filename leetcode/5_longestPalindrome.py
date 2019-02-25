# 给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。
#
# 示例 1：
#
# 输入: "babad"
# 输出: "bab"
# 注意: "aba" 也是一个有效答案。
# 示例 2：
#
# 输入: "cbbd"
# 输出: "bb"


class Solution:
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        maxlen = len(s)
        while True:
            i = 0
            while i + maxlen <= len(s):
                templist = s[i:i + maxlen]
                reverttemplist = templist[::-1]
                if templist == reverttemplist:
                    return templist
                i = i + 1
            maxlen = maxlen - 1
            if maxlen == 0:
                return "No solution"