import math  # Import the math module for mathematical operations


# Bose–Chaudhuri–Hocquenghem


# Function to add two numbers in Galois Field using XOR operation
def gf_add(a, b):
    return a ^ b  # XOR operation for binary fields

# Function to multiply two numbers in Galois Field modulo an irreducible polynomial
def gf_multiply(a, b, irreducible_poly):
    result = 0  # Initialize the result variable to store the multiplication result
    while b:  # Continue the loop until b becomes zero
        if b & 1:  # If the least significant bit of b is 1
            result ^= a  # Add 'a' to the result using XOR operation
        a <<= 1  # Left shift 'a' by one bit (equivalent to multiplying 'a' by 2)
        if a & (1 << len(bin(irreducible_poly)) - 3):  # Check if the degree of 'a' is greater than or equal to the degree of the irreducible polynomial
            a ^= irreducible_poly  # If so, subtract the irreducible polynomial from 'a' using XOR operation
        b >>= 1  # Right shift 'b' by one bit (equivalent to dividing 'b' by 2)
    return result  # Return the result of the multiplication modulo the irreducible polynomial


# Function to find the closest power of 2 less than or equal to a given number
def closest_power_of_2(n):
    power = 1  # Start with the power of 2 as 1
    while power <= n:  # Continue doubling the power of 2 until it exceeds or equals the given number
        power <<= 1  # Left shift the power by 1 bit (equivalent to multiplying by 2)
    return power >> 1  # Right shift the power by 1 bit to get the closest power of 2 less than or equal to the given number


# Function to find primitive elements in a Galois Field
def find_primitive_elements(irreducible_poly):
    field_size = closest_power_of_2(irreducible_poly)  # Find the size of the Galois Field
    primitive_elements = []  # Initialize a list to store primitive elements
    for alpha in range(1, field_size):  # Iterate over all elements in the Galois Field
        powers = set()  # Initialize a set to store the powers of the current element
        current = alpha  # Start with the current element as alpha
        for _ in range(field_size - 1):  # Iterate for the order of the multiplicative group
            powers.add(current)  # Add the current power to the set
            current = gf_multiply(current, alpha, irreducible_poly)  # Multiply by alpha in the Galois Field
        # Check if all powers are distinct and 1 is included
        if len(powers) == field_size - 1 and 1 in powers:
            primitive_elements.append(alpha)  # If so, add alpha to the list of primitive elements
    return primitive_elements[0]  # Return the first primitive element found


# Irreducible polynomial for GF(2^4)

# Function to convert a binary number (as a string) to an integer
def bintoint(binnum: str):
    result = 0  # Initialize the result variable to store the converted integer
    for i in range(len(binnum)):  # Iterate over each character in the binary string
        result += (int(binnum[i]) * 2**i)  # Convert the binary digit to integer and multiply by the corresponding power of 2, then add to the result
    return result  # Return the converted integer

# Function to find conjugates of an element in Galois Field
def find_conjugates(alpha, irreducible_poly):
    conjugates = []  # Initialize a list to store the conjugates of alpha
    conjugate = 1  # Start with the conjugate as 1
    field_size = 1 << len(bin(irreducible_poly)) - 3  # Calculate the size of the Galois Field
    for _ in range(field_size):  # Iterate for the size of the Galois Field
        conjugate = gf_multiply(alpha, conjugate, irreducible_poly)  # Calculate the conjugate of alpha
        conjugates.append(conjugate)  # Add the conjugate to the list of conjugates
    return conjugates  # Return the list of conjugates


# print("Conjugates of alpha:", conjugates)

# Function to multiply two polynomials represented as lists of coefficients
def mult(poly1, poly2):
    result = []  # Initialize the result list
    max_deg = max(len(poly1), len(poly2))  # Find the maximum degree among the two polynomials
    for _ in range(max_deg + 1):  # Initialize the result list with empty lists for each degree up to the maximum degree
        result.append([])
    for i in range(len(poly1)):  # Iterate over the terms of the first polynomial
        for j in range(len(poly1[i])):  # Iterate over the coefficients of the current term of the first polynomial
            for k in range(len(poly2)):  # Iterate over the terms of the second polynomial
                for l in range(len(poly2[k])):  # Iterate over the coefficients of the current term of the second polynomial
                    curr = poly1[i][j] * poly2[k][l]  # Multiply the coefficients of the current terms
                    if curr in result[i + k]:  # If the degree already exists in the result, update the coefficient
                        result[i + k].remove(curr)
                        result[i + k].append(curr * 2)
                    else:  # Otherwise, add the coefficient to the result
                        (result[i + k]).append(curr)
    
    return result  # Return the result list of coefficients for the multiplied polynomial


