# from itertools import groupby
# from operator import itemgetter
A = [2,3,4,5,6,6,7,7,8,8]
# newA = []
# for x in :
#   if x % 1 == 0:
#       newA.append(x*2)

# print(newA)
# print(type(newA))

# g = [x for x in A]
# print(g)
# # print(type(g))    
# # print("i want to suck")
# newA2 = {x*2 for x in A}
# print(type(newA2))
# f = {x: x*2 for x in A}
# print(f)

# nums = [2,3,4]
# for i in range(len(nums)):

# print(nums)
# print("who's watching me???")
# print(100/x)
# A = [5,6]
# B = [x for x in A if x % 2 == 0]
# print(B)

# async def foo():
#   print('d')

# print(158//158)
# def lone_sum(a, b, c):
# 	sum = 0
# 	if a != b and a != c: sum += a
# 	if b != a and b != c: sum += b
# 	if c != a and c != b: sum += c

# 	return sum
# print(lone_sum(2,3,5))


def sum(n):
	if n//5>=5:
		print(n)
	else:
		print("hey")
sum(6)

def round_sum(a, b, c):
  def round10(num):
    if (num-10*(num//10))>=5:
      return num + ((num//10+1)*10-num)
    else:
      return num - num%5
  return round10(a) +  round10(b) + round10(c)


def round10(num):
  mod = num % 10
  num -= mod
  if mod >= 5: num += 10
  return num
print(round10(6))





# F = 1
# FACTORS = 0
# while True:
#   if NUM%F == 0:
#       D = NUM//F
#       print(NUM, "=", F, "*", D)
#       if F == 1:
#           FACTORS = FACTORS + 0
#       elif F == D:
#           FACTORS = FACTORS + 1
#       else:
#           FACTORS = FACTORS + 2
#   F =+ 1
#   if F*F > NUM:
#       break

# print(NUM, FACTORS)

# test = '''
# 19.23 math
# 1924 math
# 24/39 tok
# '''




# x = 3
# y = 2
# if x != y:
#   print("fuck")
# print(x==y)
# c = 2
# def b():
# 	a = 1
# 	a==c
# 	print(a)
# b()







# nums = [1,2,3]

# print(len(nums))

def sum(nums):
	 for i in range(len(nums)):
		nums[i-1] + 
	return nums
print(sum(nums))	


# # def string_splosion(str):
# #   result = ""
# #   for i in range(len(str)):
# #     result = result + str[:i+1]
# #   return result
# # print("str"[:3])
# # print(string_splosion("Code"))
# #CCoCodCode

# str = "asdsa"
# A = ['A', 'b', 'c']
# for I in range(len(A)-1):
# 	T=A[I]
# 	A[I]=A[:I+1]
# 	A[:-I+1] = T
# 	I = I + 1
# 	if I == 2:
# 		break
# print(A)