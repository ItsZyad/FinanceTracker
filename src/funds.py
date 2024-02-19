## Contains all functions and classes relating to the adding and subtracting of funds. Fund Queries
## are not found in this file- see query.py for that.
##
## @Author: Zyad O.
## @Created: DEC 30 / '23
## @Version: v0.2
##
## ------------------------------------------------------------------------------------------------

from src.currency import *
from src.utilities import FTError

from enum import Enum
from typing import Optional, Dict, Tuple
from benedict import benedict


class Entry:
	def __init__(self, amount: float, currency: str = "CAD"):
		self.__amount = ConvertToDollar(amount, currency)

		# Internal representation of all entries is the U.S. dollar.
		self.__currency = currency.upper()

	def GetAmount(self) -> float:
		return self.__amount

	def GetFormattedAmount(self) -> str:
		splitted = str(self.__amount).split("")
		splitted.reverse()

		out = ""

		for i in range(len(splitted)):
			if i % 3 == 0:
				out += ","

			out += splitted[i]

		return out

	def GetCurrency(self):
		return self.__currency

	def SetAmount(self, amount: float, currency: str = "CAD") -> None:
		USDAmount = ConvertToDollar(amount, currency)

		self.__amount = USDAmount

	def SubtractAmount(self, amount: float, currency: str = "CAD") -> float:
		USDAmount = ConvertToDollar(amount, currency)

		if round(USDAmount, 2) > self.__amount:
			self.__amount = 0
			return 0

		self.__amount -= USDAmount
		return self.__amount

	def AddAmount(self, amount: float, currency: str = "CAD") -> float:
		if amount < 0:
			FTError("Cannot add an amount to this entry that is less than zero. Use SubtractAmount() instead.")
			return self.__amount

		USDAmount = round(ConvertToDollar(amount, currency), 2)

		self.__amount += USDAmount
		return self.__amount


class FundForm(Enum):
	# Bank account funds that I have *right now*.
	DEBIT = 1,

	# Cash/coins.
	PHYSICAL = 2,

	# Money that someone owes me.
	DEBT = 3


class FundEntry(Entry):
	def __init__(self, amount: float, currency: str = "CAD", form: FundForm = FundForm.DEBIT, debtor: Optional[str] = None):
		super().__init__(amount, currency)

		self.__form = form

		if form == FundForm.DEBT and debtor is None:
			FTError("Cannot generate debt-based FundEntry with no debtor! Please provide a name for the debtor. If no name can provided please write 'N/A'")
			return

		self.__debtor = debtor

	def GetForm(self) -> FundForm:
		return self.__form

	def GetDebtor(self) -> Optional[str]:
		return self.__debtor


class FundEntries:
	def __init__(self):
		self.__entries = []

	def GetEntry(self, index: int) -> FundEntry:
		return self.__entries[index]

	def GetAllEntries(self) -> List[FundEntry]:
		return self.__entries

	def AddFunds(self, entry: FundEntry) -> None:
		for e in self.__entries:
			if not entry.GetForm() == e.GetForm():
				continue

			if entry.GetForm() == FundForm.DEBT and entry.GetDebtor() != e.GetDebtor():
				continue

			e.AddAmount(entry.GetAmount(), entry.GetCurrency())
			return

		self.__entries.append(entry)

	def RemoveFunds(self, amount: float, currency: str = "CAD", form: Optional[FundForm] = None, debtor: Optional[str] = None) -> None:
		USDAmount = ConvertToDollar(amount, currency)

		if form == FundForm.DEBT:
			if debtor is None:

				## Find someone to lower their debt balance.
				for entry in self.__entries:
					if entry.GetDebtor() is not None:
						if round(entry.GetAmount(), 2) == round(USDAmount, 2):
							self.__entries.remove(entry)
							return

						entry.SubtractAmount(amount)
						return

			## Search through and find the debtor in question -- helper function maybe?
			for entry in self.__entries:
				if entry.GetDebtor() == debtor:
					if round(entry.GetAmount(), 2) == round(USDAmount, 2):
						self.__entries.remove(entry)
						return

					entry.SubtractAmount(amount)
					return

			FTError(f"Cannot find debtor with name: {debtor}. Perhaps this is a typo?")
			return

		## Find the first entry that has an amount greater than or equal to the amount provided
		for entry in self.__entries:
			if form is None or form == entry.GetForm():
				if round(entry.GetAmount(), 2) == round(USDAmount, 2):
					self.__entries.remove(entry)
					return

				entry.SubtractAmount(amount)

	def SetFunds(self, amount: float, currency: str = "CAD", form: Optional[FundForm] = None, debtor: Optional[str] = None) -> None:
		for entry in self.__entries:
			entryCurrency = entry.GetCurrency()
			entryForm = entry.GetForm()
			entryDebtor = entry.GetDebtor()

			if entryForm == form and entryCurrency == currency.upper() and entryDebtor == debtor:
				entry.SetAmount(amount, currency)
				return


