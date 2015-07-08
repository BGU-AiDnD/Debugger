package Debug;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Scanner;

import org.apache.poi.EncryptedDocumentException;
import org.apache.poi.openxml4j.exceptions.InvalidFormatException;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.WorkbookFactory;

public class Modify {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		
		String source = args[0];//"barinel.xlsx";
		String csvData = args[1];// "barinelOptA.csv";
		String sheetName = args[2]; //"barinelOptA" or "planner"
		
	    InputStream inp;
		try {
			inp = new FileInputStream(source);
			String[][] rows=readCsv(csvData);
			
	    Workbook wb;
			wb = WorkbookFactory.create(inp);
	    Sheet sheet = wb.getSheet(sheetName);
	    for(int i=0;i<rows.length;i++){
	    	for(int j=0;j<rows[i].length;j++){
	    	    Row row = sheet.getRow(i);
	    	    Cell cell = row.getCell(j);
	    	    
	    	    if (Cell.CELL_TYPE_NUMERIC==cell.getCellType()){
	    	    double cellContents = cell.getNumericCellValue(); 
	    	    cellContents=Double.parseDouble(rows[i][j]);
	    	    //Modify the cellContents here
	    	    // Write the output to a file
	    	    cell.setCellValue(cellContents); 
	    	    }
	    	    
	    	    if (Cell.CELL_TYPE_STRING==cell.getCellType()){
	    	    String cellContents = cell.getStringCellValue(); 
	    	    cellContents=rows[i][j];
	    	    //Modify the cellContents here
	    	    // Write the output to a file
	    	    cell.setCellValue(cellContents); 
	    	    }
	    	}
	    }
	    wb.getCreationHelper().createFormulaEvaluator().evaluateAll();
	    wb.setForceFormulaRecalculation(true);
	    FileOutputStream fileOut = new FileOutputStream(source);
	    wb.write(fileOut);
	    fileOut.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		catch (EncryptedDocumentException | InvalidFormatException
				| IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	
	
	public static String[][] readCsv(String filePath) throws IOException {
	    ArrayList < String[] > result = new ArrayList < String[] > ();
	    Scanner scan = new Scanner(new File(filePath));
	    while (scan.hasNextLine()) {
	        String line = scan.nextLine();
	        String[] lineArray = line.split(",");
	        result.add(lineArray);
	        }
	    String[][] ans=new String[0][0];
	        return result.toArray(ans);
	    }

	

}
