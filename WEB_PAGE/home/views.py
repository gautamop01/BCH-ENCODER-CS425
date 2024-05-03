from django.shortcuts import render

import math
def gf_add(a, b):
    return a ^ b  # XOR operation for binary fields

def gf_multiply(a, b, irreducible_poly):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & (1 << len(bin(irreducible_poly)) - 3):
            a ^= irreducible_poly
        b >>= 1
    return result

def closest_power_of_2(n):
    power = 1
    while power <= n:
        power <<= 1
    return power >> 1

def find_primitive_elements(irreducible_poly):
    field_size = closest_power_of_2(irreducible_poly)
    primitive_elements = []
    for alpha in range(1, field_size):  # Iterate over all elements in GF(2^4)
        powers = set()
        current = alpha
        for _ in range(field_size - 1):  # Order of multiplicative group of GF(2^4) is 15
            powers.add(current)
            current = gf_multiply(current, alpha, irreducible_poly)
        if len(powers) == field_size - 1 and 1 in powers:  # Check if all powers are distinct and 1 is included
            primitive_elements.append(alpha)
    return primitive_elements[0]

# Irreducible polynomial for GF(2^4)

def bintoint(binnum : str):
    result = 0
    for i in range(len(binnum)):
        result+=(int(binnum[i]) * 2**i)
    return result



def find_conjugates(alpha, irreducible_poly):
    conjugates = []
    conjugate = 1
    field_size = 1 << len(bin(irreducible_poly)) - 3
    for _ in range(field_size):
        conjugate = gf_multiply(alpha, conjugate, irreducible_poly)
        conjugates.append(conjugate)
    return conjugates



def mult(poly1, poly2):
    result = []
    max_deg = max(len(poly1),len(poly2))
    for _ in range(max_deg + 1):
        result.append([])
    for i in range(len(poly1)):
        for j in range(len(poly1[i])):
            for k in range(len(poly2)):
                for l in range(len(poly2[k])):
                    curr = poly1[i][j] * poly2[k][l]
                    if curr in result[i+k]:
                        result[i+k].remove(curr)
                        result[i+k].append(curr * 2)
                    else:
                        (result[i+k]).append(curr)
    
    return result

def convert_to_single_list(poly):
    result = []
    for i in range(len(poly)):
        curr = 0
        for j in range(len(poly[i])):
            if poly[i][j] == 1:
                curr += 1
            else:
                power = math.log2(poly[i][j])
                if power == 1:
                    curr += 0

                elif power and 1:
                    curr += 1
                else:
                    curr += 0
        result.append(curr % 2)
    
    return result

def compute_mxi(roots : set, conjugates, primitive_element):
    powers = []
    for i in roots:
        for j in range(len(conjugates)):
            if conjugates[j] == i:
                powers.append(j + 1)
                break
    polys = []
    for i in powers:
        polys.append([[1],[primitive_element**i]])
    while len(polys) > 1:
        poly_1 = polys.pop()
        poly_2 = polys.pop()
        polys.append(mult(poly_1,poly_2))
    proper_poly = convert_to_single_list(polys[0])
    return proper_poly





def multiply_poly(poly1 : list,poly2 : list):
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


def encoder(irreducible_poly_str: str, redudancy : int, message : str):
    irreducible_poly = bintoint(irreducible_poly_str)
    field_size = closest_power_of_2(irreducible_poly)
    primitive_element = find_primitive_elements(irreducible_poly)
    conjugates = find_conjugates(primitive_element, irreducible_poly)
    t = redudancy

    m_xs = []
    for i in range(1,2*t,2):
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
        m_xs.append(multiply_poly(poly1,poly2))

    generator_polynomial = m_xs[0]


    message = [0 if c == '0' else 1 for c in message]

    encoded_message = multiply_poly(message, generator_polynomial)

    return generator_polynomial, encoded_message


# Create your views here.
def home(request):
    if request.method == 'POST':
        irreducible_poly_str = request.POST.get('irreduciblePoly')
        field_size = closest_power_of_2(bintoint(irreducible_poly_str))
        redudancy = int(request.POST.get('redundancy'))
        message = request.POST.get('message')
        generator_poly, encoded_message = encoder(irreducible_poly_str=irreducible_poly_str, redudancy=redudancy, message=message)
        context = {}
        if len(message) != field_size -  len(generator_poly):
            context = {'Error' : "Message Length Not Compatible, Message Length should be {}".format(field_size - len(generator_poly))}
        else:
            context = {'generator_poly' : generator_poly, 'encoded_message': encoded_message}
        
        return render(request,'home.html',context=context)
    
    return render(request,'home.html')