JunkMailRecognize destination is recoginze a new email is junk email or not.

1.JunkMailRecognize is using the Bayes Mathematical.
The "junkmail_study.py" is the program that study the junk mail & normal mail.
The "junkmail_check.py" is the program that can recoginze the emails are junk mails or normal mail and generate a report.

2.Installation guide: python program, needn't install it.
Verify it in windows10.

3.The program is developped by using Python3.6(64-bit).

4.How to run the programs.
4.1 Open the config.ini, I show you the example:
mailfolder_junk = "C:\temp\outlook\junk"
mailfolder_normal = "C:\temp\enron_mail_20150507\maildir\allen-p"
keywordfile_junk = "C:\temp\outlook\keywordfile_junk.ini"
keywordfile_normal = "C:\temp\outlook\keywordfile_normal.ini"
file_studied_mail_junk = "C:\temp\outlook\studiedfiles_junk.ini"
file_studied_mail_normal = "C:\temp\outlook\studiedfiles_mail.ini"
junklevel=0.9
CheckedWords=15
unknown_mail_list="C:\temp\outlook\studiedfiles_junk.ini"
unknown_mail_check_result="C:\temp\example\studiedfiles_junk_result_0.9.txt"

The "mailfolder_junk" is a folder, there are junk mails under the folder, it is the junk mail dataset.I provide my junk mail dataset(junk.zip) for you. My junk mail dataset is from my email. You should define it by yourself.
The "mailfolder_normal" is a folder,there are normal mails under the folder,it is the normal mail dataset.I provide my normal mail dataset(allen-p.zip) for you. The normal mail dataset is from https://www.cs.cmu.edu/~enron/. You should define it by yourself.
For the "keywordfile_junk","keywordfile_normal","file_studied_mail_junk","file_studied_mail_normal": "junkmail_study.py" program will generate four files to save machine learning result.You should define the file path by yourself.
"junkmail_study.py" program need you define above six parameters.

4.2 For the "junkmail_study.py" program. Please open the IDLE(Python 3.6 64-bit).
Press the ctrl-O to open the "junkmail_study.py" file, press the F5 to run.Program will output the "end" if it runs correctly.

4.3 How to recoginze new mails are junk mail or not.
Open the config.ini, define the "unknown_mail_list" value, there are many mails absolute path in it.
For example:
C:\temp\outlook\junk\subject_0175752.txt
C:\temp\outlook\junk\subject_0180736.txt
C:\temp\outlook\junk\subject_0190752.txt
...
Run the "junkmail_check.py" in IDLE(Python 3.6 64-bit).
Define the "unknown_mail_check_result" output file, the program "junkmail_check.py" will generate a result in the "unknown_mail_check_result" file like this:
[0] C:\temp\outlook\junk\subject_0175752.txt is a normal mail.
[1] C:\temp\outlook\junk\subject_0180736.txt is a junk mail.
[2] C:\temp\outlook\junk\subject_0190752.txt is a junk mail.
[3] C:\temp\outlook\junk\subject_0195141.txt is a normal mail.
[4] C:\temp\outlook\junk\subject_0201125.txt is a junk mail.
[5] C:\temp\outlook\junk\subject_0_205224.txt is a normal mail.
[6] C:\temp\outlook\junk\subject_0_211319.txt is a junk mail.
[7] C:\temp\outlook\junk\subject_0_211601.txt is a junk mail.
3034 emails and program finds 0 junk mail 0.0%, find 3034 normal mail 100.0%, with 0.9

The "pystudiedfiles_junk_result_0.9.txt" & "pystudiedfiles_normal_result_0.9.txt" are check result example for junk mail data set and normal mail data set.

For the "junklevel":The threshold value to decide the email is a junk mail or not. If program gets the value is more than "junklevel" by calculating, program will think the email is a junk mail,otherwise, the mail is a normal email.
The "junklevel" should be a decimal less than 1.0 and more than 0.1
For the "CheckedWords", it should be a positive integer, not zero.
My program doesn't check the range for the "junklevel" & "CheckedWords",you can use the default value.

JunkMailRecognize is using the Bayes Mathematical.
Bayesian email filters utilize Bayes' theorem. Bayes' theorem is used several times in the context of spam: 
a first time, to compute the probability that the message is spam, knowing that a given word appears in this message;
a second time, to compute the probability that the message is spam, taking into consideration all of its words (or a relevant subset of them);
sometimes a third time, to deal with rare words.
Computing the probability that a message containing a given word is spam.
Let's suppose the suspected message contains the word "replica". Most people who are used to receiving e-mail know that this message is likely to be spam, more precisely a proposal to sell counterfeit copies of well-known brands of watches. The spam detection software, however, does not "know" such facts; all it can do is compute probabilities.
The formula used by the software to determine that, is derived from Bayes' theorem.
