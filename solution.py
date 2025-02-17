class Solution:
    def plusOne(self, digits: list[int]):
        print(digits)
        sol = ""
        for x in digits:
            sol += str(x)
        sol = str((int(sol)) + 1)

        sol = [int(x) for digit in sol]
        return sol


sol = Solution()
num = sol.plusOne(list({1, 2, 3}))
print(type(num[0]))
