//data type of timely warning
	//json the data type
//seperate emails by content-type
import java.io.*;
import java.util.*;
public class timelyWarning {
	public static void main(String [] args){
		final String path = System.getProperty("user.dir"); //finds local directory
		File reader = new File(path + "\\Timely Warning.mbox"); //adds file name to end of local directory
		dataEmail[] emailArray = new dataEmail[60]; //creates an array of dataEmail
		try{
			int dataEmailIndex = 0;
			final Scanner fileRead = new Scanner(reader); //new scanner to read in from file
			while(fileRead.hasNextLine()){ //while there are more lines in the file keep going
				String nextLine = fileRead.nextLine(); //reads in line
				if(nextLine.contains("Content-Type: multipart/alternative")){ //if it finds this string it is a new email
					ArrayList<String> holdEmail = new ArrayList<String>(); //used to send to new dataEmail
					Boolean newEmail = true;
					do{
						nextLine = fileRead.nextLine();
						if(nextLine.contains("Content-Type: text/plain")){ //if it finds this string, the info we need is inside the block
							Boolean textPart = true;
							do{
								nextLine = fileRead.nextLine();
								if(nextLine.contains("Content-Type: text/html")){ //this is the end of the block with the information
									newEmail = false;							 //when we find it, set checks to false and move on to find next email
									textPart = false;
								}
								else{
									holdEmail.add(nextLine); //adds the string to the ArrayList
								}
							}while(textPart);
							emailArray[dataEmailIndex] = new dataEmail(holdEmail);
							emailArray[dataEmailIndex].decode();
							emailArray[dataEmailIndex].setVar();
							//emailArray[dataEmailIndex].print();
							dataEmailIndex++;
						}
					}while(newEmail);
				}
			}
			fileRead.close();
			String forFile = "";
			String forOut = "";
			for(int r=0;r<54;r++){
				boolean updateHold = emailArray[r].returnUpdate();
				String[] holdVars = new String[5];
				if(!updateHold){
					holdVars[0] = emailArray[r].returnVars()[0];
					holdVars[1] = emailArray[r].returnVars()[1];
					holdVars[2] = emailArray[r].returnVars()[2];
					holdVars[3] = emailArray[r].returnVars()[3];
					holdVars[4] = emailArray[r].returnVars()[4];
					for(int t=0;t<5;t++){
						if(!holdVars[t].isEmpty()){
							forFile = forFile + holdVars[t] + "!$%";
							forOut = forOut + holdVars[t] + "\n";
						}
					}
				}
			}
			System.out.println(forOut);
			Writer toFile = null;
			File fp = new File(System.getProperty("user.dir") + "\\Email Text" + "\\emails.txt");
			try{
				toFile = new BufferedWriter(new FileWriter(fp));
				toFile.write(forFile);
				toFile.close();
			}
			catch(IOException e){
				throw new RuntimeException(e);
			}
		}
		catch(FileNotFoundException x){
			throw new RuntimeException(x);
		}
	}
}
