## All functions and classes which are called to load data from the disk into working memory on
## program start-up or while it's running are in this file.
##
## @Author: Zyad O.
## @Created: DEC 30 / '23
## @Version: v0.2
##
## ------------------------------------------------------------------------------------------------

from utilities import FTError

from typing import List
from bs4 import BeautifulSoup
from json import loads
import pickle
import time
import requests


def SaveCurrencyData(currencyData: List) -> None:
	try:
		open("../data/currencyRates.dat", "wb")

	except FileNotFoundError:
		FTError("Cannot find currency rates file...\nHas it been moved or deleted?")
		return None

	saveFile = open("../data/currencyRates.dat", "wb")
	saveData = {
		"rates" : currencyData,
		"last_updated" : time.time_ns()
	}

	pickle.dump(saveData, saveFile, pickle.HIGHEST_PROTOCOL)
	saveFile.close()


def RequestCurrencyInfo() -> List:
	# yes, I'm too cheap for an API call. I'm not spending 60 a month for that.
	conversionRawHTML = requests.get("https://www.exchange-rates.org/current-rates/usd").text
	soup = BeautifulSoup(conversionRawHTML, "html.parser")
	conversionRawJSON = soup.find_all("script")[1].string
	cleanedConversionData = []

	for i in loads(conversionRawJSON)["mainEntity"]["itemListElement"]:
		if i["currency"] == "USD":
			cleanedConversionData.append(i)

	SaveCurrencyData(cleanedConversionData)
	return cleanedConversionData


def ConvertToDollar(amount: float, currency: str = "CAD") -> float:
	currency = currency.upper()

	if currency == "USD":
		return amount

	rates = GetCurrencyRates()
	multiplier = 0

	for rate in rates:
		if rate["currentExchangeRate"]["priceCurrency"] == currency:
			multiplier = rate["currentExchangeRate"]["price"]
			break

	try:
		amount / float(multiplier)

	except ZeroDivisionError:
		FTError(f"Provided currency: {currency} either has no stated value or does not exist!")
		return -1

	return amount / float(multiplier)


def ConvertFromDollar(amount: float, currency: str = "CAD") -> float:
	currency = currency.upper()

	if currency == "USD":
		return amount

	rates = GetCurrencyRates()
	multiplier = 0

	for rate in rates:
		if rate["currentExchangeRate"]["priceCurrency"] == currency:
			multiplier = rate["currentExchangeRate"]["price"]
			break

	if multiplier == 0:
		FTError(f"Provided currency: {currency} either has no stated value or does not exist!")
		return -1

	return amount * float(multiplier)


def GetCurrencyRates() -> List:
	file = open("../data/currencyRates.dat", "rb")
	conversionData = pickle.load(file)
	file.close()

	return conversionData["rates"]


def GetCurrencyLastUpdate() -> time:
	file = open("../data/currencyRates.dat", "rb")
	conversionData = pickle.load(file)
	file.close()

	return conversionData["last_updated"]

# RequestCurrencyInfo()
# print(GetCurrencyRates())
# print(f"100 EGP -> USD: {ConvertToDollar(100, 'EGP')}")
# print(f"100 USD -> EGP: {ConvertFromDollar(100, 'EGP')}")

# singleRate = GetSingleConversion("CAD")
# print(singleRate)