class Solution:

    #遍历
    def maxSubArray(self, nums) -> int:
        max = -2**31
        tempsum = 0

        for i,item in enumerate(nums):
            tempsum += item
            max = max if max > tempsum else tempsum

            if tempsum < 0:
                tempsum = 0

        return max

        #dongtai
        # sum[i] = max(sum[i - 1] + a[i], a[i])
        # length = len(nums)
        # for i in range(1, length):
        #     # 当前值的大小与前面的值之和比较，若当前值更大，则取当前值，舍弃前面的值之和
        #     subMaxSum = max(nums[i] + nums[i - 1], nums[i])
        #     nums[i] = subMaxSum  # 将当前和最大的赋给nums[i]，新的nums存储的为和值
        # return max(nums)




s = Solution()
print(s.maxSubArray([-2,1,-3,4,-1,2,1,-5,4]))