class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __str__(self):
        output = str(self.feet) + " feet, " + str(self.inches) + " inches"
        return output
    
    def __sub__(self, other):
        # Converting both objects' height into inches
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches

        # Subtract heights to find difference
        total_height_inches = height_A_inches - height_B_inches

        # Get output in feet
        output_feet = total_height_inches // 12
        
        #Get output in inches
        output_inches = total_height_inches - (output_feet *12)

        # Return final output as a new height object
        return Height(output_feet, output_inches)

person_A_height = Height(5, 10)
person_B_height = Height(4, 9)
height_difference = person_A_height - person_B_height

print("Height difference: ", height_difference)