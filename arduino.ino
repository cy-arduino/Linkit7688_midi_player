const int buzPin = 9;

String readBuf;
int inFreq;

void setup() {  
  //to mt7688 mpu
  Serial1.begin(57600);

  //USB UART
  Serial.begin(115200);
}

void loop() {
  if(Serial1.available()){

    //read line
    readBuf = "";
    while(1){
      char c = Serial1.read();
      if(c == -1)
        continue;//no data...
      if(c == '\n')
        break;
      readBuf += c;
    }

    //Serial.print("readBuf:");
    //Serial.println(readBuf);

    switch(readBuf[0]){
      case 'f':
        //set frequency
        inFreq = readBuf.substring(2).toInt();
        Serial.print("frequency: ");
        Serial.println(inFreq);
        break;
      case 't':
        //tone
        Serial.println("tone");
        tone(buzPin, inFreq);
        break;
      case 'n':
        //notone
        Serial.println("notone");
        noTone(buzPin);
        break;
      default:
        Serial.println("unknown cmd: " + readBuf);
    }
  }
}
