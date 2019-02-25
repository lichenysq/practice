# 给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。
#
# 示例 1:
#
# 输入: "abcabcbb"
# 输出: 3
# 解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
# 示例 2:
#
# 输入: "bbbbb"
# 输出: 1
# 解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
# 示例 3:
#
# 输入: "pwwkew"
# 输出: 3
# 解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
#      请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
class Solution:
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """

        maxlen = len(set(s))
        if maxlen <= 2:
            return maxlen

        for trylen in list(range(3,maxlen+1))[::-1]:
            maxtry = len(s) - trylen
            for i in range(maxtry+1):
                if len(s[i:i + trylen]) == len(set(s[i:i + trylen])):
                    print(s[i:i + trylen])
                    return trylen



so = Solution()
print(so.lengthOfLongestSubstring("ohvhjdml"))



