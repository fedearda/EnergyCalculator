import argparse
from asammdf import MDF
import pandas as pd
from openpyxl.styles import Font, PatternFill

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input MF4 file")
    parser.add_argument("--output", help="Output Excel file", default=None)
    parser.add_argument("--start", type=float, default=None, help="Start time in seconds to cut data")
    parser.add_argument("--stop", type=float, default=None, help="End time in seconds to cut data")

    args = parser.parse_args()

    mdf = MDF(args.input)
    signals_list = "BMC_Strom", "BMC_Spannung"
    
    missing_signals = [s for s in signals_list if s not in mdf]
    
    if missing_signals:
        raise ValueError(f"The following signals were not found in the trace: {' ,'.join(missing_signals)}")
        
    df = mdf.to_dataframe(channels=signals_list)
    df.reset_index(names="timestamp",inplace=True)
    
    if args.start is not None:
        df = df[df["timestamp"] >= args.start]
        
    if args.stop is not None:
        df = df[df["timestamp"] <= args.stop]
        
    df["Instant power [W]"] = -df["BMC_Strom"]*df["BMC_Spannung"]
    
    t = df["timestamp"].values
    p = df["Instant power [W]"].values
    CONVERSION_FACTOR = 1/3600/1000
    energy = 0
    
    for i in range(1, len(p)):
        dt = t[i] - t[i-1]
        energy = energy + (p[i] + p[i-1]) * 0.5 * dt * CONVERSION_FACTOR
    
    print(f"Total energy = {energy:.3f} kWh")
    
    if args.output is not None:
        with pd.ExcelWriter(args.output, engine="openpyxl",mode='w') as writer:
            df.to_excel(writer, index=False)
            ws = writer.sheets["Sheet1"]
            
            col = df.shape[1]+2
            if energy < 1:
                label_e = "Total energy [Wh]"
                energy = energy * 1000
            else:
                label_e = "Total energy [Wh]"
            ws.cell(row=1, column=col, value=label_e).font = Font(bold=True)
            ws.cell(row=2, column=col, value=energy).fill = PatternFill(start_color="00FF00", patternType='solid')
        print("Export completed")

if __name__ == "__main__":
    main()