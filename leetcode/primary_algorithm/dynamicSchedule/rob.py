
# https://blog.csdn.net/qq_34364995/article/details/80544497
class Solution:
    def rob(self, nums) -> int:
        #r[i] = max(r[i-1],r[i-2]+nums[i])
        r = {}
        if len(nums) == 0:
            return 0
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums[0], nums[1])
        else:
            r[0] = nums[0]
            r[1] = max(nums[0], nums[1])
            for i in range(2, len(nums)):
                r[i] = max(r[i - 1], r[i - 2] + nums[i])
        return r[len(nums) - 1]



        # last = 0
        # now = 0
        # for i in nums:
        #     last, now = now, max(last + i, now)
        # print(now)
        # return now


s = Solution()
print(s.rob([2,7,9,3,1]))