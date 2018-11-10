class interpolation:

    def linear_interpolation(self, pt1, pt2, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2
        take as input
        pt1: known point pt1 and f(pt1) or intensity value
        pt2: known point pt2 and f(pt2) or intensity value
        unknown: take and unknown location
        return the f(unknown) or intentity at unknown"""

        #Write your code for linear interpolation here
        if pt1[0][0] == pt2[0][0] :
            intensity = self.calculate(pt1,pt2,unknown,1)

        elif pt1[0][1] == pt2[0][1]:
            intensity = self.calculate(pt1, pt2, unknown, 0)

        return intensity

    def bilinear_interpolation(self, pt1, pt2, pt3, pt4, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2
        take as input
        pt1: known point pt1 and f(pt1) or intensity value
        pt2: known point pt2 and f(pt2) or intensity value
        pt1: known point pt3 and f(pt3) or intensity value
        pt2: known point pt4 and f(pt4) or intensity value
        unknown: take and unknown location
        return the f(unknown) or intentity at unknown"""

        # Write your code for bilinear interpolation here
        # May be you can reuse or call linear interpolatio method to compute this task

        unknown1 = list(pt1[0])
        unknown1[0] = unknown[0]
        unknown1 = tuple(unknown1)
        intensity1 = self.linear_interpolation(pt1,pt2,unknown1)

        unknown2 = list(pt3[0])
        unknown2[0] = unknown[0]
        unknown2 = tuple(unknown2)
        intensity2 = self.linear_interpolation(pt3,pt4,unknown2)

        intensity = self.linear_interpolation((unknown1,intensity1),(unknown2,intensity2),unknown)
        #print(intensity)
        return intensity


    def calculate(self,pt1,pt2,unknown,i):
        #print(pt1,pt2,unknown,i)
        return (((pt2[0][i] - unknown[i]) * pt1[1]) + ((unknown[i] - pt1[0][i]) * pt2[1]))/(pt2[0][i] - pt1[0][i])