# Function to convert a list of polynomial coefficients into a single list representing the polynomial
def convert_to_single_list(poly):
    result = []  # Initialize the result list to store the converted polynomial
    for i in range(len(poly)):  # Iterate over each term in the polynomial
        curr = 0  # Initialize the current coefficient value
        for j in range(len(poly[i])):  # Iterate over the coefficients of the current term
            if poly[i][j] == 1:  # If the coefficient is 1, add 1 to the current value
                curr += 1
            else:  # If the coefficient is not 1, calculate the power of 2 represented by the coefficient
                power = math.log2(poly[i][j])  # Calculate the power of 2
                if power == 1:  # If the power is 1, add 0 to the current value (2^1 = 2, which is not included in the polynomial)
                    curr += 0
                elif power and 1:  # If the power is an integer and not equal to 1, add 1 to the current value
                    curr += 1
                else:  # If the power is not an integer, add 0 to the current value (2^0 = 1, which is included in the polynomial)
                    curr += 0
        result.append(curr % 2)  # Append the current value modulo 2 to the result list (to get either 0 or 1)
    
    return result  # Return the result list representing the converted polynomial


# Function to compute the m(x)i polynomial
def compute_mxi(roots: set, conjugates, primitive_element):
    powers = []  # Initialize a list to store the powers corresponding to the roots
    for i in roots:  # Iterate over the roots
        for j in range(len(conjugates)):  # Iterate over the conjugates
            if conjugates[j] == i:  # If the conjugate matches the root
                powers.append(j + 1)  # Add the power (index + 1) to the powers list
                break  # Break the inner loop
    polys = []  # Initialize a list to store the polynomial terms
    for i in powers:  # Iterate over the powers
        polys.append([[1], [primitive_element**i]])  # Create a term [1, primitive_element^i] and add it to polys
    while len(polys) > 1:  # Continue until there is only one polynomial left in polys
        poly_1 = polys.pop()  # Remove and get the last polynomial from polys
        poly_2 = polys.pop()  # Remove and get the second-last polynomial from polys
        polys.append(mult(poly_1, poly_2))  # Multiply the two polynomials and add the result back to polys
    proper_poly = convert_to_single_list(polys[0])  # Get the first polynomial from polys and convert it to a single list
    return proper_poly  # Return the final m(x)i polynomial


# Function to multiply two polynomials modulo 2
def multiply_poly(poly1: list, poly2: list):
    deg1 = len(poly1) - 1
    deg2 = len(poly2) - 1
    
    # Initialize the result polynomial
    result_deg = deg1 + deg2
    result_poly = [0] * (result_deg + 1)
    
    # Perform polynomial multiplication modulo 2
    for i in range(deg1 + 1):
        for j in range(deg2 + 1):
            # Multiply the coefficients and add to the corresponding term in the result polynomial modulo 2
            result_poly[i + j] ^= poly1[i] * poly2[j]
    
    return result_poly

# Main function
def main():
    # Read the irreducible polynomial
    irreducible_poly_str = input("Enter Irreducible Polynomial: ")
    irreducible_poly = bintoint(irreducible_poly_str)
    field_size = closest_power_of_2(irreducible_poly)
    primitive_element = find_primitive_elements(irreducible_poly)
    conjugates = find_conjugates(primitive_element, irreducible_poly)
    t = int(input("Enter the desired redundancy: "))

    m_xs = []
    for i in range(1, 2 * t, 2):
        alpha = conjugates[i - 1]
        conjugate_roots = set()
        conjugate_roots.add(alpha)
        j = i
        while True:
            j = j * 2 % (field_size - 1)
            if conjugates[j - 1] in conjugate_roots:
                break
            conjugate_roots.add(conjugates[j - 1])
        mxi = compute_mxi(conjugate_roots, conjugates, primitive_element)
        m_xs.append(mxi)
    
    while len(m_xs) > 1:
        poly1 = m_xs.pop()
        poly2 = m_xs.pop()
        m_xs.append(multiply_poly(poly1, poly2))

    generator_polynomial = m_xs[0]
    print('\nGenerated polynomial is : ', generator_polynomial, '\n')

    message = input("Enter the Message: ")

    message = [0 if c == '0' else 1 for c in message]

    encoded_message = multiply_poly(message, generator_polynomial)

    print(encoded_message)

if __name__ == '__main__':
    main()
