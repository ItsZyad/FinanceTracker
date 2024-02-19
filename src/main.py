## Contains main loop function and starting function call.
##
## @Author: Zyad O.
## @Created: OCT 30 / '23
## @Version: v0.1
##
## ------------------------------------------------------------------------------------------------

from strings import title, commandString
from currency import *
from funds import GetFundEntries, FundEntries, FundEntry, FundForm, SaveFundEntries
from params import ParamHandler

import time
from typing import Dict, List, Optional, Any
from benedict import benedict

HOUR_NS = 3600000000000


def Startup() -> Dict:
	timeNow = time.time_ns()
	lastUpdatedRates = GetCurrencyLastUpdate()
	returnDict = {
		"currency" : {
			"currencyInfo" : GetCurrencyRates(),
			"lastUpdated" : lastUpdatedRates
		},
		"entries" : {
			"entryList" : FundEntries(),
			"lastUpdated" : timeNow
		}
	}

	if timeNow - lastUpdatedRates >= HOUR_NS * 24:
		currencyInfo = RequestCurrencyInfo()
		returnDict["currency"]["currencyInfo"] = currencyInfo
		returnDict["currency"]["lastUpdated"] = timeNow

	entriesRaw = GetFundEntries()

	if entriesRaw is not None:
		entries = entriesRaw["entries"]
		lastUpdatedEntries = entriesRaw["last_updated"]

		returnDict["entries"]["entryList"] = entries
		returnDict["entries"]["lastUpdated"] = lastUpdatedEntries

	return returnDict


def GenerateArgumentDict(params: ParamHandler, minArgs: int, argumentIndexes: Dict) -> Optional[Dict[str, Any]]:
	if len(params) < minArgs:
		print(f"Insufficient arguments. Must provide at least {minArgs} arguments to the {params.command.upper()} command")
		return None

	arguments = {}

	i = 0
	for param in params.GetAllParams():
		if list(param.values())[0] is None:
			arguments.update({argumentIndexes[params.command][i]: list(param.keys())[0]})

		else:
			arguments.update(param)

		i += 1

	return arguments


