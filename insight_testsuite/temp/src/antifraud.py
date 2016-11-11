### Python code developed for the project "antifraud"
### Writen by Kun Zhang

### Parameter list

MaxDeg = 4      # Maximal degree taken cared by this code. It is adjustable.

Level3 = MaxDeg     ## must >= 3 and <= MaxDeg

import sys

### The class "Deg" is the most essential and used to store the degree information
### Just 1 instance in this project
class Deg:
    def __init__(self):

        ### The combination of self.User & self.Pos is for bidirectional diction
        ### They always have the same size
        self._ID = {}       # obtain User ID from position in triangle
        self._Pos = {}      # obtain sequence from User ID, starting from 0
                            # is the x-axis in triangle, while in y-axis: -1

        ### self.Deg is a lower triangle matrix, storing the degree information
        self._Deg = []
        self._IDNum = 0
        self._FileOutput = False
        self._FileExist = False


    ### Handle the first transaction
    def _FirstTran(self, ID1, ID2):

        self._ID[0] = ID1
        self._ID[1] = ID2
        self._Pos[ID1] = 0
        self._Pos[ID2] = 1
        self._Deg.append([1])
        self._IDNum += 2


    ### Add a new ID
    def _NewID(self, ID):

        self._IDNum += 1
        self._ID[self._IDNum - 1] = ID
        self._Pos[ID] = self._IDNum - 1
        self._Deg.append([0]*(self._IDNum-1))


    ### Get positions of all friends within "MaxDeg"th-degree
    def _GetFriP(self, P1):

        FP = [[P1]]

        for i in range(1, MaxDeg):
            FP.append([])

        ### Get position from row
        for i in range(0, P1):
            TheDeg = self._Deg[P1-1][i]
            if TheDeg >0 and TheDeg < MaxDeg:
                FP[TheDeg] += [i]

        ### Get position from column
        for i in range(P1, self._IDNum-1):
            TheDeg = self._Deg[i][P1]
            if TheDeg > 0 and TheDeg < MaxDeg:
                FP[TheDeg] += [i+1]

        return FP


    ### Set degree for a specific position
    def _SetDeg(self, P1, P2, Deg):
        py = max([P1, P2])-1
        px = min([P1, P2])
        if self._Deg[py][px] > Deg or self._Deg[py][px] == 0:
            self._Deg[py][px] = Deg;


    ### Set degrees based on positions
    def _SetDegs(self, FP1, FP2):

        l1 = len(FP1)
        l2 = len(FP2)

        if l1 == 1 and l2 == 1:
            self._SetDeg(FP1[0], FP2[0], 1)

        elif l1 == MaxDeg and l2 == 1:
            for i in range(0, l1):
                for m in FP1[i]:
                    self._SetDeg(m, FP2[0], i+1)

        elif l1 == 1 and l2 == MaxDeg:
            for i in range(0, l2):
                for m in FP2[i]:
                    self._SetDeg(FP1[0], m, i+1)

        elif l1 == MaxDeg and l2 == MaxDeg:
            for i in range(0,l1):
                for j in range(0, MaxDeg-i):
                    for m in FP1[i]:
                        for n in FP2[j]:
                            if m != n:      # not a same node
                                self._SetDeg(m, n, i+j+1)

        else:
            print('Error: friends position variable has a wrong size!')
            sys.exit()


    ### Handle a regular transaction
    def _Tran(self, ID1, ID2):

        if ID1 not in self._ID.values() and ID2 not in self._ID.values():
            self._NewID(ID1)
            self._NewID(ID2)
            self._SetDegs([self._Pos[ID1]], [self._Pos[ID2]])

        elif ID1 not in self._ID.values() and ID2 in self._ID.values():
            self._NewID(ID1)
            self._FriP2 = self._GetFriP(self._Pos[ID2])
            self._SetDegs([self._Pos[ID1]], self._FriP2)

        elif ID1 in self._ID.values() and ID2 not in self._ID.values():
            self._FriP1 = self._GetFriP(self._Pos[ID1])
            self._NewID(ID2)
            self._SetDegs(self._FriP1, [self._Pos[ID2]])

        elif ID1 in self._ID.values() and ID2 in self._ID.values():
            self._FriP1 = self._GetFriP(self._Pos[ID1])
            self._FriP2 = self._GetFriP(self._Pos[ID2])
            self._SetDegs(self._FriP1, self._FriP2)


    ### Get degree
    def _GetDeg(self, ID1, ID2):
        if ID1 not in self._ID.values() or ID2 not in self._ID.values():
            return 0
        else:
            p1, p2 = self._Pos[ID1], self._Pos[ID2]
            return self._Deg[max([p1, p2])-1][min([p1, p2])]


    ### Open files for writing results
    def OpenFiles(self, FileOut):

        self._FileOutput = True

        if self._FileOutput and not self._FileExist:
            self._File1 = open(FileOut[0], 'w')
            self._File2 = open(FileOut[1], 'w')
            self._File3 = open(FileOut[2], 'w')
            self._FileExist = True

        elif self._FileOutput and self._FileExist:
            self._File1 = open(FileOut[0], 'a+')
            self._File2 = open(FileOut[1], 'a+')
            self._File3 = open(FileOut[2], 'a+')


    ### Close files
    def CloseFiles(self):
        if self._FileOutput:
            self._File1.close()
            self._File2.close()
            self._File3.close()
            self._FileOutput = False


    ### Output results to files
    def _Output2File(self, theDeg):

        if theDeg < 1 or theDeg > MaxDeg:
            self._File1.write('unverified\n')
            self._File2.write('unverified\n')
            self._File3.write('unverified\n')

        elif theDeg == 1:
            self._File1.write('trusted\n')
            self._File2.write('trusted\n')
            self._File3.write('trusted\n')

        elif theDeg == 2:
            self._File1.write('unverified\n')
            self._File2.write('trusted\n')
            self._File3.write('trusted\n')

        else:
            self._File1.write('unverified\n')
            self._File2.write('unverified\n')
            self._File3.write('trusted\n')

    def _SendWarning(self, theDeg):

        if theDeg < 1 and theDeg > MaxDeg:
            print("unverified: This user is beyond the friend range you set. \
            Are you sure you would like to proceed with this payment?")
        elif theDeg == 1:
            pass
        elif theDeg == 2:
            print("unverified: You've never had a transaction with this user before. \
            Are you sure you would like to proceed with this payment?")
        else:
            print("unverified: This user is not a friend or a \"friend of a friend\". \
            Are you sure you would like to proceed with this payment?")


    ### Process each transaction
    def ProcTran(self, ID1, ID2):

        self._theDeg = self._GetDeg(ID1, ID2)

        ### Warnings
        # self._SendWarning(self._theDeg)

        ### Outputs to files
        if self._FileOutput:
            self._Output2File(self._theDeg)

        if len(self._ID) == 0:
            self._FirstTran(ID1, ID2)
        else:
            self._Tran(ID1, ID2)

    def __exit__(self):
        if self._FileOutput:
            self.CloseFiles()

### Get ID from each transaction and ignore other information
def GetID(FileName):

    User = []

    with open(FileName, 'r+', newline='') as f:
        strf = f.read()
        strs = strf.split('\n')

    for m in range(1, len(strs)):       ### jump the first line
        n = strs[m].split(',')
        if len(n) > 2:
            if n[1] != n[2]:
                User.append([n[1].strip(), n[2].strip()])
            else:
                print('Error: You cannot make a transaction with yourself\n')
                sys.exit()

    return User


###### Main program ###############################################

def main(argv):
    D = Deg()

    ### Extract user ID from the past data
    ID0 = GetID(argv[1])

    ### Build library based on the past data
    for m in ID0:
        D.ProcTran(m[0], m[1])

    ### Begin to output
    D.OpenFiles(argv[3:6])

    ### Extract user ID from the "stream" data
    ID1 = GetID(argv[2])

    ### Process the "stream" data and output to files
    for n in ID1:
        D.ProcTran(n[0], n[1])


import sys

if __name__ == '__main__':
    main(sys.argv)