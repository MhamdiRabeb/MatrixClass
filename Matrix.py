import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        det=0.0
        if self.h > 1:
            #for a 2x2 matrix: self=((a,b),(c,d))
            #det=ad-bc
            det=self[0][0]*self[1][1]-self[0][1]*self[1][0]
        else:
            #for a 1*1 matrix self=a
            #det=absolute value(a)
            det=self[0][0]
            if det < 0:
                det=-det
        return det

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        #trace of self is the sum of main diagonal elements
        #on the main diagonal i=j
        tr=0
        for i in range(self.w):
            tr=tr+self[i][i]
        return tr


    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")      
        
        if self.h==1: 
            det=self.determinant()
            inv = zeroes((self.w),(self.h))      
            inv[0][0]=(1/det)
        elif self.h==2:   
            I=identity(self.h)
            tr=self.trace()
            A = self.g
            det=self.determinant()
            inv = zeroes((self.w),(self.h))       
            inv=(1/det)*((tr*I)-A)
            
        return inv

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """       
        tr = zeroes((self.w),(self.h))
        for i in range(self.w):
            for j in range(self.h):
                tr[i][j]=self.g[j][i]             
        return tr


    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same")
        
        #addition of element by element of each Matrix
        sm = zeroes((self.w),(self.h))
        for i in range(self.w):
            for j in range(self.h):
                sm[i][j]=self[i][j]+other[i][j]
        return sm

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        # negative value of each element
        neg=self.g
        neg=Matrix.__rmul__(self,-1)
        return neg


    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        #substraction of element by element of each Matrix
        sb = zeroes((self.h),(self.w))
        for i in range(self.h):
            for j in range(self.w):
                sb[i][j]=self[i][j]-other[i][j]
        return sb


    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        if(self.w==other.h):            
            ml = zeroes((self.h),(other.w))
            for i in range(self.h):
                for j in range(other.w):
                    for k in range(other.h):
                        ml[i][j] += self[i][k]*other[k][j]
            return ml
        else:
            raise(ValueError, "Matrices can only be added if width of self is equal to height of other")    

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            pass
           
            rml = zeroes((self.w),(self.h))
            for i in range(self.h):
                for j in range(self.w):
                    rml[i][j]=self[i][j]*other
            return rml

            