class DebtForm(Enum):
	PHYSICAL = 1,
	CREDIT = 2


class DebtEntry(Entry):
	def __init__(self, amount: float, creditor: str, currency: str = "CAD", form: DebtForm = DebtForm.CREDIT, due: Optional[int] = None):
		super().__init__(amount, currency)

		self.__creditor = creditor
		self.__form = form

		# TODO: properly implement due dates for debt.
		self.__due = due

	def GetCreditor(self) -> str:
		return self.__creditor

	# def GetDebtor(self) -> str:
	# 	return self.GetCreditor()

	def GetForm(self) -> DebtForm:
		return self.__form

	def GetDueDate(self) -> int:
		return self.__due


class DebtEntries:
	def __init__(self) -> None:
		self.__entries: Dict[str, List[DebtEntry]] = {}

	def GetAllEntries(self) -> Dict[str, List[DebtEntry]]:
		return self.__entries

	def GetEntriesByCreditor(self, creditor: str) -> List[DebtEntry]:
		return self.__entries.get(creditor)

	def GetEntryList(self) -> List[DebtEntry]:
		entryList = []
		values = self.__entries.values()

		for entries in values:
			entryList.extend(entries)

		return entryList

	def GetAllCreditors(self) -> List[str]:
		return list(self.__entries.keys())

	def CreditorExists(self, creditor: str) -> bool:
		return creditor in self.GetAllCreditors()

	def AddDebtEntries(self, *entries: DebtEntry) -> None:
		for entry in entries:
			self.AddDebt(entry.GetAmount(), entry.GetCreditor(), entry.GetCurrency(), entry.GetForm())

	def AddDebt(self, amount: float, creditor: str, currency: str = "CAD", form: Optional[DebtForm] = DebtForm.CREDIT) -> None:
		entries = benedict(self.__entries)
		currency = currency.upper()

		if not self.CreditorExists(creditor):
			entries[creditor] = [DebtEntry(amount, creditor, currency, form)]
			return

		# Creditor exists
		entry: DebtEntry
		for entry in entries[creditor]:

			# If a form is not specified then add the amount to the first entry with the same currency
			if form is None:
				if entry.GetCurrency() == currency:
					entry.AddAmount(amount, currency)
					return

			if entry.GetCurrency() == currency and entry.GetForm() == form:
				entry.AddAmount(amount, currency)
				return

		entries[creditor].append(DebtEntry(amount, creditor, currency, form))
		return

	def RemoveDebt(self, amount: float, creditor: str, currency: str = "CAD", form: Optional[DebtForm] = DebtForm.CREDIT) -> None:
		entries = benedict(self.__entries)
		currency = currency.upper()

		if not creditor in self.GetAllCreditors():
			FTError(f"The creditor name provided: {creditor} does not exist! Could this be a typo?")
			return

		entry: DebtEntry
		for entry in entries[creditor]:
			if amount < entry.GetAmount():
				continue

			if form is None:
				if entry.GetCurrency() == currency:
					entry.SubtractAmount(amount, currency)

			else:
				if entry.GetCurrency() == currency and entry.GetForm() == form:
					entry.SubtractAmount(amount, currency)

			if entry.GetAmount() == 0:
				self.__entries[creditor].remove(entry)
				continue

		if len(self.__entries[creditor]) == 0:
			self.__entries.pop(creditor)

	def SetDebt(self, amount: float, creditor: str, currency: str = "CAD", form: Optional[DebtForm] = DebtForm.CREDIT) -> None:
		entries = benedict(self.__entries)

		if amount < 0:
			FTError("Cannot set debt entry amount to a value less than 0!")
			return

		for entry in entries[creditor]:
			entryCurrency = entry.GetCurrency()
			entryForm = entry.GetForm()

			if entryForm == form and entryCurrency == currency.upper():
				entry.SetAmount(amount, currency)
				return


def SaveFundEntries(entries: FundEntries) -> None:
	try:
		open("../data/entries.dat", "wb")

	except FileNotFoundError:
		# Todo: Perhaps it should create the file if it can't find it?
		FTError("Cannot find entries file...\nHas it been moved or deleted?")
		return None

	saveFile = open("../data/entries.dat", "wb")
	saveData = {
		"entries" : entries,
		"last_updated" : time.time_ns()
	}

	pickle.dump(saveData, saveFile, pickle.HIGHEST_PROTOCOL)
	saveFile.close()


def GetFundEntries() -> Optional[Dict]:
	try:
		pickle.load(open("../data/entries.dat", "rb"))

	except FileNotFoundError:
		FTError("Cannot find entries file...\nHas it been moved or deleted?")
		return None

	except EOFError:
		FTError("Fund entries file is empty.")
		return None

	file = open("../data/entries.dat", "rb")
	entries = pickle.load(file)
	file.close()

	return entries
