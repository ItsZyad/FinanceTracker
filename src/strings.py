## I'm keeping all the strings/localizations for the program in this file, for now, as not clutter
## the other files. It is sorted by which strings belong where.
##
## @Author: Zyad O.
## @Created: DEC 30 / '23
## @Version: v0.1
##
## ------------------------------------------------------------------------------------------------

#############
## MAIN.PY ##
#############

title = """
███████╗██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗██╗ █████╗ ██╗         ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██║██╔══██╗██║         ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
█████╗  ██║██╔██╗ ██║███████║██╔██╗ ██║██║     ██║███████║██║            ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
██╔══╝  ██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██║██╔══██║██║            ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║     ██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗██║██║  ██║███████╗       ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                                                                                                                                                                                                                                 
"""

commandString = """
1. >>> AddFunds     [amount : decimal] ?[form : string] ?[currency : string]
	   - Adds funds to the overall account. The forms that currency can take are: Bank Debit, Physical Reserve.
	   - You may specify a currency to add currency in. The default currency is CAD.

2. >>> RemoveFunds  [amount : decimal] ?[form : string] ?[currency : string]
	   - Removes funds from the overall account. The forms that currency can take are: Bank Debit, Physical Reserve.
	   - You may specify a currency to add currency in. The default currency is CAD.

3. >>> GetExchange  [currency : string] [amount : decimal]
	   - Downloads the latest exchange rates between the U.S. dollar and a provided currency.
	   - If no currency is provided, then the program will download ALL available exchange rates.

4. >>> AddCredit    [amount : decimal] ?[currency : string]
	   - Adds credit debt to the overall account.

5. >>> RemoveCredit [amount : decimal] ?[currency : string]
	   - Removes credit debt from the overall account.

6. >>> ShowFunds
	   - Shows a complete breakdown of all active funds, physical reserves, as well credit debts by currency.

7. >>> QueryFunds   (WIP!)

8. >>> Help
	   - Shows this info sheet.

9. >>> Exit/Stop
	   - Stops the program.
"""
