import csv
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def processLog(filePath):
    
    totalRecCount = 0
    totalWeight = 0
    totalTemp = 0
    totalPH = 0
    errorCount = 0
    
    
    try:
        with open(filePath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                
                try:
                    weight = float(row['fish_weight'])
                    temp = float(row['water_temp'])
                    pH = float(row['pH_level'])
                    error_code = int(row['error_code'])
                    
                    
                except (ValueError, KeyError) as e:
                    logging.error(f"Malformed line skipped: {row}")
                    continue
                
            
            totalRecCount += 1
            
            if error_code != 0:
                errorCount += 1
                logging.warning(f"Error detected at {row['timestamp']} with code {error_code}")
            else:
                totalWeight += weight
                totalTemp += temp
                totalPH += pH
                
            if totalRecCount > 0:
                avgWeight = totalWeight / (totalRecCount - errorCount) if (totalRecCount - errorCount) > 0 else 0
                avgTemp = totalTemp / (totalRecCount - errorCount) if (totalRecCount - errorCount) > 0 else 0
                avgPH = totalPH / (totalRecCount - errorCount) if (totalRecCount - errorCount) > 0 else 0
                
                summary = {
                    "total_records": totalRecCount,
                    "error_count": errorCount,
                    "error_percent": round(errorCount / totalRecCount * 100, 2),
                    "average_weight": round(avgWeight, 2),
                    "average_temperature": round(avgTemp, 2),
                    "average_pH": round(avgPH, 2)
                }
                
                with open("hatchSum.json", "w") as jsonfile:
                    json.dump(summary, jsonfile, indent=4)
                    logging.info("Summary saved to summary.json")


    except FileNotFoundError:
        logging.error(f"File not found: {filePath}")
        
        


if __name__ == "__main__":
    processLog('hatchery_data.csv')
                    
        
    

