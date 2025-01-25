

def checkDirectionFacing(rows: int, cols: int):
    if rows > cols:
        if cols % 2 == 0:
            return "U"
        else: 
            return "D"
    else:
        if rows % 2 == 0:
            return "L"
        else:
            return "R"

cases = int(input())
for i in range(cases):
    rows, cols = map(int, input().split())
    print(checkDirectionFacing(rows, cols))
    
    



