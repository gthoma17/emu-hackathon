/*
 * Tyler Bixler
 * Stores information scraped from emails
 * Methods:
 * constructor() - takes in an ArrayList<String> that holds all information
 * print() - Prints out entire information from email
 * decode() - gets rid of UTF-8 characters and other junky stuff
 * setVar() - sets location,date,crime,email_text
 * returnVars() - returns variables above
 */
import java.util.*;
import java.io.*;
public class dataEmail {
	private ArrayList<String> holdData; //variables, hold various information, names are indicative of stored information
	private String location="";
	private String date = "";
	private String crime = "";
	private String onCampus = "";
	private String email_text = "";
	private Boolean updateCk = false;
	
	public dataEmail(ArrayList<String> data){ //constructor
		holdData = data;
	}
	public void print(){ //print method
		int sizeof = holdData.size();
		for(int i=0;i<sizeof;i++){
			System.out.println(holdData.get(i));
		}
	}
	public void decode(){ //gets rid of junky characters/words
		int sizeof = holdData.size();
		for(int i=0;i<sizeof;i++){
			String s1 = holdData.get(i);
			s1 = s1.replaceAll("=C2=A0","");
			s1 = s1.replaceAll("=20","");
			s1 = s1.replaceAll("=C2=A0=20", "");
			s1 = s1.replaceAll("=E2=80=99", "'");
			s1 = s1.replaceAll("=E2=80=9D", "\"");
			s1 = s1.replaceAll("=E2=80=93", "");
			s1 = s1.replaceAll("=E2=80", "");
			s1 = s1.replaceAll("Content-Transfer-Encoding: quoted-printable", "");
			s1 = s1.replaceAll("=","");

			holdData.set(i, s1);
		}
	}
	public void setVar(){ //searches strings for keywords, saves information from string for data points
		int sizeof = holdData.size();
		int email_text_start=0;
		int email_text_end=0;
		for(int j=0;j<sizeof;j++){
			String boolCk = holdData.get(j);
			if(boolCk.contains("Update")||boolCk.contains("update")||boolCk.contains("UPDATE"))
				updateCk = true;
		}
		if(updateCk==false){
			for(int i =0;i<sizeof;i++){
				String holdString = holdData.get(i);
				if(holdString.contains("Timely Warning")){
					date = holdString;
				}
				else if(holdString.contains("Reported Crime")){
					crime = holdString;
					holdString = holdData.get(i+1);
					if(!holdString.isEmpty())
						crime = crime + holdString;
					if(crime.contains("Off")&&crime.contains("Campus"))
						onCampus = "false";
					else
						onCampus = "true";
				}
				else if(holdString.contains("Location")){
					location = holdString;
					email_text_start = i+1;
				}
				else if(holdString.contains("Anyone with any information")){
					email_text_end = i-1;
				}
			};
			int k = email_text_end;
			for(int j = email_text_start;j<k;j++){
				email_text = email_text + holdData.get(j);
			}
		}
	}
	public String[] returnVars(){ //returns main variables
		String[] holdVars = new String[5];
		holdVars[0] = this.date;
		holdVars[1] = this.crime;
		holdVars[2] = this.onCampus;
		holdVars[3] = this.location;
		holdVars[4] = this.email_text;
		return holdVars;
	}
	public boolean returnUpdate(){ //returns boolean value for whether or not email was an update, which we don't need
		return this.updateCk;
	}
}
