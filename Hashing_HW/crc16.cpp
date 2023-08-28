// Yannie Wu, ylw4sj
// CS 3710 Homework: Hashing (Task 1: CRC insecurity)
#include <boost/crc.hpp>
#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>

using namespace std;


// Returns checksum as a decimal number
int getCRC(const string& my_string) {
    boost::crc_16_type result;
    result.process_bytes(my_string.data(), my_string.length());
    return result.checksum();
}

int main(int argc, char** argv){

	string inputFile = argv[1];
    int goalCrc = stoi(argv[2], 0, 16); // Convert from hex to decimal

    // Read contents of text file
   	char c;
   	string msg;

   	ifstream file(inputFile);
   	file >> noskipws;
   	while ( file >> c ){
   		msg += c;
   	}
   	file.close();

   	// Add message to text file
   	msg += "\nyannie was here :) \n";

   	// Brute force solve for new checksum
   	char random_chars[6];
   	while (true){
   		string newMsg = msg;
   		for (int i = 0; i < 6; i++) {
   			newMsg += char(rand() % 256);
   		}
   		if (getCRC(newMsg) == goalCrc) {
   			ofstream output;
  			output.open ("output.txt");
  			output << newMsg;
  			output.close();
   			break;
   		}
   	}
}