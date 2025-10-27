from argparse import ArgumentParser
import os
from math import cos,sin

def generate_dft_coefficients(size):
    cos_coeff = []
    sin_coeff = []
    for k in range(size):
        cos_row = []
        sin_row = []
        for n in range(size):
            angle = -2 * 3.141592653589793 * k * n / size
            cos_row.append(f"{round(cos(angle), 6)}")
            sin_row.append(f"{round(sin(angle), 6)}")
        cos_coeff.append(cos_row)
        sin_coeff.append(sin_row)
    return cos_coeff, sin_coeff

def dft_coefficients_to_c(cos_coeff, sin_coeff):
    size = len(cos_coeff)
    cos_coeff = [[f"{float(val):.6f}" for val in row] for row in cos_coeff]
    sin_coeff = [[f"{float(val):.6f}" for val in row] for row in sin_coeff]
    header_lines = []
    header_lines.append(f"#ifndef DFT_COEFFICIENTS_{size}_H")
    header_lines.append(f"#define DFT_COEFFICIENTS_{size}_H\n")
    
    header_lines.append(f"const float cos_coeff_table[{size}][{size}] = {{")
    for row in cos_coeff:
        header_lines.append("    {" + ", ".join(row) + "},")
    header_lines.append("};\n")
    
    header_lines.append(f"const float sin_coeff_table[{size}][{size}] = {{")
    for row in sin_coeff:
        header_lines.append("    {" + ", ".join(row) + "},")

    header_lines.append("};\n")
    header_lines.append(f"#endif // DFT_COEFFICIENTS_{size}_H")
    return "\n".join(header_lines)

if __name__ == "__main__":
    parser = ArgumentParser(description="Generate DFT input files.")
    parser.add_argument("directory", type=str, help="directory to generate coefficients")
    parser.add_argument("size", type=int, help="number of coefficients to generate")

    args = parser.parse_args()
    
    cos_coeff, sin_coeff = generate_dft_coefficients(args.size)
    header_string = dft_coefficients_to_c(cos_coeff, sin_coeff)
    print(header_string)
    
    filename = f"coefficients{args.size}_2D.h"
    filepath = f"{args.directory}/{filename}"
    os.makedirs(args.directory, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(header_string)