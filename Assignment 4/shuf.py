#!/usr/bin/python

import random, sys, string
from optparse import OptionParser

class shuf:
    def __init__(self, filename, headcount, repeat, inputRange, args):
        
        self.stdinUsed = False
        
        if (len(args) == 0 or (len(args) == 1 and args[0] == '-')) and inputRange is None:
            self.lines = sys.stdin.readlines()
            self.stdinUsed = True
        
        self.headcount = headcount
        
        
        headcountPassed = False
        if headcount < sys.maxsize:
            headcountPassed = True
        
        self.repeatForever = False
        self.inputRange = inputRange
        self.repeat = repeat
        
        #if the i flag is not passed
        if filename != None and self.stdinUsed is False:
            f = open(filename, 'r')
            self.lines = f.readlines()
        
        #if no headcount is passed
        if headcountPassed == False:
            #if i flag not passed
            if filename != None:
                headcount = self.headcount = len(self.lines)
            if self.repeat == True:
                self.repeatForever = True
        else:
            self.headcount = headcount
        
        #if the i flag is passed
        if filename == None:
            if repeat == True and headcountPassed == False:
                self.repeatForever = True
                self.headcount = headcount
            
            return
        
    
        #headcount > number of lines in file
        if headcount > len(self.lines) and headcount != sys.maxsize and self.repeat is False:
            headcount = len(self.lines)
            self.headcount = headcount
 
 
        if self.stdinUsed is False:
            f.close()

    
    def shuffle(self):
        if self.inputRange != None:
            numsInOrder = []
            for i in range(len(self.inputRange)):
                if self.inputRange[i] == '-':
                    firstNumber = self.inputRange[0:i]
                    secondNumber = self.inputRange[i+1:]
                    break
            for i in range(int(firstNumber), int(secondNumber) + 1):
                numsInOrder.append(str(i) + '\n')
                    #return numsInOrder
                    
           
            self.lines = numsInOrder
            
            #self.repeat = False
    
            # if no head count is specified
            
            
            
            if self.headcount >= sys.maxsize:
                self.headcount = len(numsInOrder)
            elif self.headcount > len(range(int(firstNumber), int(secondNumber) + 1)) and self.repeat == False:
                self.headcount = len(numsInOrder)
    
    
    
        shuffledLines = []
    
    
        if self.stdinUsed is True:
            self.headcount = len(self.lines)
    
    
        for i in range(self.headcount):
            randomLineNumber = random.choice(range(len(self.lines)))
            shuffledLines.append(self.lines[randomLineNumber])
            #to prevent repetition
            if self.repeat == False:
                del self.lines[randomLineNumber]
        return shuffledLines
        #return random.choice(self.lines)

def main():
    version_msg = "%prog 1.0"
    usage_msg = """%prog [OPTION]... [FILE]
  or:  shuf.py -i LO-HI [OPTION]...
Write a random permutation of the input lines to standard output.
    
With no FILE, or when FILE is -, read standard input."""

    parser = OptionParser(version=version_msg,
                          usage=usage_msg)
    parser.add_option("-n", "--head-count",
                      action="store", dest="headcount", default=sys.maxsize,
                      help="Output at most HEADCOUNT lines. By default, all input lines are output")
    parser.add_option("-r", "--repeat", action="store_true", dest="repeat", default=False, help="Output lines can be repeated")
    parser.add_option("-i", "--input-range", action="store", dest="inputRange", help="Act as if input came from a file containing the range of unsigned decimal integers LO-HI, one per line.")

    options, args = parser.parse_args(sys.argv[1:])

    
    try:
        headcount = float(options.headcount)
        headcount = int(headcount)
    except:
        parser.error("invalid line count: {0}".
                     format(options.headcount))

    if headcount == 0:
        return

    if headcount < 0:
        parser.error("invalid line count: {0}".
                     format(options.headcount))
    




#I'm adding this
    try:
        repeat = bool(options.repeat)
    except:
        parser.error("invalid REPEAT: {0}".
                     format(options.repeat))

    #input range error check
    inputRange = options.inputRange





    #can't use i flag and supply a file
    if len(args) > 0 and inputRange is not None:
        parser.error("extra operand: {0}".
                     format(args[0]))

    #if it doesn't contain a dash, throw an error
    if inputRange is not None:
        #if it doesn't contain a dash, throw an error
        numDashes = 0
        for character in inputRange:
            if character == '-':
                numDashes += 1
        if numDashes != 1:
            parser.error("invalid input range: {0}".
                         format(options.inputRange))
        #now we know it has one dash, let's separate it into parts
        for i in range(len(inputRange)):
            if inputRange[i] == '-':
                firstNumber = inputRange[0:i]
                secondNumber = inputRange[i+1:]
                break
        try:
            firstNumber = int(firstNumber)
        except:
            parser.error("invalid input range: {0}".
                         format(firstNumber))
                         
        try:
            secondNumber = int(secondNumber)
        except:
            parser.error("invalid input range: {0}".
                 format(secondNumber))
                
        if firstNumber > secondNumber:
            parser.error("invalid input range: {0}".
                     format(options.inputRange))
    

    if inputRange is None and len(args) > 0:
        input_file = args[0]
    else:
        input_file = None

    try:
        generator = shuf(input_file, headcount, repeat, inputRange, args)
         
        if generator.repeatForever == True:
            while True:
                shuffledFile = generator.shuffle()
                for currLine in shuffledFile:
                    sys.stdout.write(currLine)

         
        shuffledFile = generator.shuffle()
        for currLine in shuffledFile:
            sys.stdout.write(currLine)
    except IOError as e:
        errno = e.errno
        strerror = e.strerror
        parser.error("I/O error({0}): {1}".
                     format(errno, strerror))

if __name__ == "__main__":
    main()
