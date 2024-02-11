from utilities import FTError

from typing import Dict, List, Optional, Union


class ParamHandler:
	def __init__(self, commandStr: str) -> None:
		self.__namedParams = {}
		self.__unnamedParams = {}

		self.__params = self.__ParamSplitter(commandStr.split(" "))
		self.command = commandStr.split(" ")[0].lower()

	def __ParamSplitter(self, parameters: List[str]) -> Optional[List[Union[Dict[str, str], Dict[str, None]]]]:
		paramList = []

		for param in parameters[1:]:
			if ":" in param:
				splitted = param.split(":")

				if len(splitted) < 2:
					FTError(f"Invalid command parameter format: {param}. Please ensure there are no spaces around the colon.")
					return

				paramList.append({splitted[0] : splitted[1]})
				self.__namedParams.update({splitted[0] : splitted[1]})

			else:
				paramList.append({param : None})
				self.__unnamedParams.update({param : None})

		return paramList

	def HasParams(self) -> bool:
		return self.__len__() > 0

	def HasUnnamedParams(self) -> bool:
		return len(self.__unnamedParams) > 0

	def HasNamedParams(self) -> bool:
		return len(self.__namedParams.keys()) > 0

	def GetNamedParams(self) -> Dict[str, str]:
		return self.__namedParams

	def GetUnnamedParams(self) -> Dict[str, None]:
		return self.__unnamedParams

	def GetAllParams(self) -> List[Union[Dict[str, str], Dict[str, None]]]:
		return self.__params

	def __len__(self) -> int:
		return len(self.__params)
