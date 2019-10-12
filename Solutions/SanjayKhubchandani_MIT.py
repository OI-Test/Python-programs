n = int(input())
pf = []
while n>1:
	if (n%2 == 0):
		n = n/2 
		pf.append("2")
	elif (n%3 == 0):
		n = n/3 
		pf.append("3")
	elif (n%5 == 0):
		n = n/5 
		pf.append("5")
	elif (n%7 == 0):
		n = n/7
		pf.append("7")
	else :
		pf.append(n)
		break
print(pf)
