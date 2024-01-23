---
layout: post
title: UofTCTF 2024 Writeup
categories: [writeup]
tags: [web, jail, forensics, misc, iot]
date: 2024-01-15 22:42 +0700
img_path: 'https://raw.githubusercontent.com/T3l3sc0p3/ctf-writeups/master/UofTCTF-2024/'
image:
  path: logo.png
---

Hi, I want to share with you guys a writeup of some challenges that I have solved in **UofTCTF 2024**. I hope you like it!

Let's start!

# Introduction

## General Information (10 pts)

![Good Luck](Introduction/img/good-luck.png)

It was just a sanity check~

`Flag: UofTCTF{600d_1uck}`

Btw, this is the Discord link of the contest: [https://discord.gg/Un7avdkq7Z](https://discord.gg/Un7avdkq7Z)

# IoT

## Baby's First IoT Introduction (10 pts)

![Baby's First IoT Introduction](Iot/img/babys-first-iot-introduction.png)

Yea, I understand the mission lol

`Flag: {i_understand_the_mission}`

## Baby's First IoT Flag 1 (100 pts)

![Baby's First IoT Flag 1](Iot/img/baby-first-iot-flag-1.png)

First, I search "FCC ID, Q87-WRT54GV81" on Google and found some results like: [https://fccid.io/Q87-WRT54GV81](https://fccid.io/Q87-WRT54GV81)

After then, I click on "Frequency Range" and go to this link: [https://fccid.io/frequency-explorer.php?lower=2412.00000000&upper=2462.00000000](https://fccid.io/frequency-explorer.php?lower=2412.00000000&upper=2462.00000000)

Lastly, I take the value from "Frequency Center" is `2437` MHz and send it to port 3895 to get the flag

`Flag: {FCC_ID_Recon}`

# Miscellaneous

## Out of the Bucket (100 pts)

![Out of the Bucket](Miscellaneous/img/out-of-the-bucket.png)

After examining the url for a while, I saw an XML file when accessing [https://storage.googleapis.com/out-of-the-bucket/](https://storage.googleapis.com/out-of-the-bucket/)

As you can see in the image below, there is a file named **dont_show** in **secret** directory

![](Miscellaneous/img/out-of-the-bucket-1.png)

Download and read the file to obtain the flag:

`Flag: uoftctf{allUsers_is_not_safe}`

# Jail

## Baby's First Pyjail (100 pts)

![baby's first pyjail](Jail/img/babys-first-py-jail.png)

```python
# List the attributes and the blacklist
print(dir())
# Make the blacklist empty
blacklist = []
# import os to execute command and get flag~
import os; os.system("ls -al")
os.system("cat flag")
```

![](Jail/img/babys-first-py-jail-flag.png)

`Flag: uoftctf{you_got_out_of_jail_free}`

# Forensics

## Secret Message 1 (100 pts)

![Secret Message 1](Forensics/img/secret-message-1.png)

In this challenge, I simply open the PDF file using browser and get the flag~

![easy flag](Forensics/img/secret-message-flag.png)

`Flag: uoftctf{fired_for_leaking_secrets_in_a_pdf}`

## EnableMe (358 pts)

![EnableMe](Forensics/img/enableme.png)

First, I ran the command `file invoice.docm` to determine the file type and I knew that this was a word file

![word](Forensics/img/enableme-word.png)

When opened it, I saw that there was a macro script in the file. And I just need to change `MsgBox` from `v10` to `v9` in the `AutoOpen` macro script to obtain the flag

![macro](Forensics/img/enableme-macro.png)

`Flag: uoftctf{d0cx_f1l35_c4n_run_c0de_t000}`

In case you were curious, the value of `v10` is: `YOU HAVE BEEN HACKED! Just kidding :)`

# Web

## Voice Changer (232 pts)

![Voice Changer](Web/img/voice-changer.png)

This is a web application that allows us to alter our voice by changing the pitch

![Interface](Web/img/voice-changer-1.png)

If you try to record and use Burp Suite to intercept the request, you will notice that there are two places where malicious code can be injected: the "pitch" and "input-file" fields

![Request](Web/img/voice-changer-2.png)

At first, I attempted to upload a PHP shell script, but unfortunately I was unable to upload any shell to the server. Therefore, I changed to injecting the "pitch"

```sh
$(ls)
```

When looked at the output, I noticed that some files appeared, which meant that I could execute code on the server. This type of vulnerability is called **OS Command Injection**~

![Injection](Web/img/voice-changer-3.png)

After some searching, I found a **secret.txt** file in **/**. Now, all I needed to do was run this command to obtain the flag:

```sh
$(cat /secret.txt)
```

`Flag: uoftctf{Y0URPitchIS70OH!9H}`

## The Varsity (293 pts)

![The Varsity](Web/img/the-varsity.png)

This is a newspaper website. At first, look at the **server.js* file in the source code. We see that if we want to access the entire catalogue, we must be "premium"

![premium](Web/img/the-varsity-1.png)

However, this seems impossible because we need **FLAG** value, so we will register without voucher

![guest](Web/img/the-varsity-2.png)

Also in that **server.js** file. We see that the last article contains the flag but it need to be "premium" to read the article

Most people attempt to bypass this by changing the JSON Web Token (JWT) token. However, this method does not work and results in a "Not Authenticated" error

Upon closer inspection, I discover that the `parseInt()` function has a weird behavior as you can see in the image below:

<p align="center"><a href="https://www.w3schools.com/jsref/jsref_parseint.asp"><img src="Web/img/the-varsity-3.png" alt="parseInt"></a></p>

By modifying the value `{"issue":"9"}` to `{"issue":"9 8"}` or any other similar value, we can access the article that contains the flag

![Flag](Web/img/the-varsity-4.png)

`Flag: uoftctf{w31rd_b3h4v10r_0f_parseInt()!}`

## No Code (362 pts)

![No Code](Web/img/no-code.png)

Firstly, I analyzed the source code, which revealed that the function would read code from the parameter `code` with the `POST` method at the `/execute`

![Source Code](Web/img/no-code-1.png)

However, there was a regex (Regular Expression) to filter all printable characters at the beginning, which made it impossible to add any code

After using [regexr.com](https://regexr.com/), I realized that this regex only filtered almost everything except the line break `\n`

I hypothesized that this regex only filtered the code before the line break, not after it, as it appeared in some Command Injection CTF challenges that I solved before. And this hypothesis was correct. After adding a line break, I was able to run Python code, but with some limitations

![line break](Web/img/no-code-2.png)

To speed up the process, I used a [SSTI payload](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#exploit-the-ssti-by-calling-ospopenread) to run the command without restrictions

```python
__builtins__.__import__('os').popen('ls -al').read()
```

![flag.txt](Web/img/no-code-3.png)

Finally, I executed the `cat flag.txt` command to obtain the flag

```python
__builtins__.__import__('os').popen('cat flag.txt').read()
```

**Side notes:** I actually solved `No Code` challenge before the source code was published =))

`Flag: uoftctf{r3g3x_3p1c_f41L_XDDD}`

**Thanks for reading <33**
