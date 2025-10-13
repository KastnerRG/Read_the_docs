import re

def parse_fir_report(file_path):
    results = {
        "Estimated Clock Period (ns)": None,
        "Latency max (cycles)": None,
        "Interval max (cycles)": None,
        "BRAM_18K Total": None,
        "DSP Total": None,
        "FF Total": None,
        "LUT Total": None
    }

    with open(file_path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        # Estimated Clock Period
        if "Clock" in line and "Target" in line and "Estimated" in line:
            # The next line should contain the data
            clock_line = lines[i + 2]
            match = re.search(r'\|\s*\w+\s*\|\s*[\d.]+\s*ns\|\s*([\d.]+)\s*ns', clock_line)
            if match:
                results["Estimated Clock Period (ns)"] = float(match.group(1))

        # Latency and Interval
        if "Latency (cycles)" in line:
            data_line = lines[i + 3]
            parts = [p.strip() for p in data_line.strip('|').split('|')]
            if len(parts) >= 6:
                try:
                    results["Latency max (cycles)"] = int(parts[1])
                    results["Interval max (cycles)"] = int(parts[5])
                except ValueError:
                    pass

        # Utilization - Totals
        if "|Total" in line:
            parts = [p.strip() for p in line.strip('|').split('|')]
            if len(parts) >= 5:
                try:
                    results["BRAM_18K Total"] = int(parts[1]) if parts[1] != '-' else 0
                    results["DSP Total"] = int(parts[2]) if parts[2] != '-' else 0
                    results["FF Total"] = int(parts[3]) if parts[3] != '-' else 0
                    results["LUT Total"] = int(parts[4]) if parts[4] != '-' else 0
                except ValueError:
                    pass

    return results

if __name__ == "__main__":
    report_path = "fir_csynth.rpt"  # Replace with actual path if needed
    parsed = parse_fir_report(report_path)
    print("\n")
    for key, value in parsed.items():
        print(f"{key}: {value}")
