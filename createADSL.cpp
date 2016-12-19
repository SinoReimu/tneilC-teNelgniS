#include<stdio.h>
#include<windows.h>
#include<string.h>
int main(int argc,char*argv[])
{
	if (argc == 1) return -1;
	printf ("%s \n",argv[1]);
	char szCommandLine[29]="rasdial \"";
	char mAfter[] = "\" \"\x0D\x0A";
	char com1[] = "\" \"";
	char final[] = "\"";
	strcat(szCommandLine,argv[4]);
	strcat(szCommandLine,mAfter);
	strcat(szCommandLine,argv[1]);
	strcat(szCommandLine,argv[2]);
	strcat(szCommandLine,com1);
	strcat(szCommandLine,argv[3]);
	strcat(szCommandLine,final);
	printf("%s\n", szCommandLine);
	STARTUPINFO si={sizeof(si)};
	PROCESS_INFORMATION pi;
	si.dwFlags=STARTF_USESHOWWINDOW;
	si.wShowWindow=TRUE;
	BOOL bRet=CreateProcess(
		NULL,
		szCommandLine,
		NULL,
		NULL,
		FALSE,
		CREATE_NEW_CONSOLE,
		NULL,
		NULL,
		&si,
		&pi);
	if(bRet)
	{
		CloseHandle(pi.hThread);
		CloseHandle(pi.hProcess);
	}
	return 0;
}
