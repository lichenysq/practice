# Given an array of integers, return indices of the two numbers such that they add up to a specific target.
# 输入一个整数数组，从数组找出两个数使得他们的和等于一个给定的值，返回它们在数组中的位置。
#
# You may assume that each input would have exactly one solution, and you may not use the same element twice.
# 你需要确保每个输入的数组都有一个确定的解，并且每个元素只能使用一次。

def twoSum(self, nums, target):
    dic = {}
    for i, num in enumerate(nums):
        if num in dic:
            return [dic[num], i]
        else:
            dic[target - num] = i


