#-*-coding:utf-8-*-
class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        n = l1
        num_l1 = ""
        # get num of l1
        while n:
            num_l1 = num_l1 + str(n.val)
            n = n.next
        num_l1 = num_l1[::-1]

        m = l2
        num_l2 = ""
        # get num of l1
        while m:
            num_l2 = num_l2 + str(m.val)
            m = m.next
        num_l2 = num_l2[::-1]

        result = str(int(num_l1) + int(num_l2))
        rev_result = result[::-1]

        list_result = []
        for s in rev_result:
            list_result.append(int(s))
        return list_result