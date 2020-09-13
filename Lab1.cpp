#include <iostream>
#include <vector>
#include <string>


int main ( int argc, char *argv[] )
{
//НАШ КОД


    string file_name = "";
    cin >> file_name;
    file_name +=".txt";
	ifstream in_file(file_name);
	// Если мы не можем открыть файл для чтения его содержимого
	if (!in_file)
	{
		cerr << "Uh oh, Input.txt could not be opened for reading!" << endl;
		exit(1);
	}

    vector <vector <double>> matrix; //матрица смежности
    int n=0;
    in_file >> n;
    for (int i=0; i<n; i++) {
        vector <double> str;
        for (int j=0; j<n; j++) {
            double node;
            in_file>>node;
            str.push_back(node);
        }
        matrix.push_back(str);
    }

}