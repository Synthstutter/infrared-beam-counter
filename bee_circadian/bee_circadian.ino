signed int threshold[]={130,130,130,200,200,200};
const int readPin[]={A0, A1, A2, A3, A4, A5}; 
unsigned int sensVal[6];
boolean passed[6];
boolean previousPassed[6];
long int calSensVal[6];
int count[6];
int incomingByte;

void setup() {
    Serial.begin(9600); 
  
}

void loop() {
  if (Serial.available()>0){
    incomingByte=Serial.read();
  }
    if (incomingByte==1){    
      int i=0;
      for (i=0;i<6;i++){
	if (!calSensVal[i] ||  calSensVal[i] > analogRead(readPin[i])){
	  calSensVal[i]=analogRead(readPin[i]);}
      }
        
        String calib_concat="\nSensor 0: " + String(calSensVal[0]) +
                            "\nSensor 1: " + String(calSensVal[1]) +
                            "\nSensor 2: " + String(calSensVal[2]) + 
                            "\nSensor 3: " + String(calSensVal[3]) +
                            "\nSensor 4: " + String(calSensVal[4]) +
      	                    "\nSensor 5: " + String(calSensVal[5]);
        Serial.println(calib_concat);
        incomingByte=false;
    }

    if (incomingByte==2){
        int i=0;
        for (i=0;i<6;i= i+1){
	  sensVal[i]=analogRead(readPin[i]);    
	    if (sensVal[i] >= calSensVal[i]*threshold[i]/100 && previousPassed[i]==false){
                previousPassed[i]=true;
                Serial.print(i);   
	        /* String toPython= "p:" + String(i)        */
	        /* Serial.println(toPython) */
                delay(2);
            }
            if (abs(sensVal[i]-calSensVal[i]) <3){
       	      previousPassed[i]=false;
            }     
	}
   
    }          
   
}

