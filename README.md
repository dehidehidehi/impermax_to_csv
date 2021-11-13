![](imgs/impermax_title.png)
## Effortlessly keep track of 150+ ever changing APY rates!

This project is **not affiliated with Impermax**, this is not an official release.
___
## Constantly identifying the best APYs on Impermax is a pain.
This tool allows you to effortlessly compare the best APYs over:
- 150+ unique tokens supply and borrow APYs.
- 75+ pairs and their unique leveraged LP APYs.
- 4 blockchains (ETH, MATIC, ARB, AVAX)

### Example use case: finding the best stable coin to lend.
This is from our dedicated Google Sheets template (linked below). You can directly paste the data there!
> **Filter used**: Only stablecoins with a supply greater than $100k USD over all available blockchains in descending order.**
> 
>*Comment*: DAI from the USDC/DAI pair on SushiSwap on the MATIC chain has the best supply APR, followed by USDC.e from the USDC.e/USDT.e pair on TraderJoe (Avalanche chain).
>
> ![](imgs/impermax_example_usage.png)

### $$$ Attempting to guilt you into giving me money $$$
___
<img align="left" width="80" style="margin-right: 50px; margin-bottom: 0px;" src="https://preview.redd.it/yvkkz5ibdqs71.jpg?width=960&crop=smart&auto=webp&s=7c50d6477cf9f8d6b91d21006c3dd28ddb6da3de">  

Hi! This tool should save you tons of time and hopefully even more money.   
**I recently lost my job** helping old people use computers.  
If you want to help me you can:

-  Surprise me by sending tokens either of these addresses:
   -  ETHEREUM : 0x880E8D09740994c75a1d1c75E07dF52fb26f385c  
   -  **MATIC : 0x880E8D09740994c75a1d1c75E07dF52fb26f385c**  
   -  SOLANA : C9bzkzpbt5KdKbqmMq56r3rsvtbRWHK6AeWX7dinA5LL
-  Share my dev skills with other people in the space ! I'm trying to get noticed by making crypto related tools <3
-  Let me know on Discord (DehiDehi#8605) or Twitter (@dehikupo)!  

Thank you for your time :)


### Installation to run the data fetching script requires:
___
- Some computer knowledge, and knowing how to enter commands in a Windows terminal.
- Windows 10. Has not been tested on other platforms, but could also work.
- Python 3.9 must be installed: https://www.python.org/downloads/release/python-390/
  - Does **not work** with Python 3.10.
- Git must be installed: https://git-scm.com/downloads

#### Optional: the Google Sheets template
Paste the data here after it's been generated (see instructions below): https://docs.google.com/spreadsheets/d/13dkbAPx0WSgNpDEDPrNTfrGF_QchMh4M1S5suFsAkO4/

### First time installation instructions
___
Create a new folder, then cd into it with the terminal. Then copy-paste these commands.
```console
  git clone https://github.com/dehidehidehi/impermax_to_csv.git
 ```

```console
  cd impermax
  pip install -r requirements.txt
 ```

>Note for devs: of course, run this in a venv instead.

#### How to retrieve the data
This script is the one which retrieves the data.
___
```console
  cd impermax
  python impermax_to_csv.py
```
Wait for a couple seconds; a directory called "output" should have appeared with your data under the "impermax" root directory.  
The created file is a comma-separated file which you can open in your favourite excel-like software.

### Forking and development
___
Any fork or improvement on this app must be open source as well (GPL-3.0 License).
