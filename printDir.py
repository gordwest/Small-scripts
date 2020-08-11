import os, sys

def printDir(directory, baseLevel, showHidden=False):
    """ recursively print the directory tree of a given directory
    params:
        directory: string - current directory the function is on (first will be the cwd)
        baseLevel: int - level of root directory (used to configure indenting of sub-directories)
        showHidden: bool - condition for printing hidden files 
    """
    files = os.listdir(directory) # get list directory
    indent = generateIndent(directory.count('/') - baseLevel) # configure indent size for current directory

    if showHidden: # check bool for printing hidden files
        for item in sorted(files, key=str.casefold):
            newPath = '{}/{}'.format(directory, item)
            if os.path.isdir(newPath):
                print(indent+item)
                printDir(newPath, baseLevel, showHidden) # recursively call the function again whenever it encounters a nested folder
            else:
                print(indent+item)
    else:
        for item in sorted(files, key=str.casefold):
            newPath = '{}/{}'.format(directory, item)
            if item[:1] != '.': # skip hidden files
                if os.path.isdir(newPath):
                    print(indent + item + ':')
                    printDir(newPath, baseLevel, showHidden) # recursively call the function again whenever it encounters a nested folder
                else:
                    print(indent + item)

def generateIndent(x):
    """ creates the correct indent given a size
    """
    i, indent = 0, ''
    while i < x:
        indent += '   '
        i += 1
    return indent

def main():
    path = os.getcwd()
    # path = '/Users/gord/Documents'
    baseLevel = path.count('/')

    try:
        cond = bool(sys.argv[1])
        printDir(path, baseLevel, cond)
    except:
        printDir(path, baseLevel)

if __name__ == "__main__":
    main()


