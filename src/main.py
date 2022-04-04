from solver import *

try:
    print("15 Puzzle Solver Using BNB")
    print("\nChoose your input :\n1. Random By Program\n2. File Input")
    Option = int(input("\nSelect Option : "))
    if Option == 1:
        print("\nRandom By Program may take a while to generate a solution.\n")
        print("\nContinue? (y/n)\n")
        if input("(y/n) : ") == "y":
            print("\nGenerating random puzzle...")
            puzzle = randomize()
            final = read_matrix("final.txt")
            print("Puzzle To Solve:\n")
            printMatrix(puzzle)
            print("Kurang[i] Value:\n")
            listKurang = [0]*17
            sigmakurang = sigmaKurang(puzzle, listKurang)
            for i in range(1,17):
                print("kurang[" + str(i)+ "] = " + str(listKurang[i]))
            print("\nSigma Kurang[i] + X: "+ str(sigmaKurangIPlusX(sigmakurang, checkEmptyPosition(puzzle)))+ "\n")
            solve(puzzle, final)
        else:
            print("\nProgram dihentikan\n")
            exit()
    elif Option == 2:
        filename = input("\nInput Filename: ")
        file = "../test/" + filename
        puzzle = read_matrix(file)
        final = read_matrix("final.txt")
        print("Puzzle To Solve:\n")
        printMatrix(puzzle)
        print("Kurang[i] Value:\n")
        listKurang = [0]*17
        sigmakurang = sigmaKurang(puzzle, listKurang)
        for i in range(1,17):
            print("kurang[" + str(i)+ "] = " + str(listKurang[i]))
        print("\nSigma Kurang[i] + X: "+ str(sigmaKurangIPlusX(sigmakurang, checkEmptyPosition(puzzle)))+ "\n")
        solve(puzzle, final)
    else:
        print("\nInvalid Input. Program Stop\n")

except:
    print("\nInvalid filename input, make sure your test case is already in test folder. Program Stop\n")