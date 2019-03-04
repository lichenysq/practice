class Solution:
    # 动态规划  只能允许一次买卖：转变为 最大连续子数组之和得问题， 如果允许多次，则转变为非连续最大和问题
    #前n项和大于0 就可继续加    若小于0 ，则放弃前n项，取下一项为新数组的第一项，   取其中的最大值
    def maxProfit(self, prices):
        profit = []
        for i in range(len(prices)-1):
            profit.append(prices[i+1]-prices[i])

        print(profit)

        max = 0
        temp = 0
        for item in profit:
            if temp + item > 0:
                temp = temp + item
            else:
                temp = 0
            max = max if max > temp else temp

        print(max)

s = Solution()
s.maxProfit([7,1,5,3,6,4])