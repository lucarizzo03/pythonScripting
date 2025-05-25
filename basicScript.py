import csv
import logging

logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

def processLog(filePath):
    totalFish = 0
    errorCount = 0
    totalWeight = 0
    successCount = 0
    totalProcessTime = 0
    
    try:
        with open(filePath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader: 
                
                try:
                    error_code = int(row['error_code'])
                    weight = float(row['fish_weight'])
                    process_time = float(row['processing_time'])
                except (ValueError, KeyError) as e:
                    logging.error(f"Malformed line skipped: {row}")
                    continue
                    
                totalFish += 1
                
                if error_code != 0:
                    errorCount += 1
                    logging.warning(f"Error detected at {row['timestamp']} with code {error_code}")
                else:
                    totalWeight += weight 
                    successCount += 1
                    totalProcessTime += process_time
                    
                
                logging.info(f"Total fish processed: {totalFish}")
                logging.info(f"Error count: {errorCount} ({errorCount/totalFish*100:.2f}%)")
                
                if successCount > 0:
                    logging.info(f"Average weight (kg): {totalWeight/successCount:.2f}")
                    logging.info(f"Average processing time (s): {totalProcessTime/successCount:.2f}")
                else:
                    logging.info("No successful fish processed.")
                
                    
    except FileNotFoundError:
        logging.error(f"File not found: {filePath}")
        
        

if __name__ == "__main__":
    processLog('fish.csv')
        
        
                    
    
    
    