def MainLoop():
	print("Starting up...\n")

	startupInfo = Startup()
	entries: FundEntries = startupInfo["entries"]["entryList"]

	argumentIndexes = {
		"addfunds" : ["amount", "form", "currency", "debtor"],
		"removefunds": ["amount", "form", "currency", "debtor"],
		"setfunds" : ["amount", "form", "currency", "debtor"],
		"getexchange": ["currency", "amount"]
	}

	validForms = {
		FundForm.DEBIT : ["debit"],
		FundForm.DEBT : ["debt"],
		FundForm.PHYSICAL : ["physical", "cash"]
	}

	for line in title.split("\n"):
		# time.sleep(0.3)
		print(line)

	print("Welcome to the financial tracker!\n")
	print("From within the financial tracker, you can monitor and modify your current incomes, expenses, debts, and reserves. \nChoose an option from below or, alternatively, use 'help' to find more information about the commands available to you;")
	print(commandString + "\nType the name of a command from above followed by its parameters (see the 'help' command for more \ninfo on that), or type a number corresponding to the chosen command")

	while True:
		userInput = input(">>> ")
		cleanedInput = userInput.lower()
		params = ParamHandler(cleanedInput)

		if params.command == "help":
			print(commandString)

		###########################################################################################

		elif params.command in ("exit", "stop"):
			print("Would you like to save the changes made? (y/n)")

			while True:
				saveChanges = input(">>> ").lower()

				if saveChanges == "y":
					print("Saving changes...")

					SaveFundEntries(entries)
					break

				elif saveChanges == "n":
					print("Dropping changes and exiting...")
					break

				else:
					print("Unrecognized response...")

			print("Exiting program...")
			break

		###########################################################################################

		elif params.command == "addfunds":
			arguments = GenerateArgumentDict(params, 1, argumentIndexes)

			if arguments.get("amount") is None:
				continue

			arguments.setdefault("form", "debit")
			arguments.setdefault("currency", "cad")
			arguments.setdefault("debtor", None)

			for validTypes in validForms:
				if arguments["form"].lower() in validForms[validTypes]:
					arguments["form"] = validTypes
					break

			if not isinstance(arguments["form"], FundForm):
				print(f"{arguments['form']} is not a valid currency form.")
				continue

			entries.AddFunds(FundEntry(float(arguments["amount"]), arguments["currency"], arguments["form"], arguments["debtor"]))

		###########################################################################################

		elif params.command == "removefunds":
			arguments = GenerateArgumentDict(params, 1, argumentIndexes)

			if arguments is None or arguments.get("amount") is None:
				print("You must provide an amount to add to the financial entries!")
				continue

			arguments.setdefault("form", "debit")
			arguments.setdefault("currency", "cad")
			arguments.setdefault("debtor", None)

			for validTypes in validForms:
				if arguments["form"].lower() in validForms[validTypes]:
					arguments["form"] = validTypes
					break

			if not isinstance(arguments["form"], FundForm):
				print(f"{arguments['form']} is not a valid currency form.")
				continue

			entries.RemoveFunds(float(arguments["amount"]), arguments["currency"], arguments["form"], arguments["debtor"])

		###########################################################################################

		elif params.command == "setfunds":
			arguments = GenerateArgumentDict(params, 1, argumentIndexes)

			if arguments is None or arguments.get("amount") is None:
				print("You must provide an amount to set the financial entries to!")
				continue

			arguments.setdefault("form", "debit")
			arguments.setdefault("currency", "cad")
			arguments.setdefault("debtor", None)

			for validTypes in validForms:
				if arguments["form"].lower() in validForms[validTypes]:
					arguments["form"] = validTypes
					break

			if not isinstance(arguments["form"], FundForm):
				print(f"{arguments['form']} is not a valid currency form.")
				continue

			entries.SetFunds(float(arguments["amount"]), arguments["currency"], arguments["form"], arguments["debtor"])

		###########################################################################################

		elif params.command == "getexchange":
			arguments = GenerateArgumentDict(params, 2, argumentIndexes)

			if arguments.get("currency") is None:
				print("Please specify a currency code to fetch.")
				continue

			if arguments.get("amount") is None:
				arguments["amount"] = 1

			exchange = ConvertToDollar(float(arguments["amount"]), arguments["currency"])
			print(f"{arguments['amount']} {arguments['currency'].upper()} --> {round(exchange, 4)} USD")

		###########################################################################################

		elif params.command == "showfunds":
			fundsByCurrency = benedict()
			allFunds = entries.GetAllEntries()

			for entry in allFunds:
				currency = entry.GetCurrency()
				form = entry.GetForm()

				if not f'{currency}.{form.name}' in fundsByCurrency:
					fundsByCurrency[currency, form.name] = []

				fundsByCurrency[currency, form.name].append(entry)

			for currency in fundsByCurrency:
				print(f"{currency}: ")
				currTotal = 0

				for form in fundsByCurrency[currency]:
					print(" " * 2, f"{form}: ")
					subtotal = 0

					i = 1
					for entry in fundsByCurrency[currency][form]:
						print(" " * 4, f"{i}: {round(ConvertFromDollar(entry.GetAmount(), currency), 2)} {currency}")
						subtotal += entry.GetAmount()

						i += 1

					print("\n", " " * 4, f"Subtotal: {round(ConvertFromDollar(subtotal, currency), 2)} {currency}")
					currTotal += subtotal

				print("\n", " " * 2, f"Currency Total: {round(currTotal, 2)} USD")

		###########################################################################################

		else:
			print("'" + userInput + "' is an unrecognized command :/")
			print("Refer to the 'help' command for more information.")

MainLoop()
