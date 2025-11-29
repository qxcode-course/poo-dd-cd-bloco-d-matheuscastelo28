class Phone:
  def __init__(self, id: str, number: str):
    self.__id: str = id
    self.__number: str = number

  def getId(self) -> str:
    return self.__id
  
  def getNumber(self) -> str:
    return self.__number
  
  def isValid(self) -> bool:
    return True
  
  def __str__(self):
    return f"{self.__id}:{self.__number}"

class Contact:
  def __init__(self, name: str):
    self.__name: str = name
    self.__favorited: bool = False
    self.__phones: list[Phone] = []

  def addPhone(self, phone: Phone):
    self.__phones.append(phone)

  def rmPhone(self, index: int):
    if 0 <= index < len(self.__phones):
      self.__phones.pop(index)

  def toggleFavorited(self):
    self.__favorited = not self.__favorited

  def isFavorited(self) -> bool:
    return self.__favorited
  
  def getPhones(self):
    return self.__phones
  
  def getName(self) -> str:
    return self.__name
  
  def setName(self, name: str):
    self.__name = name

  def __str__(self):
    phoneStrList = [str(phone) for phone in self.__phones]
    return f"{self.__name} [{", ".join(phoneStrList)}]"

class Agenda:
  def __init__(self):
    self.__contacts: list[Contact] = []

  def getContacts(self) -> list[Contact]:
    return sorted(self.__contacts, key=lambda contact: contact.getName())
  
  def findPosByName(self, name):
    for i in range(len(self.__contacts)):
      if self.__contacts[i].getName() == name:
        return i
    return -1
  
  def getContact(self, name: str) -> None:
    index = self.findPosByName(name)
    if index == -1:
      return None
    return self.__contacts[index]
  
  def addContact(self, name: str, phones: list[Phone]):
    contactIndex = self.findPosByName(name)
    if contactIndex != -1:
      contact = self.__contacts[contactIndex]
      for phone in phones:
        contact.addPhone(phone)
      return
    
    contact = Contact(name)
    for phone in phones:
      contact.addPhone(phone)
    self.__contacts.append(contact)
  
  def rmContact(self, name: str):
    index = self.findPosByName(name)
    if index != -1:
      self.__contacts.pop(index)

  def search(self, pattern: str) -> list[Contact]:
    result = []
    for contact in self.getContacts():
      if pattern in str(contact):
        result.append("- "+ str(contact))
    return "\n".join(result)
  
  def getFavorited(self) -> list[Contact]:
    result = []
    for contact in self.getContacts():
      if contact.isFavorited():
        result.append(contact)
    return result
  
  def favoriteContact(self, name: str):
    contact = self.getContact(name)
    if contact is not None:
      contact.toggleFavorited()

  def __str__(self):
    result = []
    for contact in self.getContacts():
      mark = "@ " if contact.isFavorited() else "- "
      result.append(mark + str(contact))
    return "\n".join(result)
  
def buildPhoneFromString(phoneStr: str) -> Phone:
  id, number = phoneStr.split(":")
  return Phone(id, number)

def main():
  agenda = Agenda()

  while True:
    cmd = input()
    args = cmd.split()
    print("$" + cmd)

    if args[0] == "add":
      name = args[1]
      phones = []

      for i in range(2, len(args)):
        phone = buildPhoneFromString(args[i])
        phones.append(phone)

      agenda.addContact(name, phones)
    elif args[0] == "show":
      print(agenda)
    elif args[0] == "end":
      break
    elif args[0] == "rmFone":
      name = args[1]
      index = int(args[2])
      contact = agenda.getContact(name)
      if contact:
        contact.rmPhone(index)
      agenda.rmContact(name)
      agenda.addContact(contact.getName(), contact.getPhones())
    elif args[0] == "rm":
      name = args[1]
      agenda.rmContact(name)
    elif args[0] == "search":
      pattern = args[1]
      print(agenda.search(pattern))
    elif args[0] == "tfav":
      name = args[1]
      agenda.favoriteContact(name)
    elif args[0] == "favs":
      favs = agenda.getFavorited()
      print("\n".join(f"@ {str(fav)}" for fav in favs))
    else:
      print("fail: comando invalido")


if __name__ == "__main__":
  main()